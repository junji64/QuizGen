# 프로젝트 현황판

|     | 객관식 | 주관식 | 참/거짓 | 빈칸 | 한글 | 비고 |
|-----|-----|------|-----|----|----|----|
| 주제  |  o  |   x  |  x  | x  | x |   |
| 이미지 |  o  |  x   |  x  | x  | x |   |
| pdf  |  o  |  x   |  x  |  x  | o |  |
| 유튜브 | o  | x  | x | x |o| 10분내외  |
| 영상  | x  |  x  | x  |x | x    | |

# 문제 유형 별 최적화 된 프롬프트 (Last Update Date : 2024-05-09)
---
##  필수 고려 사항 
> * 문제와 답이 나와야함.
> * 요금은 고려하지 않음.
---

## 유형 객관식 MCQ(multiple-choice problem)
> *  Create a quiz based on the context of {content}. 
   Include a variety of question types such as multiple choice, true/false, and short answer
   to test the participants understanding and knowledge depth.
   Put the answer at the end of each quiz. After finishing to generate quizes, translate them into Korean for print.
> * 2. Generate multiple-choice questions based on the given concept and translate korean, only prints korean.   
> * 3. 주어진 개념에 맞는 문제를 생성해줘 
> * 시험자 : 신현수
> * 결과 : Not yet
---
## 유형: 참 거짓 True/False
> * 1. Generate true or false questions based on the given concept and translate korean, only prints korean.
> * 2. 주어진 개념에 맞는 문제를 생성해줘 
> * 시험자 : 
> * 결과 :
---
## 유형: 주관식 Short answer
> * __1. Generate short-answer questions based on the given concept and translate korean, only prints korean.__
> * 2. 
> * 시험자 : 신현수
> * 결과 : 오라클에서 CROSS JOIN은 무엇입니까? <br>CROSS JOIN을 사용할 때, 어떤 경우에 유용합니까?<br> RIGHT OUTER JOIN은 무엇을 의미합니까?<br>LEFT OUTER JOIN과 RIGHT OUTER JOIN의 차이는 무엇입니까?
---
## 유형: 빈칸 Blank
> * 1. Generate fill in the blank questions based on the given concept and translate korean, only prints korean.
> * 2. 주어진 개념에 맞는 문제를 생성해줘 
> * 시험자 : 
> * 결과 :
---
## 단기 목적
> * UI 만들기
> * 벤치마킹할 사이트 결정하기
> * 랭체인 아웃풋 parser (json, html 로 만드는 것 (chekcbox
> * 한글 유튜브 영상 (청크 사용)
> * 한글 pdf 로부터 객관식 문제 풀이 ( gpt4사용)
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

