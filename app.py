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
        # This part helps the app find the file in the cloud folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        mouth_path = os.path.join(current_dir, "mouth.mp4")
        
        if not os.path.exists(mouth_path):
            # Try the capital version just in case
            mouth_path = os.path.join(current_dir, "mouth.MP4")

        if os.path.exists(mouth_path):
            st.info("Blending object and mouth... please wait.")
            output = "final_skit.mp4"
            
            # The Command now uses the full path to the mouth file
            cmd = (
                f"ffmpeg -y -loop 1 -i temp_obj.jpg -i '{mouth_path}' "
                f"-filter_complex '[1:v]scale=300:-1[m];[0:v][m]overlay=(W-w)/2:(H-h)*0.7:shortest=1' "
                f"-pix_fmt yuv420p -an {output}"
            )
            
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    st.video(output)
                    st.success("Boom! Your skit is ready.")
                else:
                    st.error(f"FFmpeg error: {result.stderr}")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error(f"Still can't find the mouth file! Looked at: {mouth_path}")
