# AutoTicket

Real-time speed limit sign detection system using YOLO and EasyOCR, with a web interface built using FastAPI and Dash.

---

## Development Environment Setup

### Option 1: Using Docker (Recommended)
This is the easiest way to ensure consistent development environments across the team.

1. Install Docker on your system:
   - [Docker Desktop for Windows/Mac](https://www.docker.com/products/docker-desktop)
   - [Docker Engine for Linux](https://docs.docker.com/engine/install/)

2. Navigate to the App directory and build/run the container:
   ```bash
   # Navigate to App directory
   cd App

   # Build the Docker image
   docker build -t autoticket .

   # Run the container
   docker run -p 8000:8000 autoticket
   ```

### Option 2: Using Conda
If you prefer using Conda for managing Python environments:

1. Install Miniconda:
   - [Windows](https://docs.conda.io/en/latest/miniconda.html#windows-installers)
   - [macOS](https://docs.conda.io/en/latest/miniconda.html#macos-installers)
   - [Linux](https://docs.conda.io/en/latest/miniconda.html#linux-installers)

2. Create and activate the conda environment:
   ```bash
   # Create environment from file
   conda env create -f environment.yml

   # Activate environment
   conda activate autoticket
   ```

3. Run the application:
   ```bash
   python App/App.py
   ```

### Option 3: Local Setup
If you prefer not to use Docker or Conda, you can set up the environment directly:

1. Ensure you have Python 3.11 installed

2. Navigate to the App directory and create a virtual environment:
   ```bash
   # Navigate to App directory
   cd App

   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python App.py
   ```

## Accessing the Application

Once running, access the application at:
- Web Interface: http://localhost:8000

## Project Structure
```
autoticket/
├── App/
│   ├── core/
│   │   ├── __init__.py       # Package initialization
│   │   ├── detector.py       # Main detection class
│   │   ├── yolo_detector.py  # YOLO implementations
│   │   ├── ocr_reader.py     # OCR implementation
│   │   └── utils.py          # Helper functions
│   ├── configs/
│   │   ├── single_class.yaml # Config for YOLO + OCR
│   │   └── multi_class.yaml  # Config for multi-class YOLO
│   ├── App.py               # Main application file
│   └── requirements.txt     # Python dependencies
├── environment.yml          # Conda environment file
└── README.md
```

## Dataset Preparation and Labeling

### Step 1: Organize Dataset by Speed Limit
Organize raw images by speed limit to simplify labeling. This step will place images into folders by speed limit under `data/dataset/images/train/[speed_limit]`.
```bash
python App/tools/organize_dataset.py
```

When prompted, enter each speed limit (e.g., 20, 30, 50). You can leave the prompt blank to process all speed limits at once.

### Step 2: Trim Dataset for Efficient Labeling
Limit the number of images per base (such as different sizes of the same sign) to reduce duplicates and make labeling manageable.
```bash
python App/tools/dataset_prep.py
```

This step:
- Groups images by base (e.g., 00000, 00001) and retains a specified number per group.
- Splits data into train and val folders under `data/dataset/images`.

### Step 3: Start Labeling with Label Studio
Use Label Studio to label the organized dataset. Label Studio will allow you to draw bounding boxes around speed limit signs for each speed category.

1. Start Label Studio:
   ```bash
   python App/tools/labeling_helper.py
   ```
   
2. Open Label Studio at http://localhost:8080.
3. For each speed limit:
   - Create a Project for the speed limit category and import images from `data/dataset/images/train/[speed_limit]`.
   - Label signs with bounding boxes using the labels `20kmt`, `30kmt`, etc., for each speed limit.
4. **Export the labeled data** in YOLO format after completing each project, saving the labels in `data/dataset/labels/train/[speed_limit]`.

### Step 4: Validate Dataset
Validate the dataset to ensure that each image has an associated label file and that bounding box values are within the acceptable range. This step helps catch any labeling errors before training.
```bash
python App/tools/dataset_validator.py
```

If any issues are detected, the tool will output specific files with missing or incorrect labels.

---

After completing the steps, your dataset should be ready for training.

## Troubleshooting

### Common Issues:
1. Port already in use:
   - Change the port mapping in the docker run command
   - Or kill the process using port 8000
   ```bash
   docker ps
   docker kill <container_id>
   ```

2. Docker daemon not running:
   - Ensure Docker is running on your system

3. Conda environment creation fails:
   - Try updating conda: `conda update -n base conda`
   - Check if you have sufficient permissions
   ```bash
   # Remove failed environment if needed
   conda env remove -n autoticket
   # Try creating again
   conda env create -f environment.yml
   ```

Note: For development with camera features, use either the Conda or local setup option. Docker is primarily used to ensure consistent package versions across the team.