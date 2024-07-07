from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
import faiss
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.document_loaders import CSVLoader
from prompts import prompt1,prompt2
import json
import m2metricforge.main as mf
from pars import parse
import re
from langchain.schema import AIMessage


local_llm = "qwen2"
llm = ChatOllama(model=local_llm, format="json", temperature=0)
embedding_model = HuggingFaceEmbeddings(model_name="cointegrated/rubert-tiny2")
prompt = ChatPromptTemplate.from_template(prompt2)


def llm_chain(question):
    """
    Функция для построения chain для вызова invoke
    :return: на выходе функция дает chain, который можно запускать с помощью invoke
    """

    db = FAISS.load_local(r"faiss_try1", embedding_model, allow_dangerous_deserialization=True)
    search_kwargs = {
        'k': 10,  # Number of nearest neighbors to retrieve
        'nprobe': 5,  # Number of clusters to explore
        'metric_type': faiss.IndexFlatL2,  # Use Euclidean distance  METRIC_L2
        'efSearch': 50,  # HNSW-specific parameter for search quality
        'max_dist': 0.5,  # Maximum distance for neighbors
    }
    retriever = db.as_retriever() #search_kwargs=search_kwargs
    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )
    result = chain.invoke(question)
    parsed_data = json.loads(result)
    link_pars = parsed_data.get("Link")
    link = "https://" + str(link_pars)
    link_info = str(parse(link))
    question = question + " Это мой вопрос, в ответе на него может помочь: " + link_info

    text = "ОТВЕЧАЙ ТОЛЬКО НА РУССКОМ ЯЗЫКЕ. Сделай коротки ответ. Ты - бот для обслуживания разработчиков для приложения RuStore, аналог Google Play. У меня есть следующий вопрос: {question}"

    prompt2 = ChatPromptTemplate.from_template(text)
    chain2 = (
             {"question": RunnablePassthrough()}
             | prompt2
             | llm
             | StrOutputParser()
    )
    result2 = chain2.invoke(question)
    parsed_data2 = json.loads(result2)
    try:
        link_pars2 = parsed_data2.get("answer") + "\nСсылка, где вы можете ознакомиться с информацией более подробно: " + link
    except TypeError:
        link_pars2 = parsed_data2.get("ответ") + "\nСсылка, где вы можете ознакомиться с информацией более подробно: " + link
    # chat_template = ChatPromptTemplate.from_messages(
    #     [
    #         SystemMessage(
    #             content=(f"""Ты - бот для обслуживания разработчиков для приложения RuStore, аналог Google Play. Ты получаешь информацию для ответа из этой ссылки  {link}. Твой ответ должен быть следующего формата:
    #                      1. Ответ на вопрос пользователя.
    #                      2. Исправленный код в ```code``` если требуется."
    #                      3. Ссылка: """)
    #         ),
    #         HumanMessagePromptTemplate.from_template("{text}"),
    #     ]
    # )
    # chain2 = SystemMessage | HumanMessage | llm | StrOutputParser
    # messages = chat_template.format_messages(text=text)
    # response = llm(messages)
    # json_content = response.content
    # output_cleaned = json_content.replace('\n', '\n').replace('"', '\"')
    # output_cleaned = f'{{ "answer": "{output_cleaned[12:-4]}" }}'
    # print(output_cleaned)
    # # parsed_data = json.loads(json_content)
    # # answer_data = parsed_data["answer"]
    # # print(answer_data)
    # # response_final = parsed_data.get("answer") + " Ссылка, по которой вы можете ознакомиться более подробно: " + link
    return link_pars2
#llm_chain("Подскажите пожалуйста, настройка для push «icon string» подразумевает что при использование этого значение, в конечный push будет отображаться иконка используемого приложения?")

