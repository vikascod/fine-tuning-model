import csv
import json
from src.utils import get_file_format


class DataPreprocess:

    def load_training_data(self, data_file):
        parsed_data = get_file_format(data_file)
        return parsed_data
