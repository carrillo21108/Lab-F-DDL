#ScanGenerator.py

from graphviz import Digraph
# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), '../resources'))

from YalexLib import YalexRecognizer
import AfdLib
import AfLib
import AstLib
import RegexLib
from AstLib import Node

import pickle


#Clase Lexer
class Lexer:
    def __init__(self,afd,yalex_tokens,input_tokens=[]):
        self.afd = afd
        self.yalex_tokens = yalex_tokens
        self.input_tokens = input_tokens

def generateLexer(pklName,file_path):
    definitions_id = []
    tokens_regex = []
    yalex_tokens = []
        
    yalexRecognizer = YalexRecognizer()

    #Lectura del documento yalex
    with open(file_path, 'r', encoding='utf-8') as file:
        yalexContent = file.read()  # Leer todo el contenido del archivo
    
    if yalexRecognizer.yalexRecognize(yalexContent):
    

        for key in yalexRecognizer.get_rule_tokens():
            tokens_regex.append(key)

        for key in yalexRecognizer.get_definitions():
            definitions_id.append(key)
    

        new_afdPos = [9] #Reconociendo chars y strings
        i=11
        for item in definitions_id:
            yalexRecognizer.afds.append(AfdLib.createAFD(item+'■'))
            i+=1
            new_afdPos.append(i)

        i=0

        print(tokens_regex)
        print('\n')
        #Reemplazando las variables de las definiciones en el regex de tokens
        new_tokens_regex = []
        while i<len(tokens_regex):
            token = yalexRecognizer.valueRecognize(new_afdPos,tokens_regex[i])

            if token.content!="":
                new_tokens_regex.append(token.content+'■')
                yalex_tokens.append(token._id)
            i+=1
        
        tokens_regex = new_tokens_regex
        print(tokens_regex)
        print(yalex_tokens)


        lexer_regex = '|'.join(tokens_regex)
        lexer_regex = '('+lexer_regex+')'


        #Construccion Lexer
        lexer = Lexer(AfdLib.createLexerAFD(lexer_regex,yalex_tokens,yalexRecognizer.get_rule_tokens()),set(yalex_tokens))
    
        # Abrimos un archivo en modo binario de escritura
        with open(pklName, 'wb') as archivo_salida:
            # Serializamos el objeto y lo guardamos en el archivo
            pickle.dump(lexer, archivo_salida)
            
        return yalexRecognizer
    else:
        return None