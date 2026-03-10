from neo4j import GraphDatabase
from neo4j_graphrag.indexes import create_vector_index
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.indexes import upsert_vectors
from neo4j_graphrag.types import EntityType
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"
INDEX_NAME = "vector-index-name"

# Connect to the Neo4j database
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Create the index
create_vector_index(
    driver,
    INDEX_NAME,
    label="Chunk",
    embedding_property="embedding",
    dimensions=3072,
    similarity_fn="euclidean",
)

# Generate an embedding for some text
text = (
    "The son of Duke Leto Atreides and the Lady Jessica, Paul is the heir of House "
    "Atreides, an aristocratic family that rules the planet Caladan."
)

embedder = OpenAIEmbeddings(model="text-embedding-3-large")

vector = embedder.embed_query(text)

# Upsert the vector
upsert_vectors(
    driver,
    ids=["1234"],
    embedding_property="vectorProperty",
    embeddings=[vector],
    entity_type=EntityType.NODE,
)

driver.close()

