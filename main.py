import streamlit as st

st.title("Moving Helper AI")
st.write("Generate a simple moving plan based on your items, budget, and moving date.")

move_date = st.date_input("Move date")
budget = st.text_input("Budget", placeholder="$300")
items = st.text_area("Items", placeholder="2 queen mattresses, clothes, books, small cabinets...")
need_storage = st.checkbox("I need storage")
need_truck = st.checkbox("I need a truck")

if st.button("Generate Plan"):
    st.subheader("Your Moving Plan")

    st.markdown(f"""
### Summary
- Move date: {move_date}
- Budget: {budget}
- Storage needed: {need_storage}
- Truck needed: {need_truck}

### Packing Priority
1. Pack clothes and personal items first.
2. Donate or throw away unused items.
3. Protect fragile items.
4. Move large items like mattresses last.

### Suggested Timeline
- 7 days before: sort and donate items.
- 3 days before: pack most boxes.
- 1 day before: prepare essentials bag.
- Moving day: move large furniture first.

### Final Checklist
- Return keys
- Clean fridge and sink
- Take photos
- Check storage/truck reservation
""")