from pathlib import Path
import shutil
import random
from tqdm import tqdm
import cv2
import numpy as np

class DatasetPreparator:
    def __init__(self, source_dir, target_dir):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.classes = ['20', '30', '50', '60', '70', '80', '100', '120']
        
    def prepare_dataset(self, train_split=0.8):
        """Prepare dataset structure"""
        # Create directories
        for split in ['train', 'val']:
            (self.output_dir / split / 'images').mkdir(parents=True, exist_ok=True)
            (self.output_dir / split / 'labels').mkdir(parents=True, exist_ok=True)

        # Process each class
        for class_id, class_name in enumerate(self.classes):
            print(f'Processing class: {class_name}')
            class_dir = self.source_dir / class_name
            images = list(class_dir.glob('*.jpg'))
            
            random.shuffle(images)
            split_idx = int(len(images) * train_split)
            train_images = images[:split_idx]
            val_images = images[split_idx:]
            
            self._process_images(train_images, 'train', class_id)
            self._process_images(val_images, 'val', class_id)