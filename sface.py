import os
import numpy as np
import cv2
from pathlib import Path

# ==========================================
# 1. SETUP PATHS AND MODEL CONFIGURATIONS
# ==========================================

YUNET_PATH = os.path.join( "face_detection_yunet_2026may.onnx")
SFACE_PATH = os.path.join( "face_recognition_sface_2021dec.onnx")
EMOTION_PATH = os.path.join("emotion-ferplus.onnx")
TARGET_IMAGE_PATH = os.path.join("image.jpg")
REFERENCE_FACES_DIR = os.path.join("reference_faces")

# Recognizer thresholds
COSINE_THRESHOLD = 0.363
L2_THRESHOLD = 1.128

# Emotion labels array (Strict Microsoft emotion-ferplus-8 ONNX Model Zoo Ordering)
EMOTIONS = ["Neutral", "Happy", "Surprise", "Sad", "Angry", "Disgust", "Fear", "Contempt"]

# PER-EMOTION THRESHOLDS (Adjusted thresholds for realistic live camera triggers)
EMOTION_THRESHOLDS = {
    "Neutral": 0.40,
    "Happy": 0.40,
    "Surprise": 0.40,
    "Sad": 0.40,
    "Angry": 0.40,
    "Disgust": 0.40,
    "Fear": 0.40,
    "Contempt": 0.40
}

# Guard check for files
for path in [YUNET_PATH, SFACE_PATH, EMOTION_PATH]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing required project file: {path}")

# Create reference faces directory if it doesn't exist
os.makedirs(REFERENCE_FACES_DIR, exist_ok=True)

# ==========================================
# 2. INITIALIZE ALL OPENCV MODELS
# ==========================================
# Face detector
detector = cv2.FaceDetectorYN.create(
    model=YUNET_PATH, config="", input_size=(320, 320),
    score_threshold=0.6, nms_threshold=0.3, top_k=5000
)

# Face recognizer
recognizer = cv2.FaceRecognizerSF.create(model=SFACE_PATH, config="")

# Face expression net
emotion_net = cv2.dnn.readNetFromONNX(EMOTION_PATH)

# ==========================================
# 3. LOAD ALL REFERENCE FACES WITH NAMES
# ==========================================

reference_embeddings = {}

def load_reference_faces():
    """Load all faces from reference_faces directory and encode them."""
    if not os.path.exists(REFERENCE_FACES_DIR):
        print(f"[INFO] Reference faces directory not found: {REFERENCE_FACES_DIR}")
        return {}
    
    embeddings = {}
    for person_name in os.listdir(REFERENCE_FACES_DIR):
        person_dir = os.path.join(REFERENCE_FACES_DIR, person_name)
        
        if not os.path.isdir(person_dir):
            continue
        
        person_embeddings = []
        image_files = [f for f in os.listdir(person_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        
        if not image_files:
            print(f"[WARNING] No images found for person: {person_name}")
            continue
        
        for img_file in image_files:
            img_path = os.path.join(person_dir, img_file)
            try:
                ref_img = cv2.imread(img_path)
                if ref_img is None:
                    print(f"[WARNING] Could not read image: {img_path}")
                    continue
                
                h, w, _ = ref_img.shape
                detector.setInputSize((w, h))
                _, faces = detector.detect(ref_img)
                
                if faces is not None and len(faces) > 0:
                    face_aligned = recognizer.alignCrop(ref_img, faces[0])
                    embedding = recognizer.feature(face_aligned)
                    person_embeddings.append(embedding)
                else:
                    print(f"[WARNING] No face detected in {img_path}")
            except Exception as e:
                print(f"[ERROR] Processing {img_path}: {str(e)}")
        
        if person_embeddings:
            # Average all embeddings for this person
            embeddings[person_name] = np.mean(person_embeddings, axis=0)
            print(f"[LOADED] {person_name}: {len(person_embeddings)} reference image(s)")
    
    return embeddings

reference_embeddings = load_reference_faces()

if not reference_embeddings:
    print(f"\n[INFO] No reference faces found. Please add reference images:")
    print(f"[INFO] Create folders in '{REFERENCE_FACES_DIR}' with person names as folder names")
    print(f"[INFO] Place one or more face photos in each folder")
    print(f"[INFO] Example: {REFERENCE_FACES_DIR}/John/photo1.jpg")
else:
    print(f"\n[SUCCESS] Loaded {len(reference_embeddings)} person(s): {list(reference_embeddings.keys())}\n")

# ==========================================
# 4. IDENTIFY DETECTED FACE AGAINST REFERENCES
# ==========================================

def identify_face(live_embedding):
    """
    Compare detected face embedding against all reference embeddings.
    Returns (name, cosine_score, l2_score) for best match.
    """
    if not reference_embeddings:
        return "Unknown", 0.0, float('inf')
    
    best_name = "Unknown"
    best_cosine_score = -1
    best_l2_score = float('inf')
    
    for person_name, ref_embedding in reference_embeddings.items():
        cosine_score = recognizer.match(ref_embedding, live_embedding, cv2.FaceRecognizerSF_FR_COSINE)
        l2_score = recognizer.match(ref_embedding, live_embedding, cv2.FaceRecognizerSF_FR_NORM_L2)
        
        # Check if this is the best match so far
        if cosine_score > best_cosine_score:
            best_cosine_score = cosine_score
            best_l2_score = l2_score
            best_name = person_name
    
    return best_name, best_cosine_score, best_l2_score

# ==========================================
# 5. UNIFIED LIVE MONITORING LOOP
# ==========================================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Failed to connect to system webcam.")

print("Multi-Person Identity & Mood Tracker initiated. Press 'q' to close window.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h_f, w_f, _ = frame.shape
    detector.setInputSize((w_f, h_f))
    _, live_faces = detector.detect(frame)

    if live_faces is not None:
        for face in live_faces:
            # 1. Gather bounding coordinates safely
            x, y, w, h = list(map(int, face[:4]))
            x, y = max(0, x), max(0, y)
            w, h = min(w_f - x, w), min(h_f - y, h)
            if w <= 0 or h <= 0:
                continue

            # 2. PROCESS IDENTITY (SFace Integration - Multi-person)
            live_face_aligned = recognizer.alignCrop(frame, face)
            live_embedding = recognizer.feature(live_face_aligned)
            
            identified_name, cosine_score, l2_score = identify_face(live_embedding)
            
            # Evaluate identity match conditions
            if cosine_score >= COSINE_THRESHOLD and l2_score <= L2_THRESHOLD:
                identity_label = identified_name
                border_color = (0, 255, 0)  # Green color for known persons
            else:
                identity_label = "Unknown"
                border_color = (0, 0, 255)  # Red color for strangers

            # 3. PROCESS MOOD DETECTION (Contrast Enhanced)
            try:
                pad_w = int(w * 0.15)
                pad_h = int(h * 0.15)
                
                x1 = max(0, x - pad_w)
                y1 = max(0, y - pad_h)
                x2 = min(w_f, x + w + pad_w)
                y2 = min(h_f, y + h + pad_h)
                
                face_crop = frame[y1:y2, x1:x2]
                
                if face_crop.size > 0:
                    # Step A: Convert to grayscale AND Equalize Histogram 
                    # (Crucial: This forces facial wrinkles/shadows to pop out for the AI)
                    gray_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
                    gray_crop = cv2.equalizeHist(gray_crop) 
                    
                    # Step B & C: Build Blob
                    emotion_blob = cv2.dnn.blobFromImage(
                        gray_crop, 
                        scalefactor=1.0, 
                        size=(64, 64), 
                        mean=0, 
                        swapRB=False, 
                        crop=False
                    )
                    
                    emotion_net.setInput(emotion_blob)
                    emotion_preds = emotion_net.forward()
                    
                    # Step D: Extract logits and normalize
                    logits = emotion_preds[0].flatten()
                    shifted_logits = logits - np.max(logits)
                    exp_preds = np.exp(shifted_logits)
                    probabilities = exp_preds / np.sum(exp_preds)
                    
                    # Sort the array to find the top predictions
                    top_indices = np.argsort(probabilities)[::-1]
                    pred_idx = top_indices[0]
                    detected_emotion = EMOTIONS[pred_idx]
                    confidence = probabilities[pred_idx]
                    
                    # --- DEBUG CONSOLE: Watch these numbers when you make a face ---
                    print(f"[{identity_label}] Top 3: {EMOTIONS[top_indices[0]]}({probabilities[top_indices[0]]*100:.0f}%) | "
                          f"{EMOTIONS[top_indices[1]]}({probabilities[top_indices[1]]*100:.0f}%) | "
                          f"{EMOTIONS[top_indices[2]]}({probabilities[top_indices[2]]*100:.0f}%)")
                    
                    # Filter output through threshold constraints
                    target_threshold = EMOTION_THRESHOLDS.get(detected_emotion, 0.40)
                    if confidence >= target_threshold:
                        mood_label = f"{detected_emotion} ({confidence * 100:.0f}%)"
                    else:
                        mood_label = f"Uncertain ({detected_emotion}: {confidence * 100:.0f}%)"
                else:
                    mood_label = "Crop Failed"
                    
            except Exception as e:
                mood_label = "Computing..."
            
            # 4. RENDER UNIFIED OVERLAY
            cv2.rectangle(frame, (x, y), (x + w, y + h), border_color, 2)
            
            # Combine identity and emotion status string
            display_text = f"{identity_label} | Mood: {mood_label}"
            cv2.putText(frame, display_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, border_color, 2)

    cv2.imshow("Multi-Person Identity & Mood Tracker System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
