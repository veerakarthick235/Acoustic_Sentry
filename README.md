# 🎧 Acoustic Sentry: AI Cough Analysis Prototype

**Acoustic Sentry** is a **web-based prototype** designed for the **CuraQuest Ideathon**.  
It demonstrates an innovative system for analyzing **cough sounds using AI** to provide an **initial risk assessment** for respiratory diseases.  

The application records a user’s cough in the browser, sends it to a **Python Flask backend** for analysis, and displays a **simulated risk level** along with a **visual spectrogram** of the audio.

> ⚙️ *Note: This project focuses on demonstrating workflow, not medical accuracy. The AI analysis is simulated for prototype purposes.*

---

## 🖼️ Screenshot
*(It is highly recommended to include a screenshot of your running application here.)*

---

## ✨ Features

- 🎙️ **In-Browser Audio Recording** – Uses the **MediaRecorder API** to capture audio directly from the user’s microphone.  
- 🧠 **Python Backend** – A lightweight **Flask server** handles audio uploads and processing.  
- 🤖 **Simulated AI Analysis** – Mimics an ML model to classify coughs into **Low**, **Medium**, or **High** risk categories.  
- 🎵 **Dynamic Spectrogram Generation** – Creates and displays a **mel-spectrogram** for each cough using **librosa** and **matplotlib**.  
- 🖥️ **Responsive UI** – A clean, dark-themed interface optimized for both desktop and mobile browsers.  

---

## 🛠️ Tech Stack

| Layer | Technology |
|--------|-------------|
| **Backend** | Python, Flask |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Audio Processing** | Librosa |
| **Image Generation** | Matplotlib |
| **System Dependency** | FFmpeg |

---

## 📁 Project Structure

```
acoustic-sentry/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
├── templates/
│   └── index.html
├── uploads/
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure the following are installed:

- **Python 3.9+**
- **FFmpeg** *(required for Librosa to process audio)*  

> If FFmpeg is not installed, please follow the official installation guide for your operating system.

---

### Installation & Setup

#### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/acoustic-sentry.git
cd acoustic-sentry
```

#### 2️⃣ Create and activate a virtual environment

```bash
# Create environment
python -m venv venv

# Activate it (Windows)
.env\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

#### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, use this:

```
Flask>=2.0
Flask-Cors>=3.0
librosa>=0.9
matplotlib>=3.5
numpy
```

---

### Run the Application

```bash
python app.py
```

Now open your browser and go to:

🔗 **http://127.0.0.1:5000**

---

## 🎤 Usage

1. Open the app — your browser will ask for **microphone access** → click **Allow**.  
2. Click the **microphone icon** to start recording.  
3. Cough clearly near your microphone.  
4. Click again to stop recording.  
5. Wait for the server to process the audio.  
6. View your **simulated risk level** and **spectrogram visualization**.

---

## ⚠️ Disclaimer

This is a **proof-of-concept prototype**.  
The analysis is **simulated** and **not based on a trained AI model**.  
It should **not be used for medical diagnosis or decisions**.  
Always consult a **qualified healthcare professional** for health concerns.

---

## 💡 Future Improvements

- [ ] **Integrate a Real ML Model:**  
  Train a CNN on a real cough dataset to replace simulated analysis.  

- [ ] **User Accounts:**  
  Add authentication to track user recording history.  

- [ ] **Database Integration:**  
  Store audio metadata, results, and user profiles (PostgreSQL or SQLite).  

- [ ] **Enhanced Audio Features:**  
  Include advanced features such as **MFCCs**, **Chroma**, and **Zero-Crossing Rate** for richer analysis.  

---

📘 **Author:** Veera Karthick  
🎓 *AI & Data Science Student*

