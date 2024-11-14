from pathlib import Path
import shutil
from tqdm import tqdm

def organize_dataset(speed_limit=None):
    """
    Organize dataset for one or all speed limits, maintaining folder structure.
    Args:
        speed_limit (str): Speed limit to process ('20', '30', ..., '100') or None for all.
    """
    # Set up paths relative to the project root
    base_dir = Path(__file__).resolve().parents[2]  # Go up two levels
    german_signs = base_dir / 'germantrafficsigns' / 'train'
    dataset_images = base_dir / 'data' / 'dataset' / 'images' / 'train'
    dataset_labels = base_dir / 'data' / 'dataset' / 'labels' / 'train'
    classes = ['20', '30', '50', '60', '70', '80', '100'] if not speed_limit else [speed_limit]

    for cls in classes:
        source_dir = german_signs / cls
        if not source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {source_dir}")

        print(f"\nProcessing {cls} km/h signs...")
        images = list(source_dir.glob('*.jpg'))
        
        # Create directories for images and labels if they don't exist
        image_target_dir = dataset_images / cls
        label_target_dir = dataset_labels / cls
        image_target_dir.mkdir(parents=True, exist_ok=True)
        label_target_dir.mkdir(parents=True, exist_ok=True)

        print(f"Found {len(images)} images in {cls} folder")

        for img in tqdm(images, desc=f"Moving {cls} km/h images"):
            shutil.copy2(img, image_target_dir / img.name)

        print(f"\nDataset organization complete! Processed {len(images)} images")
        print(f"Images directory: {image_target_dir}")
        print(f"Labels directory (empty): {label_target_dir}")

if __name__ == "__main__":
    try:
        speed_limit = input("Enter speed limit to process (20/30/50/60/70/80/100 or leave blank for all): ").strip()
        if speed_limit and speed_limit not in ['20', '30', '50', '60', '70', '80', '100']:
            raise ValueError("Invalid speed limit")
        organize_dataset(speed_limit=speed_limit)
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease verify the germantrafficsigns folder location:")
        print("Expected structure:")
        print("autoticket/")
        print("├── App/")
        print("└── germantrafficsigns/")
        print("    └── train/")
        print("        └── 100/")
