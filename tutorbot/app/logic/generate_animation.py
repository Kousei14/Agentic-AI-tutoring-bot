from tutorbot.assets.models.VideoGeneration import VideoGenerationModels

class AnimationGeneratorAgent:
    def __init__(self):
        pass

    def generate(self,
                 prompt: str, 
                 number_of_outputs: int = 1, 
                 aspect_ratio: str = "16:9"):
        
        videos = VideoGenerationModels(
            model = "veo-3.0-generate-001"
        ).generate(
            prompt = prompt,
            image_path = "tutorbot/assets/images/illustration.jpg",
            number_of_videos = number_of_outputs,
            aspect_ratio = aspect_ratio
        )

        return videos