import streamlit as st

st.title("🎙️ The Secret Life of Things")

# Trigger iPhone camera
uploaded_file = st.file_uploader("Capture your object", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    st.image(uploaded_file, caption="Object Detected!", use_container_width=True)
    
    persona = st.selectbox("Who is this?", ["Sassy Receipt", "Anxious Toaster", "Grumpy Dumbbell"])
    rant = st.text_area(f"What is the {persona} saying?", "I can't believe you bought that!")

    if st.button("Generate Video"):
        st.info("The FFmpeg engine is warming up...")
