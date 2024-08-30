from crewai import Task
from prompts.bel_prompt import question_prompt, answer_prompt, fake_prompt, verifying_prompt
from files_processing import CustomHandler
from textwrap import dedent


class DataPreparerTasks():
    def make_question(self, agent, input_text, task_index):
        return Task(
            description=question_prompt.replace("<<input_text>>", input_text),
            agent=agent,
            expected_output=f"One question about Belarusian language, country, culture or history",
            callback=CustomHandler(task_index=task_index, task_name="question").save_to_csv,
        )

    def find_fact(self, agent, input_text, question, task_index):
        return Task(
            description=answer_prompt.replace("<<input_text>>", input_text),
            agent=agent,
            context=[question],
            expected_output=dedent(f"""Right answer for the input question 
            about Belarusian language, country, culture or history"""),
            callback=CustomHandler(task_index=task_index, task_name="fact").save_to_csv,
        )

    def dream_up_fact(self, agent, question, fact, task_index):
        return Task(
            description=fake_prompt,
            agent=agent,
            context=[question, fact],
            expected_output=dedent(f"""Wrong answer for the input question
            about Belarusian language, country, culture or history"""),
            callback=CustomHandler(task_index=task_index, task_name="fake").save_to_csv,
        )

    def verifying(self, agent, question, fact, fake, task_index):
        return Task(
            description=verifying_prompt,
            agent=agent,
            context=[question, fact, fake],
            expected_output="List of numbers of wrong criterions, or an empty list if there are none",
            callback=CustomHandler(task_index=task_index, task_name="verifying").save_to_csv,
        )
