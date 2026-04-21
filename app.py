import streamlit as st
import subprocess
import os
import requests

st.set_page_config(page_title="Cartoon Life of Things", layout="centered")
st.title("🎨 Cartoon Life of Things")

# 1. Setup paths for the cloud environment
base_path = os.path.dirname(__file__)
mouth_path = os.path.join(base_path, "mouth.mp4")

# 2. Input Section
uploaded_file = st.file_uploader("Capture your object", type=['jpg', 'jpeg', 'png'])
rant = st.text_area("What is the object saying?", "I can't believe you bought another coffee!")

if uploaded_file:
    # Save the uploaded image locally for FFmpeg to process
    with open("temp_obj.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.image("temp_obj.jpg", caption="Original Photo", use_container_width=True)

    if st.button("🪄 Create Viral Skit"):
        # Check if mouth file exists
        if not os.path.exists(mouth_path):
            st.error(f"Cannot find mouth.mp4. Please check your GitHub files!")
            st.write("Files found in folder:", os.listdir(base_path))
        else:
            try:
                # 3. Generate Sassy Voice (ElevenLabs)
                st.info("🎙️ Generating Sassy Voice...")
                api_key = st.secrets["ELEVENLABS_API_KEY"]
                # Using 'Bella' voice ID - you can change this ID for different characters
                voice_url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
                headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
                data = {
                    "text": rant,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
                }
                
                voice_res = requests.post(voice_url, json=data, headers=headers)
                if voice_res.status_code == 200:
                    with open("rant.mp3", "wb") as f:
                        f.write(voice_res.content)
                else:
                    st.error(f"ElevenLabs Error: {voice_res.text}")
                    st.stop()

                # 4. Cartoonify & Sync (FFmpeg)
                st.info("✍️ Sketching and Animating...")
                output_file = "final_cartoon_skit.mp4"
                
                # Manual cartoon filters (eq and unsharp) + overlaying mouth + adding audio
                cmd = (
                    f"ffmpeg -y -loop 1 -i temp_obj.jpg -i '{mouth_path}' -i rant.mp3 "
                    f"-filter_complex '[0:v]edgedetect=low=0.1:high=0.4,format=yuv420p[outline];"
                    f"[0:v]eq=brightness=0.05:saturation=1.6:contrast=1.3,unsharp=5:5:1.5[color];"
                    f"[color][outline]blend=all_mode=multiply[cartoonish];"
                    f"[1:v]scale=400:-1[m];[cartoonish][m]overlay=(W-w)/2:(H-h)*0.65:shortest=1' "
                    f"-pix_fmt yuv420p -map 2:a -c:a aac -b:a 128k -shortest {output_file}"
                )
                
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    st.video(output_file)
                    st.success("🔥 Your Cartoon Skit is ready! Save and share.")
                else:
                    st.error(f"FFmpeg failed: {result.stderr}")

            except Exception as e:
                st.error(f"An error occurred: {e}")


