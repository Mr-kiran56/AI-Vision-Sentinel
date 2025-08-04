## 🚀 Just launched "AI Vision Sentinel" - a real-time facial recognition system with Wikipedia integration!


Excited to share my latest project: **AI Vision Sentinel**! This innovative system combines computer vision with web scraping to create an intelligent facial recognition solution.

🔍 **What it does:**
- Real-time face detection and identification using OpenCV
- Dynamic Wikipedia scraping for instant biography generation
- Interactive dashboard with live camera feed and recognition analytics
- Intelligent "identification hold" system to pause scanning after recognition

💻 **Tech stack:**
- Python (Flask backend)
- OpenCV and face_recognition libraries
- BeautifulSoup for web scraping
- Modern HTML/CSS/JS frontend with animated UI
- Real-time video streaming

This project challenged me to solve several interesting problems:
- Implementing efficient face encoding matching
- Creating a seamless Wikipedia scraping pipeline
- Designing an intuitive UI with real-time feedback
- Developing an identification hold system for user control


# AI Vision Sentinel

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0.1-green)](https://flask.palletsprojects.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5.5-red)](https://opencv.org)

**AI Vision Sentinel** is a real-time facial recognition system that identifies 
individuals and automatically retrieves their biographies from Wikipedia. 
The system features an interactive dashboard with live camera feed, recognition analytics, and detailed profile views.

## Key Features

- **Real-time Face Identification**  
  Identifies known individuals using facial encoding matching

- **Wikipedia Integration**  
  Automatically scrapes and displays biographies and images

- **Intelligent Hold System**  
  Pauses identification after successful recognition until manually continued

- **Modern Interactive UI**  
  Animated dashboard with live camera feed and recognition metrics

- **Detailed Profile Views**  
  Typewriter-effect biography display with verification badges

## Tech Stack

- **Backend**: Python, Flask
- **Computer Vision**: OpenCV, face_recognition
- **Web Scraping**: BeautifulSoup, requests
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: NumPy, Pickle

## Installation

1. Clone repository:
```bash
git clone https://github.com/KiranPunna/ai-vision-sentinel.git
cd ai-vision-sentinel
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Prepare face database:
- Add known faces to `static/faces` directory (format: `name.jpg`)
- Generate encodings:
```bash
python encoding_generator.py
```

5. Run application:
```bash
python app.py
```

## Usage

1. Access the dashboard at `http://localhost:5000`
2. Point camera at a person's face
3. View recognition results in real-time
4. Click "Discover Full Profile" for biography
5. Use "Continue Scanning" to resume identification

## Project Structure

```
├── app.py                 - Main application
├── encoding_generator.py  - Face encoding generator
├── templates/             - HTML templates
│   ├── index.html         - Main dashboard
│   └── about.html         - Profile view
├── static/                - Static assets
│   └── faces/             - Known face images
├── Encodefile.p           - Face encodings
└── requirements.txt       - Dependencies
```

## Future Enhancements

- Add authentication system
- Implement recognition for groups of people
- Add database integration
- Develop mobile application version
