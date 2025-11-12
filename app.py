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



import java.util.*;

class HDLC_Framing {
    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);

        // ---------- BIT STUFFING ----------
        System.out.println("Enter bit stream:");
        String bits = sc.nextLine();
        String stuffed = "";
        int count = 0;

        for (int i = 0; i < bits.length(); i++) {
            char b = bits.charAt(i);
            stuffed += b;
            if (b == '1') {
                count++;
                if (count == 5) {
                    stuffed += '0'; // insert 0 after five 1’s
                    count = 0;
                }
            } else {
                count = 0;
            }
        }

        System.out.println("\nBit Stuffed Data: " + stuffed);

        // ---------- CHARACTER STUFFING ----------
        System.out.println("\nEnter message for character stuffing:");
        String msg = sc.nextLine();

        char FLAG = '~';
        char ESC = '}';
        String stuffedMsg = "~"; // start flag

        for (int i = 0; i < msg.length(); i++) {
            char c = msg.charAt(i);
            if (c == FLAG || c == ESC)
                stuffedMsg += ESC; // add escape
            stuffedMsg += c;
        }

        stuffedMsg += "~"; // end flag
        System.out.println("\nCharacter Stuffed Frame: " + stuffedMsg);

        sc.close();
    }
}




# Sentiment Analysis using LSTM (Easy Version)

from tensorflow.keras.datasets import imdb
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Step 1: Load dataset
max_words = 5000
max_len = 100
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_words)

# Step 2: Preprocess (pad sequences)
x_train = pad_sequences(x_train, maxlen=max_len)
x_test = pad_sequences(x_test, maxlen=max_len)

# Step 3: Build LSTM model
model = Sequential()
model.add(Embedding(max_words, 32, input_length=max_len))
model.add(LSTM(64))
model.add(Dense(1, activation='sigmoid'))

# Step 4: Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Step 5: Train model
print("Training model... Please wait.")
model.fit(x_train, y_train, epochs=2, batch_size=64, validation_data=(x_test, y_test))

# Step 6: Evaluate
loss, accuracy = model.evaluate(x_test, y_test)
print("\n✅ Test Accuracy:", accuracy)










# Sentiment Analysis using LSTM

# Step 1: Import Libraries
import numpy as np
from tensorflow.keras.datasets import imdb
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Step 2: Load Dataset
max_features = 5000  # Number of words to consider as features
maxlen = 200         # Cut texts after this number of words
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=max_features)

# Step 3: Preprocess Data
X_train = pad_sequences(X_train, maxlen=maxlen)
X_test = pad_sequences(X_test, maxlen=maxlen)

# Step 4: Build LSTM Model
model = Sequential()
model.add(Embedding(max_features, 128, input_length=maxlen))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1, activation='sigmoid'))

# Step 5: Compile the Model
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Step 6: Train the Model
print("Training the model...")
history = model.fit(X_train, y_train,
                    batch_size=64,
                    epochs=2,
                    validation_data=(X_test, y_test))

# Step 7: Evaluate the Model
score, acc = model.evaluate(X_test, y_test, batch_size=64)
print("\nTest Score:", score)
print("Test Accuracy:", acc)

# Step 8: Make Predictions
sample_review = "This movie was absolutely fantastic! The story and acting were great."
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(num_words=max_features)
tokenizer.fit_on_texts([sample_review])
seq = tokenizer.texts_to_sequences([sample_review])
padded = pad_sequences(seq, maxlen=maxlen)
pred = model.predict(padded)
sentiment = "Positive 😀" if pred[0][0] > 0.5 else "Negative 😞"

print("\nSample Review:", sample_review)
print("Predicted Sentiment:", sentiment)
