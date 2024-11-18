import subprocess
from pathlib import Path
import webbrowser
import time
import os

class SpeedLimitLabeler:
    def __init__(self):
        # Adjust the base directory to align with dataset location
        self.base_dir = Path(__file__).resolve().parents[2]  # Go up two levels to reach 'autoticket'
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
        print(f"4. Import images from: {train_dir}")
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
        print("3. Download and extract the zip file")
        print("4. Process the labels using:")
        print("   labeler.process_exported_labels('/path/to/extracted/folder', speed_limit)")

    def process_exported_labels(self, export_dir, speed_limit):
        """Process exported labels from Label Studio and move them to correct location"""
        # Convert to absolute path if needed
        export_dir = Path(export_dir).expanduser().resolve()
        labels_dir = export_dir / 'labels'
        target_dir = self.dataset_dir / 'labels' / 'train' / str(speed_limit)
        
        if not labels_dir.exists():
            raise FileNotFoundError(f"Labels directory not found in {export_dir}")
        
        # Create target directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Fixed class mapping that matches multi_class.yaml order
        yaml_class_order = {
            '20kmt': 0,
            '30kmt': 1,
            '50kmt': 2,
            '60kmt': 3,
            '70kmt': 4,
            '80kmt': 5,
            '100kmt': 6
        }
        
        # Process each label file
        for label_file in labels_dir.glob('*.txt'):
            # Extract original filename (remove the random prefix)
            original_name = label_file.name.split('-', 1)[1] if '-' in label_file.name else label_file.name
            
            # Read and modify label content
            with open(label_file) as f:
                lines = f.readlines()
            
            # Update class IDs to match YAML config
            modified_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 5:
                    # Always use the class ID that matches our speed limit in the YAML order
                    parts[0] = str(yaml_class_order[f'{speed_limit}kmt'])
                    modified_lines.append(' '.join(parts) + '\n')
            
            # Write to target directory with correct filename
            with open(target_dir / original_name, 'w') as f:
                f.writelines(modified_lines)
        
        print(f"\nLabels processed and moved to: {target_dir}")

if __name__ == "__main__":
    labeler = SpeedLimitLabeler()
    speed_limit = input("Enter speed limit to label (20/30/50/60/70/80/100): ")
    if speed_limit not in ['20', '30', '50', '60', '70', '80', '100']:
        raise ValueError("Invalid speed limit")
    
    action = input("Enter action (setup/process): ").lower()
    if action == 'setup':
        labeler.setup_labeling_project(speed_limit)
    elif action == 'process':
        export_path = input("Enter path to extracted export folder: ")
        labeler.process_exported_labels(export_path, speed_limit)
    else:
        print("Invalid action. Use 'setup' or 'process'")
