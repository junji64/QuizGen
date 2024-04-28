import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# 퀴즈 생성기에 오신 것을 환영합니다! 👋")

st.sidebar.success("문제 생성에 참고할 파일을 선택하여 주십시오.")

st.markdown(
    """
    퀴즈 생성기는 문서, 유튜브 링크, 이미지, 주제 등을 참고하여 이와 관련된 문제를 생성해 주는 서비스 입니다.
    출제자 뿐만 아니라 학습자도 예상 문제를 만들어 학습에 도움을 받을 수 있습니다.
    **👈 업로드할 파일 종류를 선택하여 서비스를 둘러 보십시오.
    ### 저희에게 궁금한 점이 있으시다면
    - 연락하기 [메일](2091126@hansung.ac.kr)
    - 문서 둘러보기 [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### 제안 하기
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)
