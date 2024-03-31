import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template


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
    user_question = "Generate multiple-choice questions based on the given concept and translate korean, only prints korean. "  # 여기에 사용자에게 표시할 질문을 입력하세요
    handle_userinput(user_question)

def on_short_answer_button_click():
    user_question = "Generate short-answer questions based on the given concept and translate korean, only prints korean. "  # 여기에 사용자에게 표시할 질문을 입력하세요
    handle_userinput(user_question)

def on_true_false_button_click():
    user_question = "Generate true or false questions based on the given concept and translate korean, only prints korean. "  # 여기에 사용자에게 표시할 질문을 입력하세요
    handle_userinput(user_question)

def on_blanks_button_click():
    user_question = "Generate blanks questions based on the given concept and translate korean, only prints korean. "  # 여기에 사용자에게 표시할 질문을 입력하세요
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
    st.caption("PDF 업로드 후 원하시는 문제를 선택하여 주십시오. ")
    #user_question = st.text_input("Ask a question about your documents: ")
    #if user_question:
        #handle_userinput(user_question)

    if st.button('객관식 문제 생성'):
        st.session_state.chat_history = None
        on_multiple_button_click()

    if st.button('주관식 문제 생성'):
        st.session_state.chat_history = None
        on_short_answer_button_click()

    if st.button('참/거짓 문제 생성'):
        st.session_state.chat_history = None
        on_true_false_button_click()

    if st.button('빈칸 맞추기 문제 생성'):
        st.session_state.chat_history = None
        on_blanks_button_click()

    with st.sidebar:
        st.subheader("문서 업로드")
        pdf_docs = st.file_uploader(
            "PDF를 업로드 한 후, '처리' 버튼을 눌러 주십시오.", accept_multiple_files=True)
        if st.button("처리"):
            with st.spinner("처리 중"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

                st.success('처리 완료!', icon="✅")


if __name__ == '__main__':
    main()
