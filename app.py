import streamlit as st
import subprocess
import os

st.title("🎙️ The Secret Life of Things")

uploaded_file = st.file_uploader("Capture your object", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    with open("temp_obj.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.image("temp_obj.jpg", use_container_width=True)
    
    persona = st.selectbox("Who is this?", ["Sassy Receipt", "Anxious Toaster", "Grumpy Dumbbell"])
    rant = st.text_area("What is the rant?", "I saw that credit card statement!")

    if st.button("🎬 Generate Viral Video"):
        # Check for both cases just to be safe!
        mouth_file = "mouth.mp4" if os.path.exists("mouth.mp4") else "mouth.MP4"
        
        if os.path.exists(mouth_file):
            st.info("Blending object and mouth... please wait.")
            output = "final_skit.mp4"
            
            # The 'Bulletproof' Command:
            # -an: Removes problematic audio for now
            # -shortest: Stops the video when the mouth stops
            cmd = (
                f"ffmpeg -y -loop 1 -i temp_obj.jpg -i {mouth_file} "
                f"-filter_complex '[1:v]scale=300:-1[m];[0:v][m]overlay=(W-w)/2:(H-h)*0.7:shortest=1' "
                f"-pix_fmt yuv420p -an {output}"
            )
            
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    st.video(output)
                    st.success("Boom! Your skit is ready.")
                else:
                    st.error(f"FFmpeg failed: {result.stderr}")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Missing 'mouth.mp4'! Please check your GitHub file name.")

