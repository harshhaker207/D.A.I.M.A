# 🎯 Multi-Person Face Recognition + Mood Detection System

A Python-based real-time face recognition system that can **detect and identify multiple people simultaneously** while also detecting their emotions/mood.

## ✨ Features

- 👥 **Multi-Person Detection** - Detect and identify multiple people in one frame
- 😊 **Mood Detection** - Recognize emotions: Happy, Sad, Angry, Neutral, Surprise, Disgust, Fear, Contempt
- 📸 **Easy Person Management** - Interactive tool to add/delete people with just a name
- 📷 **Webcam Capture** - Take reference photos directly from webcam
- 📁 **File Import** - Add existing photos from your computer
- 🎬 **Real-Time Processing** - Live webcam feed analysis
- 🟩/🟥 **Visual Feedback** - Green box for known people, red for unknown

## 🚀 Quick Start

### 1. Add People to the System
```bash
python add_person.py
```

Choose an option:
- **Option 1**: Add person from files (browse existing photos)
- **Option 2**: Add person from webcam (capture photos)
- **Option 3**: View all registered people
- **Option 4**: Delete a person
- **Option 5**: Exit

### 2. Run Face Recognition
```bash
python sface.py
```

The system will detect all faces, label them with names, and show emotions!

## 📁 Project Structure

```
Facerecog+mood system/
├── sface.py                           # Main face recognition program
├── add_person.py                      # Interactive person management tool
├── face_detection_yunet_2026may.onnx  # Face detection model
├── face_recognition_sface_2021dec.onnx # Face recognition model
├── emotion-ferplus.onnx               # Emotion detection model
├── reference_faces/                   # Auto-created - stores person photos
│   ├── John/
│   │   ├── photo1.jpg
│   │   └── photo2.jpg
│   └── Sarah/
│       ├── sarah_1.jpg
│       └── sarah_2.jpg
├── QUICK_START.md                     # Quick reference guide
└── README.md                          # This file
```

## 📊 How It Works

### Adding a Person

#### Option 1: From Files
1. Run `python add_person.py`
2. Select "1 - Add person from files"
3. Enter person's name
4. Provide file paths to photos (one per line)
5. System creates folder and organizes photos automatically

#### Option 2: From Webcam
1. Run `python add_person.py`
2. Select "2 - Add person from webcam"
3. Enter person's name
4. Press SPACE to capture photos
5. Press Q when done

### Detecting Faces

When you run `sface.py`:
- System loads all registered people
- Webcam detects faces in real-time
- Each detected face is compared with all reference embeddings
- Best match determines the person's name
- Mood is detected separately for each face
- Results displayed on video feed

## 🎨 Display Format

```
[PersonName] | Mood: Happy (85%)
```

**Colors:**
- 🟩 **Green box** = Known person (matches reference embedding)
- 🟥 **Red box** = Unknown person (doesn't match any reference)

## ⚙️ System Requirements

- Python 3.7+
- OpenCV (`opencv-python`)
- NumPy (`numpy`)
- Webcam access

## 📦 Installation

```bash
pip install opencv-python numpy
```

All ONNX models are included in the project.

## 🔧 Configuration

### Adjust Recognition Sensitivity

Edit `sface.py` to modify thresholds:

```python
COSINE_THRESHOLD = 0.363  # Higher = stricter matching
L2_THRESHOLD = 1.128      # Lower = stricter matching
```

- **Increase thresholds** → More "Unknown" faces
- **Decrease thresholds** → More loose matching (false positives)

### Emotion Confidence Levels

Edit `sface.py` to modify emotion detection thresholds:

```python
EMOTION_THRESHOLDS = {
    "Neutral": 0.40,
    "Happy": 0.40,
    # ... adjust per emotion
}
```

## 💡 Tips for Best Results

✅ **Quality > Quantity**: 2-3 clear photos > many blurry photos
✅ **Variety**: Different angles, lighting, and expressions
✅ **Lighting**: Well-lit photos work best
✅ **Face Position**: Front-facing or near-frontal faces
✅ **Resolution**: Higher resolution photos improve accuracy

## 🎯 Recommended Setup

For each person, add:
1. **Photo 1**: Face straight-on, good lighting
2. **Photo 2**: Face from slight angle, different lighting
3. **Photo 3**: (Optional) Different expression or lighting

## 📋 File Format Support

Supported image formats: `.jpg`, `.jpeg`, `.png`, `.bmp`

## 🎮 Keyboard Controls

**During Face Recognition (sface.py):**
- **Q** = Exit and close window

**During Webcam Capture (add_person.py option 2):**
- **SPACE** = Capture photo
- **Q** = Finish adding photos
- **ESC** = Cancel operation

## 🔍 Understanding the Output

### Console Output Example
```
[LOADED] John: 2 reference image(s)
[LOADED] Sarah: 3 reference image(s)
[SUCCESS] Loaded 2 person(s): ['John', 'Sarah']

Multi-Person Identity & Mood Tracker initiated. Press 'q' to close window.
[John] Top 3: Happy(92%) | Neutral(6%) | Surprise(2%)
[Sarah] Top 3: Neutral(85%) | Happy(12%) | Sad(3%)
```

**Interpretation:**
- `[John]` - Person detected and identified
- `Happy(92%)` - Top predicted emotion with confidence
- Shows top 3 most likely emotions

## 🆘 Troubleshooting

### "No faces detected in image"
→ Try photos with clearer faces, better lighting

### "Person not recognized"
→ Add more reference photos, check lighting conditions

### "Webcam not opening"
→ Check camera is connected, restart script

### "No reference faces found"
→ Add at least one person using `add_person.py` first

### Accuracy issues
→ Add more diverse reference photos (different angles/lighting)

## 📊 Model Information

| Model | Purpose | Source |
|-------|---------|--------|
| YuNet | Face Detection | OpenCV |
| SFace | Face Recognition | OpenCV |
| FERPlus | Emotion Detection | Microsoft ONNX Zoo |

## 🤝 Contributing

To improve the system:
- Add more reference photos for better accuracy
- Test with different lighting conditions
- Report issues with specific face angles

## 📝 License

This project uses OpenCV models available under their respective licenses.

## ✅ Checklist Before Running

- [ ] All `.onnx` model files present
- [ ] `reference_faces/` folder exists (auto-created on first run)
- [ ] At least one person added via `add_person.py`
- [ ] Webcam is working
- [ ] Python packages installed (`opencv-python`, `numpy`)

## 🎉 You're Ready!

1. **Add people**: `python add_person.py`
2. **Start detection**: `python sface.py`
3. **Enjoy**: Real-time multi-person face recognition!

---

**Questions?** Check `QUICK_START.md` for common tasks or `MULTI_PERSON_SETUP.md` for detailed setup.
