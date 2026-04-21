import streamlit as st
import subprocess
import os

st.title("🎙️ The Secret Life of Things")

# 1. Capture Object
uploaded_file = st.file_uploader("Capture your object", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    with open("temp_obj.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.image("temp_obj.jpg", use_container_width=True)
    
    # 2. Character Setup
    persona = st.selectbox("Who is this?", ["Sassy Receipt", "Anxious Toaster", "Grumpy Dumbbell"])
    rant = st.text_area("What is the rant?", "I saw that credit card statement!")

    if st.button("🎬 Generate Viral Video"):
        if os.path.exists("mouth.MP4"):
            st.info("Blending object and mouth... please wait.")
            output = "final_skit.mp4"
            
            # FFmpeg: Places mouth in the middle-bottom of the object
            cmd = (
                f"ffmpeg -y -loop 1 -i temp_obj.jpg -i mouth.mp4 "
                f"-filter_complex '[1:v]scale=300:-1[m];[0:v][m]overlay=(W-w)/2:(H-h)*0.7:shortest=1' "
                f"-pix_fmt yuv420p -c:a copy {output}"
            )
            
            try:
                subprocess.run(cmd, shell=True, check=True)
                st.video(output)
                st.success("Boom! Your skit is ready. Save it to your phone!")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Missing 'mouth.mp4'! Please upload it to GitHub.")
