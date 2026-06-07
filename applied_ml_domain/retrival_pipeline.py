from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from io import BytesIO
from PIL import Image
import base64

embedding_model = HuggingFaceEmbeddings(model_name = "BAAI/bge-m3")
llm = ChatOllama(model='gemma4')

db = Chroma(
    embedding_function=embedding_model,
    persist_directory="db/chroma_db_2",
    collection_metadata={'hnsw:space' : 'cosine'}
)

def retrieve(query):
    response={}

    retriever = db.as_retriever(search_kwargs={"k": 5})
    relevent_chunks = retriever.invoke(query)
    relevent_docs=""
    images = []
    tables = []
    sources = []
    for i , chunk in enumerate(relevent_chunks, 1):

        relevent_docs += f"Document {i}:\n{chunk.page_content}\n"

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

        {relevent_docs}

        Return ONLY the answer in Markdown.

    """

    gen_res = llm.invoke(content).content
    response['text'] = gen_res
    response['images'] = images
    response['tables'] = tables
    response['sources'] = list(set(sources))

    return response

