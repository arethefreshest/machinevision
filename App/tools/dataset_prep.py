import os
from pathlib import Path
import shutil
import random
from tqdm import tqdm
import re

class DatasetPreparator:
    def __init__(self, source_dir=None, target_dir=None, base_retention_ratio=0.2):
        # Set base paths relative to project root
        self.base_dir = Path(__file__).resolve().parents[2]
        self.source_dir = self.base_dir / 'data' / 'dataset' / 'images' / 'train' if source_dir is None else Path(source_dir)
        self.target_dir = self.base_dir / 'data' / 'dataset' / 'images' if target_dir is None else Path(target_dir)
        self.base_retention_ratio = base_retention_ratio
        self.classes = ['20', '30', '50', '60', '70', '80', '100']

    def prepare_dataset(self, train_split=0.8, speed_limit=None):
        """Prepare dataset structure with grouped trimming."""
        limits_to_process = [speed_limit] if speed_limit and speed_limit in self.classes else self.classes

        for class_name in limits_to_process:
            print(f'\nProcessing class: {class_name}')
            class_dir = self.source_dir / class_name
            images = list(class_dir.glob('*.jpg'))
            print(f"Found {len(images)} images in {class_name} km/h folder before trimming")

            # Calculate adaptive retention ratio based on the total number of images
            retention_ratio = self.calculate_retention_ratio(len(images))

            # Group images by base name and apply adaptive retention strategy
            grouped_images = self._group_and_select_images(images, retention_ratio)
            print(f"Retained {len(grouped_images)} images in {class_name} km/h folder after trimming")

            # Split dataset into train and val sets
            random.shuffle(grouped_images)
            split_idx = int(len(grouped_images) * train_split)
            train_images = grouped_images[:split_idx]
            val_images = grouped_images[split_idx:]
            
            # Move selected images to their respective folders and remove unselected ones
            self._process_images(train_images, val_images, class_name)

    def calculate_retention_ratio(self, total_images):
        """Calculate retention ratio based on total images in a class."""
        if total_images < 500:
            return 0.5  # Higher retention for smaller classes
        elif total_images < 1000:
            return 0.3
        else:
            return self.base_retention_ratio  # Use default ratio for larger classes

    def _group_and_select_images(self, images, retention_ratio):
        """Group images by base and apply adaptive retention."""
        grouped_images = {}
        selected_images = []

        # Regex to extract the base name (e.g., "00000" from "00000_00001.jpg")
        base_pattern = re.compile(r'(\d+)_\d+\.jpg')

        # Group images by base name
        for img in images:
            base_name = base_pattern.match(img.name).group(1)
            if base_name not in grouped_images:
                grouped_images[base_name] = []
            grouped_images[base_name].append(img)

        # Apply retention: select at least one per group, then apply the retention ratio
        for group in grouped_images.values():
            # Ensure at least one image per group
            selected_group = [random.choice(group)]
            
            # Apply percentage-based selection for additional images
            additional_images = random.sample(group, min(len(group), int(len(group) * retention_ratio)))
            selected_group.extend(additional_images)
            
            # Avoid duplicates and add to final selection
            selected_images.extend(set(selected_group))

        return selected_images

    def _process_images(self, train_images, val_images, class_name):
        """Helper to move images into the dataset structure and remove unselected images."""
        train_folder = self.source_dir / class_name
        val_folder = self.target_dir / 'val' / class_name
        val_folder.mkdir(parents=True, exist_ok=True)

        # Move selected validation images to val folder
        for img in tqdm(val_images, desc=f"Processing val set for {class_name}"):
            shutil.move(img, val_folder / img.name)

        # Keep only selected train images and delete any others in train folder
        selected_train_names = {img.name for img in train_images}
        for img in train_folder.glob('*.jpg'):
            if img.name not in selected_train_names:
                img.unlink()  # Delete unselected images

        print(f"Train set for {class_name} has {len(train_images)} images")
        print(f"Val set for {class_name} has {len(val_images)} images")

if __name__ == "__main__":
    preparator = DatasetPreparator()
    speed_limit = input("Enter speed limit to trim (20/30/50/60/70/80/100 or leave blank for all): ").strip()
    speed_limit = speed_limit if speed_limit in preparator.classes else None
    preparator.prepare_dataset(speed_limit=speed_limit)
