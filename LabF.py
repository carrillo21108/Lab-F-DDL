import LRLib
import pickle

# grammar = {
#     'E':["E + T",'T'],
#     'T':["T * F",'F'],
#     'F':['( E )','id']
# }

with open('grammar.pkl', 'rb') as archivo_entrada:
        grammar = pickle.load(archivo_entrada)
        
grammar = LRLib.augment_grammar(grammar)

text = "id times id plus id"
input_value = LRLib.Fifo()

for item in text.split(' '):
    input_value.insert(item)

parsing_table = LRLib.generate_SLRTable(grammar)    
LRLib.LRParsing(grammar,parsing_table,input_value)
    
