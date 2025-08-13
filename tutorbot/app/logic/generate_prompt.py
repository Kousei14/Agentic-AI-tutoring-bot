from typing import Literal

class PromptFormatter:
    def __init__(self):
        pass

    def read_prompt(self,
                    user_problem: str = None, 
                    mode: Literal["answer_generator", "illustration_utils_generator"] = "answer_generator") -> str:
        
        with open(file = f"tutorbot/assets/prompts/{mode}_prompt.txt", 
                  mode = "r", 
                  encoding = "utf-8") as f:
            
            prompt = f.read()

        match mode:
            case ("answer_generator" | 
                  "illustration_utils_generator" | 
                  "illustration_utils_generator_v2"):
                return prompt.format(user_problem = user_problem)
            case _:
                return prompt