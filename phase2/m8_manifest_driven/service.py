from pathlib import Path
import io,json,hashlib
import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError
from fastapi import FastAPI, File, UploadFile, HTTPException
from ultralytics import YOLO
from manifest_validation import validate_manifest

HERE=Path(__file__).resolve().parent
CONFIG=json.loads((HERE/'release_manifest.json').read_text())
validate_manifest(CONFIG)
Image.MAX_IMAGE_PIXELS=CONFIG['input_limits']['pil_max_image_pixels']

def check_hash(path,expected):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(4*1024*1024),b''): h.update(chunk)
    if h.hexdigest()!=expected: raise RuntimeError('Model checksum mismatch')

det_path=HERE/CONFIG['weights']['detector']['file']
seg_path=HERE/CONFIG['weights']['segmenter']['file']
for key,path in [('detector',det_path),('segmenter',seg_path)]:
    if not path.is_file(): raise RuntimeError(f'Missing {path}')
    check_hash(path,CONFIG['weights'][key]['sha256'])
det=YOLO(str(det_path))
seg=YOLO(str(seg_path))
app=FastAPI(title='Project9 Waste Conveyor — Phase2 prototype')

@app.get('/health')
def health():
    return {'status':'ok','backend':'PyTorch','device':CONFIG['device'],
            'classes':CONFIG['class_names'], 'model_verified':True}

def overlap(a,b):
    x1=max(a[0],b[0]);y1=max(a[1],b[1]);x2=min(a[2],b[2]);y2=min(a[3],b[3])
    inter=max(0,x2-x1)*max(0,y2-y1)
    aa=max(0,a[2]-a[0])*max(0,a[3]-a[1]);ab=max(0,b[2]-b[0])*max(0,b[3]-b[1])
    return inter/(aa+ab-inter+1e-12)

@app.post('/predict')
async def predict(file:UploadFile=File(...)):
    max_upload_mb=CONFIG['inference']['max_upload_mb']
    max_upload_bytes=max_upload_mb*1024*1024
    raw=await file.read(max_upload_bytes+1)
    if len(raw)>max_upload_bytes:raise HTTPException(413,f'Max upload {max_upload_mb} MB')
    if not raw:raise HTTPException(400,'Empty file')
    try:
        with Image.open(io.BytesIO(raw)) as im:
            img=im.convert('RGB')
        minimum=CONFIG['input_limits']['min_dimension_px']
        maximum=CONFIG['input_limits']['max_dimension_px']
        if not minimum<=img.width<=maximum or not minimum<=img.height<=maximum:
            raise ValueError('Image dimensions out of range')
        rgb=np.array(img)
        bgr=cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR)
    except (UnidentifiedImageError,ValueError,OSError,Image.DecompressionBombError):
        raise HTTPException(400,'Invalid or unsupported image')
    opts=dict(conf=CONFIG['confidence'],iou=CONFIG['nms_iou'],imgsz=CONFIG['imgsz'],
              device=CONFIG['device'],verbose=False)
    # Ultralytics expects BGR numpy arrays; upload RGB is converted above.
    detection=det.predict(bgr,**opts)[0]
    segmentation=seg.predict(bgr,retina_masks=True,**opts)[0]
    d_boxes=detection.boxes.xyxy.cpu().numpy()
    d_classes=detection.boxes.cls.int().cpu().numpy()
    d_scores=detection.boxes.conf.cpu().numpy()
    s_boxes=segmentation.boxes.xyxy.cpu().numpy()
    s_classes=segmentation.boxes.cls.int().cpu().numpy()
    s_polygons=[] if segmentation.masks is None else segmentation.masks.xy
    used=set(); objects=[]
    for bb,c,conf in zip(d_boxes,d_classes,d_scores):
        options=[(overlap(bb,sb),j) for j,(sb,sc) in enumerate(zip(s_boxes,s_classes))
                 if sc==c and j not in used]
        score,j=max(options,default=(0.,-1))
        is_match=(j>=0 and score>=CONFIG['inference']['box_mask_match_min_iou'] and j<len(s_polygons) and len(s_polygons[j])>=3)
        polygon=None; centroid=None
        if is_match:
            used.add(j)
            pts=np.asarray(s_polygons[j],dtype=np.float32)
            mom=cv2.moments(pts)
            if mom['m00']>1e-12:
                centroid=[round(float(mom['m10']/mom['m00']),1),
                          round(float(mom['m01']/mom['m00']),1)]
            polygon=np.round(pts,1).tolist()
        objects.append({'material':CONFIG['class_names'][int(c)],
             'confidence':round(float(conf),4),
             'bbox_xyxy':[round(float(v),1) for v in bb],
             'mask_polygon_xy':polygon,'pick_point_xy':centroid,
             'requires_review':not is_match})
    counts={name:sum(o['material']==name for o in objects) for name in CONFIG['class_names']}
    return {'image_width':img.width,'image_height':img.height,'objects':objects,
            'counts':counts,'pick_point_units':'original_image_pixels'}
