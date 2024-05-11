#YalexLib.py

import AfdLib

class TokenId:
    genericId = "TOKEN1"

    def setId(self,_id=None):
        if _id is None:
            _id = TokenId.genericId
            TokenId.genericId = TokenId.genericId[:5]+str(int(TokenId.genericId[5:]) + 1)

        self._id = _id

    def setContent(self,content=""):
        self.content = content


class YalexRecognizer:
    #Son tomadas como espacio, tabulacion y salto de linea literal
    delim_regex = "\"\s\t\n\""
    letter = "'A'-'Z''a'-'z'"
    digit = "'0'-'9'"
    #Mejorable al considerar todos los caracteres ASCII
    especial_chars = "\",_+-.?!$~`|/:;=<>#^@%&\\\""
    parens = "\"()\""
    brackets = "\"\[\]\""
    curly_brackets = "\"{}\""
    open_curly_bracket = "\"{\""
    close_curly_bracket = "\"}\""
    #Unicamente con espace entre ''
    quotes = "'\'''\"'"
    backslash = "\"\\\""
    kleene = "\"*\""
    blank_space = "\"\s\""
    
    ws = f"[{delim_regex}]+"
    allLetter = f"{letter}\"ÁÉÍÓÚ\"\"áéíóú\""
    _id = f"[{letter}]([{letter}]|[{digit}])*"
    
    let = "let"
    rule = "rule"
    tokens = "tokens"
    equal = "="
    
    string = f"[{quotes}][{letter}{digit}{especial_chars}{brackets}{curly_brackets}{blank_space}{parens}{kleene}]+[{quotes}]"
    # char = f"[{quotes}][{letter}{digit}]+[{quotes}]"
    
    union = "[\"|\"]"
    action = f"[{open_curly_bracket}][{allLetter}{digit}{delim_regex}{especial_chars}{parens}{kleene}{brackets}{quotes}]*[{close_curly_bracket}]"

    
    comment_regex = f"\(\*[{allLetter}{digit}{delim_regex}{especial_chars}{kleene}{brackets}{quotes}]*\*\)"
    definition_regex = f"{let}{ws}{_id}{ws}{equal}{ws}[{allLetter}{digit}{especial_chars}{brackets}{quotes}{backslash}{blank_space}{parens}{kleene}]+"
    rule_regex = f"{rule}{ws}{_id}{ws}{equal}{ws}[{allLetter}{digit}{delim_regex}{especial_chars}{parens}{kleene}{brackets}{curly_brackets}{quotes}]+[{close_curly_bracket}]"
    
    def __init__(self):
        regex = [
            YalexRecognizer.comment_regex,      #0
            YalexRecognizer.definition_regex,   #1
            YalexRecognizer.rule_regex,         #2
            YalexRecognizer.ws,                 #3
            YalexRecognizer.let,                #4
            YalexRecognizer._id,                #5
            YalexRecognizer.equal,              #6
            YalexRecognizer.rule,               #7
            YalexRecognizer.tokens,             #8
            YalexRecognizer.string,             #9
            YalexRecognizer.union,              #10
            YalexRecognizer.action,             #11
            ]
        self.afds = []
        for item in regex:
            self.afds.append(AfdLib.createAFD(item+'■'))
            
        self.comments = []
        self.definitions = {}
        self.rule_tokens = {}
        self.actions = []

    def step_simulate_AFD(self,afd_pos,c,lookAhead):
        afd = self.afds[afd_pos]
        res = afd.step_simulation(c, lookAhead)
        state = list(res)[0] if len(list(res))>0 else None

        if state in afd.accept:
            return 0
        elif state in afd.states:
            return 1
        else:
            return 2
        
    def segmentRecognize(self,afd_pos,i,content):
        accept = (False,0,"")
        first = i
        # Bucle hasta que se alcance el final del contenido
        while i <= len(content):  # Asegura que haya espacio para lookAhead
            char = content[i] if i<len(content) else ""  # Carácter actual
            lookAhead = content[i + 1] if i<len(content)-1 else ""  # Carácter siguiente
        
            # Procesa el carácter aquí
            res =self.step_simulate_AFD(afd_pos, char, lookAhead)
            if res == 0:
                last = i+1
                accept = (True,last,content[first:last]) #Estado de aceptacion, ultima posicion de lookAhead, contenido aceptado
        
            elif res == 2:
                if accept[0]:
                    return accept
                else:
                    return (False,i,"")

            i += 1  # Incrementa la posición para el próximo carácter
        
    def definitionRecognize(self,content):
        # Inicializa la posición
        #print(content)
        definition = []
        first = 0
        while first<=len(content):
            #Longer sera utilizado para encontrar la primera aceptacion encontrada mas larga
            longer = [-1,len(content)+1,""] #Pos del AFD, Ultima posicion de lookAhead, contenido aceptado
            afdPos = [3,4,5,6]

            #Revisar entre los AFDs definidos en el yalexRecognizer
            for i in afdPos:
                res = self.segmentRecognize(i,first,content)
    
                if res[0]:
                    # print("ACEPTADO por " + str(i))
                    # print(res[2])
                    if len(res[2])>len(longer[2]):
                        longer[0] = i
                        longer[1] = res[1]
                        longer[2] = res[2]
                # else:
                #     print("NO ACEPTADO por " + str(i))
        
            if longer[0]==3: #ws
                pass
            elif longer[0]==4: #let
                pass
            elif longer[0]==5 and len(definition)==0: #id
                definition.append(longer[2])
            elif longer[0]==6: #eq
                pass
            else: #resto de la definicion
                definition.append(content[first:])
                break
                
            first = longer[1]
            #print(longer[0])
            #input("Presione [Enter] para continuar.")   
        
        self.definitions[definition[0]] = definition[1]
    
    def ruleRecognize(self,content):
        # Inicializa la posición
        #print(content)
        identifier = []
        first = 0
        while first<=len(content):
            #Longer sera utilizado para encontrar la primera aceptacion encontrada mas larga
            longer = [-1,len(content)+1,""] #Pos del AFD, Ultima posicion de lookAhead, contenido aceptado
            afdPos = [7,8,9,10,11,3,5,6,0]

            #Revisar entre los AFDs definidos en el yalexRecognizer
            for i in afdPos:
                res = self.segmentRecognize(i,first,content)
    
                if res[0]:
                    # print("ACEPTADO por " + str(i))
                    # print(res[2])
                    if len(res[2])>len(longer[2]):
                        longer[0] = i
                        longer[1] = res[1]
                        longer[2] = res[2]
                # else:
                #     print("NO ACEPTADO por " + str(i))
        
            if longer[0]==7: #rule
                pass
            elif longer[0]==8: #tokens
                pass
            elif longer[0]==9 or longer[0]==5: #char o string, id
                if len(identifier)>0:
                   self.rule_tokens[identifier.pop()] = ""
                   
                identifier.append(longer[2])
            elif longer[0]==10: #|
                pass
            elif longer[0]==11: #action
                if len(identifier)>0:
                    self.rule_tokens[identifier.pop()] = longer[2]
                else:
                    self.actions.append(longer[2])
            elif longer[0]==3: #ws
                pass
            elif longer[0]==6: #eq
                pass
            elif longer[0]==0: #Comentario
                self.comments.append(longer[2])
            else: #resto de la definicion
                break
                
            first = longer[1]
            #print(longer[0])
            #input("Presione [Enter] para continuar.")
    
        #Agregando identificadores o char/string sin return
        for item in identifier:
            self.rule_tokens[item] = ""

    def valueRecognize(self,new_afdPos,content):
        # Inicializa la posición
        # print(content)
        token_id = TokenId()
        new_content = ""
        first = 0
        change = True
        firstIteration = True

        while change:
            while first<=len(content):
                #Longer sera utilizado para encontrar la primera aceptacion encontrada mas larga
                longer = [-1,len(content)+1,""] #Pos del AFD, Ultima posicion de lookAhead, contenido aceptado
                afdPos = new_afdPos

                #Revisar entre los AFDs definidos en el yalexRecognizer
                for i in afdPos:
                    res = self.segmentRecognize(i,first,content)
    
                    if res[0]:
                        # print("ACEPTADO por " + str(i))
                        # print(res[2])
                        if len(res[2])>len(longer[2]):
                            longer[0] = i
                            longer[1] = res[1]
                            longer[2] = res[2]
                    # else:
                    #     print("NO ACEPTADO por " + str(i))
        
                if longer[0]==9: #String
                    if firstIteration:
                        token_id.setId()

                    new_content+=longer[2]
                    first = longer[1]
                
                elif longer[0]!=-1: #identificador
                    if firstIteration:
                        token_id.setId(longer[2])

                    new_content+=self.definitions[longer[2]]
                    first = longer[1]
                else: #No reconocido
                    if firstIteration:
                        print("ERROR al reconocer TOKEN " + content)
                        first = len(content)+1
                    else:
                        new_content+=content[first] if first<len(content) else ""
                        first+=1

                firstIteration = False
            
                # print(longer[0])
                # input("Presione [Enter] para continuar.")
        
            if content!=new_content:
                first=0
                content=new_content
                new_content=""
                # print("CONTENIDO: "+content)
            else:
                change = False
                token_id.setContent(new_content)
                # print("CONTENIDO: "+content)
            
        return token_id
    
    def yalexRecognize(self,yalexContent):
        # Inicializa la posición
        first = 0
        while first<=len(yalexContent):
            #Longer sera utilizado para encontrar la primera aceptacion encontrada mas larga
            longer = [-1,len(yalexContent)+1,""] #Pos del AFD, Ultima posicion de lookAhead, contenido aceptado
            afdPos = [0,1,2,3,11]
            longer_error = 0

            #Revisar entre los AFDs definidos en el yalexRecognizer
            for i in afdPos:
                res = self.segmentRecognize(i,first,yalexContent)
    
                if res[0]:
                    # print("ACEPTADO por " + str(i))
                    # print(res[2])
                    if len(res[2])>len(longer[2]):
                        longer[0] = i
                        longer[1] = res[1]
                        longer[2] = res[2]
                else:
                    if res[1]>longer_error:
                        longer_error = res[1]
                    # print("NO ACEPTADO por " + str(i))
    
            if longer[0]==0: #Comentario
                self.comments.append(longer[2])
            elif longer[0]==1: #Definicion
                self.definitionRecognize(longer[2])
            elif longer[0]==2: #Rule
                self.ruleRecognize(longer[2])
            elif longer[0]==3: #ws
                pass
            elif longer[0]==11: #action
                self.actions.append(longer[2])
            elif longer[0]==-1 and first!=len(yalexContent): #Error
                message = f"ERROR al reconocer archivo Yalex en caracter no. {longer_error+1}: "
                posicion = ' '*len(message)
                for item in yalexContent[first:longer_error]:
                    if item=='\n':
                        posicion+='\n'
                    elif item=='\t':
                        posicion+='\t'
                    else:
                        posicion+=' '
                        
                print(message+yalexContent[first:longer_error+1])
                print(posicion + '^')
                return False

            first = longer[1]
            # input("Presione [Enter] para continuar.")
            
        return True
            
            
    def get_comments(self):
        return self.comments
    
    def get_definitions(self):
        return self.definitions
    
    def get_rule_tokens(self):
        return self.rule_tokens
    
    def get_actions(self):
        return self.actions