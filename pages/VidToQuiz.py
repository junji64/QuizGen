
import streamlit as st
import cv2  # pip install opencv-python
import base64
import tempfile
from openai import OpenAI
import os

# Retrieve the OpenAI API Key from secrets
#api_key = db.secrets.get(name="OPENAI_API_KEY")
from dotenv import load_dotenv

load_dotenv()
# Initialize the OpenAI client with the API key
client = OpenAI()


@st.cache_data
def video_to_base64_frames(video_buffer):
    """Convert video to a series of base64 encoded frames"""
    base64_frames = []
    # Read the file's bytes
    video_bytes = video_buffer.read()
    # Create a temporary file for the video
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_bytes)
        temp_video_name = temp_video.name
    # Load the video from the temporary file
    video = cv2.VideoCapture(temp_video_name)
    # Read each frame from the video and encode it as base64
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64_frames.append(base64.b64encode(buffer).decode("utf-8"))
    video.release()
    # Clean up the temporary file
    try:
        os.remove(temp_video_name)
    except Exception as e:
        st.error(f"Error removing temporary file: {e}")
    return base64_frames


# Initialize Streamlit app
st.title("비디오 기반 문제 생성")
st.markdown(
    "#### [GPT-4 Vision](https://platform.openai.com/docs/guides/vision) "
)


# Initialize session state variables
if "base64_frames" not in st.session_state:
    st.session_state.base64_frames = None
if "script" not in st.session_state:
    st.session_state.script = ""

# File uploader for video files
uploaded_video = st.file_uploader("Upload a video file", type=["mp4"])
if uploaded_video:
    with st.expander("Watch video", expanded=False):
        st.video(uploaded_video)
# Process video and generate script
if uploaded_video is not None:
    if st.button("Convert Video to Frames"):
        with st.spinner("Converting Video to Frames..."):
            # Convert video to base64 frames and store in session state
            st.session_state.base64_frames = video_to_base64_frames(uploaded_video)
            st.success(f"{len(st.session_state.base64_frames)} frames read.")
        # Display a sample frame from the video
        with st.expander("A Sample Frame", expanded=False):
            st.image(
                base64.b64decode(st.session_state.base64_frames[0].encode("utf-8")),
                caption="Sample Frame",
            )

# Button to generate script
if st.session_state.base64_frames and st.button("Generate Script"):
    PROMPT_MESSAGES = [
        {
            "role": "user",
            "content": [
                "These are frames from a cooking show video. Generate a Quiz based on video.",
                *map(
                    lambda x: {"image": x, "resize": 768},
                    st.session_state.base64_frames[0::10000],
                ),
            ],
        },
    ]
    with st.spinner("Generating script..."):
        full_response = ""
        message_placeholder = st.empty()
        # Call OpenAI API to generate script based on the video frames
        for completion in client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=PROMPT_MESSAGES,
            max_tokens=10,
            stream=True,
        ):
            # Check if there is content to display
            if completion.choices[0].delta.content is not None:
                full_response += completion.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
            st.session_state.script = full_response
        with st.expander("Edit Generated Script:", expanded=False):
            st.text_area("Generated Script", st.session_state.script, height=500)

