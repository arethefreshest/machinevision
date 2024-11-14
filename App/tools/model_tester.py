import cv2
import numpy as np
from pathlib import Path
from core.detector import SpeedLimitDetector
import time

class ModelTester:
    def __init__(self, model_path=None):
        self.detector = SpeedLimitDetector()
        
    def test_on_video(self, video_path, output_path=None):
        """Test model on video file or webcam"""
        cap = cv2.VideoCapture(0 if video_path == 'webcam' else video_path)
        
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, 20.0,
                                  (int(cap.get(3)), int(cap.get(4))))
            
        fps_history = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            start_time = time.time()
            
            # Test both approaches
            two_stage_results = self.detector.detect_two_stage(frame)
            single_stage_results = self.detector.detect_single_stage(frame)
            
            # Draw results
            frame = self._draw_results(frame, two_stage_results, single_stage_results)
            
            # Calculate FPS
            fps = 1.0 / (time.time() - start_time)
            fps_history.append(fps)
            
            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if output_path:
                out.write(frame)
                
            cv2.imshow('Speed Limit Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cap.release()
        if output_path:
            out.release()
        cv2.destroyAllWindows()
        
        return np.mean(fps_history)
    
    def _draw_results(self, frame, two_stage_results, single_stage_results):
        """Draw detection results on frame"""
        # Draw two-stage results in green
        for det in two_stage_results:
            x1, y1, x2, y2 = map(int, det['bbox'])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{det['speed_limit']}km/h", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
        # Draw single-stage results in blue
        for det in single_stage_results:
            x1, y1, x2, y2 = map(int, det['bbox'])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f"{det['speed_limit']}km/h", (x1, y1-30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            
        return frame