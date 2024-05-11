#ScanGenerator.py

from graphviz import Digraph
from YalexLib import YalexRecognizer
import AfdLib
import AfLib
import AstLib
import RegexLib
from AstLib import Node

import pickle

def generateLexer(pklName,file_path):
    definitions_id = []
    tokens_regex = []
    yalex_tokens = []
        
    yalexRecognizer = YalexRecognizer()

    #Lectura del documento yalex
    with open(file_path, 'r', encoding='utf-8') as file:
        yalexContent = file.read()  # Leer todo el contenido del archivo
    
    if yalexRecognizer.yalexRecognize(yalexContent):
        # print(yalexRecognizer.get_comments())
        # print('\n')
        # print(yalexRecognizer.get_definitions())
        # print('\n')
        # print(yalexRecognizer.get_rule_tokens())
        # print('\n')
        # print(yalexRecognizer.get_actions())
        # print('\n')
    

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

        # k=1
        # for item in tokens_regex:
        #     # subafd = afdLib.createAFD(item)
        #     # subafd_graph = afLib.plot_af(subafd.start)
        #     # nombre_archivo_pdf = 'AFD '+str(k)
        #     # subafd_graph.view(filename=nombre_archivo_pdf,cleanup=True)
        #     postfix = regexLib.shunting_yard(item)
            
        #     #Construccion AST
        #     ast_root = astLib.create_ast(postfix)
        #     ast_graph = astLib.plot_tree(ast_root)
        #     nombre_archivo_pdf = 'Subarbol de Expresion '+str(k)
        #     ast_graph.view(filename=nombre_archivo_pdf,cleanup=True)
        #     k+=1

        lexer = '|'.join(tokens_regex)
        lexer = '('+lexer+')'

        # print(lexer)
        # print('\n')
            
        #Construccion AFD
        afd = AfdLib.createLexerAFD(lexer,yalexRecognizer.get_rule_tokens())
        afd.yalex_tokens = set(yalex_tokens)
        # afd_graph = AfLib.plot_af(afd.start)
        # nombre_archivo_pdf = 'AFD'
        # afd_graph.view(filename=nombre_archivo_pdf,cleanup=True)

        # #Construccion de postfix
        # postfix = regexLib.shunting_yard(lexer)
            
        # #Construccion AST
        # ast_root = astLib.create_ast(postfix)
        # ast_graph = astLib.plot_tree(ast_root)
        # nombre_archivo_pdf = 'Arbol de expresion'
        # ast_graph.view(filename=nombre_archivo_pdf,cleanup=True)
    
        # Abrimos un archivo en modo binario de escritura
        with open(pklName, 'wb') as archivo_salida:
            # Serializamos el objeto y lo guardamos en el archivo
            pickle.dump(afd, archivo_salida)
            
        return yalexRecognizer
    else:
        return None