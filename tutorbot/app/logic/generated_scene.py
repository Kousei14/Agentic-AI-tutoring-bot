from manim import *
import os

from tutorbot.app.logic.generate_answer import AnswerGeneratorAgent
from tutorbot.app.logic.generate_answer import IllustrationUtilsGeneratorAgent
from tutorbot.app.logic.generate_illustration import IllustrationGeneratorAgent
from tutorbot.app.logic.generate_audio import AudioGeneratorAgent

from tutorbot.utils.ImageUtils import (bytes_to_image,
                                       bytes_to_array)

prompt = os.getenv("PROBLEM_PROMPT", "Default prompt not provided.")

config.flush_cache = True
class AnimationScene(Scene):
    def construct(self):
        
        print(f"Problem Prompt: {prompt}")
        
        # 1 - Generate text
        # --- narration_lines, math_lines, summary
        answer_generator = AnswerGeneratorAgent()
        answer = answer_generator.generate(
            prompt = prompt
            )
        
        narration_lines = answer["narration_lines"]
        math_lines = answer["math_lines"]
        summary = answer["summary"]
        
        # --- illustration_prompt, illustration_narration
        illustration_utils_generator = IllustrationUtilsGeneratorAgent()
        illustration_utils = illustration_utils_generator.generate(
            prompt = prompt
        )

        illustration_prompt = illustration_utils["generated_prompt"]
        illustration_narration = illustration_utils["illustration_narration"]

        # 2 - Generate audio
        audio_generator = AudioGeneratorAgent()
        path = "tutorbot/assets/{filename}"

        # --- narration_lines_duration
        narration_lines_duration = [
            audio_generator.generate(
                script = line, 
                filename = path.format(filename = f"narration_clips/temp_line_{idx}.mp3"),
                mode = "default_tts") for idx, line in enumerate(narration_lines)
                ]
        
        # --- summary_duration
        summary_duration = audio_generator.generate(
            script = summary[1], 
            filename = path.format(filename = "narration_clips/summary_narration.wav"), 
            mode = "gemini_tts",
            model = "gemini-2.5-flash-preview-tts"
            )
        
        # --- illustration_narration_duration
        illustration_narration_duration = audio_generator.generate(
            script = illustration_narration,
            filename = path.format(filename = "narration_clips/illustration_narration.wav"),
            mode = "gemini_tts",
            model = "gemini-2.5-flash-preview-tts"
            )
        
        # 3 - Generate image
        illustration_generator = IllustrationGeneratorAgent()
        path = "tutorbot/assets/{filename}"

        # --- generated_illustration
        generated_illustration = illustration_generator.generate(
            prompt = f"{illustration_prompt}", 
            number_of_outputs = 1,
            aspect_ratio = "16:9"
        )

        # --- Convert bytes to array and then to Manim ImageMobject
        image_array = bytes_to_array(
            bytes = generated_illustration
            )

        img = ImageMobject(image_array)

        # --- bytes to image
        bytes_to_image(
            bytes = generated_illustration, 
            filename = "illustration.jpg"
            )

        # 4 - Animation
        font_size = 40
        line_spacing = 0.3
        screen_bottom_y = -3.5
        all_lines = VGroup()

        # --- Summary
        summary_path = "tutorbot/assets/narration_clips/summary_narration.wav"

        title = Paragraph(
            summary[0], 
            alignment = "center", 
            line_spacing = 0.8
            )
        title.scale_to_fit_width(12)
        title.move_to([0, 1, 0])  # slightly higher than center
        self.play(Write(title), runtime = 1)
        self.add_sound(summary_path)
        self.wait(summary_duration)
        self.play(Unwrite(title), run_time = 1)

        # --- Illustration
        illustration_path = "tutorbot/assets/narration_clips/illustration_narration.wav"

        self.play(FadeIn(img))
        self.add_sound(illustration_path)
        self.wait(illustration_narration_duration)
        self.play(FadeOut(img))
        
        # --- Problem Solving
        narration_line_path = "tutorbot/assets/narration_clips/temp_line_{idx}.mp3"

        for idx, line in enumerate(math_lines):
            if not line.strip():
                self.add_sound(narration_line_path.format(idx = idx))
                self.wait(narration_lines_duration[idx])
                continue

            new_line = MathTex(line, font_size = font_size)

            if idx == len(math_lines) - 1:
                new_line.set_color(YELLOW)

            if not all_lines:
                
                # If this is the first line, position it at the top of the screen
                new_line.to_edge(UP)
                self.play(Write(new_line), run_time = 1)
            else:

                # Predict new position before scroll
                new_line.next_to(all_lines[-1], DOWN, buff = line_spacing)

                if new_line.get_bottom()[1] < screen_bottom_y:

                    # Store last y-position before scrolling
                    last_y = all_lines[-1].get_y()
                    scroll_amount = all_lines[0].height + line_spacing + 0.4

                    self.play(
                        AnimationGroup(
                            all_lines.animate.shift(UP * scroll_amount),
                            Write(new_line.move_to([0, last_y, 0])),
                            lag_ratio = 0.0,
                            run_time = 1
                        )
                    )
                else:
                    # If it fits, just write it below the last line
                    self.play(Write(new_line), run_time = 1)

            self.add_sound(narration_line_path.format(idx = idx))
            self.wait(narration_lines_duration[idx])
            all_lines.add(new_line)
