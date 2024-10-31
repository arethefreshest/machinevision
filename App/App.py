import sys
import subprocess
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from dash import Dash, html
import cv2
from dash.dependencies import Output, Input
import base64
from core.yolo_detector import SingleClassDetector, MultiClassDetector

# Initialize FastAPI application
fastapi_app = FastAPI()

# Add CORS middleware to allow requests from any origin
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# OpenCV video capture setup
# Attempt to initialize the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the camera. Please check camera permissions or try a different index.")
else:
    print("Camera successfully initialized!")

def generate_frames():
    """Generator function that captures frames from the camera and yields them in JPEG format."""
    while True:
        success, frame = cap.read()
        if not success:
            print("Warning: Failed to capture frame from camera.")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# FastAPI route to stream video
@fastapi_app.get('/video_feed')
async def video_feed():
    """API endpoint to stream the video feed using FastAPI."""
    return StreamingResponse(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

# Initialize Dash application
dash_app = Dash(__name__)

# Layout for Dash application
dash_app.layout = html.Div([
    html.H1(children='Camera Feed', style={'textAlign': 'center'}),
    html.Img(id='video-stream', src="http://127.0.0.1:8000/video_feed", style={'width': '640px', 'height': '480px'})
])

# Mount the Dash app to FastAPI using WSGIMiddleware
fastapi_app.mount("/", WSGIMiddleware(dash_app.server))

def train_models():
    # Train both approaches
    single_class = SingleClassDetector()
    multi_class = MultiClassDetector()
    
    print("Training single-class detector...")
    single_results = single_class.train(epochs=100)
    
    print("Training multi-class detector...")
    multi_results = multi_class.train(epochs=100)
    
    return single_results, multi_results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', action='store_true', help='Train models')
    args = parser.parse_args()
    
    if args.train:
        train_models()
    else:
        import uvicorn
        uvicorn.run("App:fastapi_app", host="127.0.0.1", port=8000, reload=True)
