import json
import uuid

import streamlit as st


class Main:
    def __init__(self):
        if 'questions' not in st.session_state:
            with open("questions.json") as fr:
                st.session_state.questions = json.load(fr)
        if 'answers' not in st.session_state:
            with open("answers.json") as fr:
                st.session_state.answers = json.load(fr)
        if 'correct_answers' not in st.session_state:
            st.session_state.correct_answers = {}
        if 'letters' not in st.session_state:
            st.session_state.letters = {1: "А", 2: "Б", 3: "В"}

    @staticmethod
    def answer(current, valid, question_index):
        if current == valid:
            st.session_state.correct_answers[question_index] = True
        else:
            st.session_state.correct_answers[question_index] = False

    def get_page(self, topic):
        qa_dict = st.session_state['questions'][topic]
        qs = [int(i) for i in qa_dict.keys()]
        q_min, q_max = min(qs), max(qs)
        st.title(f"{topic} {q_min}-{q_max}")
        for i, qa in qa_dict.items():
            st.markdown(f"Вопрос {i}: {qa['q']}")
            nums = list(range(1, 4))
            [st.button(label=f"{st.session_state.letters[v]}) {qa[str(v)]}", key=uuid.uuid4(), on_click=self.answer,
                       args=(st.session_state['answers'][i], v, i)) for v in nums]
            if st.session_state.correct_answers.get(i):
                st.success("Верно")

    def run(self):
        for topic, qa_dict in st.session_state['questions'].items():
            for i, qa in qa_dict.items():
                print(f"Вопрос {i}:\n{qa['q']}")
                [print(v, qa[str(v)]) for v in range(1, 4)]
                # print(f"Ответ:\n{qa[str(self.answers[i])]}")
                input("...")

    def stream(self):
        selected_page = st.sidebar.selectbox("Select a page", st.session_state['questions'].keys())
        self.get_page(selected_page)


if __name__ == '__main__':
    Main().stream()
