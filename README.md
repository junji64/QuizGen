# 프로젝트 개요
* 문제 출제자의 편의를 돕기 위한 문제 생성기입니다.
* 학습자도 본인의 학업 성취도를 평가하기 위하여 사용할 수 있습니다.
* [직접 해보기](https://hsu-quizgen.streamlit.app)
* ![ezgif-3-57ad839840](https://github.com/ShinHyun-soo/QuizGen/assets/69250097/b9e538bc-a675-4125-a4b0-8d96f60725dc)


# Runs
```python
streamlit run Home.py
```

# Requirements
* langchain==0.1.13
* PyPDF2==3.0.1
* python-dotenv==1.0.0
* streamlit==1.33
* openai==1.23.6
* faiss-cpu==1.7.4
* altair==4
* tiktoken==0.5.2
* langchain-openai == 0.1.4
* transformers == 4.29.2
* pillow == 10.3.0

# 문제 유형 별 최적화 된 프롬프트

## 해야 할 일 
* 문제와 답 출력
* 


## 유형 MCQ(multiple-choice problem)
* 프롬프트 1 Generate multiple-choice questions based on the given concept and translate korean, only prints korean.   
프롬프트 2 주어진 개념에 맞는 문제를 생성해줘 
 
시험자 : 
결과 :
요금 고려하지 말고 품질만 고려하여 실험

유형 MCQ(multiple-choice problem)
프롬프트 1 Generate multiple-choice questions based on the given concept and translate korean, only prints korean. 
프롬프트 2 주어진 개념에 맞는 문제를 생성해줘 

시험자 : 
결과 :
요금 고려하지 말고 품질만 고려하여 실험

유형 True/False
프롬프트 1 "Generate true or false questions based on the given concept and translate korean, only prints korean. "
프롬프트 2 주어진 개념에 맞는 문제를 생성해줘 

시험자 : 
결과 :
요금 고려하지 말고 품질만 고려하여 실험

유형 MCQ(multiple-choice problem)
프롬프트 1 Generate multiple-choice questions based on the given concept and translate korean, only prints korean. 
프롬프트 2 주어진 개념에 맞는 문제를 생성해줘 

시험자 : 
결과 :
요금 고려하지 말고 품질만 고려하여 실험

유형 MCQ(multiple-choice problem)
프롬프트 1 Generate multiple-choice questions based on the given concept and translate korean, only prints korean. 
프롬프트 2 주어진 개념에 맞는 문제를 생성해줘 

시험자 : 
결과 :
요금 고려하지 말고 품질만 고려하여 실험


단기 목적


UI 만들기
벤치마킹할 사이트 결정하기
랭체인 아웃풋 parser (json, html 로 만드는 것 (chekcbox

한글 유튜브 영상 (청크 사용)
한글 pdf 로부터 객관식 문제 풀이 ( gpt4사용)
