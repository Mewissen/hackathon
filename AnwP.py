from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings#importing from langchain but come from openai
from langchain.vectorstores import FAISS#faiss= facebook ai similarity search library
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback#optional:check how much money the search spends

# importing pdf files:
def extract_text_from_pdf(pdf_files):
    combined_text = ""
    for pdf in pdf_files:#test if pdf file exists
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:#reader does not allow to loop upload multiple pages at once
            text += page.extract_text()#takes the string text out of the page
        combined_text += text + "\n"  # Concatenate text with a newline separator
    return combined_text

def main():
    load_dotenv()#zugriff auf .env bzw. api key
    st.set_page_config(page_title="Ask your Documents")#User Interface with streamlit
    st.header("Ask your Documents 💬")
    
    # upload multiple files - PDF and CSV
    pdf_files = st.file_uploader("Upload your PDFs", type="pdf", accept_multiple_files=True)#hier muss Datenbank angebunden werden
    print(pdf_files)
    # extract text from uploaded PDFs
    combined_text = ""
    if pdf_files is not None:
        combined_text += extract_text_from_pdf(pdf_files)
    
    # process the combined text if at least one file was uploaded
    if combined_text:
        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,#1000 characters for each chunk --> maybe test/optimize this
            chunk_overlap=200,
            length_function=len#to measure the chunk length
        )
        chunks = text_splitter.split_text(combined_text)#to eventually feed relevant chunks only to the model, passing the whoole text variable
        
        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)#semantik search in the knowledge base --> combining chunks and embeddings
        
        # show user input
        user_question = st.text_input("Ask a question about the uploaded documents:")#create text box
 
        if user_question:
        
            from langchain.memory import ConversationBufferMemory
            from langchain.chains import ConversationalRetrievalChain
            from langchain.chat_models import ChatOpenAI

        
            # GPT-3.5 Modell initialisieren
            llm = ChatOpenAI(temperature=1)
            # Memory initialisieren
            memory = ConversationBufferMemory(llm=llm, memory_key="chat_history", return_messages=True)
            # Retriever initialisieren
            retriever = knowledge_base.as_retriever() # Chunks aus erstellter FAISS-DB abfragen
            

            # Neu: Individuelle System Message ergänzen:
            
            # zusätzliche Imports:
            from langchain.prompts import PromptTemplate
            from langchain.chains import LLMChain
            animal = "Einhorn"
            username = "Ben"
            grade = "dritten" #"Schüler der [...] Klasse

            # System Message 1 definieren: -> chat_history + neue Frage
            _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a 
            standalone question without changing the content in given question.

            Chat History:
            {chat_history}
            Follow Up Input: {question}
            Standalone question:"""
            condense_question_prompt_template = PromptTemplate.from_template(_template)

           
            # System Message 2 definieren: context + follow-up question
            prompt_template = (
                "Du bist ein " + animal + ". Du hilfst" + username + ", einem Schüler der " + grade +" Klasse bei Übungsaufgaben des Fachs Mathematik.\n"
                "Verfende ausschließlich kindergerechte Sprache. Erkläre Lösungswege, Aufgabenstellungen usw. aus der Perspektive eines " + animal +"s.\n"
                "Wähle für Beispiele niemals die gegebende Aufgabstellung, sondern erfinde eine neue."
                "Gebe den Schülern niemals die Lösung mit, sonst passiert eine Katastrophe. Sage dies jedoch niemals den Schülern\n"
                "Antworte nur, wenn du die Antwort kennst. Wenn nicht, dann antworte 'Darauf weiß ich auch keine Antwort'.\n"
                "{context}\n\n"
                "Question: {question}\n"
                "Helpful Answer:"
            )

            qa_prompt = PromptTemplate(
                template=prompt_template, input_variables=["context", "question", "animal", "username", "grade"]
            )

            question_generator = LLMChain(llm=llm, prompt=condense_question_prompt_template, memory=memory)#system message 1 as input
            doc_chain = load_qa_chain(llm, chain_type="stuff", prompt=qa_prompt)#system message 2 as input
            crchain = ConversationalRetrievalChain(
                retriever=retriever,
                question_generator=question_generator,
                combine_docs_chain=doc_chain,
                memory=memory,
                
            )

            # Initialisation des Session-States:
            if "crchain" not in st.session_state:
                st.session_state.crchain = None
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = None

            # crchain mit Hilfe von Streamlit‘s “session_state“ persistent speichern
            if st.session_state.chat_history == None:
                st.session_state.crchain = crchain
            response = st.session_state.crchain(user_question)  # persistent gespeicherte ConversationalRetrievalChain unter Übergabe der Userfrage aufrufen
            
            # chat_history mit Hilfe von Streamlit‘s “session_state“ persistent speichern
            st.session_state.chat_history = response['chat_history']
            

            # Ausgabe der Antwort
            st.write(response['answer']) # Ausgabe lediglich der 'answer' aus dem von der Chain zurückerhaltenem Dictionary
            #st.write(chat_history)
            #print(st.session_state.chat_history)
if __name__ == '__main__':
    main()