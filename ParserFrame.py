# ParserFrame.py
        
if __name__ == "__main__": 
    name = input("Ingrese el nombre del archivo py del parser: ")
    
    # Definir el contenido del nuevo archivo Python Parser.py
    contenido = f"""#Parser.py
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
with open('{name}.pkl', 'rb') as archivo_entrada:
    parser = pickle.load(archivo_entrada)
        
grammar = LRLib.augment_grammar(parser.grammar)
input_value = LRLib.Fifo()

for item in parser.input_tokens:
    input_value.insert(item)

parsing_table = LRLib.generate_SLRTable(grammar)
if parsing_table:
    LRLib.print_parsing_table(parsing_table)
    LRLib.LRParsing(grammar,parsing_table,input_value)
"""


    # Especificar el nombre del archivo que deseas crear
    nombre_archivo = name+".py"

    # Abrir el archivo para escritura
    with open(nombre_archivo, 'w') as archivo:
        # Escribir el contenido al archivo
        archivo.write(contenido)

    print(f'Archivo {nombre_archivo} generado con exito.')
    
