import chromadb
from chromadb.api import ClientAPI
from glob import glob
import re

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
                chunks = []
                text = file.read()
                for start in range(0, len(text), chunk_size - 20):
                    end = start + chunk_size
                    if end > len(text):
                        end = -1
                    chunks.append(text[start:end])
            for i in range(len(chunks)):
                docs.append(chunks[i])
                names.append(name + str(i))
        if len(docs) > 0:
            col.add(
                ids=names,
                documents=docs,
            )

def query(col: chromadb.Collection,texts: list[str]) -> list[list[str]] | None:
    result = col.query(
        query_texts=texts, n_results=3
    )
    return result["documents"]

if __name__ == "__main__":
    client = load_client("client")
    col = client.get_or_create_collection("test")
    add_to_collection(col, "test_data/", 2000)
