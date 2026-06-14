from openai import OpenAI
import streamlit as st
import base64
import io
import json
import cv2
import av
from datetime import date, datetime
from streamlit_mic_recorder import mic_recorder
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def image_to_base64(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode("utf-8")


def frame_to_base64(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    return base64.b64encode(buffer).decode("utf-8")


def transcribe_audio_bytes(audio_bytes, filename="voice.wav"):
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = filename
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript.text

def parse_date_safe(date_text):
    if not date_text:
        return None

    try:
        return datetime.strptime(
            date_text,
            "%Y-%m-%d"
        ).date()
    except:
        return None

def extract_form_info(text):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Extract moving information from the user's text.

Return ONLY valid JSON.

{{
  "move_date": "",
  "budget": "",
  "items": "",
  "need_storage": false,
  "need_truck": false,
  "distance": "",
  "amount": "",
  "language": ""
}}
move_date must be in YYYY-MM-DD format.

If user says:
- July 10
- 7/10
- 7月10号
- tomorrow

convert it to YYYY-MM-DD.
If no move date is mentioned, return "".

distance must be one of:
"Same apartment/community", "Within the same city", "Long distance", or "".

amount must be one of:
"Small", "Medium", "Large", or "".

User text:
{text}
"""
    )
    return json.loads(response.output_text)


class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.latest_frame = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.latest_frame = img
        return av.VideoFrame.from_ndarray(img, format="bgr24")


if "voice_transcripts" not in st.session_state:
    st.session_state.voice_transcripts = []

if "extracted_info" not in st.session_state:
    st.session_state.extracted_info = {}


st.title("Moving Helper AI")
st.write("Use live video, images, voice, and text to generate a moving plan.")


st.markdown("## Live Video Mode / 实时视频模式")

ctx = webrtc_streamer(
    key="live-video",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False}
)

include_live_frame = st.checkbox(
    "Include current live video frame in AI analysis / 将当前实时视频帧加入分析",
    value=False
)


st.markdown("## Image Inputs / 图片输入")

camera_picture = st.camera_input("Take a photo / 拍照")

uploaded_images = st.file_uploader(
    "Upload one or more images / 上传一张或多张图片",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

st.markdown("## Voice Inputs / 语音输入")

if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None

audio = mic_recorder(
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=True,
    key="recorder"
)

st.write("Audio debug:", audio is not None)

if audio and audio.get("bytes"):
    audio_id = audio.get("id", len(audio["bytes"]))

    if audio_id != st.session_state.last_audio_id:
        st.session_state.last_audio_id = audio_id

        try:
            with st.spinner("Transcribing voice..."):
                text = transcribe_audio_bytes(
                    audio["bytes"],
                    f"voice_{len(st.session_state.voice_transcripts)}.wav"
                )

            st.session_state.voice_transcripts.append(text)

            combined_text = "\n".join(st.session_state.voice_transcripts)
            st.session_state.extracted_info = extract_form_info(combined_text)

            st.success("Voice transcribed. / 语音已转写。")
            st.write(text)

        except Exception as e:
            st.error(f"Voice processing failed: {e}")

st.markdown("## Moving Details / 搬家信息")

extracted = st.session_state.extracted_info

move_date = st.date_input("Move date / 搬家日期", value=date.today())

budget_default = 300
if extracted.get("budget", "").replace("$", "").isdigit():
    budget_default = int(extracted["budget"].replace("$", ""))

budget = st.slider("Budget / 预算 ($)", 50, 2000, budget_default, 50)

selected_items = st.multiselect(
    "Common items / 常见物品",
    [
        "Mattress",
        "Bed Frame",
        "Desk",
        "Chair",
        "Books",
        "Clothes",
        "Shoes",
        "TV",
        "Monitor",
        "Kitchen Items",
        "Cabinet",
        "Storage Bins",
        "Bike"
    ]
)

custom_items = st.text_area(
    "Other items / 其他物品",
    value=extracted.get("items", ""),
    placeholder="Gaming PC, guitar, printer..."
)

manual_question = st.text_area(
    "Manual question / 手动问题",
    placeholder="How should I pack these items? Do I need storage?"
)

items = ", ".join(selected_items)
if custom_items:
    items = items + ", " + custom_items if items else custom_items

need_storage = st.checkbox(
    "I need storage / 我需要仓库",
    value=extracted.get("need_storage", False)
)

need_truck = st.checkbox(
    "I need a truck / 我需要卡车",
    value=extracted.get("need_truck", False)
)

distance_options = [
    "Same apartment/community",
    "Within the same city",
    "Long distance"
]

distance_default = extracted.get("distance", "")
distance = st.selectbox(
    "Moving distance / 搬家距离",
    distance_options,
    index=distance_options.index(distance_default)
    if distance_default in distance_options
    else 0
)

amount_options = ["Small", "Medium", "Large"]

estimated_amount = "Small"
if len(selected_items) >= 4 or any(x in selected_items for x in ["Mattress", "Desk", "Cabinet"]):
    estimated_amount = "Medium"
if len(selected_items) >= 8:
    estimated_amount = "Large"

amount_default = extracted.get("amount", "") or estimated_amount

amount = st.selectbox(
    "Amount of stuff / 物品数量",
    amount_options,
    index=amount_options.index(amount_default)
    if amount_default in amount_options
    else 0
)


st.markdown("## Input Check / 输入检测")

visual_count = 0
if camera_picture:
    visual_count += 1
if uploaded_images:
    visual_count += len(uploaded_images)
if include_live_frame and ctx.video_processor and ctx.video_processor.latest_frame is not None:
    visual_count += 1

voice_count = len(st.session_state.voice_transcripts)

if visual_count == 0:
    st.warning("No visual input detected. / 未检测到视觉输入。")
else:
    st.success(f"{visual_count} visual input(s) detected. / 已检测到 {visual_count} 个视觉输入。")

if voice_count == 0:
    st.warning("No voice input detected. / 未检测到语音输入。")
else:
    st.success(f"{voice_count} voice clip(s) detected. / 已检测到 {voice_count} 段语音。")

progress = 0
if visual_count:
    progress += 25
if voice_count:
    progress += 25
if items:
    progress += 25
if budget:
    progress += 25

st.progress(progress)
st.write(f"Input completeness / 输入完整度: {progress}%")


st.markdown("## AI Analysis / AI 分析")

if st.button("Analyze All Inputs / 分析所有输入"):
    try:
        visual_base64_list = []

        if camera_picture:
            visual_base64_list.append(image_to_base64(camera_picture))

        if uploaded_images:
            for img in uploaded_images:
                visual_base64_list.append(image_to_base64(img))

        if include_live_frame and ctx.video_processor:
            frame = ctx.video_processor.latest_frame
            if frame is not None:
                visual_base64_list.append(frame_to_base64(frame))

        combined_voice_text = "\n".join(st.session_state.voice_transcripts)

        user_question = manual_question or combined_voice_text or items

        if not user_question and not visual_base64_list:
            st.warning("Please provide image, video frame, voice, or text first. / 请先提供图片、视频帧、语音或文字。")
        else:
            if not user_question:
                user_question = "Please give moving suggestions based on the visual inputs."

            prompt = (
                "You are a bilingual moving assistant. "
                "Analyze all provided images/video frames and the user's text or voice transcripts. "
                "Answer in both English and Chinese. "
                "Focus on packing, storage, transportation, fragile items, donation, moving order, and cost control. "
                "If no clear moving items are visible, say so honestly. "
                f"Move date: {move_date}. "
                f"Budget: ${budget}. "
                f"Items: {items}. "
                f"Need storage: {need_storage}. "
                f"Need truck: {need_truck}. "
                f"Distance: {distance}. "
                f"Amount: {amount}. "
                f"User question / 用户问题: {user_question}"
            )

            content = [{"type": "input_text", "text": prompt}]

            for image_base64 in visual_base64_list:
                content.append({
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image_base64}"
                })

            with st.spinner("Analyzing all inputs..."):
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=[
                        {
                            "role": "user",
                            "content": content
                        }
                    ]
                )

            ai_text = response.output_text

            st.subheader("User Question / 用户问题")
            st.write(user_question)

            st.subheader("AI Multimodal Analysis / AI 多模态分析")
            st.write(ai_text)

    except Exception as e:
        st.error(f"AI analysis failed: {e}")


if st.button("Generate Plan / 生成搬家计划"):
    st.subheader("Your Moving Plan / 你的搬家计划")

    if not items and visual_count == 0 and voice_count == 0:
        st.warning("Please provide at least one input first. / 请先提供至少一种输入。")
    else:
        st.markdown(f"""
### Summary / 总结
- Move date / 搬家日期: {move_date}
- Budget / 预算: ${budget}
- Storage needed / 是否需要仓库: {need_storage}
- Truck needed / 是否需要卡车: {need_truck}
- Distance / 距离: {distance}
- Amount / 物品数量: {amount}
- Visual inputs / 视觉输入数量: {visual_count}
- Voice clips / 语音数量: {voice_count}
""")

        st.markdown("### Packing Priority / 打包优先级")

        lower_items = items.lower()

        if "mattress" in lower_items or "bed" in lower_items:
            st.write("1. Prepare mattress bags and move mattresses last. / 准备床垫保护袋，床垫最后搬。")
        else:
            st.write("1. Pack daily-use items last. / 日用品最后打包。")

        if "books" in lower_items:
            st.write("2. Pack books in small boxes because they get heavy quickly. / 书很重，请用小箱子打包。")

        if "clothes" in lower_items:
            st.write("3. Pack clothes in suitcases, vacuum bags, or large boxes. / 衣服可以放进行李箱、真空袋或大箱子。")

        st.write("4. Keep passport, wallet, chargers, documents, and medication in one essentials bag. / 护照、钱包、充电器、文件和药品随身携带。")

        st.markdown("### Storage Suggestion / 仓储建议")

        if need_storage:
            if amount == "Small":
                st.write("A 5x5 storage unit may be enough. / 5x5 可能够用。")
            elif amount == "Medium":
                st.write("A 5x10 storage unit is safer. / 5x10 更稳妥。")
            else:
                st.write("Consider a 10x10 storage unit. / 建议考虑 10x10。")
        else:
            st.write("Storage is not selected. Consider direct moving or donation. / 未选择仓储，可考虑直接搬走或捐赠。")

        st.markdown("### Timeline / 时间线")
        st.write("- 7 days before: sort items, donate unused things, buy boxes.")
        st.write("- 3 days before: pack non-essential items.")
        st.write("- 1 day before: prepare essentials bag and confirm truck/storage.")
        st.write("- Moving day: move large items carefully and keep valuables with you.")