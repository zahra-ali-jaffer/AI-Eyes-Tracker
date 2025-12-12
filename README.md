# AI Eyes Tracker

AI Eyes Tracker is a real-time drowsiness detection system in Python. It uses OpenCV to capture webcam video, MediaPipe Face Mesh to detect facial landmarks, and calculates the Eye Aspect Ratio (EAR) to determine if eyes are open or closed. The live feed is displayed in a Tkinter GUI with EAR values and alerts for prolonged eye closure.

## Features
- Real-time webcam detection  
- EAR calculation for both eyes  
- Drowsiness alerts for prolonged eye closure  
- Tkinter GUI with live video and overlay comments  
- Exit button to safely close the app

## EAR (Eye Aspect Ratio)
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
- `p1…p6` are eye landmarks from MediaPipe.  
- EAR below threshold triggers drowsiness alert.

## **Technical Stack**

| Technology      | Purpose                                         |
|-----------------|-------------------------------------------------|
| Python 3.10+    | Programming language                            |
| OpenCV          | Webcam capture, image processing, overlay text |
| MediaPipe       | Facial landmark detection                       |
| Numpy           | Numerical calculations (EAR)                    |
| Tkinter         | GUI display                                     |
| Pillow (PIL)    | Convert OpenCV images for Tkinter              |

## Usage
- python AI_Eyes_Tracker.py
- Green EAR values: eyes open
- Red "DROWSINESS ALERT!": eyes closed too long
- Click Exit button to close app safely
