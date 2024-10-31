import cv2
import numpy as np
import easyocr
import re

class OCRReader:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        
    def preprocess_sign(self, image):
        """Preprocess cropped sign for better OCR"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast = clahe.apply(gray)
        _, thresh = cv2.threshold(contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        height = 200
        aspect = image.shape[1] / image.shape[0]
        width = int(height * aspect)
        resized = cv2.resize(thresh, (width, height))
        return resized

    def read_sign(self, image):
        """Read speed limit from cropped sign image"""
        processed = self.preprocess_sign(image)
        results = self.reader.readtext(processed)
        
        if not results:
            results = self.reader.readtext(image)
            
        for text in results:
            numbers = re.findall(r'\d+', text[1])
            if numbers:
                return int(numbers[0])
        return None
    
    