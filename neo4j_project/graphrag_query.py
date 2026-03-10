from neo4j import GraphDatabase
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.retrievers import VectorRetriever
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"
INDEX_NAME = "vector-index-name"

# Connect to the Neo4j database
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Create an Embedder object
embedder = OpenAIEmbeddings(model="text-embedding-3-large")

# Initialize the retriever
retriever = VectorRetriever(driver, INDEX_NAME, embedder)

# Instantiate the LLM
llm = OpenAILLM(model_name="gpt-4o-mini", model_params={"temperature": 0})

# Instantiate the RAG pipeline
rag = GraphRAG(retriever=retriever, llm=llm)

# Query the graph
query_text = "Who is Paul Atreides?"
response = rag.search(query_text=query_text, retriever_config={"top_k": 5})
print(response.answer)
driver.close()