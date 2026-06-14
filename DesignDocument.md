# **Project Overview**

Moving Helper AI is a multimodal moving assistant that helps users organize and plan a move using voice, images, live video, and text inputs.

The goal is to reduce the effort required to estimate moving needs, identify moving items, and generate personalized moving recommendations.

⸻

# **2. Planned User Stories**

User Story 1

As a user, I want to describe my moving situation using voice so that I do not need to manually type everything. And I think that kind of saving time for me.

Status: Implemented

⸻

User Story 2

As a user, I want to upload photos of my room so that AI can understand what items I need to move.

Status: Implemented

⸻

User Story 3

As a user, I want to use my webcam to show my belongings so that AI can analyze the current environment.

Status: Implemented

⸻

User Story 4

As a user, I want AI to automatically extract moving information such as move date, budget, storage needs, and transportation requirements. So I add some prompts for AI to automatically analyzes those imformation from the voice.

Status: Implemented

⸻

User Story 5

As a user, I want AI to generate a complete moving plan including packing suggestions, storage advice, and moving timelines.

Status: Implemented

⸻

# **3. System Architecture**

Input Layer

* Voice Input
* Image Upload
* Live Video
* Text Input

↓

Processing Layer

* Whisper Speech Recognition
* GPT-4.1 Mini Information Extraction
* Image Analysis

↓

Output Layer

* Moving Recommendations
* Packing Suggestions
* Storage Planning
* Moving Timeline


# **4. Cost Optimization Ideas**

Ideas Considered

* Real-time video analysis
* Continuous video streaming
* Large reasoning models
* Full video processing

Problems

These approaches significantly increase API cost and computation requirements.



# **5. Cost Optimization Techniques Actually Used**

Technique 1

Use GPT-4.1 Mini instead of larger models.

Benefit:
Lower API cost while maintaining acceptable quality.

Technique 2

Use Whisper transcription once and store the result in session state.

Benefit:
Avoid repeated speech-to-text requests.

Technique 3

Process only uploaded images and optional video frames.

Benefit:
Avoid continuous video processing costs.

Technique 4

Reuse extracted moving information.

Benefit:
Reduce duplicate API calls.



# **6. Future Improvements**

* Moving cost estimation
* Truck size recommendation
* Storage size recommendation
* Integration with moving companies
* Real-time video analysis
* Mobile deployment


# **7. Conclusion**

Moving Helper AI demonstrates how multimodal AI can simplify moving-related planning tasks while maintaining low operational cost through selective processing and lightweight model choices.
