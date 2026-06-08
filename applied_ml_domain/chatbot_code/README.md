# Research RAG

---

## Overview 

---

>This is a multimodal Retrieval-Augmented Generation (RAG) system , which ingests various research papers related to LLMs, Transformers and RAG systems. The architecture supports multi-modal retrieval capabilities, allowing extraction of relevant textual content, tables, and images from research documents. This is achieved by converting images and tables into summarized textual representations using a LLM and store their embeddings in the VectorDatabase. Retrieved outputs are rendered through a frontend supporting Markdown, LaTeX enabling structured visualization of mathematical expressions, technical content, and research artifacts.

## Features

---

1. **Multimodal RAG** - Retrieves textual content, tables, and images from research papers
2. **Reranking** - Reranks retrieved chunks to select highly relevant chunks.
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
%%{
init: {
'theme':'base',
'themeVariables':{
'lineColor':'#FFFFFF',
'primaryBorderColor':'#FFFFFF',
'primaryTextColor':'#000000'
}
}
}%%

flowchart TD

A[Research Papers PDFs] --> B[PDF Parsing]

B --> C1[Text Extraction]
B --> C2[Table Extraction]
B --> C3[Image Extraction]

C1 --> D[Structure Aware Chunking<br/>chunk_by_title]
C2 --> D
C3 --> D

D --> E[Chunk]

E --> F1[Raw Text]
E --> F2[Tables HTML]
E --> F3[Images Base64]

F1 --> G[Multimodal Preprocessing<br/>LLM extracts information from Images and tables]
F2 --> G
F3 --> G

G --> H1[Preserve Document Text]
G --> H2[Summarize Tables]
G --> H3[Summarize Images]

H1 --> I[Create LangChain Documents]
H2 --> I
H3 --> I

I --> J[Metadata]
I --> S[page_content]

S --> W[Processed Text]

L --> K[BGE-M3 Embeddings]

W --> L[Batch Processing]

K --> M[(ChromaDB)]

J --> R1
J --> R2
J --> R3

R1[Raw Images] --> M
R2[Raw Tables] --> M
R3[Source Metadata] --> M

linkStyle default stroke:#FFFFFF,stroke-width:2px
classDef source fill:#FFE4B5,color:#000000,stroke:#333333
classDef extract fill:#B0E0E6,color:#000000,stroke:#333333
classDef process fill:#D8BFD8,color:#000000,stroke:#333333
classDef storage fill:#90EE90,color:#000000,stroke:#333333
classDef embed fill:#FFB6C1,color:#000000,stroke:#333333

class A source
class B,C1,C2,C3 extract
class D,E,F1,F2,F3,G,H1,H2,H3,I,S,W process
class K,L embed
class M,R1,R2,R3,J storage
```

---

## Retrieval Pipeline

```mermaid
%%{
init: {
'theme':'base',
'themeVariables':{
'lineColor':'#FFFFFF',
'primaryBorderColor':'#FFFFFF',
'primaryTextColor':'#000000'
}
}
}%%

flowchart TD

A[User Query]

A --> B[Hybrid Retrieval]

B --> C1[BM25 Search]
B --> C2[Vector Search]

C1 --> D[RRF Merge]
C2 --> D

D --> E[Cross Encoder Reranker]

E --> F[Top Chunks]

F --> G1[Text]
F --> G2[Images]
F --> G3[Tables]

G1 --> H[Gemma 4]

G2 --> I[Frontend Rendering]
G3 --> I
H --> I

I --> J1[Markdown]
I --> J2[LaTeX]
I --> J3[Images]
I --> J4[Tables]

linkStyle default stroke:#FFFFFF,stroke-width:2px
classDef input fill:#FFE4B5,color:#000000,stroke:#333333
classDef retrieval fill:#ADD8E6,color:#000000,stroke:#333333
classDef rerank fill:#FFB6C1,color:#000000,stroke:#333333
classDef generation fill:#D8BFD8,color:#000000,stroke:#333333
classDef output fill:#90EE90,color:#000000,stroke:#333333

class A input
class B,C1,C2,D retrieval
class E,F rerank
class G1,G2,G3,H,I generation
class J1,J2,J3,J4 output
```





