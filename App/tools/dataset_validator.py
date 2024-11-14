import cv2
from pathlib import Path
import numpy as np
from tqdm import tqdm

class DatasetValidator:
    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)
        
    def validate_dataset(self):
        """Validate dataset structure and contents"""
        issues = []
        
        # Check directory structure
        for split in ['train', 'val']:
            for subdir in ['images', 'labels']:
                path = self.dataset_path / split / subdir
                if not path.exists():
                    issues.append(f"Missing directory: {path}")
                    
        # Validate image-label pairs
        for split in ['train', 'val']:
            img_dir = self.dataset_path / split / 'images'
            label_dir = self.dataset_path / split / 'labels'
            
            for img_path in tqdm(list(img_dir.glob('*.jpg')), desc=f'Validating {split}'):
                label_path = label_dir / f'{img_path.stem}.txt'
                
                # Check if label exists
                if not label_path.exists():
                    issues.append(f"Missing label for {img_path}")
                    continue
                
                # Validate label format
                try:
                    with open(label_path) as f:
                        lines = f.readlines()
                        for line in lines:
                            elements = line.strip().split()
                            if len(elements) != 5:
                                issues.append(f"Incorrect format in {label_path}: {line}")
                                continue
                            class_id, x, y, w, h = map(float, elements)
                            if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                                issues.append(f"Invalid bbox values in {label_path}: {line}")
                except:
                    issues.append(f"Invalid label format in {label_path}")
                
        if issues:
            print("\nValidation issues found:")
            for issue in issues:
                print(issue)
        else:
            print("\nDataset validation passed with no issues.")
                
        return issues

if __name__ == "__main__":
    validator = DatasetValidator("../../data/dataset")
    validator.validate_dataset()
