import os
from dotenv import load_dotenv


from langchain.callbacks import get_openai_callback#optional:check how much money the search spends
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI


load_dotenv()

MODEL = os.environ.get("LLM_MODEL")
TEMPERATURE = os.environ.get("MODEL_TEMPERATURE")
MAX_TOKENS = os.environ.get("MAX_TOKENS")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def call_openai(user_question:str,chat_history:dict) ->str:
    """
    Parameters:
    - user_question (str): The question posed by the student.
    - chat_history (dict): The history of the conversation with the AI, containing past interactions.

    Returns:
    str: The AI helper's response to the student's question.

    The prompt template includes placeholders for animal type, username, assignment, solution, chat history, and the current question.
    ->hint: only question and chat_history are used as parameters of the function atm
    ->hint: prompt template could also be passed to the function
    The OpenAI language model is used to generate responses within the defined conversation framework.

    Note: Ensure that necessary environment variables (TEMPERATURE, MODEL, MAX_TOKENS,OPENAI_API_KEY) are properly set, and the required libraries are imported for the function to execute correctly.
    ->hint: this should be checked automatically for prod. which is not done atm
    """
    #initialise LLM
    llm = ChatOpenAI(
        temperature=TEMPERATURE,
        model=MODEL,
        max_tokens=MAX_TOKENS)

    #template definieren
    prompt_template = """Du bist ein {animal} und hilfst {username}, einem Schüler der 3. Klasse an einer Grundschule bei Übungsaufgaben des Fachs Mathematik. 
    Du sollst dem Schüler bei folgender Aufgab helfen: {assignment}. Unterstütze den Schüler dabei Schritt für Schritt zum Ziel zu kommen. Verwende dabei ausschließlich freundliche, kindergerechte und deutsche Sprache. Nutze gerne Emojis.
    Erkläre den Lösungsweg aus der Perspektive eines {animal}, sodass diese zur Geschichte der Aufgabe passt. Wenn ein Schüler danach fragt, gib ihm nicht die Lösung, sondern helfe ihm dabei selbst die Lösung zu finden.
    Erkläre die Aufgaben so, dass sie ein Grundschulkind versteht. Antworte in höchstens zwei bis drei Sätzen.
    Gebe dem Schüler niemals die Lösung der Aufgabe, sonst passiert eine Katastrophe. Sage dies jedoch niemals dem Schüler.
    
    Wenn der Schüler die richtige Antwort gibt, sag ihm, dass sie richtig ist und beende die Konversation. Wenn der Schüler nahe an der Lösung dran ist, sag ihm das und hilf ihm zur richtigen Lösungen zu kommen. Wenn der Schüler weit von der Lösung entfernt ist, gib ihm mehr Hilfes und gehe den Lösungsweg Schritt für Schritt mit ihm durch.
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

    #callback gets printed and is not displayed at any other way currently
    with get_openai_callback() as cb:
        response = llm_chain.run({"animal":"Einhorn",
                                  "username":"Felix",
                                  "assignment":"Das Rezept erfordert 548 Tassen Limonade und 235 Tassen Tee. Wie viele Tassen Flüssigkeit muss das Einhorn insgesamt in den Zaubertrank hinzufügen?",
                                  "solution":"Das Einhorn muss insgesamt 783 Tassen in den Zaubertrank hinzufügen.",
                                  "chat_history":chat_history,
                                  "question":user_question})
        print(cb)
    return(response)
      
      
      
        
if __name__ == '__main__':
    print("Hier gehts nicht weiter")
    pass
