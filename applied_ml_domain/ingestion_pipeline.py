from langchain_chroma import Chroma
from unstructured.chunking.title import chunk_by_title
from unstructured.partition.pdf import partition_pdf
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
import os
import torch

doc_size=32
db_path="db/chroma_db_2"

llm = ChatOllama(model="gemma4")
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3", model_kwargs={"device":"cuda"}) #, encode_kwargs={"batch_size":8}
db = Chroma(embedding_function=embedding_model, persist_directory=db_path, collection_metadata={'hnsw:space' : 'cosine'})

system_message = \
"""
You are a document preprocessing engine for a Retrieval-Augmented Generation (RAG) pipeline.

Your goal is to generate embedding-optimized content for vector retrieval.

INPUT MAY CONTAIN:

Plain document text
Extracted tables
Image descriptions / OCR / visual outputs

RULES:

DOCUMENT TEXT:

Preserve document text exactly as provided
Do NOT summarize document text
Do NOT rewrite document text
Output document text unchanged

TABLES:

Convert tables into concise retrieval-optimized summaries
Extract entities, metrics, variables, relationships, trends, and important values
Preserve technical terminology and keywords
Describe what information the table conveys

IMAGES:

Convert images into concise retrieval-optimized summaries
Describe objects, diagrams, labels, text, charts, relationships, and structure
Include trends, axes, units, and observations when applicable
Focus on informational content only

RETRIEVAL RULES:

Optimize output for semantic embeddings and cosine similarity retrieval
Preserve important keywords and entity names
Produce self-contained outputs
Prioritize semantic density over readability

OUTPUT FORMAT:

TEXT:



TABLES:

IMAGES:



STRICT RULES:

Never ask questions
Never request input
Never explain actions
Never output introductions
Never output examples
Return only the processed output
"""
sys_mes = SystemMessage(content=system_message)

def create_ai_summary(content_data):

    if content_data['tables'] or content_data['images']:
        content_msg=[]

        message=f"TEXT : {content_data['text']}\n"
        if content_data['tables']:
            message += "TABLES (in html format )are :\n"
            for i, table in enumerate(content_data['tables']):
                message+=f"TABLE {i+1}\n"
                message+=table
                message+="\n"

        content_msg.append({"type":'text', "text":message})
        if content_data['images']:

            for image_base64 in content_data['images']:
                # we say LLM to treat this data as image (send it to vision model), LLM  expect in form of URL
                content_msg.append({
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{image_base64}"} # data url -> data type, encoding , data
                ) 

        message = HumanMessage(content=content_msg)
        summary = llm.invoke([sys_mes, message]) 

        return summary.content
    else:
        return content_data['text']

def ingestion_pipeline(docs_path):

    docs_names = os.listdir(docs_path)
    documents=[]
    for a, doc_name in enumerate(docs_names, 1):

        print(a, "Document", os.path.join(docs_path, doc_name))

        elements = partition_pdf(os.path.join(docs_path, doc_name), strategy="hi_res", infer_table_structure=True, extract_image_block_types=['Image'], extract_image_block_to_payload=True)
        chunks = chunk_by_title(elements, max_characters=2000, new_after_n_chars=1500, combine_text_under_n_chars=300)
        
        print("No of chunks", len(chunks))
        for i, chunk in enumerate(chunks, 1): 

            print(i, "/", len(chunks))
            content_data={
                'text':chunk.text,
                'tables':[],
                'images':[],
            }

            if getattr(chunk, 'metadata') and getattr(chunk.metadata, 'orig_elements'):
                for element in chunk.metadata.orig_elements:
                    element_type = type(element).__name__

                    if element_type == 'Table':
                        content_data['tables'].append(element.metadata.text_as_html)

                    if element_type == 'Image':
                        content_data['images'].append(element.metadata.image_base64)

            summary = create_ai_summary(content_data)
            #print(summary)
            
            doc = Document(
                page_content=summary,
                metadata={
                    "source":doc_name,
                    "raw_text" : content_data['text'],
                }
            )

            if content_data['tables']:
                doc.metadata['raw_tables'] = content_data['tables']

            if content_data['images']:
                doc.metadata['raw_images'] = content_data['images']
            
            documents.append(doc)

            if len(documents)>=doc_size:
                db.add_documents(documents)
                documents=[]
                torch.cuda.empty_cache()
        if documents:
            db.add_documents(documents)
            documents=[]
            torch.cuda.empty_cache()
        
    return db

db = ingestion_pipeline("data")

