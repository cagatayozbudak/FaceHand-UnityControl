🎮 Face & Hand Controlled Unity Character
Control a 3D ship in Unity using your face and hand movements with Python & OpenCV via UDP communication.

This project uses:
- MediaPipe for face & hand detection (in Python)
- Unity for rendering and applying movement
- UDP sockets for real-time communication between Python and Unity

🛠 Requirements
- Python
  - Python 3.7+
  - opencv-python
  - mediapipe
  - numpy

Install dependencies: pip install opencv-python mediapipe numpy

✅ Make sure your webcam is working properly.

- Unity
  - Unity 2021+ (any recent version works)
  - A simple 3D ship model in the scene (you can use any free model from Unity Asset Store)
  - A GameObject with the PlayerMovement.cs script attached

✅ C# scripting must be enabled (this is included by default in Unity installs).
Make sure your Unity version supports C# and UDP communication via System.Net.Sockets namespace.
 
🧠 How It Works
1. Python uses MediaPipe to detect:
   - Face movement (X, Y, Z axis)
   - Single-hand position (for left/right rotation)
2. Python sends this data over UDP to Unity (127.0.0.1:5052)
3. Unity receives and applies the movement & rotation to the ship.
