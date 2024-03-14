from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_pinecone import PineconeVectorStore
from langchain.tools.retriever import create_retriever_tool

from dotenv import load_dotenv
import os
load_dotenv() 

openai_api_key = os.environ.get("OPENAI_ACCESS_TOKEN")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")

def pinecone_retrival_index_setup():
    pc = Pinecone(api_key=pinecone_api_key)
    index_name = 'llm-for-sql-agent'
    index = pc.Index(index_name)
    embedding_dim = index.describe_index_stats()['dimension']
    return embedding_dim, index_name

def pinecone_retrival_vectorstore():
    text_dim, index_name = pinecone_retrival_index_setup()
    doc_embedding = "text-embedding-3-small"

    embeddings = OpenAIEmbeddings(
        model=doc_embedding,
        openai_api_key=openai_api_key,
        dimensions=text_dim
    )

    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings)

    retriever = vectorstore.as_retriever(search_kwargs=dict(k=3))
    return retriever

document_retriever_tool = create_retriever_tool(
    retriever=pinecone_retrival_vectorstore(),
    name="document_search",
    description="Search for information about documents not related to any SQL query. For any questions about Documents, you must use this tool!",
)

def main():
    question = """
    How much was the taxi fare on the invoice?
    """
    print(document_retriever_tool.run(question))
    
if __name__ == "__main__":
    main()