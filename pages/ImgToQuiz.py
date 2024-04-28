import streamlit as st
import openai
from dotenv import load_dotenv
from transformers import pipeline
from PIL import Image

load_dotenv()


def generate_text(prompt, max_tokens=100):
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=max_tokens
    )
    return response.choices[0].text.strip()


def main():
    caption = pipeline('image-to-text', model="Salesforce/blip-image-captioning-large")
    st.title("이미지 기반 퀴즈 생성")

    prompt = "Create Quiz based on : "

    # Sidebar for user input
    with st.sidebar:
        st.header("이미지 업로드")
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        with st.spinner("업로드 중"):
            if uploaded_image is not None:
                image = Image.open(uploaded_image)
                st.image(image, caption="Upload Image", use_column_width=True)

                with st.spinner("캡션 생성 중"):
                    if st.button("업로드"):
                        captions = caption(image)
                        prompt += captions[0]['generated_text']

    max_tokens = st.number_input("Max Tokens", min_value=10, max_value=500, value=100)
    generate_button = st.button("퀴즈 생성")
    # Main content area
    if generate_button:
        with st.spinner("Generating..."):
            generated_text = generate_text(prompt, max_tokens)
        st.subheader("Generated Text")
        st.write(generated_text)


if __name__ == "__main__":
    main()
