import numpy as np

def crop_bbox(image, bbox):
    """Crop image using bounding box coordinates"""
    x1, y1, x2, y2 = [int(coord) for coord in bbox]
    return image[y1:y2, x1:x2]

def compute_iou(box1, box2):
    """Compute Intersection over Union (IoU) between two bounding boxes"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    
    union = area1 + area2 - intersection
    return intersection / union
    