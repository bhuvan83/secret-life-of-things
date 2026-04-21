import streamlit as st
import subprocess
import os

st.title("🎨 Cartoon Life of Things")

uploaded_file = st.file_uploader("Capture your object", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    with open("temp_obj.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.image("temp_obj.jpg", caption="Normal Object", use_container_width=True)

    if st.button("🪄 Cartoonify & Animate"):
        base_path = os.path.dirname(__file__)
        mouth_path = os.path.join(base_path, "mouth.mp4")
        output = "cartoon_skit.mp4"

        if os.path.exists(mouth_path):
            st.info("Sketching and animating... please wait.")
            
            # The 'Cartoon' Command:
            # edgedetect: creates outlines
            # curves: boosts colors to look like a comic book
            cmd = (
                f"ffmpeg -y -loop 1 -i temp_obj.jpg -i '{mouth_path}' "
                f"-filter_complex '[0:v]edgedetect=low=0.1:high=0.4,format=yuv420p[outline];"
                f"[0:v]curves=preset=lighter_print[color];"
                f"[color][outline]blend=all_mode=multiply[cartoonish];"
                f"[1:v]scale=350:-1[m];[cartoonish][m]overlay=(W-w)/2:(H-h)*0.6:shortest=1' "
                f"-pix_fmt yuv420p -an {output}"
            )
            
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    st.video(output)
                    st.success("Your object is now a cartoon star!")
                else:
                    st.error(f"FFmpeg error: {result.stderr}")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Missing mouth.mp4 file on GitHub!")

