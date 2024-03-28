import csv
import json
from file_converter import get_file_format


class DataPreprocess:

    def load_training_data(self, data_file):
        parsed_data = get_file_format(data_file)
        return parsed_data


# data_file = "data/output.csv"
# # data_file = input("Enter data file path : ")
# data_preprocessor = DataPreprocess()
# parsed_data = data_preprocessor.load_training_data(data_file)
