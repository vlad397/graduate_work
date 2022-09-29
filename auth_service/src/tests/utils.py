import json
from pathlib import Path


def load_index(index_name: str):
    return json.load(open(f"{Path(__file__).parent}/testdata/indexes/index_{index_name}.json"))


def load_data(data_name: str):
    return json.load(open(f"{Path(__file__).parent}/testdata/data/data_{data_name}.json"))
