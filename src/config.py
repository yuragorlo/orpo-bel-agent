import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = "../input"
OUTPUT_DIR = "../output"
INPUT_FILE = "historyia_minska_2006.pdf"

MAX_RPM = 5
MODEL_NAME = "gpt-3.5-turbo-0125"
# MODEL_NAME = "llama3-70b-8192"
# MODEL_NAME = "llama3-8b-8192"
CHUNK_PDF_SIZE = 1000
THREAD_LIMIT = 12
