from fastapi import File, UploadFile
import os, openai
from utilities.config import OPENAI_API_KEY
from utilities.responses import bad_request_response, error_response
from .utils import save_document

openai.api_key = OPENAI_API_KEY


def upload_knowledge(file: UploadFile = File(...)):
    try:
        if file.content_type != "application/pdf":
            return bad_request_response(
                msg="Invalid file type. Only PDF files are accepted."
            )

        else:
            UPLOAD_DIRECTORY = "media"
            os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

            file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

            with open(file_path, "wb") as buffer:
                file_content = file.file.read()
                buffer.write(file_content)

            save_docs = save_document(file_path, file.filename)

            os.remove(file_path)
            return save_docs

    except Exception as e:
        print(repr(e))
        return error_response(msg="Failed", exception=e)
