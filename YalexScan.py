#Scan.py
# Este es un archivo Python generado automaticamente
import pickle

grammar = dict()
yapar_tokens = set()

            
def step_simulate_AFD(afd,c,lookAhead):
    res = afd.step_simulation(c, lookAhead)
    state = list(res)[0] if len(list(res))>0 else None

    if state in afd.accept:
        return (0,state.action)
    elif state in afd.states:
        return (1,"")
    else:
        return (2,"")
            
def segmentRecognize(afd,i,content):
    accept = (False,0,"")
    first = i
    # Bucle hasta que se alcance el final del contenido
    while i <= len(content):  # Asegura que haya espacio para lookAhead
        char = content[i] if i<len(content) else ""  # Caracter actual
        lookAhead = content[i + 1] if i<len(content)-1 else ""  # Caracter siguiente
        
        # Procesa el caracter aqui
        res = step_simulate_AFD(afd, char, lookAhead)
        if res[0] == 0:
            last = i+1
            accept = (True,last,content[first:last],res[1]) #Estado de aceptacion, ultima posicion de lookAhead, contenido aceptado, accion
        
        elif res[0] == 2:
            if accept[0]:
                return accept
            else:
                return (False,i,"","")

        i += 1  # Incrementa la posicion para el proximo caracter
        
def genericFunction(value,content):
    local_namespace = {}
    local_namespace['value'] = value

    codigo_funcion = f'def tempFunction(value):\n'
    if len(content)>0:
        for linea in content.split('\n'):
            codigo_funcion += f'    {linea}\n'
    else:
        codigo_funcion += f'    return None\n'
        
    codigo_funcion += 'resultado = tempFunction(value)'
    
    try:
        # Ejecuta la definicion de la funcion y luego la llama
        exec(codigo_funcion, globals(), local_namespace)

        # Devuelve el resultado de la funcion
        return local_namespace['resultado']
        
    except Exception as e:
        print(f"Error al ejecutar el codigo: {e}")
        return None
            
def tokensRecognize(afd,txtContent):
    # Inicializa la posicion
    first = 0
    while first<=len(txtContent):
        res = segmentRecognize(afd,first,txtContent)
        nextFirst = res[1]
        
        if res[0]:
            print(">> ACEPTADO <<")
            print(res[2])
            resultado = genericFunction(res[2],res[3][1:-1])
            resultado = resultado if resultado!=None else ""
            print(resultado)
        elif not res[0] and first!=len(txtContent):
            message = f"-- ERROR LEXICO -- al reconocer archivo txt en caracter no. {res[1]+1}: "
            posicion = ' '*len(message)
            for item in txtContent[first:res[1]]:
                if item=='\n':
                    posicion+='\n'
                elif item=='\t':
                    posicion+='\t'
                else:
                    posicion+=' '
                    
            nextFirst+=1
            print(message+txtContent[first:nextFirst])
            print(posicion + '^')
            
        else:
            nextFirst+=1

        first = nextFirst

#Lectura del objeto pkl
with open('yalex.pkl', 'rb') as archivo_entrada:
    afd = pickle.load(archivo_entrada)

document = input("Ingrese el nombre del archivo a escanear: ")                
#Lectura del documento txt
with open(document, 'r', encoding='utf-8') as file:
    txtContent = file.read()  # Leer todo el contenido del archivo
        
tokensRecognize(afd,txtContent)

with open('grammar.pkl', 'wb') as archivo_salida:
        # Serializamos el diccionario y lo guardamos en el archivo
        pickle.dump(grammar, archivo_salida)

