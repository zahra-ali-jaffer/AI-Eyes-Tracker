import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Tkinter setup
root = tk.Tk()
root.title("Drowsiness Detector")
root.geometry("800x600")

video_label = tk.Label(root)
video_label.pack()

# Exit button
def close_app():
    global cap
    if cap.isOpened():
        cap.release()  # Release webcam
    root.destroy()     # Close window

exit_button = tk.Button(root, text="Exit", command=close_app, font=("Helvetica", 14), fg="white", bg="red")
exit_button.pack(pady=10)

# Webcam setup
cap = cv2.VideoCapture(0)

# Eye indices and thresholds
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]

EAR_THRESHOLD = 0.25
CLOSED_FRAMES = 0
MAX_CLOSED_FRAMES = 15

# EAR calculation
def eye_aspect_ratio(landmarks, eye_indices, width, height):
    points = np.array([[landmarks[i].x * width, landmarks[i].y * height] for i in eye_indices])
    dist1 = np.linalg.norm(points[1] - points[5])
    dist2 = np.linalg.norm(points[2] - points[4])
    dist3 = np.linalg.norm(points[0] - points[3])
    return (dist1 + dist2) / (2.0 * dist3)

# Main update loop
def update_frame():
    global CLOSED_FRAMES

    # Stop if window is closed
    if not root.winfo_exists():
        return

    ret, frame = cap.read()
    if not ret:
        root.after(10, update_frame)
        return

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    comment = ""
    color = (0, 255, 0)  # default green

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            leftEAR = eye_aspect_ratio(face_landmarks.landmark, LEFT_EYE, w, h)
            rightEAR = eye_aspect_ratio(face_landmarks.landmark, RIGHT_EYE, w, h)
            avgEAR = (leftEAR + rightEAR) / 2

            if avgEAR < EAR_THRESHOLD:
                CLOSED_FRAMES += 1
            else:
                CLOSED_FRAMES = 0

            if CLOSED_FRAMES > MAX_CLOSED_FRAMES:
                comment = "DROWSINESS ALERT!"
                color = (0, 0, 255)  # red
            else:
                comment = f"EAR: {avgEAR:.2f}"
                color = (0, 255, 0)  # green

            # Overlay comment on frame
            cv2.putText(frame, comment, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)

    # Convert frame to ImageTk
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    root.after(10, update_frame)

# Start loop
update_frame()
root.mainloop()
