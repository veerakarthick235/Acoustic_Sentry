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