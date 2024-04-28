import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.write("# 퀴즈 생성기에 오신 것을 환영합니다!👋 현재 ImgToQuiz 실행시 서버 다운됨, 실행 금지.")

st.markdown(
    """
    AI를 사용하여 MCQs, 참/거짓, 빈칸 채우기, FAQs 와 같은 다양한 퀴즈를 생성해 보세요.   
    
    ---
    ### About QuizGen
    > * 둘러보기 [문서](https://github.com/ShinHyun-soo/QuizGen)
    > * 연락하기 [메일](mailto:2091126@hansung.ac.kr)
    """
)
