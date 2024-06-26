
import os
import sys
import time
import threading

from src.utils.colors import colors
from src.document import service as DocService
from src.entities.ollama_model import OllamaModel
from src.document import retrieval as DocRetrieval
from src.entities.model_open_ai import ModelOpenAI
from src.document import repository as DocRepository

class Agent:
    
    def __init__(self):
        self.model_ollama = OllamaModel()
        self.model_open_ai = ModelOpenAI()
        self.doc_db = DocRetrieval
        
    def welcome(self):
        print("\n",f"{colors.WARNING} Como posso ajudar hoje? {colors.ENDC}", "\n")
    
    def available(self):
        print("\n",f"{colors.WARNING} Quer perguntar mais alguma coisa? {colors.ENDC}", "\n")
        
    def question(self, question):
        result = self.doc_db.query(question, self.model_ollama.embed(question), 10)
        documents = self.doc_db.docs_to_text(result)
        answer = self.model_open_ai.question(question, documents)
        self.delay_write(answer)
        self.available()
        return answer
    
    def consult(self, question):
        doc1 = DocRetrieval.lines_to_text(DocRepository.query_metadata_include(question, 5))
        doc2 = DocRetrieval.lines_to_text(DocRetrieval.query_text(question, 5))
        documents = f"{doc1} \n {doc2}"
        answer = self.model_open_ai.question(question, documents)
        self.delay_write(answer)
        self.available()
        return answer
    
    def delay_write(self, content, delay=0.01):
        print(f"{colors.OKCYAN}------------------------------------------------------------------------------------------------------------------------------------------", "\n", end='', flush=True)
        print(f"{colors.BOLD}R: {colors.ENDC}{colors.OKCYAN}", end='', flush=True)
        
        for letter in content:
            print(letter, end='', flush=True)
            time.sleep(delay)
        
        print() 
        print(f"{colors.OKCYAN}------------------------------------------------------------------------------------------------------------------------------------------{colors.ENDC}")
        print("\n") 
    