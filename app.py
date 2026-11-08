import streamlit as st
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, ColorClip

st.set_page_config(page_title="Monique Video Animator", layout="centered")

st.title("🎥 Monique Video - Custom Greeting Animator")
st.write("Generate vertical (9:16) animated wishes with zero text cropping.")

# UI Inputs
uploaded_file = st.file_uploader("Upload Logo or Background (e.g., 1000606388.jpg)", type=['jpg', 'png', 'jpeg'])
greeting_text = st.text_area("Greeting Text", "Wishing you a Happy Diwali\nand a Prosperous New Year!")
video_duration = st.slider("Video Duration (seconds)", min_value=10, max_value=60, value=30)
bg_color = st.color_picker("Background Color", "#000000")

# Helper function to convert hex to RGB for MoviePy
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

if st.button("Generate Vertical Video"):
    if uploaded_file is not None:
        with st.spinner("Rendering your video... this might take a minute."):
            # Save uploaded file temporarily
            temp_img_path = "temp_logo.jpg"
            with open(temp_img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                # 1. Create Base Vertical Canvas (1080x1920)
                rgb_bg = hex_to_rgb(bg_color)
                base_clip = ColorClip(size=(1080, 1920), color=rgb_bg).set_duration(video_duration)
                
                # 2. Process Logo
                logo_clip = (ImageClip(temp_img_path)
                             .resize(width=900)  # Leaves a safe margin on the sides
                             .set_position(("center", 400)) # Positioned in the upper half
                             .set_duration(video_duration)
                             .crossfadein(1.0)) # Adds a slight fade-in animation
                
                # 3. Process Text (method='caption' auto-wraps text to prevent cropping)
                txt_clip = (TextClip(greeting_text, fontsize=80, color='white', 
                                     font='Arial-Bold', size=(900, None), method='caption')
                            .set_position(("center", 1200)) # Positioned in the lower half
                            .set_duration(video_duration)
                            .crossfadein(2.0))
                
                # 4. Composite and Export
                final_video = CompositeVideoClip([base_clip, logo_clip, txt_clip])
                output_path = "final_greeting.mp4"
                
                # Write file at 24fps to balance smoothness and render speed
                final_video.write_videofile(output_path, fps=24, codec="libx264", audio=False, logger=None)
                
                st.success("Video generated successfully!")
                st.video(output_path)
                
                # Download Button
                with open(output_path, "rb") as file:
                    st.download_button(label="Download Video", data=file, file_name="Diwali_Wish.mp4", mime="video/mp4")
                    
            except Exception as e:
                st.error(f"An error occurred during rendering: {e}")
    else:
        st.error("Please upload the Monique Video logo file to proceed.")
