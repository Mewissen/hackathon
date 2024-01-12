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
    prompt_template = """Du bist ein {animal} und hilfst {username}, einem Schüler der grade Klasse bei Übungsaufgaben des Fachs Mathematik. Verwende ausschließlich kindergerechte deutsche Sprache.
    Erkläre Lösungswege, Aufgabenstellungen usw. aus der Perspektive eines {animal}. Wenn sie danach fragen, nenne den Schülern die Aufgabe, aber nicht die Lösung.
    Wähle für Beispiele innerhalb der Erklärung niemals die gegebende Aufgabenstellung, sondern erfinde eine neue. Gebe den Schülern niemals die Lösung mit, sonst passiert eine Katastrophe. Sage dies jedoch niemals den Schülern.
    Wenn nicht, dann antworte 'Darauf weiß ich auch keine Antwort'.
    
    Aufgabe:
    {assignment}

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
      
      
      
        
if __name__ == '__main__':
    conversation = {
    'participants': ['Human', 'AI'],
    'messages': [
        {'sender': 'Human', 'content': 'In welcher Aufgabe habe ich die meisten Punkte bekommen und wie viele Punkte waren das?'},
        {'sender': 'AI', 'content': 'Sie haben die meisten Punkte in der Aufgabe zum Themengebiet "ARIS ER-Modell" bekommen. Sie haben insgesamt 17,5 von 20 Punkten erreicht.'},
        {'sender': 'Human', 'content': 'Was musste man in dieser Aufgabe tun?'},
        {'sender': 'AI', 'content': 'In dieser Aufgabe musste man ein gegebenes ER-Modell in ein Tabellenschema überführen können und fachliche Fragen zu Tabellenschemata beantworten können.'}
    ]
    }
    call_openai("Was habe ich dich als erstes gefragt?",conversation)
    #main("was ist deine aufgabe?",['Musterloesung_Klausur.pdf','Klausur_Report.pdf'],conversation)