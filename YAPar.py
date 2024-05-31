#Parser.py
# Este es un archivo Python generado automaticamente
import pickle
# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), 'parser'))

import LRLib

#Clase Parser
class Parser:
    def __init__(self,grammar,input_tokens):
        self.grammar = grammar
        self.input_tokens = input_tokens

#Lectura del objeto pkl       
with open('YAPar.pkl', 'rb') as archivo_entrada:
    parser = pickle.load(archivo_entrada)
        
grammar = LRLib.augment_grammar(parser.grammar)
input_value = LRLib.Fifo()

for item in parser.input_tokens:
    input_value.insert(item)

parsing_table = LRLib.generate_SLRTable(grammar)
if parsing_table:
    LRLib.print_parsing_table(parsing_table)
    LRLib.LRParsing(grammar,parsing_table,input_value)
