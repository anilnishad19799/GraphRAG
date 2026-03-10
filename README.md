# 🧠 GraphRAG — Three Implementation Approaches

GraphRAG (Graph Retrieval-Augmented Generation) is an advanced RAG technique that combines vector search with knowledge graph reasoning to enable more accurate, multi-hop, and relationship-aware contextual retrieval from documents.

This repository contains **three different approaches** to building a GraphRAG pipeline, ranging from a quick CLI-based setup to a full web API with Docker, and a Neo4j-powered knowledge graph variant.

---

## 📁 Project Structure

```
GraphRAG/
├── Terminal/          # Method 1: Official Microsoft GraphRAG (CLI)
├── project/           # Method 2: FastAPI + Docker Compose web app
└── neo4j_project/     # Method 3: Neo4j-based GraphRAG pipeline
```

---

## 🔧 Prerequisites

- Python 3.12+
- OpenAI API Key (`gpt-4o-mini` + `text-embedding-3-small`)
- Docker & Docker Compose (for Method 2)
- Neo4j instance (for Method 3)

---

## Method 1 — Official Microsoft GraphRAG (CLI / Terminal)

The simplest way to get started. Uses the official [Microsoft GraphRAG](https://microsoft.github.io/graphrag/) library via the command line.

### Folder: `Terminal/`

```
Terminal/
├── main.py              # Entry point
├── settings.yaml        # GraphRAG configuration
├── .env                 # API key
├── pyproject.toml       # Project metadata
├── input/               # Place your .txt documents here
├── output/              # Generated graph artifacts (parquet, LanceDB)
├── cache/               # LLM call cache
├── logs/                # Indexing and query logs
└── prompts/             # Custom prompt templates
```

### Setup

```bash
cd Terminal

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install graphrag
```

### Configure

Create a `.env` file:
```env
GRAPHRAG_API_KEY=your_openai_api_key_here
```

The `settings.yaml` is pre-configured with sensible defaults:
- **LLM:** `gpt-4o-mini`
- **Embeddings:** `text-embedding-3-small`
- **Chunk size:** 1200 tokens with 100 token overlap
- **Vector store:** LanceDB (local)
- **Entity types:** organization, person, geo, event

### Usage

**Step 1 — Initialize project (first time only):**
```bash
graphrag init --root .
```

**Step 2 — Add your documents:**
```bash
# Place your .txt files in the input/ folder
cp your_document.txt input/
```

**Step 3 — Index (build the knowledge graph):**
```bash
graphrag index --root .
```

**Step 4 — Query:**
```bash
# Local search (entity-aware, good for specific questions)
graphrag query "Who is the main character?" --method local

# Global search (community-level, good for broad themes)
graphrag query "What are the main themes?" --method global

# DRIFT search (exploratory, dynamic)
graphrag query "What relationships exist?" --method drift

# Basic search
graphrag query "Summarize the plot" --method basic
```

### Search Methods Explained

| Method | Best For | How It Works |
|--------|----------|--------------|
| `local` | Specific entity questions | Retrieves entity neighborhood + related text |
| `global` | Broad thematic questions | Aggregates community reports |
| `drift` | Exploratory discovery | Dynamic query expansion |
| `basic` | Simple vector lookups | Standard semantic similarity |

---

## Method 2 — FastAPI + Docker Compose Web App

A full-featured REST API with a web UI, packaged as a Docker container. Ideal for serving GraphRAG as a service.

### Folder: `project/`

```
project/
├── app.py               # FastAPI application
├── index.html           # Web UI frontend
├── Dockerfile           # Container definition
├── docker-compose.yml   # Multi-service orchestration
├── requirements.txt     # Python dependencies
├── settings.yaml        # GraphRAG configuration
├── .env                 # API key
├── input/               # Mounted volume for documents
├── output/              # Mounted volume for graph artifacts
├── cache/               # LLM call cache
├── logs/                # Application logs
└── prompts/             # Custom prompt templates
```

### Setup & Run

**Step 1 — Configure your API key:**
```bash
cd project
# Edit .env
echo "GRAPHRAG_API_KEY=your_openai_api_key_here" > .env
```

**Step 2 — Build and start the container:**
```bash
docker-compose up --build
```

The app will be available at **http://localhost:8000**

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve the web UI |
| `POST` | `/upload/` | Upload a document (`.txt`) |
| `POST` | `/index/` | Trigger graph indexing |
| `POST` | `/query/` | Query the knowledge graph |

### Example API Usage

**Upload a document:**
```bash
curl -X POST "http://localhost:8000/upload/" \
  -F "file=@your_document.txt"
```

**Build the index:**
```bash
curl -X POST "http://localhost:8000/index/"
```

**Query:**
```bash
curl -X POST "http://localhost:8000/query/" \
  -F "question=Who is the main character?" \
  -F "mode=local"
```

### Docker Volumes

The `docker-compose.yml` mounts two host directories so your data persists outside the container:

```yaml
volumes:
  - ./input:/app/input    # Source documents
  - ./output:/app/output  # Graph index artifacts
```

### Dependencies

```
fastapi
uvicorn[standard]
python-multipart
graphrag
lancedb
pyarrow
openai
python-dotenv
```

---

## Method 3 — Neo4j Knowledge Graph Pipeline

Uses the `neo4j-graphrag` Python library to build a proper knowledge graph in Neo4j, with vector indexing and a RAG pipeline on top. Best for production use cases requiring persistent, inspectable, and queryable graphs.

### Folder: `neo4j_project/`

```
neo4j_project/
├── graph_rag_KGpipeline.py   # Build knowledge graph from text
├── graphrag_indexing.py      # Create vector index + upsert embeddings
├── graphrag_query.py         # Query the graph with RAG
├── 1.ipynb                   # Jupyter notebook walkthrough
└── .env                      # API key
```

### Prerequisites

Start a Neo4j instance (Docker recommended):

```bash
docker run \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```

Neo4j Browser will be available at **http://localhost:7474**

### Setup

```bash
cd neo4j_project
pip install neo4j neo4j-graphrag openai python-dotenv
```

Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 1 — Build the Knowledge Graph

`graph_rag_KGpipeline.py` uses `SimpleKGPipeline` to extract entities and relationships from text and store them in Neo4j.

```python
# Customize your schema
node_types = ["Person", "House", "Planet"]
relationship_types = ["PARENT_OF", "HEIR_OF", "RULES"]
patterns = [
    ("Person", "PARENT_OF", "Person"),
    ("Person", "HEIR_OF", "House"),
    ("House", "RULES", "Planet"),
]
```

Run:
```bash
python graph_rag_KGpipeline.py
```

### Step 2 — Create Vector Index & Embed

`graphrag_indexing.py` creates a vector index on the Neo4j `Chunk` nodes and upserts embeddings.

```bash
python graphrag_indexing.py
```

Configuration inside the file:
```python
INDEX_NAME = "vector-index-name"
# Uses text-embedding-3-large (3072 dimensions)
# Similarity: euclidean
```

### Step 3 — Query with RAG

`graphrag_query.py` wires together the vector retriever, LLM, and GraphRAG pipeline.

```bash
python graphrag_query.py
```

Example:
```python
query_text = "Who is Paul Atreides?"
response = rag.search(query_text=query_text, retriever_config={"top_k": 5})
print(response.answer)
```

### Architecture

```
Text Input
    │
    ▼
SimpleKGPipeline (LLM extraction)
    │
    ▼
Neo4j Graph (nodes + relationships)
    │
    ▼
Vector Index (OpenAI embeddings)
    │
    ▼
VectorRetriever → GraphRAG → LLM → Answer
```

---

## 🔑 Environment Variables

All three methods use OpenAI. Make sure your `.env` file is set before running:

| Variable | Used In | Description |
|----------|---------|-------------|
| `GRAPHRAG_API_KEY` | Terminal, project | OpenAI API key for Microsoft GraphRAG |
| `OPENAI_API_KEY` | neo4j_project | OpenAI API key for Neo4j GraphRAG |

> ⚠️ **Never commit your `.env` files to version control.** Each folder includes `.env` in `.gitignore`.

---

## 📊 Comparison of Methods

| Feature | Terminal (CLI) | FastAPI + Docker | Neo4j |
|---------|---------------|-----------------|-------|
| Setup complexity | Low | Medium | Medium–High |
| Best for | Local experimentation | Serving as an API | Production / enterprise |
| Vector store | LanceDB (file-based) | LanceDB (file-based) | Neo4j (persistent DB) |
| Graph visibility | Parquet files | Parquet files | Visual Neo4j Browser |
| Multi-hop queries | ✅ | ✅ | ✅ |
| Custom schema | Via prompts | Via prompts | Explicit node/edge types |
| Persistence | File system | Docker volumes | Neo4j database |
| Web UI | ❌ | ✅ | Neo4j Browser |

---

## 📚 Resources

- [Microsoft GraphRAG Documentation](https://microsoft.github.io/graphrag/)
- [Neo4j GraphRAG Python Library](https://neo4j.com/labs/neo4j-graphrag-python/)
- [GraphRAG Paper (Microsoft Research)](https://arxiv.org/abs/2404.16130)
- [LanceDB Documentation](https://lancedb.github.io/lancedb/)

---

## 📄 License

This project is for educational and demonstration purposes. See individual library licenses for Microsoft GraphRAG and Neo4j GraphRAG.
