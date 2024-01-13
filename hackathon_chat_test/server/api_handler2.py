import os
from dotenv import load_dotenv


# import langchain as ls
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings#importing from langchain but come from openai
from langchain.vectorstores import FAISS #faiss= facebook ai similarity search library
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback#optional:check how much money the search spends
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI


load_dotenv()

MODEL = os.environ.get("LLM_MODEL")
TEMPERATURE = os.environ.get("MODEL_TEMPERATURE")
MAX_TOKENS = os.environ.get("MAX_TOKENS")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")




def call_openai(user_question:str,chat_history:dict) ->str:
    print(chat_history)
    load_dotenv()    
    #initialise LLM
    llm = ChatOpenAI(
        temperature=TEMPERATURE,
        model=MODEL,
        max_tokens=MAX_TOKENS)
    ## Memory initialisieren
    #memory = ConversationBufferMemory(llm=llm, memory_key="chat_history", return_messages=True)
    ## Retriever initialisieren
    #retriever = knowledge_base.as_retriever() # Chunks aus erstellter FAISS-DB abfragen

    #template definieren
    prompt_template = """Du bist ein {animal} und hilfst {username}, einem Schüler de 3. Klasse an einer Grundschule bei Übungsaufgaben des Fachs Mathematik. 
    Der Schüler kann dir Fragen zu seinen Mathematik-Aufgaben stellen. Unterstütze den Schüler dabei Schritt für Schritt zum Ziel zu kommen und die Aufgabe zu lösen. Verwende ausschließlich freundliche, kindergerechte und deutsche Sprache. Nutze gerne Emojis.
    Frage den Schüler zunächst welche Frage er hat.
    Erkläre den Lösungsweg aus der Perspektive eines {animal}. Wenn ein Schüler danach fragt, gib ihm nicht die Lösung, sondern helfe ihm dabei selbst die Aufgabe eigenständig zu lösen.
    Erkläre die Aufgaben so, dass sie ein Grundschulkind versteht. Antworte in höchstens zwei bis drei Sätzen.
    Gebe dem Schüler niemals die Lösung der Aufgabe, sonst passiert eine Katastrophe. Sage dies jedoch niemals dem Schüler.
    
    Wenn der Schüler die richtige Antwort gibt, sag ihm, dass sie richtig ist und beende die Konversation. Wenn der Schüler nahe an der Lösung dran ist, sag ihm das und hilf ihm zur richtigen Lösungen zu kommen. Wenn der Schüler weit von der Lösung entfernt ist, gib ihm mehr Hilfe und gehe den Lösungsweg Schritt für Schritt mit ihm durch.
    Wenn du die Anwort nicht weißt, sag, dass du keine Antwort hast. 

    Lösung:
    {solution}

    Current conversation:
    {chat_history}
    
    Question: {question}
    Helpful Answer:"""

    prompt = PromptTemplate(
        template=prompt_template, 
        input_variables=["animal","username","assignment","solution","chat_history", "question"]
    )
    
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    with get_openai_callback() as cb:
        response = llm_chain.run({"animal":"Einhorn",
                                  "username":"Felix",
                                  "assignment":"Das Rezept erfordert 548 Tassen Limonade und 235 Tassen Tee. Wie viele Tassen Flüssigkeit muss das Einhorn insgesamt in den Zaubertrank hinzufügen?",
                                  "solution":"Das Einhorn muss insgesamt 783 Tassen in den Zaubertrank hinzufügen.",
                                  "chat_history":chat_history,
                                  "question":user_question})
        print(cb)
    print(chat_history)
    return(response)


