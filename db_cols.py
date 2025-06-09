import chromadb
from chromadb.api import ClientAPI
from glob import glob
from aspose.pdf import Document
from aspose.pdf.text import TextAbsorber

def load_client(path: str) -> ClientAPI:
    return chromadb.PersistentClient(path)

def chunk_text(text: str, chunk_size: int) -> list[str]:
    chunks = []
    for start in range(0, len(text), chunk_size - 20):
        end = start + chunk_size
        if end > len(text):
            end = -1
        chunks.append(text[start:end])
    return chunks

def add_to_collection(col: chromadb.Collection, base_dir: str, chunk_size: int):
    base_dir = base_dir[:-1] if base_dir[-1] == "/" else base_dir
    paths = glob(f"{base_dir}/**/*") + glob(f"{base_dir}/*")
    for path in paths:
        docs = []
        names = []
        ext = path.split(".")[-1]
        name = path.split("/")[-1].split(".")[0]
        text = None
        if ext == "txt":
            with open(path, "r") as file:
                text = file.read()
        if ext == "pdf":
            document = Document(path)
            text_abs = TextAbsorber()
            document.pages.accept(text_abs)
            text = text_abs.text
        if text:
            chunks = chunk_text(text, chunk_size)
            print("processing", path)
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
