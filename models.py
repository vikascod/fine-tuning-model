from data_ingestion import DataPreprocess
import os
from vertexai.language_models import TextGenerationModel
from typing import Optional
from google.auth import default
from google.cloud import aiplatform
import pandas as pd
import vertexai
from vertexai.preview.language_models import CodeGenerationModel, TuningEvaluationSpec
from __future__ import annotations


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'genaiexperiments.json'


class QueryGenerator:
    def __init__(self, project_id: str, location: str, credentials_path: Optional[str] = None):
        self.project_id = project_id
        self.location = location
        vertexai.init(project=project_id, location=location)
        self.model = TextGenerationModel.from_pretrained("text-bison@001")
        self.parameters = {
            "candidate_count": 1,
            "max_output_tokens": 200,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }

    def train_model(self, jsonl_data: str):
        try:
            fine_tuning_task = self.model.tune_model(
                training_data=jsonl_data,
                train_steps=50,
                learning_rate_multiplier=1e-4,
                model_display_name="text-bison-fine-tuned",
                tuning_job_location="us-central1",
                tuned_model_location="us-central1",
            )
            fine_tuning_task.wait()
            print("Running ...")
            # Get the fine-tuned model
            self.model = self.model.from_pretrained(fine_tuning_task.model_id)
        except Exception as e:
            print(f"Error during model training: {e}")


    def predict_query(self, user_query: str) -> str:
        # Construct prompt
        prompt = f"As an expert in converting text into SQL queries, please convert the provided text into an SQL query: {user_query}"
        # Generate response
        response = self.model.predict(prompt, **self.parameters)
        return response.text


# Get user input for data file path
load_data = input("Enter data file path : ")
print("Step 1 ...")
# Initialize QueryGenerator
generator = QueryGenerator(project_id="182885694936", location="us-central1")
print("Step 2 ...")
print(generator.train_model(jsonl_data=load_data))
print("Step 3 ...")
# Get user input for query
user_query = input("Enter the question: ")
print("Step 4 ...")
# Generate response
response = generator.predict_query(user_query)
print("Step 5 ...")
# Print response
print(f"Response from Model: {response}")
print("Step 6 ...")
