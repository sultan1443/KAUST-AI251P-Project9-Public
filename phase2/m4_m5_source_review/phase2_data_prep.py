"""Phase 2 ZeroWaste-f grouped TRAIN/VAL conversion (public, source-only).

Based on the M4/M5 data builders in CORRECTED_v3. This module deliberately does
NOT download datasets, use credentials, build/evaluate Test, or overwrite outputs.
Requires an independently obtained, authorized ZeroWaste-f local extraction.
"""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import math
import os
import shutil
import tempfile

import numpy as np
import pandas as pd
from PIL import Image

CLASS_NAMES = ["cardboard", "metal", "rigid_plastic", "soft_plastic"]
TRAINING_SPLITS = ["train", "val"]
ALL_SPLITS = ["train", "val", "test"]
ORIGINAL_MANIFEST_SHA256 = "ef6b35d2ba7f6708319b824e29707b4d2001750974ac3c4da03c72c9340fdb50"
EXPECTED_COUNTS = {"train": 1851, "val": 451, "test": 929, "excluded": 1272}


def manifest_check(manifest_path):
    """Read frozen public metadata. Never recompute or optimize a new split."""
    manifest_path = Path(manifest_path)
    df = pd.read_csv(manifest_path, dtype={"sequence": str, "filename": str,
                                          "original_split": str, "split": str})
    required = {"original_split", "image_id", "filename", "sequence", "split", *CLASS_NAMES}
    if not required.issubset(df.columns):
        raise ValueError(f"Public manifest is missing: {sorted(required - set(df.columns))}")
    actual = df["split"].value_counts().to_dict()
    if actual != EXPECTED_COUNTS:
        raise ValueError(f"Frozen split counts differ: {actual}")
    if not (df.loc[df.original_split.eq("test"), "split"] == "test").all():
        raise ValueError("Original Test partition changed")
    if not (df.loc[df.split.eq("test"), "original_split"] == "test").all():
        raise ValueError("Unexpected Test source partition")
    if not df["original_split"].isin(ALL_SPLITS).all():
        raise ValueError("Unexpected original split")
    if df.duplicated(["original_split", "filename"]).any():
        raise ValueError("Duplicate names within original source split")
    sequences = {s: set(df.loc[df.split.eq(s), "sequence"]) for s in ALL_SPLITS}
    for a in ALL_SPLITS:
        for b in ALL_SPLITS:
            if a != b and sequences[a].intersection(sequences[b]):
                raise ValueError("Sequence leakage between active splits")
    for col in CLASS_NAMES:
        if (df[col] < 0).any() or df[col].isnull().any():
            raise ValueError(f"Invalid class counts in {col}")
    for name in df.filename:
        if Path(name).name != name or ".." in name or not name.lower().endswith('.png'):
            raise ValueError(f"Unsafe or unexpected image filename: {name!r}")
    print("Frozen manifest validated. Train/Val/Test/Excluded:", actual)
    print("Original, unsanitized manifest SHA256 (provenance only):", ORIGINAL_MANIFEST_SHA256)
    print("Public metadata SHA256:", hashlib.sha256(manifest_path.read_bytes()).hexdigest())
    return df


def _prepare_rows(df, source_root):
    """Build only TRAIN and VAL; test/excluded never copied into output."""
    source_root = Path(source_root)
    rows = df[df.split.isin(TRAINING_SPLITS)].copy()
    rows['export_name'] = rows['original_split'] + '__' + rows['filename']
    if rows.duplicated(['split','export_name']).any():
        raise ValueError("Duplicate exported TRAIN/VAL image basename")
    rows['source_path'] = rows.apply(lambda r: str(source_root/r.original_split/'data'/r.filename), axis=1)
    rows['annotation_path'] = rows.apply(lambda r: str(source_root/r.original_split/'labels.json'), axis=1)
    for original_split in sorted(rows.original_split.unique()):
        labels_path = source_root/original_split/'labels.json'
        if not labels_path.is_file():
            raise FileNotFoundError(f"Obtain authorized ZeroWaste-f source first: {labels_path}")
    return rows


def _read_coco(path):
    d=json.loads(Path(path).read_text(encoding='utf-8-sig'))
    images={int(i['id']):i for i in d['images']}
    classes={int(c['id']):c['name'] for c in d['categories']}
    if set(classes.values())!=set(CLASS_NAMES):
        raise ValueError(f"Unexpected source categories in {path}: {classes}")
    anns=defaultdict(list)
    for a in d['annotations']:
        anns[int(a['image_id'])].append(a)
    return images,classes,anns


def _link_or_copy(src,dst):
    src=Path(src);dst=Path(dst)
    if not src.is_file():
        raise FileNotFoundError(src)
    try:
        os.link(src,dst)
    except OSError:
        shutil.copy2(src,dst)


def _write_yaml(path, root):
    # No test: entry on purpose. Frozen once-only Test must remain external.
    text=(f'path: {root}\ntrain: images/train\nval: images/val\nnames:\n'
          + ''.join(f'  {i}: {c}\n' for i,c in enumerate(CLASS_NAMES)))
    path.write_text(text,encoding='utf8')


def _check_existing(root,task,manifest_sha):
    info_path=root/'build_info.json'
    if not info_path.is_file():
        raise FileExistsError(f"Existing directory without build_info.json: {root}; will not overwrite")
    info=json.loads(info_path.read_text())
    if info.get('task') != task or info.get('public_manifest_sha256') != manifest_sha:
        raise FileExistsError(f"Existing build differs; no overwrite: {root}")
    return info


def build_detection(df, source_root, destination, public_manifest_path):
    """Build YOLO detection labels for frozen train and val; never Test."""
    destination=Path(destination)
    manifest_sha=hashlib.sha256(Path(public_manifest_path).read_bytes()).hexdigest()
    if destination.exists():
        return _check_existing(destination,'detect',manifest_sha)
    rows=_prepare_rows(df,source_root)
    destination.parent.mkdir(parents=True,exist_ok=True)
    tmp=Path(tempfile.mkdtemp(prefix='.det_build_',dir=destination.parent))
    stats={s:dict(images=0,boxes=0,clipped=0,background=0,**{c:0 for c in CLASS_NAMES})
           for s in TRAINING_SPLITS}
    cache={}
    try:
        for split in TRAINING_SPLITS:
            (tmp/'images'/split).mkdir(parents=True)
            (tmp/'labels'/split).mkdir(parents=True)
        for row in rows.itertuples(index=False):
            if row.annotation_path not in cache:
                cache[row.annotation_path]=_read_coco(row.annotation_path)
            images,classes,annotations=cache[row.annotation_path]
            info=images[int(row.image_id)]
            W,H=int(info['width']),int(info['height'])
            with Image.open(row.source_path) as image:
                if image.size!=(W,H):
                    raise ValueError(f"Image resolution differs from COCO: {row.filename}")
            lines=[]
            for ann in annotations[int(row.image_id)]:
                class_name=classes[int(ann['category_id'])]
                cls=CLASS_NAMES.index(class_name)
                x,y,w,h=map(float,ann['bbox'])
                if not all(map(math.isfinite,(x,y,w,h))) or min(w,h)<=0:
                    raise ValueError(f"Invalid box in {row.filename}")
                x1,y1,x2,y2=(max(0,min(W,x)),max(0,min(H,y)),
                             max(0,min(W,x+w)),max(0,min(H,y+h)))
                if x2<=x1 or y2<=y1:
                    raise ValueError(f"Clipped box invalid in {row.filename}")
                stats[row.split]['clipped']+=int((x1,y1,x2,y2)!=(x,y,x+w,y+h))
                xc,yc,bw,bh=(x1+x2)/(2*W),(y1+y2)/(2*H),(x2-x1)/W,(y2-y1)/H
                lines.append(f'{cls} {xc:.8f} {yc:.8f} {bw:.8f} {bh:.8f}')
                stats[row.split]['boxes']+=1
                stats[row.split][class_name]+=1
            _link_or_copy(row.source_path,tmp/'images'/row.split/row.export_name)
            (tmp/'labels'/row.split/(Path(row.export_name).stem+'.txt')).write_text(
                '\n'.join(lines)+('\n' if lines else ''),encoding='utf8')
            stats[row.split]['images']+=1
            stats[row.split]['background']+=int(not lines)
        for split in TRAINING_SPLITS:
            exp=rows.loc[rows.split.eq(split),CLASS_NAMES].sum()
            if any(stats[split][name]!=int(exp[name]) for name in CLASS_NAMES):
                raise ValueError(f"Detection labels differ from frozen manifest for {split}")
        _write_yaml(tmp/'data.yaml',destination)
        meta={'task':'detect','source_dataset':'ZeroWaste-f','class_names':CLASS_NAMES,
              'build_splits':TRAINING_SPLITS,'public_manifest_sha256':manifest_sha,
              'original_manifest_sha256':ORIGINAL_MANIFEST_SHA256,'stats':stats}
        (tmp/'build_info.json').write_text(json.dumps(meta,indent=2)+'\n')
        tmp.rename(destination)
        return meta
    finally:
        if tmp.exists():
            shutil.rmtree(tmp)


def build_segmentation(df, source_root, destination, public_manifest_path):
    """Convert original COCO polygons to YOLO segments for train/val only."""
    from ultralytics.data.converter import merge_multi_segment
    destination=Path(destination)
    manifest_sha=hashlib.sha256(Path(public_manifest_path).read_bytes()).hexdigest()
    if destination.exists():
        return _check_existing(destination,'segment',manifest_sha)
    rows=_prepare_rows(df,source_root)
    destination.parent.mkdir(parents=True,exist_ok=True)
    tmp=Path(tempfile.mkdtemp(prefix='.seg_build_',dir=destination.parent))
    cache={};multi_count=0;sample_count=0
    try:
        for split in TRAINING_SPLITS:
            (tmp/'images'/split).mkdir(parents=True)
            (tmp/'labels'/split).mkdir(parents=True)
        for row in rows.itertuples(index=False):
            if row.annotation_path not in cache:
                cache[row.annotation_path]=_read_coco(row.annotation_path)
            images,classes,anns=cache[row.annotation_path]
            info=images[int(row.image_id)]
            W,H=int(info['width']),int(info['height'])
            labels=[]
            for ann in anns[int(row.image_id)]:
                cls=CLASS_NAMES.index(classes[int(ann['category_id'])])
                raw=ann.get('segmentation',[])
                if not isinstance(raw,list):
                    raise ValueError(f"RLE annotation not supported for {row.filename}")
                polys=[p for p in raw if len(p)>=6 and len(p)%2==0
                       and all(math.isfinite(float(v)) for v in p)]
                if not polys:
                    raise ValueError(f"Missing polygon for annotation {ann.get('id')}")
                if len(polys)>1:
                    multi_count+=1
                    xy=np.concatenate(merge_multi_segment(polys),axis=0).astype(float)
                else:
                    xy=np.array(polys[0],dtype=float).reshape(-1,2)
                if len(xy)<3:
                    raise ValueError(f"Polygon has too few points in {row.filename}")
                xy[:,0]=np.clip(xy[:,0]/W,0,1)
                xy[:,1]=np.clip(xy[:,1]/H,0,1)
                labels.append(str(cls)+' '+' '.join(f'{v:.8f}' for v in xy.reshape(-1)))
            _link_or_copy(row.source_path,tmp/'images'/row.split/row.export_name)
            (tmp/'labels'/row.split/(Path(row.export_name).stem+'.txt')).write_text(
                '\n'.join(labels)+('\n' if labels else ''),encoding='utf8')
            sample_count+=1
        _write_yaml(tmp/'data.yaml',destination)
        meta={'task':'segment','source_dataset':'ZeroWaste-f','class_names':CLASS_NAMES,
              'build_splits':TRAINING_SPLITS,'public_manifest_sha256':manifest_sha,
              'original_manifest_sha256':ORIGINAL_MANIFEST_SHA256,
              'multipolygon_annotations':multi_count,'images':sample_count}
        (tmp/'build_info.json').write_text(json.dumps(meta,indent=2)+'\n')
        tmp.rename(destination)
        return meta
    finally:
        if tmp.exists():
            shutil.rmtree(tmp)
