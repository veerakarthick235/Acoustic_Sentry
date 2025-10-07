document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const recordButton = document.getElementById('record-button');
    const statusText = document.getElementById('status-text');
    const timerDisplay = document.getElementById('timer');
    const mainContent = document.getElementById('main-content');
    const recorderCard = document.getElementById('recorder-card');
    const resultsCard = document.getElementById('results-card');
    const loader = document.getElementById('loader');
    const resetButton = document.getElementById('reset-button');

    // MediaRecorder variables
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    let timerInterval;
    let seconds = 0;

    // --- Core Recording Logic ---
    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                uploadAndAnalyze(audioBlob);
                audioChunks = [];
                stream.getTracks().forEach(track => track.stop()); // Release microphone
            };

            mediaRecorder.start();
            isRecording = true;
            updateUIAfterStart();
        } catch (error) {
            console.error('Error accessing microphone:', error);
            statusText.textContent = 'Microphone access denied. Please allow access.';
        }
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            isRecording = false;
            updateUIAfterStop();
        }
    }
    
    // --- API Communication ---
    async function uploadAndAnalyze(audioBlob) {
        showLoader();

        const formData = new FormData();
        formData.append('audio_data', audioBlob, 'cough.wav');

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.statusText}`);
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            console.error('Error uploading file:', error);
            statusText.textContent = 'Analysis failed. Please try again.';
            resetUI();
        } finally {
            hideLoader();
        }
    }

    // --- UI Update Functions ---
    function updateUIAfterStart() {
        recordButton.classList.add('recording');
        statusText.textContent = 'Recording...';
        startTimer();
    }

    function updateUIAfterStop() {
        recordButton.classList.remove('recording');
        statusText.textContent = 'Processing...';
        stopTimer();
    }

    function showLoader() {
        recorderCard.style.display = 'none';
        loader.style.display = 'block';
    }

    function hideLoader() {
        loader.style.display = 'none';
    }

    function displayResults(data) {
        document.getElementById('risk-level').textContent = data.risk_level;
        document.getElementById('risk-level').className = data.risk_level.toLowerCase().replace(' ', '-');
        document.getElementById('confidence-score').textContent = data.confidence;
        document.getElementById('feedback-text').textContent = data.feedback;
        document.getElementById('spectrogram-img').src = data.spectrogram_url;
        
        resultsCard.style.display = 'block';
    }
    
    function resetUI() {
        resultsCard.style.display = 'none';
        recorderCard.style.display = 'block';
        statusText.textContent = 'Ready to record';
        timerDisplay.textContent = '00:00';
        seconds = 0;
    }

    // --- Timer Functions ---
    function startTimer() {
        seconds = 0;
        timerDisplay.textContent = '00:00';
        timerInterval = setInterval(() => {
            seconds++;
            const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
            const secs = (seconds % 60).toString().padStart(2, '0');
            timerDisplay.textContent = `${mins}:${secs}`;
        }, 1000);
    }

    function stopTimer() {
        clearInterval(timerInterval);
    }
    
    // --- Event Listeners ---
    recordButton.addEventListener('click', () => {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    });

    resetButton.addEventListener('click', resetUI);
});