from textwrap import dedent

topic_prompt = f"Belarusian language, country, culture, history or famous Belarusians"
language_prompt = "Belarusian language"

bel_prompt = dedent(f"""
    - Use only the Belarus language for the output. No other languages are allowed. 
    - Make it maximum short, but with enough details.
    - Make sure that it about {topic_prompt}.
    - Delete emojis or special characters except allowed by the {language_prompt}.
    - Make sure that it is grammatically correct according {language_prompt} rules.
    - It is extremely important return only {language_prompt} text without translation or explanation, 
    check it again, and remake it if necessary.
""")

self_control_prompt = dedent(f"""
    - Rewrite it to a simple easy words and understandable form according requirement language 
    if it necessary and return it.
""")

self_control_verifying_prompt = dedent(f"""
    - Delite all symbols after end of list (it looks like ']') and return the list.
""")

question_prompt = dedent(f"""
    # QUESTION PROMPT #
    Choose the best question for quiz game from the input text.
    Return only one question following next steps:
    1. Find in  <<input_text>> topics about {topic_prompt}.
    2. Build the question about more interesting fact from this topics.
    3. Rebuild that in question form with symbol "?" in the end if it still necessary.
    4. Check if it match with following points and rewrite if not: {bel_prompt}.
    5. Check if not about source like number of page, or part of table of contents, but based on topics from point 1.
    5. If it looks not like the best question for quiz game from this context, 
    build another question in the point 2 and try again.
    5. Return the question after self-control: {self_control_prompt}
""")

answer_prompt = dedent(f"""
    # TRUE ANSWER PROMPT #
    Make right answer for quiz game about {topic_prompt} using input_text and the question from context.
    Return the answer to the question from context following next steps:
    1. Build the answer for context question.
    2. Make sure that it is really right answer for the input question and it based on the <<input_text>>.
    3. Check if it match the input text and rewrite if not.
    4. Check if it match with following points and rewrite if not: {bel_prompt}.
    5. Return the answer after self-control: {self_control_prompt}
""")

fake_prompt = dedent(f"""
    # FAKE ANSWER PROMPT #
    Dream up wrong answer for quiz game about {topic_prompt} for the input question and correct answer from context.
    Return the wrong answer to the question following next steps:
    1. Dream up the answer from context question.
    2. Make sure that it is really wrong answer for the input question, but looks like good alternative
    for comparing with the correct answer from context.
    3. Check if it match with following points and rewrite if not: {bel_prompt}.
    4. Return the answer after self-control: {self_control_prompt}.
""")


verifying_prompt = dedent(f"""
    # VERIFYING PROMPT #
    Make a list for quiz game about {topic_prompt} that meets the following criteria:
    1. The question is about or related to {topic_prompt} and looks like a question for a quiz game?
    2. The fake answer is fiction but looks like a good alternative to the question?
    3. The question did not contain direct the answer to the question? 
    4. The question, fake answer, and answer from context are in Belarusian language?
    5. If the answer for any of the criteria above is true skip it, otherwise add it number (only number!!!) 
    into the returned list.
    6. Return the list from previous step after self-control: {self_control_verifying_prompt}.
""")
