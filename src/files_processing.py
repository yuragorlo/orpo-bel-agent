import os
import pandas as pd
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict
from config import ROOT_DIR, OUTPUT_DIR
from csv import DictWriter

SWAP_PATH = os.path.join(ROOT_DIR, OUTPUT_DIR, 'loop_swap.csv')

class CustomHandler(BaseCallbackHandler):

    def __init__(self, task_index: int, task_name: str) -> None:
        self.task_index = task_index
        self.task_name = task_name

    def save_to_csv(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        save_data = {
            "task_index": self.task_index,
            "task_field": self.task_name,
            "output_text": outputs,
        }
        file_exist_flag = os.path.isfile(SWAP_PATH)
        with open(SWAP_PATH, 'a') as f:
            writer_obj = DictWriter(f, fieldnames=save_data.keys())
            if not file_exist_flag:
                writer_obj.writeheader()
            writer_obj.writerow(save_data)
            f.close()


def add_loop_to_result(path_result: str, path_loop: str = SWAP_PATH) -> None:
    # make result csv if not exist
    if not os.path.isfile(path_result):
        init_df = pd.DataFrame(columns=["fact", "fake", "question", "verifying"])
        init_df.to_csv(path_result)
    # concat result csv with loop csv
    old_result_df = pd.read_csv(path_result, index_col=0)
    loop_df = pd.read_csv(path_loop)
    loop_df = loop_df.pivot_table(columns="task_field", values="output_text", index="task_index", aggfunc='first')
    loop_df.index.name = None
    new_result_df = pd.concat([old_result_df, loop_df], axis=0, ignore_index=True)
    # save result csv
    new_result_df.to_csv(path_result)
    # clean loop csv
    if os.path.isfile(SWAP_PATH):
        os.remove(SWAP_PATH)
