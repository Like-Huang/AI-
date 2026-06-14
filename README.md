#Moving Helper AI

A multimodal Streamlit application that helps users generate moving plans using voice, images, live video, and text inputs.

#Project Overview

Moving can be stressful, especially for students who need to organize furniture, storage, transportation, and packing schedules.

Moving Helper AI uses speech recognition, computer vision, and large language models to simplify the moving process. Users can describe their moving situation through voice, upload photos of their belongings, or provide text instructions. The system then generates personalized moving recommendations.

⸻

#Features

Voice Input

* Record moving requirements using a microphone
* Automatic speech-to-text transcription using OpenAI Whisper
* Extract key moving information from natural language

Image Analysis

* Upload room photos
* Take photos directly from the camera
* Analyze visible items and moving conditions

Live Video Support

* Access webcam through Streamlit WebRTC
* Capture a frame from live video for AI analysis

Automatic Information Extraction

The system automatically identifies:

* Move date
* Budget
* Item list
* Storage requirements
* Truck requirements
* Moving distance
* Estimated moving volume

AI Moving Assistant

Generate recommendations for:

* Packing strategy
* Storage planning
* Transportation options
* Cost reduction
* Donation suggestions
* Moving timeline

⸻

#User Story

As a student preparing for a move, I want to describe my moving situation using voice, images, or text so that I can quickly receive a personalized moving plan without manually researching moving logistics.

⸻

#Technologies Used

* Python
* Streamlit
* OpenAI API
* GPT-4.1 Mini
* Whisper
* OpenCV
* Streamlit WebRTC
* Streamlit Mic Recorder

⸻

#Cost Optimization Strategies

To reduce operational cost:

1. GPT-4.1 Mini is used instead of larger models.
2. Audio is transcribed only once and stored in session state.
3. Images are analyzed only when provided by the user.
4. Only a single video frame is processed instead of continuous video analysis.
5. Extracted information is reused to avoid repeated API calls.

⸻

#Future Improvements

* Moving cost estimation
* Storage unit size recommendation
* Truck size recommendation
* Integration with moving company APIs
* Real-time video analysis
* Multi-user collaboration

⸻

#Installation

pip install -r requirements.txt

⸻

#Run

streamlit run main.py

⸻

#Example Workflow

1. Upload room photos or enable webcam.
2. Record moving requirements using voice.
3. Review automatically extracted information.
4. Click “Analyze All Inputs”.
5. Receive AI-generated recommendations.
6. Generate a complete moving plan.
