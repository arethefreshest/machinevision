import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import cv2

class TrainingVisualizer:
    def __init__(self, save_dir='runs/visualizations'):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def plot_training_metrics(self, results, title='Training Metrics'):
        metrics = ['box_loss', 'cls_loss', 'precision', 'recall', 'mAP50', 'mAP50-95']
        fig, axs = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle(title)
        
        for idx, metric in enumerate(metrics):
            row = idx // 2
            col = idx % 2
            values = results.results_dict[metric]
            axs[row, col].plot(values)
            axs[row, col].set_title(metric)
            axs[row, col].grid(True)
            
        plt.tight_layout()
        plt.savefig(self.save_dir / f'{title.lower().replace(" ", "_")}.png')
        plt.show()

    def plot_confusion_matrix(self, results, class_names):
        conf_matrix = results.confusion_matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(conf_matrix, annot=True, fmt='d', 
                   xticklabels=class_names, 
                   yticklabels=class_names)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.savefig(self.save_dir / 'confusion_matrix.png')
        plt.show()