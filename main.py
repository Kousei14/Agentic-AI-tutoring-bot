from tutorbot.assets.problems.problems import (get_calculus_problem,
                                               get_lin_alg_problem,
                                               get_physics_problem,
                                               get_chemistry_problem, 
                                               get_finance_problems)

import os
import time

def run_test(prompt: str):

    from tutorbot.app.logic.generate_answer import QueryProcessorAgent, AnswerGeneratorAgent, IllustrationUtilsGeneratorAgent

    start_time = time.time()

    query_processor = QueryProcessorAgent()
    processed_query = query_processor.generate(
        prompt = prompt
    )

    print(processed_query)
    print(type(processed_query))

    answer_generator = AnswerGeneratorAgent()
    answer = answer_generator.generate(
        prompt = processed_query
    )

    print(answer)
    print(type(answer))

    illustration_utils_generator = IllustrationUtilsGeneratorAgent()
    illustration_utils = illustration_utils_generator.generate(
        prompt = processed_query
    )

    print(illustration_utils)
    print(type(illustration_utils))

    end_time = time.time()

    print(f"Processing time: {end_time - start_time}")

def run(quality: str = "-pql",
        version: str = "v1.0",
        problem_prompt: str = ""):

    from manim.__main__ import main

    if version == "v2.0":
        scene_file = "generated_scene_v2"
    elif version == "v1.0":
        scene_file = "generated_scene"

    os.environ['PROBLEM_PROMPT'] = problem_prompt

    main([
            quality,
            "--flush_cache",
            f"tutorbot/app/logic/{scene_file}.py",
            "AnimationScene"
        ])

if __name__ == "__main__":

    calc_prompt = get_calculus_problem(index = 12)
    physics_prompt = get_physics_problem(index = -1)
    lin_alg_prompt = get_lin_alg_problem(index = 0)
    chem_prompt = get_chemistry_problem(index = 1)
    finance_prompt = get_finance_problems(index = 0)

    # run(quality = "-pql", version = "v2.0", problem_prompt = chem_prompt)
    run_test(prompt = chem_prompt)