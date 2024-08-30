import os
from PyPDF2 import PdfReader
from semantic_router.encoders import OpenAIEncoder
from semantic_router.splitters import RollingWindowSplitter
from semantic_router.utils.logger import logger
from functools import reduce
from config import ROOT_DIR, INPUT_DIR, INPUT_FILE


def get_chunks_from_pdf(path: str, limit: int = -1) -> list[str]:
    """
    Read pdf file from path and return a list of text not more than chunk_size
    :param path:
    :param limit:
    :return:
    """

    logger.setLevel("WARNING")
    encoder = OpenAIEncoder(name="text-embedding-ada-002",
                            openai_api_key=os.getenv("OPENAI_API_KEY"))

    splitter = RollingWindowSplitter(
        encoder=encoder,
        dynamic_threshold=True,
        min_split_tokens=200,
        max_split_tokens=800,
        window_size=2,
        plot_splits=False,
        enable_statistics=False
    )

    pdf_reader = PdfReader(path)
    text = reduce(lambda a, b: a + b, [page.extract_text() for page in pdf_reader.pages])
    if limit > 0:
        text = text[:limit]
    chunks = list(splitter([text]))

    return chunks


if __name__ == "__main__":

    ex_chunks = get_chunks_from_pdf(path=os.path.join(ROOT_DIR, INPUT_DIR, INPUT_FILE),
                                    limit=1000)
    print(f'{len(ex_chunks)=}')
    for chunk in ex_chunks[:5]:
        print(chunk.docs)
        print(" .".join(chunk.docs))
        print(type(chunk.docs))
        print('=======')