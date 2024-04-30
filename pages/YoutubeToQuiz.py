#pip install youtube-transcript-api,chromadb,langchain,streamlit
from langchain.document_loaders import YoutubeLoader
from langchain import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
import streamlit as st


# Display the Page Title
st.title(' Youtube QnA')

load_dotenv()

llm = OpenAI(temperature=0)  # Temp controls the randomness of the text

prompt = st.text_input("Paste the URL")

if prompt:
    loader = YoutubeLoader.from_youtube_url(prompt, add_video_info=False)
    docs = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    split_docs = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    doc_search = Chroma.from_documents(docs,embeddings)
    chain = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=doc_search.as_retriever())

    query = "Create quiz based on "

    if st.button("문제 생성"):
        answer = chain.run(query)
        st.session_state.script = answer
        st.text_area("Generated quiz", st.session_state.script, height=500)