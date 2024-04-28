import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms.openai import OpenAI

from htmlTemplates import css, bot_template, user_template
import base64
import os
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    #embeddings = HuggingFaceInstructEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    #llm = HuggingFaceHub(repo_id="google/mt5-base", model_kwargs={"temperature":0.7, "max_length":512})
    #llm = OllAMA.from_pretrained("achievingHuman/ollama")

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    #st.write(user_template.replace("{{MSG}}", response.content), unsafe_allow_html=True)
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            pass
            # st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

def on_multiple_button_click():
    user_question = " Generate multiple-choice questions based on the given concept and translate korean, only prints korean. "
    handle_userinput(user_question)


def on_short_answer_button_click():
    user_question = "Generate short-answer questions based on the given concept and translate korean, only prints korean."
    handle_userinput(user_question)


def on_true_false_button_click():
    user_question = "Generate true or false questions based on the given concept and translate korean, only prints korean. "
    handle_userinput(user_question)


def on_blanks_button_click():
    user_question = "Generate blanks questions based on the given concept and translate korean, only prints korean."
    handle_userinput(user_question)


def on_multiple_button_click_eng():
    user_question = " Generate multiple-choice questions based on the given concept."
    handle_userinput(user_question)


def on_short_answer_button_click_eng():
    user_question = "Generate short-answer questions based on the given concept."
    handle_userinput(user_question)


def on_true_false_button_click_eng():
    user_question = "Generate true or false questions based on the given concept. "
    handle_userinput(user_question)


def on_blanks_button_click_eng():
    user_question = "Generate blanks questions based on the given concept."
    handle_userinput(user_question)


def main():

    load_dotenv()
    st.set_page_config(page_title="퀴즈 생성기",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("퀴즈 생성기 :books:")
    st.caption("파일 업로드 후 원하시는 문제를 선택하여 주십시오. ")
    #user_question = st.text_input("Ask a question about your documents: ")
    #if user_question:
        #handle_userinput(user_question)



    lang = st.radio(
        "언어 선택",
        ["영어","한국어"],
    )
    type = st.radio(
        "종류 선택",
        ["객관식", "주관식", "참/거짓", "빈칸 맞추기"],
    )

    if lang == '한국어':
        if type == '객관식':
            if st.button('생성'):
                st.session_state.chat_history = None
                on_multiple_button_click()

        if type == '주관식':
            if st.button('생성'):
                st.session_state.chat_history = None
                on_short_answer_button_click()

        if type == '참/거짓':
            if st.button('생성'):
                st.session_state.chat_history = None
                on_true_false_button_click()

        if type == '빈칸 맞추기':
            if st.button('생성'):
                st.session_state.chat_history = None
                on_blanks_button_click()

    if lang == '영어':
        if type == '객관식':
            if st.button('생성'):
                st.session_state.chat_history = None
                on_multiple_button_click_eng()

        if type == '주관식':
            if st.button('생성'):
                st.session_state.chat_history = None
                on_short_answer_button_click_eng()

        if type == '참/거짓':
            if st.button('생성'):
                st.session_state.chat_history = None
                on_true_false_button_click_eng()

        if type == '빈칸 맞추기':
            if st.button('생성'):
                st.session_state.chat_history = None
                on_blanks_button_click_eng()

    with st.sidebar:
        st.subheader("문서 업로드")
        pdf_docs = st.file_uploader(
            "PDF 문서 여러개 업로드 가능.", accept_multiple_files=True, type=["pdf"])
        if st.button("벡터 변환"):
            with st.spinner("변환 중"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

                st.success('저장 완료!', icon="✅")

        st.subheader("이미지 업로드")
        uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "png", "jpeg"])

        if uploaded_file:
            # Display the uploaded image
            with st.expander("Image", expanded=True):
                st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

        # Toggle for showing additional details input
        show_details = st.toggle("부연 설명 입력", value=False)

        if show_details:
            # Text input for additional details about the image, shown only if toggle is True
            additional_details = st.text_area(
                "여기에 부연 설명을 작성해 주십시오.",
                disabled=not show_details
            )

        # Button to trigger the analysis
    analyze_button = st.button("이미지 기반 문제 생성", type="secondary")

    # Check if an image has been uploaded, if the API key is available, and if the button has been pressed
    if uploaded_file and analyze_button:

        with st.spinner("Analysing the image ..."):
            # Encode the image
            base64_image = encode_image(uploaded_file)

            # Optimized prompt for additional clarity and detail
            prompt_text = (
                "create quiz based on image "
            )

            if show_details and additional_details:
                prompt_text += (
                    f"\n\nAdditional Context Provided by the User:\n{additional_details}"
                )

            # Create the payload for the completion request
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ]

            # Make the request to the OpenAI API
            try:
                # Without Stream

                # response = client.chat.completions.create(
                #     model="gpt-4-vision-preview", messages=messages, max_tokens=500, stream=False
                # )
                llm = ChatOpenAI()

                # Stream the response
                full_response = ""
                message_placeholder = st.empty()
                for completion in llm.chat.completions.create(
                        model="gpt-4-vision-preview", messages=messages,
                        max_tokens=1200, stream=True
                ):
                    # Check if there is content to display
                    if completion.choices[0].delta.content is not None:
                        full_response += completion.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                # Final update to placeholder after the stream ends
                message_placeholder.markdown(full_response)

                # Display the response in the app
                # st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        # Warnings for user action required
        if not uploaded_file and analyze_button:
            st.warning("Please upload an image.")



if __name__ == '__main__':
    main()
