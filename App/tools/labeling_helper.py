import subprocess
from pathlib import Path
import webbrowser
import time
import os

class SpeedLimitLabeler:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.dataset_dir = self.base_dir / 'data' / 'dataset'
        self.classes = ['20', '30', '50', '60', '70', '80', '100']
        self.label_studio_port = 8080

    def setup_labeling_project(self, speed_limit):
        """Setup Label Studio project for specific speed limit"""
        train_dir = self.dataset_dir / 'images' / 'train' / str(speed_limit)
        
        if not train_dir.exists():
            raise FileNotFoundError(f"Training directory not found: {train_dir}. Run organize_dataset.py first.")
            
        # Label Studio labeling configuration
        labeling_config = f"""
        <View>
          <Header value="Label {speed_limit} km/h speed limit signs"/>
          <Image name="image" value="$image" zoom="true" zoomControl="true"/>
          <RectangleLabels name="label" toName="image">
            <Label value="{speed_limit}kmt" background="#FF0000" selected="true"/>
          </RectangleLabels>
        </View>
        """
        
        # Start Label Studio with environment configurations
        env = {
            'LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED': 'true',
            'LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT': '/',
            'DATA_UPLOAD_MAX_NUMBER_FILES': '2000',
            'LABEL_STUDIO_MAX_TASKS_PER_PROJECT': '2000'
        }
        
        subprocess.Popen(['label-studio', 'start', '--port', str(self.label_studio_port), '--no-browser'], env={**os.environ, **env})
        time.sleep(5)  # Allow server time to start
        
        print("\n=== Label Studio Setup Instructions ===")
        print("1. Open your browser at: http://localhost:8080")
        print(f"2. Create a new project named 'speed_limit_{speed_limit}'")
        print("3. Choose 'Object Detection with Bounding Boxes'")
        print(f"4. Import images from: {self.dataset_dir/'images'/'train'/speed_limit}")
        print("5. Use the following Labeling Interface configuration:")
        print(labeling_config)
        print("\nAfter labeling, export labels in YOLO format and save to:")
        print(f"  {self.dataset_dir / 'labels' / 'train' / str(speed_limit)} for training")
        print(f"  {self.dataset_dir / 'labels' / 'val' / str(speed_limit)} for validation")

    def export_labels(self):
        """Guide to export labels from Label Studio"""
        print("\nTo export labels:")
        print("1. Go to Export tab in Label Studio")
        print("2. Choose YOLO format")
        print("3. Save files in corresponding train/val directories under labels.")
        
if __name__ == "__main__":
    labeler = SpeedLimitLabeler()
    speed_limit = input("Enter speed limit to label (20/30/50/60/70/80/100): ")
    if speed_limit not in ['20', '30', '50', '60', '70', '80', '100']:
        raise ValueError("Invalid speed limit")
    labeler.setup_labeling_project(speed_limit)
