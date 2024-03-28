from __future__ import annotations


from typing import Optional


from google.auth import default
from google.cloud import aiplatform
import pandas as pd
import vertexai
from vertexai.preview.language_models import CodeGenerationModel, TuningEvaluationSpec


credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])


def tune_code_generation_model(
    project_id: str,
    location: str,
    training_data: pd.DataFrame | str,
    train_steps: int = 300,
    evaluation_dataset: Optional[str] = None,
    tensorboard_instance_name: Optional[str] = None,
) -> None:
    """Tune a new model, based on a prompt-response data.

    "training_data" can be either the GCS URI of a file formatted in JSONL format
    (for example: training_data=f'gs://{bucket}/{filename}.jsonl'), or a pandas
    DataFrame. Each training example should be JSONL record with two keys, for
    example:
      {
        "input_text": <input prompt>,
        "output_text": <associated output>
      },
    or the pandas DataFame should contain two columns:
      ['input_text', 'output_text']
    with rows for each training example.

    Args:
      project_id: GCP Project ID, used to initialize vertexai
      location: GCP Region, used to initialize vertexai
      training_data: GCS URI of jsonl file or pandas dataframe of training data
      train_steps: Number of training steps to use when tuning the model.
      evaluation_dataset: GCS URI of jsonl file of evaluation data.
      tensorboard_instance_name: The full name of the existing Vertex AI TensorBoard instance:
        projects/PROJECT_ID/locations/LOCATION_ID/tensorboards/TENSORBOARD_INSTANCE_ID
        Note that this instance must be in the same region as your tuning job.
    """
    vertexai.init(project=project_id, location=location, credentials=credentials)
    eval_spec = TuningEvaluationSpec(evaluation_data=evaluation_dataset)
    eval_spec.tensorboard = aiplatform.Tensorboard(
        tensorboard_name=tensorboard_instance_name
    )
    model = CodeGenerationModel.from_pretrained("code-bison@001")

    model.tune_model(
        training_data=training_data,
        # Optional:
        train_steps=train_steps,
        tuning_job_location="europe-west4",
        tuned_model_location=location,
        tuning_evaluation_spec=eval_spec,
    )

    print(model._job.status)
    return model




















































# import vertexai
# from vertexai.language_models import TextGenerationModel
# import os
# from dotenv import load_dotenv
# load_dotenv()

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'genaiexperiments.json'

# # jsonl_data = "dataset.jsonl"

# vertexai.init(project="182885694936", location="us-central1")
# parameters = {
#     "candidate_count": 1,
#     "max_output_tokens": 200,
#     "temperature": 0.2,
#     "top_p": 0.8,
#     "top_k": 40
# }

# model = TextGenerationModel.from_pretrained("text-bison@001")
# model = model.get_tuned_model("projects/182885694936/locations/us-central1/models/6628525694815043584")

# # Get user query
# user_query = input("Enter the question: ")

# # Construct prompt
# prompt = f"As an expert in converting text into SQL queries, please convert the provided text into an SQL query: {user_query}"

# # Generate response
# response = model.predict(prompt, **parameters)

# # Print response
# print(f"Response from Model: {response.text}")