"""Video understanding with Gemini 1.5 Pro."""
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.cloud import storage
import json

class VideoProcessor:
    ANALYSIS_PROMPT = """
    Analyze this video and provide:
    1. Scene-by-scene summary (timestamp, description, key objects/people)
    2. Main topics and themes
    3. Content safety assessment (safe/review/unsafe with reason)
    4. Suggested tags (max 20, specific and searchable)
    5. Overall summary (2-3 sentences)
    Return as structured JSON.
    """

    def __init__(self, project_id: str):
        vertexai.init(project=project_id, location="us-central1")
        self.model = GenerativeModel("gemini-1.5-pro-002")
        self.gcs = storage.Client(project=project_id)

    def analyze_video(self, gcs_uri: str) -> dict:
        video_part = Part.from_uri(gcs_uri, mime_type="video/mp4")
        response = self.model.generate_content(
            [video_part, self.ANALYSIS_PROMPT],
            generation_config={"response_mime_type": "application/json",
                               "max_output_tokens": 4096})
        result = json.loads(response.text)
        result["gcs_uri"] = gcs_uri
        result["model"] = "gemini-1.5-pro-002"
        return result
