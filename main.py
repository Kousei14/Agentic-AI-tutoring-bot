from tutorbot.assets.problems.problems import (get_calculus_problem,
                                               get_lin_alg_problem,
                                               get_physics_problem,
                                               get_chemistry_problem)

import os

def run_test():

    from tutorbot.app.logic.generate_answer import IllustrationUtilsGeneratorAgent
    from tutorbot.app.logic.generate_illustration import IllustrationGeneratorAgent
    from tutorbot.app.logic.generate_animation import AnimationGeneratorAgent

    from tutorbot.utils.ImageUtils import bytes_to_image
    from tutorbot.utils.VideoUtils import bytes_to_video

    # Generate illustration utils
    illustration_utils_generator = IllustrationUtilsGeneratorAgent()
    illustration_utils = illustration_utils_generator.generate(
        prompt = prompt
        )
    
    illustration_prompt = illustration_utils["generated_prompt"]
    illustration_narration = illustration_utils["illustration_narration"]
    animation_prompt = illustration_utils["animation_prompt"]

    print(illustration_utils)

    # Generate illustration
    illustration_generator = IllustrationGeneratorAgent()
    illustration = illustration_generator.generate(
        prompt = illustration_prompt,
        number_of_outputs = 1,
        aspect_ratio = "16:9"
    )

    # Convert bytes to image
    bytes_to_image(
        bytes = illustration, 
        filename = "illustration.jpg"
    )

    # Generate animation
    animation_generator = AnimationGeneratorAgent()
    animation = animation_generator.generate(
        prompt = animation_prompt,
        number_of_outputs = 1,
        aspect_ratio = "16:9"
    )

    # Convert bytes to video
    bytes_to_video(
        bytes = animation[0], 
        filename = "animation.mp4"
    )

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

    prompt = get_calculus_problem(index = 13)

    run(quality = "-pqh",
        version = "v2.0",
        problem_prompt = prompt)
    
    # run_test()