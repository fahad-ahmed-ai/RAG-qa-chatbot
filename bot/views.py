from dotenv import load_dotenv
from utilities.config import OPENAI_API_KEY, chroma_client, db
from utilities.responses import success_response, error_response
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from .prompt import SYSTEM_PROMPT
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from .schema import Query
from datetime import datetime
from .utils import refine_user_query
from .db import get_chat_history


load_dotenv()

chat_collection = db.get_collection("chat")


async def qa_bot(_schema: Query):
    try:
        get_chat = await get_chat_history()

        history = ChatMessageHistory()
        for each_chat in get_chat:
            if "user" in each_chat:
                history.add_user_message(each_chat["user"])
            if "bot" in each_chat:
                history.add_ai_message(each_chat["bot"])
        memory = ConversationBufferMemory(
            chat_memory=history, human_prefix="Human", ai_prefix="Assistant"
        )

        refined_query_text = await refine_user_query(_schema.query_text, get_chat)

        embedding_function = OpenAIEmbeddings()

        chroma_db = Chroma(
            embedding_function=embedding_function,
            client=chroma_client,
            persist_directory="db/",
        )

        results = chroma_db.similarity_search(refined_query_text, k=3)
        context_text = ""
        for doc in results:
            a = doc.page_content.replace("\n", "")
            context_text += a

        system_prompt = SYSTEM_PROMPT["bot"]
        prompt_template = system_prompt.replace("{prompt}", context_text)
        PROMPT = PromptTemplate(
            input_variables=["history", "input"], template=prompt_template
        )
        conversation = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=OPENAI_API_KEY,
            max_tokens=3000,
        )
        conversation_chain = ConversationChain(
            llm=conversation,
            prompt=PROMPT,
            memory=memory,
        )
        response = conversation_chain.invoke(input=f"{refined_query_text}")
        formatted_response = response["response"]

        user_chat_document = {
            "user": refined_query_text,
            "bot": formatted_response,
            "created_on": datetime.now(),
        }
        await chat_collection.insert_one(user_chat_document)
        return success_response(msg="Success", data={"response": formatted_response})
    except Exception as e:
        print(repr(e))
        return error_response(msg="Something went wrong")
