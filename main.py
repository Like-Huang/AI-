from openai import OpenAI
import streamlit as st
import base64
import io
import json
from datetime import date
from streamlit_mic_recorder import mic_recorder


def image_to_base64(uploaded_file):
    return base64.b64encode(
        uploaded_file.getvalue()
    ).decode("utf-8")


def extract_form_info(transcript_text):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Extract moving information from the user's spoken request.

Return ONLY valid JSON. No markdown.

Fields:
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

Rules:
- distance must be one of: "Same apartment/community", "Within the same city", "Long distance", or "".
- amount must be one of: "Small", "Medium", "Large", or "".
- language must be "Chinese", "English", or "Mixed".
- If information is missing, use empty string or false.

User transcript:
{transcript_text}
"""
    )

    return json.loads(response.output_text)


client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


st.title("Moving Helper AI")
st.write("Use camera, voice, and text to generate a moving plan.")


picture = st.camera_input("Take a photo of your items / 拍摄你的搬家物品")

st.markdown("### Voice Question / 语音问题")

audio = mic_recorder(
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=True,
    key="recorder"
)

voice_text = ""
extracted_info = {}

if audio:
    st.success("Audio received! / 已检测到音频！")

    audio_bytes = audio["bytes"]
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "voice.wav"

    try:
        with st.spinner("Transcribing voice..."):
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        voice_text = transcript.text

        st.subheader("Voice Transcript / 语音转写")
        st.write(voice_text)

        with st.spinner("Extracting moving information from voice..."):
            extracted_info = extract_form_info(voice_text)

        st.subheader("Extracted Moving Information / 自动识别的信息")
        st.json(extracted_info)

    except Exception as e:
        st.error(f"Voice processing failed: {e}")


st.markdown("### Input Check / 输入检测")

if not picture:
    st.warning("No image detected. Please take a photo. / 未检测到图片，请拍照。")
else:
    st.success("Image detected. / 已检测到图片。")

if not voice_text:
    st.warning("No voice question detected. You can record audio or type items manually. / 未检测到语音问题，可以录音或手动输入。")
else:
    st.success("Voice detected and transcribed. / 已检测到并转写语音。")


st.markdown("### Moving Details / 搬家信息")

move_date = st.date_input(
    "Move date / 搬家日期",
    value=date.today()
)

budget = st.text_input(
    "Budget / 预算",
    value=extracted_info.get("budget", "$300") if extracted_info else "$300",
    placeholder="$300"
)

items = st.text_area(
    "Items / 物品",
    value=extracted_info.get("items", "") if extracted_info else "",
    placeholder="2 queen mattresses, clothes, books, small cabinets..."
)

need_storage = st.checkbox(
    "I need storage / 我需要仓库",
    value=extracted_info.get("need_storage", False) if extracted_info else False
)

need_truck = st.checkbox(
    "I need a truck / 我需要卡车",
    value=extracted_info.get("need_truck", False) if extracted_info else False
)

distance_options = [
    "Same apartment/community",
    "Within the same city",
    "Long distance"
]

distance_default = extracted_info.get("distance", "") if extracted_info else ""

distance = st.selectbox(
    "Moving distance / 搬家距离",
    distance_options,
    index=distance_options.index(distance_default)
    if distance_default in distance_options
    else 0
)

amount_options = [
    "Small",
    "Medium",
    "Large"
]

amount_default = extracted_info.get("amount", "") if extracted_info else ""

amount = st.selectbox(
    "Amount of stuff / 物品数量",
    amount_options,
    index=amount_options.index(amount_default)
    if amount_default in amount_options
    else 0
)


if picture:
    st.image(
        picture,
        caption="Captured Image / 拍摄图片",
        use_container_width=True
    )

    if st.button("Analyze Image and Voice / 分析图片和语音"):
        try:
            image_base64 = image_to_base64(picture)

            user_question = voice_text

            if not user_question:
                user_question = items if items else "What moving suggestions can you give based on this image?"

            with st.spinner("Analyzing image and voice..."):
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": (
                                        "You are a bilingual moving assistant. "
                                        "Analyze the image and answer the user's question in both English and Chinese. "
                                        "Focus on packing, storage, transportation, fragile items, donation, "
                                        "moving order, and cost control. "
                                        "If no clear moving items are visible, say so honestly. "
                                        f"User question: {user_question}. "
                                        f"Move date: {move_date}. "
                                        f"Budget: {budget}. "
                                        f"Items typed by user: {items}. "
                                        f"Need storage: {need_storage}. "
                                        f"Need truck: {need_truck}. "
                                        f"Distance: {distance}. "
                                        f"Amount: {amount}."
                                    )
                                },
                                {
                                    "type": "input_image",
                                    "image_url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            ]
                        }
                    ]
                )

            st.subheader("User Question / 用户问题")
            st.write(user_question)

            st.subheader("AI Visual + Voice Analysis / AI 图片与语音分析")
            st.write(response.output_text)

        except Exception as e:
            st.error(f"AI analysis failed: {e}")


if st.button("Generate Plan / 生成搬家计划"):
    st.subheader("Your Moving Plan / 你的搬家计划")

    if not items and not picture and not voice_text:
        st.warning("Please enter items, take a photo, or record your question first. / 请先输入物品、拍照或录音。")
    else:
        st.markdown(f"""
### Summary / 总结
- Move date / 搬家日期: {move_date}
- Budget / 预算: {budget}
- Storage needed / 是否需要仓库: {need_storage}
- Truck needed / 是否需要卡车: {need_truck}
- Distance / 距离: {distance}
- Amount of stuff / 物品数量: {amount}
- Photo uploaded / 是否上传图片: {picture is not None}
- Voice recorded / 是否录音: {bool(voice_text)}
""")

        st.markdown("### Packing Priority / 打包优先级")

        if items:
            lower_items = items.lower()

            if "mattress" in lower_items or "bed" in lower_items:
                st.write("1. Prepare mattress bags and move mattresses last. / 准备床垫保护袋，床垫最后搬。")
            else:
                st.write("1. Pack daily-use items last. / 日用品最后打包。")

            if "books" in lower_items:
                st.write("2. Pack books in small boxes because they get heavy quickly. / 书很重，请用小箱子打包。")

            if "clothes" in lower_items:
                st.write("3. Pack clothes in suitcases, vacuum bags, or large boxes. / 衣服可以放进行李箱、真空袋或大箱子。")

        if picture:
            st.write("Photo uploaded. You can use the AI visual + voice analysis above. / 已上传图片，可参考上方 AI 分析。")

        if voice_text:
            st.write("Voice transcribed. You can use the AI visual + voice analysis above. / 已完成语音转写，可参考上方 AI 分析。")

        st.write("4. Keep important documents, chargers, toiletries, passport, wallet, and medication in one essentials bag. / 把重要文件、充电器、洗漱用品、护照、钱包和药品放在随身必需包里。")

        st.markdown("### Storage Suggestion / 仓储建议")

        if need_storage:
            if amount == "Small":
                st.write("A 5x5 storage unit may be enough. / 5x5 仓库可能够用。")
            elif amount == "Medium":
                st.write("A 5x10 storage unit is likely a safer choice. / 5x10 仓库更稳妥。")
            else:
                st.write("Consider a 10x10 storage unit, especially if you have mattresses or furniture. / 如果有床垫或家具，建议考虑 10x10。")
        else:
            st.write("Storage is not selected. Focus on direct moving and donation. / 未选择仓储，可优先考虑直接搬走或捐赠。")

        st.markdown("### Transportation Suggestion / 运输建议")

        if need_truck or amount == "Large":
            st.write("A truck or moving van is recommended. / 建议租卡车或搬家 van。")
        elif distance == "Same apartment/community":
            st.write("You may be able to move with carts or multiple small trips. / 如果在同一公寓或社区内，可以用推车多次搬运。")
        else:
            st.write("A car may work if you reduce large items. / 如果减少大件物品，普通车可能够用。")

        st.markdown("""
### Suggested Timeline / 建议时间线
- 7 days before: sort items, donate unused things, buy boxes.  
  提前 7 天：整理物品，捐掉不用的东西，购买箱子。
- 3 days before: pack most non-essential items.  
  提前 3 天：打包大部分非必需品。
- 1 day before: prepare essentials bag and confirm storage/truck.  
  提前 1 天：准备随身必需包，确认仓库和车辆。
- Moving day: move large items first or last depending on elevator/access.  
  搬家当天：根据电梯和通道情况决定先搬或后搬大件。

### Final Checklist / 最终清单
- Return keys / 归还钥匙
- Clean fridge and sink / 清空冰箱和水槽
- Take photos / 拍照留证
- Check storage or truck reservation / 确认仓库或卡车预订
- Keep passport, wallet, charger, and medication with you / 护照、钱包、充电器和药品随身携带
""")