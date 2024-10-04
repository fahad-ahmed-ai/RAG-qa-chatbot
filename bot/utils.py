from .prompt import QUESTION_REFINE_TEMPLATE
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI



async def refine_user_query(query_text, get_chat):
    try:
        prompt_template = ChatPromptTemplate.from_template(
            QUESTION_REFINE_TEMPLATE
        )
        chats_list = list(get_chat)
        index_chats = chats_list[-2:]
        chats = index_chats[::-1]
        chat_details = [
        {"question": chat.get('user'), "answer": chat.get('bot')} for chat in chats
    ]
        prompt = prompt_template.format(
            question=chat_details,
            query=query_text,
        )

        model = ChatOpenAI(
            temperature=0,
            model="gpt-4o-mini",
        )
        response_text = model.invoke(prompt)
        refined_query_text = response_text.content
        return refined_query_text   
    except Exception as e:
        print(repr(e))
        return None