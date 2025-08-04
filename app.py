from flask import Flask, render_template, Response, jsonify, url_for
import cv2
import pickle
import face_recognition
import numpy as np
import cvzone
import requests
from bs4 import BeautifulSoup
import os
import atexit
import time
import threading

app = Flask(__name__)

# Initialize camera
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    raise RuntimeError("Could not start camera.")

# Load encodings
with open("Encodefile.p", "rb") as file:
    encodeListKnown, imgIds = pickle.load(file)

# Database with corrected paths
database = {
    "Virat_Kohli": {
        "name": "Virat Kohli",
        "img": "faces/Virat_Kohli.jpg",
        "category": "Cricket Player",
        "age": "35"
    },
    "Narendra_Modi": {
        "name": "Narendra Modi",
        "img": "faces/Narendra_Modi.webp",
        "category": "Prime Minister",
        "age": "73"
    },
    "Kajal_Aggarwal": {
        "name": "Kajal Aggarwal",
        "img": "faces/Kajal_Aggarwal.jpg",
        "category": "Actress",
        "age": "37"
    }
}

# Track current person
current_status = {
    'status': 'Scanning...', 
    'name': '---',
    'held': False  # To track if identification is being held
}

# Video feed generator
def generate_frames():
    frame_count = 0
    process_every = 3
    last_face = None

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame_count += 1
        
        # Reset status if not holding identification
        if not current_status['held']:
            current_status['status'] = "Scanning..."
            current_status['name'] = "---"
            last_face = None

        if frame_count % process_every == 0 and not current_status['held']:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            faces = face_recognition.face_locations(rgb_frame)
            encodings = face_recognition.face_encodings(rgb_frame, faces)

            for encoding, faceLoc in zip(encodings, faces):
                matches = face_recognition.compare_faces(encodeListKnown, encoding)
                face_dist = face_recognition.face_distance(encodeListKnown, encoding)
                matchIndex = np.argmin(face_dist)

                if matches[matchIndex]:
                    name = imgIds[matchIndex].replace(" ", "_")
                    current_status['status'] = "Identified"
                    current_status['name'] = name
                    current_status['held'] = True  # Hold the identification
                    last_face = (faceLoc, name)
                    break

        # Draw last identified face if holding
        if current_status['held'] and last_face:
            faceLoc, name = last_face
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = (x1, y1, x2 - x1, y2 - y1)
            frame = cvzone.cornerRect(frame, bbox, rt=1)
            cv2.putText(frame, name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        # Add timestamp and FPS counter
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (130, frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Add "HOLDING" indicator when identification is held
        if current_status['held']:
            cv2.putText(frame, "HOLDING IDENTIFICATION", (frame.shape[1] - 400, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Resize for display after processing
        display_frame = cv2.resize(frame, (640, 480))
        ret, buffer = cv2.imencode('.jpg', display_frame)
        if not ret:
            continue
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_status')
def get_status():
    name = current_status["name"]
    status = current_status["status"]
    held = current_status["held"]
    person_data = database.get(name, {})
    img_url = ""
    
    # Generate image URL only if person is identified
    if status == "Identified" and person_data.get("img"):
        img_url = url_for('static', filename=person_data.get("img"))
    
    return jsonify({
        "status": status,
        "name": person_data.get("name", "---") if status == "Identified" else "---",
        "name_id": name,
        "img": img_url,
        "held": held
    })

@app.route('/reset_hold')
def reset_hold():
    current_status['held'] = False
    return jsonify(success=True)

@app.route('/about/<name>')
def about(name):
    name_key = name.replace(" ", "_")
    
    if name_key not in database:
        return "Person not found", 404

    person = database[name_key]
    url_name = person["name"].replace(" ", "_")
    wiki_url = f"https://en.wikipedia.org/wiki/{url_name}"

    try:
        response = requests.get(wiki_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract summary
        summary = []
        content = soup.find(id="mw-content-text")
        if content:
            for p in content.find_all('p'):
                text = p.get_text().strip()
                if text and len(text) > 100 and not text.startswith('^ '):
                    summary.append(text)
                if len(summary) >= 3:
                    break
        
        # Extract image
        image_url = ""
        infobox = soup.find(class_="infobox")
        if infobox:
            img_tag = infobox.find('img')
            if img_tag and 'src' in img_tag.attrs:
                image_url = "https:" + img_tag['src']
        
        # If no summary found, use a fallback
        if not summary:
            summary = [f"Wikipedia summary for {person['name']} is currently unavailable."]
    
    except Exception as e:
        print(f"Error scraping Wikipedia: {e}")
        summary = [f"Could not retrieve information from Wikipedia. Error: {str(e)}"]
        image_url = ""
    
    return render_template("about.html", summary=summary, image_url=image_url, person=person)

@atexit.register
def cleanup():
    if camera.isOpened():
        camera.release()
        print("Camera released.")

if __name__ == "__main__":
    app.run(debug=True)