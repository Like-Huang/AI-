# **Moving Helper AI 搬家助手**

A multimodal Streamlit application that helps users generate moving plans using voice, images, live video, and text inputs.

一个基于 Streamlit 的多模态 AI 搬家助手，用户可以通过语音、图片、实时视频和文本输入生成个性化搬家方案。


# **Project Overview 项目简介**


Moving can be stressful, especially for students who need to organize furniture, storage, transportation, and packing schedules.

Moving Helper AI uses speech recognition, computer vision, and large language models to simplify the moving process. Users can describe their moving situation through voice, upload photos of their belongings, or provide text instructions. The system then generates personalized moving recommendations.


搬家往往是一件繁琐而耗时的事情，尤其对于学生群体来说，需要同时考虑家具搬运、仓储、运输以及打包安排等问题。

Moving Helper AI 结合语音识别、计算机视觉和大语言模型技术，帮助用户更轻松地规划搬家流程。用户可以通过语音描述需求、上传物品照片或输入文字信息，系统将自动分析并生成个性化搬家建议。


# **Dependencies 项目依赖**

streamlit
openai
opencv-python
numpy
av
streamlit-mic-recorder
streamlit-webrtc



# **Features 功能介绍**

## Voice Input 语音输入

* Record moving requirements using a microphone
* Automatic speech-to-text transcription using OpenAI Whisper
* Extract key moving information from natural language
* 使用麦克风录制搬家需求
* 使用 OpenAI Whisper 自动进行语音转文字
* 从自然语言中提取关键搬家信息



## Image Analysis 图像分析

* Upload room photos
* Take photos directly from the camera
* Analyze visible items and moving conditions
* 上传房间照片
* 使用摄像头直接拍照
* 分析可见物品和搬家环境


## Live Video Support 实时视频支持

* Access webcam through Streamlit WebRTC
* Capture a frame from live video for AI analysis
* 通过 Streamlit WebRTC 调用摄像头
* 从实时视频中截取画面进行 AI 分析


## Automatic Information Extraction 自动信息提取

The system automatically identifies:

系统能够自动识别：

* Move date / 搬家日期
* Budget / 预算
* Item list / 物品清单
* Storage requirements / 仓储需求
* Truck requirements / 搬运车辆需求
* Moving distance / 搬家距离
* Estimated moving volume / 预计物品数量



## AI Moving Assistant AI 搬家助手

Generate recommendations for:

生成以下方面的建议：

* Packing strategy / 打包策略
* Storage planning / 仓储规划
* Transportation options / 运输方案
* Cost reduction / 成本控制
* Donation suggestions / 捐赠建议
* Moving timeline / 搬家时间安排



# **User Story 用户故事**



As a student preparing for a move, I want to describe my moving situation using voice, images, or text so that I can quickly receive a personalized moving plan without manually researching moving logistics.


作为一名准备搬家的学生，我希望能够通过语音、图片或文字描述自己的搬家需求，从而快速获得个性化搬家方案，而无需自己查找大量搬家相关信息。



# **Technologies Used 使用技术**

* Python
* Streamlit
* OpenAI API
* GPT-4.1 Mini
* Whisper
* OpenCV
* Streamlit WebRTC
* Streamlit Mic Recorder


# **Cost Optimization Strategies 成本优化策略**

To reduce operational cost:

为了降低运营成本，本项目采用了以下策略：

1. GPT-4.1 Mini is used instead of larger models.
    使用 GPT-4.1 Mini 替代更大的模型。
2. Audio is transcribed only once and stored in session state.
    语音仅转写一次，并存储在 Session State 中。
3. Images are analyzed only when provided by the user.
    仅分析用户主动提供的图片。
4. Only a single video frame is processed instead of continuous video analysis.
    仅分析单个视频帧，而非持续处理视频流。
5. Extracted information is reused to avoid repeated API calls.
    重复利用已经提取的信息，避免重复调用 API。



# **Future Improvements 未来改进方向**

* Moving cost estimation / 搬家费用估算
* Storage unit size recommendation / 仓储空间推荐
* Truck size recommendation / 搬家车辆推荐
* Integration with moving company APIs / 对接搬家公司 API
* Real-time video analysis / 实时视频分析
* Multi-user collaboration / 多用户协作功能



# **Installation 安装方式**

pip install -r requirements.txt

⸻

# **Run 运行项目**

streamlit run main.py


# **Example Workflow 使用流程**

1. Upload room photos or enable webcam.
    上传房间照片或开启摄像头。
2. Record moving requirements using voice.
    使用语音描述搬家需求。
3. Review automatically extracted information.
    查看自动提取的信息。
4. Click “Analyze All Inputs”.
    点击“Analyze All Inputs”。
5. Receive AI-generated recommendations.
    获取 AI 生成的搬家建议。
6. Generate a complete moving plan.
    生成完整搬家方案。
