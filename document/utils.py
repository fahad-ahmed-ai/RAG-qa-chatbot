from llama_parse import LlamaParse
from utilities.config import LLAMA_CLOUD_API_KEY, chroma_client
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utilities.responses import success_response, error_response


def save_document(file_path, file_name):
    try:
        llama_parse_documents = LlamaParse(
            result_type="markdown", api_key=LLAMA_CLOUD_API_KEY
        ).load_data(file_path)
        embedding = OpenAIEmbeddings()
        docs_content = llama_parse_documents[0].get_content()

        metadata = {"source": file_name}

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        text_chunks = text_splitter.split_text(docs_content)

        chroma_instance = Chroma(
            embedding_function=embedding,
            client=chroma_client,
            persist_directory="db/",
        )

        chroma_instance.add_texts(
            texts=text_chunks,
            metadatas=[metadata] * len(text_chunks),
        )
        chroma_instance.persist()
        return success_response(msg="File uploaded successfully")
    except Exception as e:
        print(repr(e))
        return error_response(msg="Failed", exception=e)