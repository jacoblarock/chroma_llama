import chromadb
from chromadb.api import ClientAPI
from glob import glob
import re
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

ef = ONNXMiniLM_L6_V2(preferred_providers=['CUDAExecutionProvider'])

def load_client(path: str) -> ClientAPI:
    return chromadb.PersistentClient(path)

def add_to_collection(col: chromadb.Collection, base_dir: str, chunk_size: int):
    base_dir = base_dir[:-1] if base_dir[-1] == "/" else base_dir
    paths = glob(f"{base_dir}/**/*") + glob(f"{base_dir}/*")
    for path in paths:
        docs = []
        names = []
        ext = path.split(".")[-1]
        name = path.split("/")[-1].split(".")[0]
        if ext in ["txt"]:
            print("processing", path)
            with open(path) as file:
                chunks = re.findall(".{1," + str(chunk_size) + "}", file.read())
            del file
            for i in range(len(chunks)):
                docs.append(chunks[i])
                names.append(name + str(i))
        if len(docs) > 0:
            col.add(
                ids=names,
                documents=docs,
            )

def query(col: chromadb.Collection,texts: list[str]):
    result = col.query(
        query_texts=texts
    )
    return result["documents"]

if __name__ == "__main__":
    client = load_client("client")
    col = client.get_or_create_collection("test", embedding_function=ef)
    add_to_collection(col, "test_data/", 1000)
