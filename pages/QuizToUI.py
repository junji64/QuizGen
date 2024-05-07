from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
import streamlit as st
from typing import List
from langchain.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()

class QuizTrueFalse(BaseModel):
    quiz_text: str = Field(description="The quiz text")
    questions: List[str] = Field(description="The quiz questions")
    answers: List[str] = Field(description="The quiz answers for each questions as True or False only.")

class QuizMultipleChoice(BaseModel):
    quiz_text: str = Field(description="The quiz text")
    questions: List[str] = Field(description="The quiz questions")
    alternatives: List[List[str]] = Field(description="The Quiz alternatives for each question as a list of lists.")
    answers: List[str] = Field(description="The quiz answers")

class QuizOpenEnded(BaseModel):
    questions: List[str] = Field(description="The quiz questions")
    answers: List[str] = Field(description="The quiz answers")



def create_the_quiz_prompt_template():
    """Create the prompt template for the quiz app."""

    template = """
You are an expert quiz maker for technical fields. Let's think step by step and
create a quiz with {num_questions} {quiz_type} questions about the following concept/content: {quiz_context}.

The format of the quiz could be one of the following:
- Multiple-choice: 
- Questions:
    <Question1>: <a. Answer 1>, <b. Answer 2>, <c. Answer 3>, <d. Answer 4>
    <Question2>: <a. Answer 1>, <b. Answer 2>, <c. Answer 3>, <d. Answer 4>
    ....
- Answers:
    <Answer1>: <a|b|c|d>
    <Answer2>: <a|b|c|d>
    ....
    Example:
    - Questions:
    - 1. What is the time complexity of a binary search tree?
        a. O(n)
        b. O(log n)
        c. O(n^2)
        d. O(1)
    - Answers: 
        1. b
- True-false:
    - Questions:
        <Question1>: <True|False>
        <Question2>: <True|False>
        .....
    - Answers:
        <Answer1>: <True|False>
        <Answer2>: <True|False>
        .....
    Example:
    - Questions:
        - 1. A binary search tree is a data structure that is used to store data?
        - 2. Binary search trees are implemented using linked lists?
    - Answers:
        - 1. True
        - 2. False
- Open-ended:
- Questions:
    <Question1>: 
    <Question2>:
- Answers:    
    <Answer1>:
    <Answer2>:
Example:
    Questions:
    - 1. What is a binary search tree?
    - 2. How are binary search trees implemented?

    - Answers: 
        1. A binary search tree is a data structure that is used to store data in a sorted manner.
        2. Binary search trees are implemented using linked lists.
"""
    prompt = ChatPromptTemplate.from_template(template)
    prompt.format(num_questions=3, quiz_type="multiple-choice", quiz_context="Data Structures in Python Programming")

    return prompt


def create_quiz_chain(prompt_template, llm, pydantic_object_schema):
    """Creates the chain for the quiz app."""
    return prompt_template | llm.with_structured_output(pydantic_object_schema)


def split_questions_answers(quiz_response):
    """Function that splits the questions and answers from the quiz response."""
    questions = quiz_response.questions # 질문 목록
    answers = quiz_response.answers
    return questions, answers


def main():


    st.title("Quiz App")
    st.write("This app generates a quiz based on a given context.")

    prompt_template = create_the_quiz_prompt_template()

    llm = ChatOpenAI(temperature=0.0)
    chain = create_quiz_chain(prompt_template, llm)
    context = st.text_area("Enter the concept/context for the quiz")
    num_questions = st.number_input("Enter the number of questions", min_value=1, max_value=10, value=3)
    quiz_type = st.selectbox("Select the quiz type", ["multiple-choice", "true-false", "open-ended"])
    if st.button("Generate Quiz"):
        quiz_response = chain.invoke({"quiz_type": quiz_type, "num_questions": num_questions, "quiz_context": context})
        st.write("Quiz Generated!")
        questions, answers = split_questions_answers(quiz_response)
        st.session_state.answers = answers
        st.session_state.questions = questions
        st.session_state.user_answers = [None]*len(questions)

        if quiz_type == "multiple-choice":
            st.write("Multiple Choice Questions")
            for i, question in enumerate(questions):
                st.markdown(question)
                for ia, answer in enumerate(st.session_state.answers):
                    checkbox_key = f"answer_{i}_{ia}"
                    st.session_state.user_answers[ia] = st.checkbox(f'{answer}', key=checkbox_key)

        elif quiz_type == "true-false":
            st.write("True/Fase Questions")
            for i, question in enumerate(questions):
                st.markdown(question)
                checkbox_key_true = f"answer_{i}-false"
                checkbox_key_false = f"answer_{i}-ture"
                if st.checkbox("Ture",key=checkbox_key_true):
                    st.session_state.user_answers[i] = True
                elif st.checkbox("False", key=checkbox_key_false):
                    st.session_state.user_answers[i] = False

        elif quiz_type == "open-ended":
            st.write("Open Ended Questions")
            for i, question in enumerate(questions):
                st.markdown(question)
                text_key = f"answer_{i}"
                st.session_state.user_answers[i] = st.text_input("Enter your answer", key=text_key)

        st.session_state["submitted_answers"] = st.form_submit_button("Submit Answers")
        if submitted:
            if None in st.session_state.user_answers:
                st.warning("Please answer all the questions before submitting.")
            else:
                score = sum([user_answer == answer for user_answer, answer in zip(st.session_state.user_answers, st.session_state.answers)])
                st.write(f'Your score is {score}/{len(questions)}')

if __name__ == "__main__":
    main()