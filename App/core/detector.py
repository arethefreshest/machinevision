from .yolo_detector import SingleClassDetector, MultiClassDetector
from .ocr_reader import OCRReader
from .utils import crop_bbox

class SpeedLimitDetector:
    def  __init__(self):
        self.single_class = SingleClassDetector()
        self.multi_class = MultiClassDetector()
        self.ocr_reader = OCRReader()
        
    def detect_two_stage(self, image):
        """YOLO + OCR approach"""
        detections = self.single_class.detect(image)
        results = []
        
        for det in detections:
                cropped = crop_bbox(image, det['bbox'])
                speed_limit = self.ocr.read_sign(cropped)
                if speed_limit:
                    results.append({
                        'speed_limit': speed_limit,
                        'confidence': det['confidence'],
                        'bbox': det['bbox']
                    })
        return results
        
    def detect_single_stage(self, image):
        """Multi-class YOLO approach"""
        return self.multi_class.detect(image)