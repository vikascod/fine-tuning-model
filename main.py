from src.components.data_ingestion import DataPreprocess
from src.components.models import QueryGenerator


data_processor = DataPreprocess()
data_file = "data/output.csv"
training_data = data_processor.load_training_data(data_file)

generator = QueryGenerator(project_id="182885694936", location="us-central1")
print("Step 2 ...")

print(generator.train_model(training_data=training_data))
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
