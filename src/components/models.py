from src.components.data_ingestion import DataPreprocess
import os
from vertexai.language_models import TextGenerationModel
from typing import Optional
from google.auth import default
from google.cloud import aiplatform
import pandas as pd
import vertexai
from vertexai.preview.language_models import CodeGenerationModel, TuningEvaluationSpec


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'genaiexperiments.json'

credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])


class QueryGenerator:
    def __init__(self, project_id: str, location: str):
        vertexai.init(project=project_id, location=location, credentials=credentials)
        self.model = CodeGenerationModel.from_pretrained("code-bison@001")
        self.parameters = {
            "candidate_count": 1,
            "max_output_tokens": 200,
            "temperature": 0.2,
            "top_k": 40
        }


    def train_model(
            self,
            training_data: pd.DataFrame | str,
            train_steps: int = 300,
            evaluation_dataset: Optional[str] = None,
            tensorboard_instance_name: Optional[str] = None,
        ) -> None:

        self.model.tune_model(
            training_data=training_data,
            train_steps=train_steps,
            tuning_job_location="us-central1",
            tuned_model_location="us-central1",
        )

        print("Model tuning initiated. Please check the Vertex AI Console for tuning job status.")
        print(self.model.status)
        return self.model



    def predict_query(self, user_query: str) -> str:
        # Construct prompt
        prompt = f"As an expert in converting text into SQL queries, please convert the provided text into an SQL query: {user_query}"
        # Generate response
        response = self.model.predict(prompt, **self.parameters)
        return response.text

