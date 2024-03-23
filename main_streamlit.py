

# Import the required libraries
import openai
import streamlit as st

# Set the GPT-3 API key
# In this case, st.secrets["pass"] is accessing the value of the "pass" secret.

#openai.api_key = st.secrets["pass"]
openai.api_key = ""

article_text = st.text_area("텍스트를 입력하십시오.")

# Create Radio Buttons
output_size = st.radio( label = "문제의 갯수를 설정하십시오.",
                        options= ["1문제", "2문제", "10문제"]
                     )

# First, we'll use an if statement to determine the desired output size
# and set the out_token variable accordingly:

if output_size == "To-The-Point":
 out_token = 50
elif output_size == "Concise":
 out_token = 128
else:
 out_token = 516

# Next, we'll add a check to make sure that the input text is long enough
# to summarize, and display a warning if it is not:

if len(article_text)<100:
    st.warning("문제를 생성하기에 단어가 충분하지 않습니다.")

if st.button("문제 생성", type='primary'):

    # Use GPT-3 to generate a summary of the article
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt="Generate four diverse multiple-choice questions based on the given concept. concept:" + article_text + "Please ensure that the questions cover different aspects of the provided text and vary in complexity. Additionally, provide only one answer corresponding to one of the questions. Thank you!",
        max_tokens=out_token,
        temperature=0.5)

    # Print the generated summary
    res = response["choices"][0]["text"]
    st.success(res)

