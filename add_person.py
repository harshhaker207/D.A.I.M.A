import os
import cv2
import shutil
from pathlib import Path

REFERENCE_FACES_DIR = os.path.join("reference_faces")

def ensure_directory():
    """Create reference_faces directory if it doesn't exist."""
    os.makedirs(REFERENCE_FACES_DIR, exist_ok=True)

def add_person_from_files():
    """Add a person by providing image file paths."""
    print("\n" + "="*60)
    print("ADD PERSON FROM FILES")
    print("="*60)
    
    person_name = input("\nEnter person's name: ").strip()
    
    if not person_name:
        print("❌ Name cannot be empty!")
        return False
    
    if not person_name.replace(" ", "").replace("-", "").isalnum():
        print("❌ Name should only contain letters, numbers, spaces, and hyphens!")
        return False
    
    person_dir = os.path.join(REFERENCE_FACES_DIR, person_name)
    
    if os.path.exists(person_dir) and os.listdir(person_dir):
        response = input(f"📁 Person '{person_name}' already exists. Add more images? (y/n): ").lower()
        if response != 'y':
            print("❌ Operation cancelled.")
            return False
    
    os.makedirs(person_dir, exist_ok=True)
    
    print(f"\n📁 Created/Using directory: {person_dir}")
    print("Provide image file paths (one per line, press Enter twice when done)")
    print("Supported formats: .jpg, .jpeg, .png, .bmp")
    
    added_count = 0
    while True:
        file_path = input(f"\nImage path #{added_count + 1} (or press Enter to finish): ").strip()
        
        if not file_path:
            break
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
        
        # Check if it's a valid image format
        valid_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.JPG', '.JPEG', '.PNG', '.BMP')
        if not file_path.lower().endswith(valid_formats):
            print(f"❌ Unsupported format. Use: {valid_formats}")
            continue
        
        try:
            # Verify it's actually an image
            img = cv2.imread(file_path)
            if img is None:
                print(f"❌ Could not read image: {file_path}")
                continue
            
            # Copy file to person directory
            filename = os.path.basename(file_path)
            dest_path = os.path.join(person_dir, filename)
            
            # Handle duplicate filenames
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(person_dir, f"{base}_{counter}{ext}")
                counter += 1
            
            shutil.copy2(file_path, dest_path)
            print(f"✅ Added: {filename}")
            added_count += 1
            
        except Exception as e:
            print(f"❌ Error processing file: {str(e)}")
    
    if added_count > 0:
        print(f"\n✅ Successfully added {added_count} image(s) for '{person_name}'!")
        return True
    else:
        print(f"⚠️  No images added for '{person_name}'.")
        if not os.listdir(person_dir):
            os.rmdir(person_dir)
        return False

def add_person_from_webcam():
    """Add a person by capturing images from webcam."""
    print("\n" + "="*60)
    print("ADD PERSON FROM WEBCAM")
    print("="*60)
    
    person_name = input("\nEnter person's name: ").strip()
    
    if not person_name:
        print("❌ Name cannot be empty!")
        return False
    
    if not person_name.replace(" ", "").replace("-", "").isalnum():
        print("❌ Name should only contain letters, numbers, spaces, and hyphens!")
        return False
    
    person_dir = os.path.join(REFERENCE_FACES_DIR, person_name)
    
    if os.path.exists(person_dir) and os.listdir(person_dir):
        response = input(f"📁 Person '{person_name}' already exists. Add more images? (y/n): ").lower()
        if response != 'y':
            print("❌ Operation cancelled.")
            return False
    
    os.makedirs(person_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open webcam!")
        return False
    
    print(f"\n📷 Webcam opened for '{person_name}'")
    print("Controls:")
    print("  SPACE - Capture image")
    print("  Q     - Finish")
    print("  ESC   - Cancel")
    
    capture_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Add instruction text on frame
        cv2.putText(frame, f"Person: {person_name} | Captured: {capture_count}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "SPACE=Capture | Q=Done | ESC=Cancel", 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow(f"Webcam - Adding {person_name}", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Space to capture
            filename = f"{person_name}_{capture_count + 1}.jpg"
            filepath = os.path.join(person_dir, filename)
            cv2.imwrite(filepath, frame)
            print(f"✅ Captured image {capture_count + 1}: {filename}")
            capture_count += 1
            
        elif key == ord('q') or key == ord('Q'):  # Q to finish
            break
            
        elif key == 27:  # ESC to cancel
            print("❌ Operation cancelled!")
            cap.release()
            cv2.destroyAllWindows()
            # Remove empty directory
            if os.path.exists(person_dir) and not os.listdir(person_dir):
                os.rmdir(person_dir)
            return False
    
    cap.release()
    cv2.destroyAllWindows()
    
    if capture_count > 0:
        print(f"\n✅ Successfully captured {capture_count} image(s) for '{person_name}'!")
        return True
    else:
        print(f"⚠️  No images captured for '{person_name}'.")
        if not os.listdir(person_dir):
            os.rmdir(person_dir)
        return False

def view_all_persons():
    """Display all registered persons and their images."""
    print("\n" + "="*60)
    print("REGISTERED PERSONS")
    print("="*60)
    
    ensure_directory()
    
    persons = [d for d in os.listdir(REFERENCE_FACES_DIR) 
               if os.path.isdir(os.path.join(REFERENCE_FACES_DIR, d))]
    
    if not persons:
        print("\n❌ No persons registered yet.")
        return
    
    print(f"\n📋 Total persons: {len(persons)}\n")
    
    for person_name in sorted(persons):
        person_dir = os.path.join(REFERENCE_FACES_DIR, person_name)
        images = [f for f in os.listdir(person_dir) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        print(f"👤 {person_name}: {len(images)} image(s)")
        for img in images:
            print(f"   └─ {img}")

def delete_person():
    """Delete a person and all their images."""
    print("\n" + "="*60)
    print("DELETE PERSON")
    print("="*60)
    
    ensure_directory()
    
    persons = [d for d in os.listdir(REFERENCE_FACES_DIR) 
               if os.path.isdir(os.path.join(REFERENCE_FACES_DIR, d))]
    
    if not persons:
        print("\n❌ No persons registered yet.")
        return
    
    print("\n📋 Registered persons:")
    for i, person in enumerate(sorted(persons), 1):
        print(f"  {i}. {person}")
    
    try:
        choice = int(input("\nEnter person number to delete (0 to cancel): "))
        if choice == 0:
            print("❌ Operation cancelled.")
            return
        
        if 1 <= choice <= len(persons):
            person_name = sorted(persons)[choice - 1]
            confirm = input(f"\n⚠️  Are you sure you want to delete '{person_name}'? (y/n): ").lower()
            
            if confirm == 'y':
                person_dir = os.path.join(REFERENCE_FACES_DIR, person_name)
                shutil.rmtree(person_dir)
                print(f"✅ Deleted '{person_name}' and all their images.")
            else:
                print("❌ Operation cancelled.")
        else:
            print("❌ Invalid choice.")
    except ValueError:
        print("❌ Invalid input.")

def main_menu():
    """Display main menu and handle user choice."""
    ensure_directory()
    
    while True:
        print("\n" + "="*60)
        print("FACE RECOGNITION - PERSON MANAGEMENT")
        print("="*60)
        print("\n1️⃣  Add person from files")
        print("2️⃣  Add person from webcam")
        print("3️⃣  View all registered persons")
        print("4️⃣  Delete a person")
        print("5️⃣  Exit")
        print("\n" + "-"*60)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            add_person_from_files()
        elif choice == '2':
            add_person_from_webcam()
        elif choice == '3':
            view_all_persons()
        elif choice == '4':
            delete_person()
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main_menu()
