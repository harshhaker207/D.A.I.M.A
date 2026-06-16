# Multi-Person Face Recognition Setup Guide

## Overview
The updated `sface.py` now supports detecting and identifying **multiple people at once** with their respective names!

## Quick Start - Add Persons (EASIEST WAY!)

### Using the Interactive Person Manager

```bash
python add_person.py
```

This opens an interactive menu where you can:

**Option 1: Add Person from Files**
- Enter person's name
- Provide image file paths
- System automatically creates folders and organizes images

**Option 2: Add Person from Webcam**
- Enter person's name
- Press SPACE to capture photos from webcam
- Press Q when done
- All photos automatically saved with the person's name

**Option 3: View All Persons**
- See all registered people
- Shows how many images each person has

**Option 4: Delete Person**
- Remove a person and all their images

## Manual Setup (Optional)

### Create Reference Folder Structure
```
reference_faces/
├── John/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
├── Sarah/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
└── Mike/
    ├── photo1.jpg
    └── photo2.jpg
```

### Step 2: Add Reference Images (MANUAL)
1. Create a folder named `reference_faces` in the same directory as `sface.py`
2. Inside `reference_faces`, create a subfolder for each person using their name
3. Add one or more clear face photos to each subfolder
   - **Recommended**: 2-3 photos per person in different lighting conditions
   - **Formats**: .jpg, .jpeg, .png, or .bmp
   - **Quality**: Clear, front-facing photos work best

### Step 3: Run the Program
```bash
python sface.py
```

## Example Output
```
[LOADED] John: 2 reference image(s)
[LOADED] Sarah: 3 reference image(s)
[LOADED] Mike: 1 reference image(s)

[SUCCESS] Loaded 3 person(s): ['John', 'Sarah', 'Mike']

Multi-Person Identity & Mood Tracker initiated. Press 'q' to close window.
[John] Top 3: Happy(85%) | Neutral(10%) | Surprise(5%)
[Sarah] Top 3: Neutral(92%) | Happy(5%) | Surprise(3%)
[Mike] Top 3: Angry(78%) | Sad(15%) | Neutral(7%)
```

## add_person.py - Interactive Menu

### Add Person from Files
```
Enter person's name: John
📁 Created/Using directory: reference_faces/John
Provide image file paths (one per line, press Enter twice when done)

Image path #1: C:/Users/harsh/Pictures/john_photo1.jpg
✅ Added: john_photo1.jpg

Image path #2: C:/Users/harsh/Pictures/john_photo2.jpg
✅ Added: john_photo2.jpg

Image path #3:
✅ Successfully added 2 image(s) for 'John'!
```

### Add Person from Webcam
```
Enter person's name: Sarah
📷 Webcam opened for 'Sarah'

Controls:
  SPACE - Capture image
  Q     - Finish
  ESC   - Cancel

SPACE → ✅ Captured image 1: Sarah_1.jpg
SPACE → ✅ Captured image 2: Sarah_2.jpg
Q → ✅ Successfully captured 2 image(s) for 'Sarah'!
```

### View All Persons
```
📋 Total persons: 2

👤 John: 2 image(s)
   └─ john_photo1.jpg
   └─ john_photo2.jpg

👤 Sarah: 2 image(s)
   └─ Sarah_1.jpg
   └─ Sarah_2.jpg
```

## Key Features

✅ **Multi-Person Detection**: Detects multiple people in the same frame simultaneously
✅ **Name Recognition**: Each person is labeled with their actual name
✅ **Mood Detection**: Shows emotion/mood for each detected person
✅ **Real-Time Processing**: Live webcam feed analysis
✅ **Flexible Reference**: Add as many people as needed
✅ **Easy Management**: Interactive CLI tool to add/delete persons
✅ **Webcam Capture**: Take photos directly from webcam
✅ **File Import**: Add existing photos from your computer

## Adjusting Sensitivity

If the system is too strict or too lenient with face matching, adjust these values in `sface.py`:

```python
COSINE_THRESHOLD = 0.363  # Higher = stricter matching
L2_THRESHOLD = 1.128      # Lower = stricter matching
```

**Tweaking Tips:**
- Increase `COSINE_THRESHOLD` and `L2_THRESHOLD` → More "Unknown" faces
- Decrease `COSINE_THRESHOLD` and `L2_THRESHOLD` → More loose matching

## Troubleshooting

### No reference faces loading
- Ensure folder structure is correct: `reference_faces/PersonName/photo.jpg`
- Check file extensions are .jpg, .jpeg, .png, or .bmp
- Verify at least one image per person

### Faces not being recognized
- Add more reference images (2-3 minimum recommended)
- Try photos with different angles/lighting
- Increase reference image quality (well-lit, front-facing)
- Adjust thresholds if needed

### Program crashes on startup
- Verify ONNX model files exist:
  - face_detection_yunet_2026may.onnx
  - face_recognition_sface_2021dec.onnx
  - emotion-ferplus.onnx

## File Structure
```
Facerecog+mood system/
├── sface.py
├── face_detection_yunet_2026may.onnx
├── face_recognition_sface_2021dec.onnx
├── emotion-ferplus.onnx
└── reference_faces/
    ├── John/
    │   ├── photo1.jpg
    │   └── photo2.jpg
    └── Sarah/
        └── photo1.jpg
```

## Notes
- The system averages multiple embeddings per person for better accuracy
- Press 'q' to quit the webcam window
- Console shows mood probabilities for debugging
