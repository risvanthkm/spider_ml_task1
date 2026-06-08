from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import  BM25Retriever
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

embedding_model = HuggingFaceEmbeddings(model_name = "BAAI/bge-m3")
llm = ChatOllama(model='gemma4')
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")

db = Chroma(
    embedding_function=embedding_model,
    persist_directory="db/chroma_db_2",
    collection_metadata={'hnsw:space' : 'cosine'}
)

stored_data = db.get()
chunks = []

for cont, metadata in zip(stored_data["documents"], stored_data["metadatas"]):
    chunks.append(Document(page_content=cont, metadata=metadata))

vector_retriever = db.as_retriever(search_kwargs={"k": 10})

keyword_retriever = BM25Retriever.from_documents(chunks)
keyword_retriever.k = 10

hybrid_retriever = EnsembleRetriever(retrievers=[vector_retriever, keyword_retriever], weights=[0.6, 0.4])

def rerank(query, chunks , top_k=3):
    combined = []

    for doc in chunks:
        combined.append([query, doc.page_content])

    scores = reranker.predict(combined)
    score_list=list(zip(chunks, scores))

    score_list.sort(key = lambda x :x[1], reverse=True)
    top_k_docs = [doc for doc, _ in score_list[:top_k-1]]

    return top_k_docs


def retrieve(query):
    response={}
    
    retrieved_chunks= hybrid_retriever.invoke(query)
    relevant_chunks = rerank(query, retrieved_chunks, 5)

    relevant_docs=""

    images = []
    tables = []
    sources = []

    for i , chunk in enumerate(relevant_chunks, 1):

        relevant_docs += f"Document {i}:\n{chunk.page_content}\n"

        if chunk.metadata.get('raw_images', None):
            images.extend(chunk.metadata['raw_images'])

        if chunk.metadata.get('raw_tables', None):
            tables.extend(chunk.metadata['raw_tables'])
            
        if chunk.metadata.get('source'):
            sources.append(chunk.metadata['source'])

    content = f"""
        You are a retrieval-based research assistant.

        Your task is to answer the QUERY using ONLY the information present in the provided DOCUMENTS.

        Rules:

        * Use ONLY information explicitly present in DOCUMENTS.
        * Do NOT use outside knowledge.
        * Do NOT mention phrases like:

        * "Based on the documents"
        * "According to the provided context"
        * "The documents state"
        * "The provided documents mention"
        * Answer directly and naturally.
        * If the DOCUMENTS do not contain sufficient information, output exactly:

        `I couldn't find relevant information for this query in the retrieved documents.`

        * Preserve mathematical expressions in LaTeX format.
        * Use proper Markdown formatting:

        * headings when useful
        * bullet lists when useful

        QUERY:

        {query}

        DOCUMENTS:

        {relevant_docs}

        Return ONLY the answer in Markdown.

    """

    gen_res = llm.invoke(content).content
    response['text'] = gen_res
    response['images'] = images
    response['tables'] = tables
    response['sources'] = list(set(sources))

    return response

