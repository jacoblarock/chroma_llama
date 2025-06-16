# Chroma_Llama
This repository is my playground for experimenting with document querying for processing with
LLMs. The ChromaDB is used as an embedding database and the ONNXMiniLM_L6_V2 model for embedding.
LLM queries are performed with Ollama or Deepseek.

## Structure
- prompts: directory for prompt storage
  - additional_context: prompt to extract topics and key-phrases to query the database.
  - answer_with_context: a wrapper for both the user query and the queried context with additional
    instructions.
- db_cols: database collection management including document digestion.
- query: user query pipeline.
