from manim import *
import os

from tutorbot.app.logic.generate_answer import (AnswerGeneratorAgent, 
                                                IllustrationUtilsGeneratorAgent, 
                                                QueryProcessorAgent)
from tutorbot.app.logic.generate_audio import AudioGeneratorAgent
from tutorbot.app.logic.generate_illustration import IllustrationGeneratorAgent
from tutorbot.app.logic.generate_animation import AnimationGeneratorAgent

from tutorbot.utils.ImageUtils import (bytes_to_image,
                                       bytes_to_array)
from tutorbot.utils.VideoUtils import (bytes_to_video,
                                       video_to_frames)
from tutorbot.utils.AudioUtils import extract_audio_from_video

prompt = os.getenv("PROBLEM_PROMPT", 
                   "Default prompt not provided.")

config.flush_cache = True
class AnimationScene(Scene):
    def construct(self):
        
        print(f"Problem Prompt: {prompt}")
        
        # 0 - Generate Query
        query_processor = QueryProcessorAgent()
        query = query_processor.generate(
            prompt = prompt
        )

        print(query)

        # 1 - Generate text
        # --- narration_lines, math_lines, summary
        answer_generator = AnswerGeneratorAgent()
        answer = answer_generator.generate(
            prompt = query
        )

        summary = answer["summary"]
        math_lines = answer["math_lines"]
        narration_lines = answer["narration_lines"]
        
        # --- illustration_prompt, illustration_narration
        illustration_utils_generator = IllustrationUtilsGeneratorAgent()
        illustration_utils = illustration_utils_generator.generate(
            prompt = query
        )

        illustration_prompt = illustration_utils["illustration_prompt"]
        illustration_narration = illustration_utils["illustration_narration"]
        illustration_animation_prompt = illustration_utils["animation_prompt"]

        print(illustration_animation_prompt)
        
        # 2 - Generate audio
        audio_generator = AudioGeneratorAgent()
        path = "tutorbot/assets/{filename}"

        # --- narration_lines_duration
        narration_mode = "default_tts"

        narration_lines_duration = [
            audio_generator.generate(
                script = line, 
                filename = path.format(filename = f"narration_clips/temp_line_{idx}"),
                mode = narration_mode) for idx, line in enumerate(narration_lines)
                ]
        
        # --- summary_duration
        summary_mode = "default_tts"

        summary_duration = audio_generator.generate(
            script = summary[1], 
            filename = path.format(filename = "narration_clips/summary_narration"),
            mode = summary_mode,
            model = "gemini-2.5-flash-preview-tts"
            )
        
        # --- illustration_narration_duration
        illustration_narration_mode = "default_tts"

        illustration_narration_duration = audio_generator.generate(
            script = illustration_narration,
            filename = path.format(filename = "narration_clips/illustration_narration"),
            mode = illustration_narration_mode,
            model = "gemini-2.5-flash-preview-tts"
            )
        
        # 3 - Generate image
        illustration_generator = IllustrationGeneratorAgent()
        path = "tutorbot/assets/{filename}"

        # --- generated_illustration
        generated_illustration = illustration_generator.generate(
            prompt = illustration_prompt, 
            number_of_outputs = 1,
            aspect_ratio = "16:9"
        )

        # --- bytes to array
        image_array = bytes_to_array(
            bytes = generated_illustration
            )

        # --- array to ImageObject
        img = ImageMobject(image_array)

        # --- bytes to image
        bytes_to_image(
            bytes = generated_illustration, 
            filename = "illustration.jpg"
            )
        
        # 4 - Generate video
        animation_generator = AnimationGeneratorAgent()

        # --- generated_animation
        generated_animation = animation_generator.generate(
            prompt = illustration_animation_prompt,
            number_of_outputs = 1,
            aspect_ratio = "16:9"
        )

        # --- bytes to video
        bytes_to_video(
            bytes = generated_animation[0], 
            filename = "animation.mp4"
        )

        font_size = 40
        line_spacing = 0.3
        screen_bottom_y = -3.5
        all_lines = VGroup()

        # Final Animation
        # --- Summary
        if summary_mode == "default_tts":
            summary_narration_path = "tutorbot/assets/narration_clips/summary_narration.mp3"
        elif summary_mode == "gemini_tts":
            summary_narration_path = "tutorbot/assets/narration_clips/summary_narration.wav"

        title = Paragraph(
            summary[0], 
            alignment = "center", 
            line_spacing = 0.8
            )
        
        title.scale_to_fit_width(12)
        title.move_to([0, 1, 0])

        self.play(Write(title), 
                  runtime = 1)
        self.add_sound(summary_narration_path)
        self.wait(summary_duration)
        self.play(Unwrite(title), 
                  run_time = 1)

        # --- Illustration & Animation
        if illustration_narration_mode == "default_tts":
            illustration_narration_path = "tutorbot/assets/narration_clips/illustration_narration.mp3"
        elif illustration_narration_mode == "gemini_tts":
            illustration_narration_path = "tutorbot/assets/narration_clips/illustration_narration.wav"
        
        animation_path = "tutorbot/assets/videos/animation.mp4"
        animation_audio_path = "tutorbot/assets/narration_clips/animation_audio.mp3"

        # ------ video to audio
        extract_audio_from_video(video_path = animation_path,
                                 audio_output_path = animation_audio_path)

        # ------ video to frames
        frames = video_to_frames(video_path = animation_path,
                                 width = img.pixel_array.shape[1],
                                 height = img.pixel_array.shape[0])

        first_frame = frames[0]
        self.play(FadeIn(first_frame),
                  runtime = 2)
        self.add_sound(illustration_narration_path)
        self.add_sound(animation_audio_path)

        frame_duration = 1 / 60 
        for idx, frame_img in enumerate(frames[1:]):
            if idx < len(frames[1:]) - 1:
                self.add(frame_img)
                self.wait(frame_duration)
                self.remove(frame_img)
            else:
                self.add(frame_img)
                self.wait(frame_duration)
                self.play(FadeOut(frame_img),
                          run_time = 1)

        remaining_time = max(illustration_narration_duration - 
                             ((len(frames) * (1 / 60)) + 3) - 9, 0)
        self.wait(remaining_time)
        self.play(FadeOut(first_frame))


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
