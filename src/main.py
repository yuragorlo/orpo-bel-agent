import time
import os
import datetime
from crewai import Crew, Process

from agents import DataPreparerAgents
from config import MAX_RPM, MODEL_NAME
from dotenv import load_dotenv
from tasks import DataPreparerTasks
from pdf_processing import get_chunks_from_pdf
from files_processing import add_loop_to_result
from config import ROOT_DIR, INPUT_DIR, OUTPUT_DIR, THREAD_LIMIT, INPUT_FILE

load_dotenv()
total_time = 0

output_filename = os.path.join(ROOT_DIR, OUTPUT_DIR, INPUT_FILE[:-4]+'.csv')

agents = DataPreparerAgents()
count_agents = len([func for func in dir(agents) if ((not func.startswith("__")) and (func != 'llm'))])
chunks = get_chunks_from_pdf(path=os.path.join(ROOT_DIR, INPUT_DIR, INPUT_FILE), limit=10000)
chunks_per_loop = THREAD_LIMIT//count_agents
count_loops = len(chunks)//chunks_per_loop + 1

print(f"Total chunks: {len(chunks)} \n Chunks per loop: {chunks_per_loop} \n Total loops: {count_loops}")
for loop in range(count_loops):
    print(f"LOOP N: {str(loop)}".center(35, '='))
    loop_chunks = chunks[loop*chunks_per_loop:(loop+1)*chunks_per_loop]
    # 0. Create agents
    agents = DataPreparerAgents()
    question_agent = agents.question_maker_agent()
    find_agent = agents.fact_finder_agent()
    dream_up_agent = agents.dream_up_fact_agent()
    verifying_agent = agents.verifying_agent()

    # 0.5 Init task lists
    tasks = DataPreparerTasks()
    question_tasks = []
    fact_tasks = []
    fake_tasks = []
    verifying_tasks = []

    for ind, chunk in enumerate(loop_chunks):
        input_text = " .".join(chunk.docs)
        print(f"Current input text length is: {len(input_text)} characters")

        # 2. Create tasks
        make_question_task = tasks.make_question(
            agent=question_agent,
            input_text=input_text,
            task_index=ind
        )
        find_fact_task = tasks.find_fact(
            agent=find_agent,
            input_text=input_text,
            question=make_question_task,
            task_index=ind
        )
        dream_up_fact_task = tasks.dream_up_fact(
            agent=dream_up_agent,
            question=make_question_task,
            fact=find_fact_task,
            task_index=ind
        )
        make_verifying_task = tasks.verifying(
            agent=verifying_agent,
            question=make_question_task,
            fact=find_fact_task,
            fake=dream_up_fact_task,
            task_index=ind
        )

        question_tasks.append(make_question_task)
        fact_tasks.append(find_fact_task)
        fake_tasks.append(dream_up_fact_task)
        verifying_tasks.append(make_verifying_task)

    # 3. Setup Crew
    crew = Crew(
        agents=[find_agent, question_agent, dream_up_agent, verifying_agent],
        tasks=[*question_tasks, *fact_tasks, *fake_tasks, *verifying_tasks],
        verbose=0,
        max_rpm=None if MODEL_NAME.startswith("gpt") else MAX_RPM,
        process=Process.sequential,
    )

    # Kick off the crew
    start_time = time.time()
    _ = crew.kickoff()

    # 4. Save output to csv
    add_loop_to_result(path_result=output_filename)
    end_time = time.time()
    loop_time = end_time - start_time
    total_time += loop_time
    print(f"Loop time: {str(datetime.timedelta(seconds=loop_time))} sec.".center(35))
print(f"Total time: {str(datetime.timedelta(seconds=total_time))} sec.".center(35))

