#!/usr/bin/env python3
"""Create labeled ZeroWaste-f classifier crops from COCO boxes without guessing labels.
Usage:
 python Create_ZeroWaste_Crops_From_COCO.py --images ./images --annotations ./instances.json --out ./zerowaste_labeled_crops --max-per-class 60
 Requires PIL; standard COCO {images,annotations,categories}; uses COCO bbox xywh.
 Do NOT distribute raw photos or image crops outside allowed dataset terms.
"""
import argparse,json,random,collections
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--images',required=True);p.add_argument('--annotations',required=True);p.add_argument('--out',required=True);p.add_argument('--max-per-class',type=int,default=60);p.add_argument('--min-width',type=int,default=30);p.add_argument('--seed',type=int,default=42)
a=p.parse_args(); rng=random.Random(a.seed)
d=json.load(open(a.annotations)); cats={c['id']:c['name'].lower().replace(' ','_').replace('-','_') for c in d['categories']}
allowed={'cardboard','metal','soft_plastic','rigid_plastic'}
ids={i['id']:i for i in d['images']}
root=Path(a.images);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
all_paths={x.name:x for x in root.rglob('*') if x.is_file()}
groups=collections.defaultdict(list)
for ann in d['annotations']:
 cat=cats.get(ann['category_id'],'')
 if cat not in allowed:continue
 img=ids.get(ann['image_id']);path=root/img['file_name'] if img else None
 if path is None: continue
 if not path.exists():path=all_paths.get(Path(img['file_name']).name)
 if path is None:continue
 bbox=ann.get('bbox',[])
 if len(bbox)!=4 or bbox[2]<a.min_width or bbox[3]<a.min_width: continue
 groups[cat].append((path,tuple(bbox),ann['id'],ann['image_id']))
if not groups:raise RuntimeError('No matching COCO boxes found; inspect category naming and annotations format')
for cat,obs in sorted(groups.items()):
 rng.shuffle(obs);selected=[];used_frames=set()
 for item in obs:
  if item[3] in used_frames:continue
  selected.append(item);used_frames.add(item[3])
  if len(selected)>=a.max_per_class:break
 for path,(x,y,w,h),ann_id,img_id in selected:
  with Image.open(path) as im:
   im=im.convert('RGB');wim,him=im.size
   xy=(int(max(0,x)),int(max(0,y)),int(min(wim,x+w)),int(min(him,y+h)))
   if xy[2]<=xy[0] or xy[3]<=xy[1]:continue
   dest=out/cat/f'{img_id}_{ann_id}.jpg';dest.parent.mkdir(exist_ok=True)
   im.crop(xy).save(dest,quality=90)
 print(cat,len(selected),'selected unique frames')
print('Done; archive the per-class folders and upload to the ZeroWaste Colab notebook')
