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

## The Pipeline
The pipeline for document query and answering has the following steps:
- LLM is given the user's query and asked what search phrases could be used to search for context.
  - The answer is given back in an array and stored.
- Database is queried with each of the phrases returned by the first query.
  - The nearest result for each query is stored stored in a list.
- The result of the previous is given in a structured format with the user query back to the LLM ans the LLM is instructed to answer the user query given the found context.