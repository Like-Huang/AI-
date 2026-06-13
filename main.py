import streamlit as st

st.title("Moving Helper AI")
st.write("Generate a simple moving plan based on your items, budget, and moving date.")

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

    if not items:
        st.warning("Please enter your items first.")
    else:
        st.markdown(f"""
### Summary
- Move date: {move_date}
- Budget: {budget}
- Storage needed: {need_storage}
- Truck needed: {need_truck}
- Distance: {distance}
- Amount of stuff: {amount}
""")

        st.markdown("### Packing Priority")

        if "mattress" in items.lower() or "bed" in items.lower():
            st.write("1. Prepare mattress bags and move mattresses last.")
        else:
            st.write("1. Pack daily-use items last.")

        if "books" in items.lower():
            st.write("2. Pack books in small boxes because they get heavy quickly.")

        if "clothes" in items.lower():
            st.write("3. Pack clothes in suitcases, vacuum bags, or large boxes.")

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