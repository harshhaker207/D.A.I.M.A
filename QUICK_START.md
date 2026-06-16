# Quick Start Guide

## 🚀 2-Minute Setup

### Step 1: Add People to the System
```bash
python add_person.py
```

Choose from menu:
- **Option 1**: Add photos from files on your computer
- **Option 2**: Capture photos using webcam (press SPACE to capture, Q to finish)
- **Option 3**: View all registered people
- **Option 4**: Delete a person

### Step 2: Start Face Recognition
```bash
python sface.py
```

The system will:
- ✅ Load all registered people
- ✅ Detect faces in real-time
- ✅ Label each face with their name
- ✅ Detect and show mood for each person
- Press **Q** to exit

## 📁 File Structure Created
```
reference_faces/
├── PersonName1/
│   ├── photo1.jpg
│   └── photo2.jpg
└── PersonName2/
    ├── photo1.jpg
    └── photo2.jpg
```

## 🎯 How to Add a Person

### Method 1: From Existing Photos
```bash
python add_person.py
→ Choose: 1 (Add person from files)
→ Enter name: John
→ Paste full file paths to your photos (one per line)
→ Press Enter twice when done
```

### Method 2: From Webcam
```bash
python add_person.py
→ Choose: 2 (Add person from webcam)
→ Enter name: Sarah
→ Press SPACE to capture photos
→ Press Q when done
```

## 🔍 What Happens During Detection

**Real-time webcam feed shows:**
- 🟩 **Green box** = Known person (matches reference)
- 🟥 **Red box** = Unknown person
- 😊 **Mood label** = Detected emotion (Happy, Sad, Angry, etc.)
- **% Confidence** = How confident the system is

## 💡 Tips for Best Results

✅ **Add 2-3 photos per person** (different angles/lighting)
✅ **Use clear, well-lit photos**
✅ **Front-facing photos work best**
✅ **Different lighting conditions help accuracy**
✅ **High resolution photos = better accuracy**

## ⚙️ System Files

| File | Purpose |
|------|---------|
| `sface.py` | Main face recognition program |
| `add_person.py` | Tool to add/manage people |
| `reference_faces/` | Stores all person photos |
| `*.onnx` | AI models (don't modify) |

## 🆘 Troubleshooting

### "No faces detected in image"
- Ensure photos show clear, front-facing faces
- Check lighting conditions
- Try different photos

### "Person not recognized"
- Add more reference photos
- Try photos from different angles
- Check face is clear and well-lit

### Webcam not working
- Check camera is connected
- Try another app to verify camera works
- Restart the script

## 🎮 Controls

**During Face Recognition (sface.py):**
- **Q** = Quit and close

**During Webcam Capture (add_person.py option 2):**
- **SPACE** = Capture photo
- **Q** = Finish adding person
- **ESC** = Cancel

## 📊 Example Output

```
[LOADED] John: 2 reference image(s)
[LOADED] Sarah: 1 reference image(s)

[SUCCESS] Loaded 2 person(s): ['John', 'Sarah']

Multi-Person Identity & Mood Tracker initiated. Press 'q' to close window.
[John] Top 3: Happy(92%) | Neutral(6%) | Surprise(2%)
[Sarah] Top 3: Neutral(88%) | Happy(8%) | Sad(4%)
```

---

**That's it! You're all set!** 🎉
