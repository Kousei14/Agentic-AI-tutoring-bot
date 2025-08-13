import ast

from tutorbot.app.logic.generate_prompt import PromptFormatter
from tutorbot.assets.models.TextGeneration import TextGenerationModels
from tutorbot.utils.TextUtils import strip_code_block_fence

class AnswerGeneratorAgent:
    def __init__(self):

        self.prompt_generator = PromptFormatter()

    def generate(self, 
                 prompt: str):
        
        answer_generator_prompt = self.prompt_generator.read_prompt(
            user_problem = prompt,
            mode = "answer_generator"
            ) 
        response = TextGenerationModels(
            mode = "gemini",
            model = "gemini-2.5-flash"
        ).generate(
            answer_generator_prompt, 
            )
        response = strip_code_block_fence(
            response
            )
        response = ast.literal_eval(
            response
            )

        return response
    
class IllustrationUtilsGeneratorAgent:
    def __init__(self):

        self.prompt_generator = PromptFormatter()

    def generate(self,
                 prompt: str):
        
        illustration_generator_prompt = self.prompt_generator.read_prompt(
            user_problem = prompt,
            mode = "illustration_utils_generator_v2"
            )
        response = TextGenerationModels(
            mode = "openai",
            model = "gpt-4o-mini"
        ).generate(
            illustration_generator_prompt
            )
        response = strip_code_block_fence(
            response
            )
        response = ast.literal_eval(
            response
            )

        return response

