# Research RAG

---

## Overview 

---

This is a multimodal Retrieval-Augmented Generation (RAG) system , which ingests various research papers related to LLMs, Transformers and RAG systems. The architecture supports multi-modal retrieval capabilities, allowing extraction of relevant textual content, tables, and images from research documents. Retrieved outputs are rendered through a frontend supporting Markdown, LaTeX, and KaTeX, enabling structured visualization of mathematical expressions, technical content, and research artifacts.

## Features

---

1. **Multimodel RAG** - Extracts textual content, tables, and images from research papers
2. **Reranking** - A reranker reorders retrieved docs.
3. **Hybrid Search** - Hybrid search combines keyword search (BM25) with vector search 
4. **Multi paper retrieval** - Supports retrieval across multiple research papers simultaneously
5. **LaTex and Markdown Support**
6. **Images and Tables Information are Retained**

## Tech Stacks

---

1. **LangChain** (RAG Orchestration)
2. **Gemma 4** (Locally Hosted LLM)
3. **BGE-M3** (Embedding Model)
4. **Unstructured** (PDF Parsing & Structure-Aware Chunking)
5. **bge-reranker-v2-m3** (Cross-Encoder)
6. **Ollama** (Runs LLMs locally)
7. **FastAPI** (Backend API)
8. **HTML, CSS, JavaScript** (Frontend)
9. **ChromaDB** (Vector Database)

## Ingestion Pipeline

```mermaid
flowchart TD

A[Research Papers PDFs] --> B[PDF Parsing]

B --> C1[Text Extraction]
B --> C2[Table Extraction]
B --> C3[Image Extraction]

C1 --> D[Structure Aware Chunking<br/>chunk_by_title]
C2 --> D
C3 --> D

D --> E[ Chunk ]

E --> F1[Raw Text]
E --> F2[Tables HTML]
E --> F3[Images Base64]

F1 --> G[Multimodal Preprocessing<br/>To extract Information from Tables and Images<br/>LLM summarizes the Tables and Images]
F2 --> G
F3 --> G

G --> H1[Preserve Document Text]
G -->|Convert Tables into Summarized Text| H2[Summarize Tables<br/>Convert Tables into Summarized Text]
G -->|Convert Images into Summarized Text| H3[Summarize Images]

H1 --> I[Create LangChain Documents]
H2 --> I
H3 --> I


J --> R1[Raw Images]
J --> R2[Raw Tables]
J --> R3[Source Metadata]

W --> K[BGE-M3 Embeddings]

I --> J[metadata]
I --> S[page_content] -->W[Processed Text content]

K --> L[Batch-wise Processing]

L --> M[Store in ChromaDB]

R1 --> M[Store in ChromaDB]
R2 --> M[Store in ChromaDB]
R3 --> M[Store in ChromaDB]


```

---

## Retrieval Pipeline

```mermaid
flowchart TD

A[User Query]

A --> B[Hybrid Retrieval]

B --> C1[BM25 Keyword Search]
B --> C2[Chroma Vector Retrieval]

C1 --> D[Merge Retrieved Chunks<br/>RRF]
C2 --> D

D --> E[Cross Encoder Reranker<br/>bge-reranker-v2-m3]

E --> F[Top Relevant Chunks]

F --> G1[Text]
F --> G2[Images]
F --> G3[Tables]

G1 --> H[Gemma 4 Generation]
G2 --> I
G3 --> I

H --> I[Frontend Rendering]

I --> J1[Markdown]

I --> J2[LaTeX ]

I --> J3[Images]

I --> J4[Tables]
```




