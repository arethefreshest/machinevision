from ultralytics import YOLO
import os
from pathlib import Path
import matplotlib.pyplot as plt

class BaseDetector:
    def train(self, config_path, epochs=100, plot=True):
        """Train the model and show metrics"""
        # Get absolute path to config
        base_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        config_path = base_dir / 'configs' / config_path
        
        # Train model
        results = self.model.train(
            data=str(config_path),
            epochs=epochs,
            plots=True  # Save plots
        )
        
        if plot:
            self._plot_metrics(results)
        
        return results
    
    def _plot_metrics(self, results):
        """Plot training metrics"""
        metrics = ['box_loss', 'cls_loss', 'precision', 'recall']
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        
        for idx, metric in enumerate(metrics):
            row = idx // 2
            col = idx % 2
            values = results.results_dict[metric]
            axs[row, col].plot(values)
            axs[row, col].set_title(metric)
            
        plt.tight_layout()
        plt.show()
        
    def validate(self, val_images):
        """Validate model on images"""
        results = []
        for img_path in val_images:
            result = self.model(img_path)
            results.extend(result)
        return results
    
    def _plot_validation_results(self, val_results, visualizer):
        """Plot validation results"""
        visualizer.plot_confusion_matrix(val_results, self.model.names)
        visualizer.plot_example_predictions(self.model, val_results[:4])

class SingleClassDetector(BaseDetector):
    def __init__(self, model_path='models/pretrained/yolo11n.pt'):
        # Get absolute path to model
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, model_path)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        self.model = YOLO(model_path)
        
    def detect(self, image):
        results = self.model(image)
        detections = []
        
        for r in results:
            for box in r.boxes:
                detections.append({
                    'confidence': float(box.conf),
                    'bbox': box.xyxy.tolist()[0]
                })
        return detections
    
    def train(self, epochs=100, plot=True):
        return super().train('single_class.yaml', epochs, plot)

class MultiClassDetector(BaseDetector):
    def __init__(self, model_path='models/pretrained/yolo11n.pt'):
        # Get absolute path to model
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, model_path)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        self.model = YOLO(model_path)
        
    def detect(self, image):
        results = self.model(image)
        detections = []
        
        for r in results:
            for box in r.boxes:
                detections.append({
                    'speed_limit': r.names[int(box.cls)],
                    'confidence': float(box.conf),
                    'bbox': box.xyxy.tolist()[0]
                })
        return detections
    
    def train(self, epochs=100, plot=True):
        return super().train('multi_class.yaml', epochs, plot)
        