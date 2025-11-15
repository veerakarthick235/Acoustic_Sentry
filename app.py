import os
import random
import uuid
from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS

# --- Machine Learning, Audio, and Plotting Imports ---
# This specific order is important for matplotlib to work in a server environment
import matplotlib
matplotlib.use('Agg') # Set the backend before importing pyplot
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np


# --- Basic Flask App Setup ---
app = Flask(__name__)
CORS(app) # Enables Cross-Origin Resource Sharing for local development


# --- Folder Configuration ---
# Define paths and create folders if they don't already exist
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(STATIC_FOLDER, 'images'), exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER


# --- Helper Function: Generate Spectrogram ---
def create_spectrogram(audio_path):
    """Generates and saves a spectrogram image from an audio file."""
    try:
        # Load the audio file
        y, sr = librosa.load(audio_path)
        
        # Create a Mel spectrogram
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        S_dB = librosa.power_to_db(S, ref=np.max)
        
        # Plot the spectrogram using matplotlib
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', fmax=8000)
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel-frequency Spectrogram')
        plt.tight_layout()
        
        # Generate a unique filename to prevent browser caching issues
        spectrogram_filename = f'spectrogram_{uuid.uuid4().hex}.png'
        save_path = os.path.join(app.config['STATIC_FOLDER'], 'images', spectrogram_filename)
        plt.savefig(save_path)
        plt.close() # Close the plot to free up memory
        
        # Return the URL path to the saved image
        return url_for('static', filename=f'images/{spectrogram_filename}')
    except Exception as e:
        print(f"Error creating spectrogram: {e}")
        return None


# --- API and Web Page Routes ---
@app.route('/')
def index():
    """Renders the main web page from the templates folder."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_cough():
    """
    Handles the audio file upload, simulates AI analysis, 
    generates a spectrogram, and returns a JSON response.
    """
    if 'audio_data' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    file = request.files['audio_data']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Save the uploaded file to a temporary location
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'cough.wav')
        file.save(filepath)

        # --- SIMULATED AI ANALYSIS ---
        # In a real R&D project, you would load a trained model here
        # and run `model.predict(processed_audio_data)`.
        # For this prototype, we simulate the results.
        risks = ['Low Risk', 'Medium Risk', 'High Risk']
        # Bias the choice towards lower risks to be more realistic
        predicted_risk = random.choices(risks, weights=[0.6, 0.3, 0.1], k=1)[0]
        confidence = round(random.uniform(75, 98), 2)

        feedback_messages = {
            "Low Risk": "The acoustic signature appears normal. This is likely a common viral cough. Monitor symptoms and consult a doctor if they worsen.",
            "Medium Risk": "Some atypical acoustic markers were detected. This could indicate bronchitis or a persistent infection. A follow-up with a healthcare professional is recommended.",
            "High Risk": "Significant anomalies in the cough signature match patterns associated with severe respiratory conditions. Please seek immediate medical consultation."
        }
        feedback = feedback_messages[predicted_risk]
        
        # --- Generate Spectrogram Visualization ---
        spectrogram_url = create_spectrogram(filepath)
        if not spectrogram_url:
            # This will happen if create_spectrogram returns None due to an error
            return jsonify({'error': 'Failed to process audio file and create spectrogram'}), 500

        # --- Prepare and Send the Final JSON Response ---
        response_data = {
            'risk_level': predicted_risk,
            'confidence': confidence,
            'feedback': feedback,
            'spectrogram_url': spectrogram_url
        }
        
        # Optional: Clean up the uploaded audio file after processing
        # os.remove(filepath)

        return jsonify(response_data)

    except Exception as e:
        # This is a general catch-all for any other unexpected errors
        print(f"An error occurred in /analyze route: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500

# --- Main Execution Block ---
if __name__ == '__main__':
    # Runs the Flask app with debug mode on

    app.run(debug=True)



























































Here is a clear, step-by-step guide on how to perform this HBase experiment inside your college lab. Follow these steps exactly and you will complete the practical smoothly.


---

✅ How to Perform the HBase Experiment in the Lab

1. Start Hadoop Services

Before using HBase, Hadoop must be running.

Open terminal and run:

start-dfs.sh
start-yarn.sh

Check if it is running:

jps

You should see:

Namenode

Datanode

SecondaryNamenode

ResourceManager

NodeManager



---

2. Start HBase

Run:

start-hbase.sh

Check if it started:

jps

You should see:

HMaster

HRegionServer



---

3. Open HBase Shell

hbase shell

Now you are inside the HBase environment.


---

🔹 Perform the Experiment Commands

(1) Create a Table

create 'student', 'personal', 'academic'


---

(2) Insert Data

put 'student', '1', 'personal:name', 'Veera'
put 'student', '1', 'personal:age', '21'
put 'student', '1', 'academic:dept', 'AI&DS'
put 'student', '1', 'academic:year', '3'


---

(3) Retrieve Data

get 'student', '1'


---

(4) Delete Data

Delete one column:

delete 'student', '1', 'personal:age'

Delete full row:

deleteall 'student', '1'


---

🧪 4. Exit HBase Shell

exit


---

🛑 5. Stop Services After Work

stop-hbase.sh
stop-dfs.sh
stop-yarn.sh


---

🎓 This is exactly what you will do in the lab.

If you want, I can also give you a lab observation table, viva questions, or a PDF version for submission.










Below is the complete Multimedia & Animation Lab record answer for
“Make a video, compress it, and convert it to other formats like MP4.”
(Simple, clear, and suitable for submission.)


---

Experiment: Video Creation, Compression & Format Conversion

Aim

To create a video, apply compression techniques to reduce its file size, and convert the video into other popular formats such as MP4 using multimedia tools.


---

Algorithm

1. Video Creation

1. Start the video creation software (e.g., Windows Movie Maker, Adobe Premiere, OpenShot, Kdenlive).


2. Import images, audio, and video clips.


3. Arrange clips on the timeline in the required order.


4. Add transitions, titles, and effects if needed.


5. Export the project as an uncompressed or high-quality video file.



2. Video Compression

1. Open any compression/conversion tool (e.g., HandBrake, VLC, FFmpeg).


2. Load the high-quality video file.


3. Select a compression preset (H.264 or H.265).


4. Set output resolution and bitrate.


5. Start compression to reduce the file size.



3. Video Format Conversion

1. Open the video converter tool.


2. Import the compressed video file.


3. Choose the output format (MP4, AVI, MKV, MOV, etc.).


4. Select the codec (H.264 for MP4).


5. Convert and save the final file.




---

Procedure

A. Creating a Video

1. Open OpenShot / Windows Movie Maker / any lab software.


2. Click Import Files and load pictures, audio, or video clips.


3. Drag and drop the media into the timeline.


4. Adjust clip duration, add text titles, transitions, and background music.


5. Go to Export Video → choose High Quality → save as .mp4 or .avi.




---

B. Compressing the Video

(Using HandBrake / VLC / FFmpeg)

1. Open HandBrake.


2. Click Open Source and select the exported video.


3. Choose a preset like Fast 720p30.


4. Under Video, select:

Video Codec: H.264 (x264)

Bitrate: 1000–2000 kbps



5. Choose the destination path and click Start Encode.


6. The compressed video is generated with lower file size.




---

C. Converting Video Format

(Using VLC or FFmpeg)

Using VLC:

1. Open VLC → Media → Convert/Save.


2. Add the compressed video file.


3. Select the output profile (e.g., Video – H.264 + MP3 (MP4)).


4. Choose destination file name with extension .mp4, .avi, or .mkv.


5. Click Start to convert.



Using FFmpeg (command line):

ffmpeg -i input.avi output.mp4


---

Results

1. A video was successfully created using multimedia editing software.


2. The created video was compressed using H.264 codec, reducing the file size without much quality loss.


3. The compressed video was converted into different formats such as MP4, AVI, and MKV using VLC/FFmpeg.


4. Thus, video creation, compression, and format conversion were achieved successfully.




---

If you want, I can also give:

✅ Viva Questions & Answers
✅ Thanglish version
✅ Diagram / workflow figure
Just tell me!


Below are the best Viva Voce questions and answers for the experiment
“Video Creation, Compression & Conversion” — professional, clear, and suitable for lab exams.


---

Viva Voce Questions & Answers

1. What is video compression?

Video compression is the process of reducing the size of a video file by removing redundant data while maintaining acceptable visual quality.


---

2. Why do we need to compress videos?

To reduce storage space, decrease upload/download time, and enable smooth streaming on various devices.


---

3. What are the two types of compression?

Lossless Compression – No quality loss.

Lossy Compression – Some quality is lost but reduces file size significantly.



---

4. Name any two video compression codecs.

H.264 and H.265.


---

5. What is a video codec?

A codec (Coder-Decoder) is a software or hardware tool used to compress and decompress video files.


---

6. What are popular video file formats?

MP4, AVI, MKV, MOV, FLV.


---

7. What is the difference between a format and a codec?

A format is a container (e.g., MP4), while a codec is the compression method used inside the container (e.g., H.264).


---

8. Which codec is commonly used in MP4 format?

H.264.


---

9. What tools are used for video conversion?

VLC Media Player, FFmpeg, HandBrake, Adobe Media Encoder.


---

10. What is FFmpeg?

FFmpeg is a command-line tool used for video editing, conversion, and compression.


---

11. Write an FFmpeg command to convert video to MP4.

ffmpeg -i input.avi output.mp4


---

12. What is bitrate?

Bitrate is the amount of data processed per second in a video and affects both file size and quality.


---

13. How does reducing bitrate affect video quality?

Lower bitrate reduces file size but may decrease quality.


---

14. What is frame rate?

Frame rate (fps) is the number of video frames displayed per second.


---

15. How does resolution affect video quality?

Higher resolution gives better clarity but increases file size.


---

16. What is transcoding?

Transcoding is converting a video from one format or codec to another.


---

17. What is a container format?

A container format stores video, audio, subtitles, and metadata in one file.


---

18. What is H.265 (HEVC)?

A modern codec that provides better compression efficiency compared to H.264.


---

19. Why is MP4 widely used?

It is compatible with almost all devices, offers good compression, and maintains high quality.


---

20. What is the purpose of creating a video in lab experiments?

To understand video production workflow, editing, compression techniques, and format conversion.


---

If you want, I can also generate:
✅ Short answers version
✅ 25 or 50 more Viva questions
✅ Notes for exam
Just tell me!
