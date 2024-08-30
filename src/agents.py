import os
from crewai import Agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from config import MODEL_NAME
from textwrap import dedent


class DataPreparerAgents():
    def __init__(self):
        if MODEL_NAME.startswith("gpt"):
            self.llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),
                                  model=MODEL_NAME)
        else:
            self.llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"),
                                model=MODEL_NAME)

    def question_maker_agent(self):
        return Agent(
            role="Question Maker",
            goal=dedent(f"""
                Generate a question based on the input text, that can be used as a question for quiz game.
                Using the input text, you need to make a question, that will be the most interesting 
                and powerful for check knowledge about Belarusian language, country, culture or history. 
                If it is not allowed by the current input text, try again."""),
            backstory=dedent("""As a professional expert of Belarus, you are responsible for making questions
                for checking knowledge about Belarus language, country, culture or history."""),
            verbose=True,
            llm=self.llm,
            max_iter=2,
            allow_delegation=False,
        )

    def fact_finder_agent(self):
        return Agent(
            role="Fact Finder",
            goal=dedent(f"""
                Find an answer in the input text for the input question and return it.
                From input text, you need to build an answer for quiz game about Belarus, country, culture or history.
                That should be true answer for input question, real fact from input source text.
                If it is not allowed by the current text and question, try again."""),
            backstory=dedent("""
                As a professional expert of Belarus, you are responsible for making right true answer 
                for the input question based on the input text about Belarus, country, culture or history.
                You never lie or make mistakes like expert, all that you return based on the input source."""),
            verbose=True,
            llm=self.llm,
            max_iter=2,
            allow_delegation=False,
        )

    def dream_up_fact_agent(self):
        return Agent(
            role="Fact Fiction",
            goal=dedent(f"""
                Transform the fact into a fictional statement while prepare this answer for quiz game. 
                Given the question and the true answer, you need to make a new answer, that looks like true, 
                but false in fact. It should be dreamed up fact from the same area as the correct answer, 
                and it should be similar and look like true, when someone compares it with the correct answer."""),
            backstory=dedent("""
                As a professional expert of Belarus and fiction writer, you are responsible for making wrong answers. 
                All that you return should looks like answer for the input question, should be the similar 
                as input true answer, but it all should be lie."""),
            verbose=True,
            llm=self.llm,
            max_iter=2,
            allow_delegation=False,
        )

    def verifying_agent(self):
        return Agent(
            role="Verifier",
            goal=dedent(f"""
                Evaluate the appropriateness of the question and answers and list the criteria from the list bellow 
                for which they are not appropriate. 
                Return an empty list if all criteria are met or the numbers of criteria these data do not meet.
                This should look exactly like the question and answers to quiz users, 
                and if it doesn't, feel free to return why it doesn't using returned list.
                """),
            backstory=dedent("""
                As a professional expert of Belarus, you are responsible for verifying all previous result. 
                You are the last instantiation, that approve all that you received is looks like 
                the good question and answers or not.
                All that you return should looks only like a list of numbers, 
                that listing the numbers of wrong criteria, or an empty list if everything is fine.
                Delete all text with exploration or any other data from response and return only returned list."""),
            verbose=True,
            llm=self.llm,
            max_iter=2,
            allow_delegation=False,
        )


if __name__ == "__main__":
    obj_ex = DataPreparerAgents(MODEL_NAME)
    print(obj_ex.count_agents)
    print(DataPreparerAgents.count_agents)
