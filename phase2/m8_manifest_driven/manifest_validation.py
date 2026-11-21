"""Validate mandatory serving settings before weights are read or models load."""
import math
from pathlib import PurePosixPath
import re


def validate_manifest(config):
    def require(condition, key, rule):
        if not condition:
            raise RuntimeError(f'Invalid release_manifest.json: {key} {rule}')

    def mapping(value, key, fields):
        require(isinstance(value, dict), key, 'must be an object.')
        for field in fields:
            require(field in value, key + '.' + field, 'is required.')
        return value

    def positive_integer(value, key):
        require(isinstance(value, int) and not isinstance(value, bool) and value > 0,
                key, 'must be a positive integer.')

    def probability(value, key):
        require(isinstance(value, (int, float)) and not isinstance(value, bool)
                and math.isfinite(value) and 0 <= value <= 1,
                key, 'must be a finite number in [0, 1].')

    mapping(config, 'root', ['project', 'class_names', 'weights', 'confidence',
                            'nms_iou', 'imgsz', 'device', 'backend', 'input_format',
                            'inference', 'input_limits', 'versions', 'status'])
    require(config['class_names'] == ['cardboard', 'metal', 'rigid_plastic', 'soft_plastic'],
            'class_names', 'must preserve the checkpoint class order.')
    require(config['device'] == 'cpu' and config['backend'] == 'PyTorch',
            'device/backend', 'must be cpu/PyTorch for this candidate.')
    for key in ['project', 'input_format', 'status']:
        require(isinstance(config[key], str) and bool(config[key].strip()), key, 'must be nonempty text.')
    for key in ['confidence', 'nms_iou']:
        probability(config[key], key)
    positive_integer(config['imgsz'], 'imgsz')
    weights = mapping(config['weights'], 'weights', ['detector', 'segmenter'])
    for role in ['detector', 'segmenter']:
        item = mapping(weights[role], 'weights.' + role, ['file', 'sha256'])
        filename = item['file']
        require(isinstance(filename, str) and filename not in ('', '.', '..')
                and PurePosixPath(filename).name == filename
                and '/' not in filename and '\\' not in filename and ':' not in filename,
                'weights.' + role + '.file', 'must be a local filename.')
        require(isinstance(item['sha256'], str) and re.fullmatch(r'[0-9a-f]{64}', item['sha256']) is not None,
                'weights.' + role + '.sha256', 'must be a lowercase SHA256 digest.')
    inference = mapping(config['inference'], 'inference', ['box_mask_match_min_iou', 'max_upload_mb'])
    probability(inference['box_mask_match_min_iou'], 'inference.box_mask_match_min_iou')
    positive_integer(inference['max_upload_mb'], 'inference.max_upload_mb')
    limits = mapping(config['input_limits'], 'input_limits',
                     ['min_dimension_px', 'max_dimension_px', 'pil_max_image_pixels'])
    for key in limits:
        if key in ['min_dimension_px', 'max_dimension_px', 'pil_max_image_pixels']:
            positive_integer(limits[key], 'input_limits.' + key)
    require(limits['min_dimension_px'] <= limits['max_dimension_px'],
            'input_limits', 'minimum dimension must not exceed maximum.')
    require(limits['pil_max_image_pixels'] >= limits['min_dimension_px']**2,
            'input_limits.pil_max_image_pixels', 'must admit at least the minimum image dimensions.')
    versions = mapping(config['versions'], 'versions', ['ultralytics', 'torch', 'fastapi', 'numpy'])
    require(all(isinstance(versions[key], str) and versions[key] for key in versions),
            'versions', 'must contain nonempty version strings.')
