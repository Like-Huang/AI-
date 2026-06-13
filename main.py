from openai import OpenAI
import streamlit as st
import base64


def image_to_base64(uploaded_file):
    return base64.b64encode(
        uploaded_file.getvalue()
    ).decode("utf-8")


client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


st.title("Moving Helper AI")
st.write("Use camera, voice, and text to generate a moving plan.")


picture = st.camera_input("Take a photo of your items")

if picture:
    st.image(
        picture,
        caption="Captured Image",
        use_container_width=True
    )

    if st.button("Analyze Image"):
        try:
            image_base64 = image_to_base64(picture)

            with st.spinner("Analyzing image..."):
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": (
                                        "Describe this image and identify any moving-related "
                                        "items such as boxes, furniture, mattresses, clothes, "
                                        "bags, or fragile objects. Then give practical packing "
                                        "or moving suggestions."
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

            st.subheader("AI Visual Analysis")
            st.write(response.output_text)

        except Exception as e:
            st.error(f"AI analysis failed: {e}")


audio = st.audio_input("Record your question")

move_date = st.date_input("Move date")
budget = st.text_input("Budget", placeholder="$300")

items = st.text_area(
    "Items",
    placeholder="2 queen mattresses, clothes, books, small cabinets..."
)

need_storage = st.checkbox("I need storage")
need_truck = st.checkbox("I need a truck")

distance = st.selectbox(
    "Moving distance",
    ["Same apartment/community", "Within the same city", "Long distance"]
)

amount = st.selectbox(
    "Amount of stuff",
    ["Small", "Medium", "Large"]
)


if st.button("Generate Plan"):
    st.subheader("Your Moving Plan")

    if not items and not picture and not audio:
        st.warning("Please enter items, take a photo, or record your question first.")
    else:
        st.markdown(f"""
### Summary
- Move date: {move_date}
- Budget: {budget}
- Storage needed: {need_storage}
- Truck needed: {need_truck}
- Distance: {distance}
- Amount of stuff: {amount}
- Photo uploaded: {picture is not None}
- Voice recorded: {audio is not None}
""")

        st.markdown("### Basic Plan")

        if items:
            lower_items = items.lower()

            if "mattress" in lower_items or "bed" in lower_items:
                st.write("1. Prepare mattress bags and move mattresses last.")
            else:
                st.write("1. Pack daily-use items last.")

            if "books" in lower_items:
                st.write("2. Pack books in small boxes because they get heavy quickly.")

            if "clothes" in lower_items:
                st.write("3. Pack clothes in suitcases, vacuum bags, or large boxes.")

        if picture:
            st.write("Photo uploaded. You can use the AI visual analysis above.")

        if audio:
            st.write("The recorded voice will be used as the user's spoken question.")

        st.write("4. Keep important documents, chargers, and toiletries in one essentials bag.")

        st.markdown("### Storage Suggestion")

        if need_storage:
            if amount == "Small":
                st.write("A 5x5 storage unit may be enough.")
            elif amount == "Medium":
                st.write("A 5x10 storage unit is likely a safer choice.")
            else:
                st.write("Consider a 10x10 storage unit, especially if you have mattresses or furniture.")
        else:
            st.write("Storage is not selected. Focus on direct moving and donation.")

        st.markdown("### Transportation Suggestion")

        if need_truck or amount == "Large":
            st.write("A truck or moving van is recommended.")
        elif distance == "Same apartment/community":
            st.write("You may be able to move with carts or multiple small trips.")
        else:
            st.write("A car may work if you reduce large items.")

        st.markdown("""
### Suggested Timeline
- 7 days before: sort items, donate unused things, buy boxes.
- 3 days before: pack most non-essential items.
- 1 day before: prepare essentials bag and confirm storage/truck.
- Moving day: move large items first or last depending on elevator/access.

### Final Checklist
- Return keys
- Clean fridge and sink
- Take photos
- Check storage or truck reservation
- Keep passport, wallet, charger, and medication with you
""")