import streamlit as st
import openai
from dotenv import load_dotenv

load_dotenv()
def generate_text(prompt, max_tokens=100):
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=max_tokens
    )
    return response.choices[0].text.strip()


def main():
    st.title("주제 기반 퀴즈 생성")

    # Sidebar for user input
    with st.sidebar:
        st.header("주제 입력")
        prompt = "Create quiz based on :"
        prompt += st.text_area("Enter your prompt here:")
        max_tokens = st.number_input("Max Tokens", min_value=10, max_value=500, value=100)
        generate_button = st.button("퀴즈 생성")

    # Main content area
    if generate_button:
        with st.spinner("Generating..."):
            generated_text = generate_text(prompt, max_tokens)
        st.subheader("Generated Text")
        st.session_state.script = generated_text
        st.text_area("Generated quiz", st.session_state.script, height=500)


if __name__ == "__main__":
    main()
