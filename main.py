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
        st.session_state.setdefault('correct_answers', {})
        st.session_state.setdefault('letters', {1: "А", 2: "Б", 3: "В"})
        st.session_state.setdefault('selected_page', sorted(st.session_state['questions'].keys())[0])

    @staticmethod
    def answer(current, valid, question_index):
        st.session_state.correct_answers[question_index] = current == valid

    @staticmethod
    def select_topic(name):
        st.session_state['selected_page'] = name

    @staticmethod
    def min_max_question_number(qa_dict):
        qs = [int(i) for i in qa_dict.keys()]
        return f"{min(qs)}-{max(qs)}"

    def get_page(self, topic):
        qa_dict = st.session_state['questions'][topic]
        st.markdown(f"## {topic} {self.min_max_question_number(qa_dict)}")
        for i, qa in qa_dict.items():
            st.markdown(f"#### Вопрос {i}: {qa['q']}")
            [st.button(label=f"{st.session_state.letters[v]}) {qa[str(v)]}",
                       key=uuid.uuid4(),
                       on_click=self.answer,
                       args=(st.session_state['answers'][i], v, i)) for v in range(1, 4)]
            if st.session_state.correct_answers.get(i):
                st.success("Верно")

    def run(self):
        for topic in sorted(st.session_state['questions'].keys()):
            st.sidebar.button(label=topic,
                              key=uuid.uuid4(),
                              on_click=self.select_topic,
                              args=(topic,))
        self.get_page(st.session_state['selected_page'])


if __name__ == '__main__':
    Main().run()
