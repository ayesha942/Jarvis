# ============================================================
#  FACE RECOGNITION MODULE
#  Detects and identifies faces using your webcam
# ============================================================

import cv2
import face_recognition
import numpy as np
import os
import config

class FaceRecognizer:
    """
    Uses two libraries:
    
    1. face_recognition (by Adam Geitgey)
       - Built on top of dlib (C++ ML library)
       - Uses a deep CNN to create 128-dimensional "face embeddings"
       - Compares embeddings to identify people
    
    2. OpenCV (cv2)
       - Handles webcam access and image processing
       - Used to capture frames and draw boxes on screen
    
    CONCEPT: Face Embeddings
    A face embedding is a list of 128 numbers that represents a face.
    Every face gets mapped to a point in 128-dimensional space.
    The same person's face always maps to nearby points.
    Different people's faces map to far-apart points.
    
    To identify someone:
    1. Capture their face → get 128 numbers
    2. Compare to known faces using euclidean distance
    3. If distance < tolerance (0.5), it's a match!
    
    CONCEPT: Euclidean Distance
    Distance between two points A and B in N dimensions:
    d = sqrt(sum((a_i - b_i)^2 for i in range(N)))
    For faces: d < 0.5 means "same person"
    """

    def __init__(self):
        self.known_face_encodings = []  # List of 128-number arrays
        self.known_face_names = []       # Corresponding person names
        self.camera = None
        
        # Load known faces from the data/known_faces/ directory
        self._load_known_faces()

    def _load_known_faces(self):
        """
        Scan the known_faces folder and encode each image.
        Filename = person's name (e.g., "john.jpg" → name is "john")
        
        CONCEPT: Face Encoding Process
        1. Load image file → RGB numpy array (height × width × 3 channels)
        2. Detect face locations using HOG or CNN detector
        3. Extract face region
        4. Run 68-point facial landmark detection (eyes, nose, mouth...)
        5. Normalize face (rotate, scale) using landmarks
        6. Pass normalized face through ResNet → 128-number vector
        """
        faces_dir = config.KNOWN_FACES_DIR
        
        if not os.path.exists(faces_dir):
            os.makedirs(faces_dir)
            print(f"📁 Created {faces_dir}/ — add your photo here as 'yourname.jpg'")
            return
        
        image_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
        
        for filename in os.listdir(faces_dir):
            if not filename.lower().endswith(image_extensions):
                continue
            
            # Name comes from filename (without extension)
            name = os.path.splitext(filename)[0].replace('_', ' ').title()
            filepath = os.path.join(faces_dir, filename)
            
            try:
                # Load image and convert to RGB
                # (OpenCV loads as BGR, face_recognition needs RGB)
                image = face_recognition.load_image_file(filepath)
                
                # Get face encodings — returns list of 128-number arrays
                # (one per face detected in the image)
                encodings = face_recognition.face_encodings(image)
                
                if encodings:
                    # Use first face found in the image
                    self.known_face_encodings.append(encodings[0])
                    self.known_face_names.append(name)
                    print(f"✅ Loaded face: {name}")
                else:
                    print(f"⚠️ No face found in {filename}")
                    
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")
        
        if self.known_face_encodings:
            print(f"👤 Loaded {len(self.known_face_encodings)} known face(s)")
        else:
            print("⚠️ No known faces loaded. Add images to data/known_faces/")

    def recognize_from_webcam(self, duration_seconds: int = 5) -> str:
        """
        Open webcam and try to recognize faces for N seconds.
        Returns the name of the recognized person, or "Unknown".
        
        CONCEPT: Video = Stream of Frames
        A webcam captures 30 frames per second (FPS).
        Each frame is an image (e.g., 640×480 pixels × 3 colors).
        We read frames in a loop and process each one.
        
        We only process every OTHER frame (frame_count % 2 == 0)
        because face recognition is slow — this doubles the speed.
        """
        import time
        
        self.camera = cv2.VideoCapture(0)  # 0 = first webcam
        
        if not self.camera.isOpened():
            return "Unknown (camera unavailable)"
        
        recognized_names = []
        start_time = time.time()
        frame_count = 0
        
        print("📷 Looking for faces...")
        
        while (time.time() - start_time) < duration_seconds:
            # Read one frame from the webcam
            # ret = True if frame was captured successfully
            # frame = numpy array shape (height, width, 3) in BGR format
            ret, frame = self.camera.read()
            
            if not ret:
                break
            
            frame_count += 1
            
            # Process every other frame for performance
            if frame_count % 2 != 0:
                continue
            
            # Resize to 1/4 size for faster processing
            # (face detection is the bottleneck)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            
            # Convert BGR (OpenCV format) → RGB (face_recognition format)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Find all faces in this frame
            # Returns list of (top, right, bottom, left) tuples
            face_locations = face_recognition.face_locations(rgb_small_frame)
            
            if not face_locations:
                continue
            
            # Encode all detected faces
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            for face_encoding in face_encodings:
                name = self._identify_face(face_encoding)
                if name:
                    recognized_names.append(name)
        
        self.camera.release()
        
        # Return most frequently seen name
        if recognized_names:
            most_common = max(set(recognized_names), key=recognized_names.count)
            return most_common
        
        return "Unknown"

    def _identify_face(self, face_encoding) -> str:
        """
        Compare a face encoding against all known faces.
        
        face_recognition.compare_faces() uses euclidean distance internally.
        Returns a boolean list: [True, False, True, ...]
        True = this known face matches within tolerance.
        
        face_recognition.face_distance() returns the actual distances.
        We pick the closest match (smallest distance).
        """
        if not self.known_face_encodings:
            return "Unknown"
        
        # Compare against all known faces
        matches = face_recognition.compare_faces(
            self.known_face_encodings, 
            face_encoding,
            tolerance=config.FACE_RECOGNITION_TOLERANCE
        )
        
        if not any(matches):
            return "Unknown"
        
        # Get distances to find best match
        face_distances = face_recognition.face_distance(
            self.known_face_encodings, 
            face_encoding
        )
        
        # Index of the closest match
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            return self.known_face_names[best_match_index]
        
        return "Unknown"

    def verify_user(self) -> tuple[bool, str]:
        """
        Check if the person at the camera is a known/authorized user.
        Returns (is_authorized, name).
        """
        name = self.recognize_from_webcam(duration_seconds=4)
        
        if name == "Unknown":
            return False, "Unknown"
        
        return True, name