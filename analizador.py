import re
from Tokens import Tokens


from tkinter import filedialog

def checkToken(Tokens):
    ids = re.compile(r'[a-zA-Z][a-zA-Z0-9]*&|[a-zA-Z][a-zA-Z0-9]*%')
    proc = re.compile(r'[a-zA-Z][A-Za-z0-9]+@$')
    constante = re.compile(r'[0-9]+')
    operador = re.compile(r'[+\-*\/%<>=!&|]+')
    pyc = re.compile(r'[;]')

    if(bool(ids.match(Tokens.lexema))):
        tokenType = "simbolo"
        print("Símbolo ", Tokens.lexema)
    elif(bool(proc.match(Tokens.lexema))):
        tokenType = "procedimiento"
        print("Procedimiento ", Tokens.lexema)
    elif(bool(constante.match(Tokens.lexema))):
        tokenType = "constante"
    elif(bool(operador.match(Tokens.lexema))):
        tokenType = "operador"
    elif(bool(pyc.match(Tokens.lexema))):
        tokenType = "PyC"
    else:
        tokenType = "NULL"

    return tokenType


file_path = filedialog.askopenfilename()

try:
    with open(file_path, "r+") as archivo, open("simbolos.txt", "w") as simbolos, open("direcciones.txt", "w") as direcciones:
        simbolos.write("TABLA DE SÍMBOLOS \n")
        simbolos.write("ID\tTOKEN\tVALOR\tD1\tD2\tPRT\tAMBITO\n")
        simbolos.write("---\t---\t---\t---\t---\t---\t---\n")

        direcciones.write("TABLA DE DIRECCIONES \n")
        direcciones.write("ID\tTOKEN\tLINEA\tVCI \n")
        direcciones.write("---\t---\t---\t---\n")

        nlineas = 0
        simbolos_dic = {} #Arreglo para almacenar los simbolos
        
        prioridades = {'*':60, '/':60, '%':60, '+': 50, '-': 50, '<': 40, '>': 40, '<=':40,
                       '>=':40, '==':40, '!=':40, '!': 30, '&&': 20, '||': 10, '=': 0}
        vci = []
        pilaDirecciones = []
        pilaOperadores = []
        pilaEstatutos = []

        for linea in archivo:
            linea = linea.strip() + ','
            tabla_tokens = linea.split(",")
            try:
                specificToken = Tokens(tabla_tokens[0], tabla_tokens[1], tabla_tokens[2], tabla_tokens[3])

                tokenType = checkToken(specificToken)
            except IndexError:
                print("El error está en", tabla_tokens[0])

            if(tokenType == "simbolo"):
                if tabla_tokens[0] not in simbolos_dic or simbolos_dic[tabla_tokens[0]] != ambito:
                    simbolos_dic[tabla_tokens[0]] = ambito
                    simbolos.write(tabla_tokens[0] +"\t" + tabla_tokens[1] + "\t0\t0\t0\t0\t" + ambito + "\n")
                    nlineas += 1

            elif(tokenType == "procedimiento"):
                direcciones.write(tabla_tokens[0] + "\t" + tabla_tokens[1] + "\t" + tabla_tokens[3] + "\t0" + "\n")
                nlineas += 1
                ambito = tabla_tokens[0]

            # Si el token es una constante, o bien, un ID; entra directamente al VCI
            if(tokenType == "constante" or tokenType == "simbolo"):
                vci.append(tabla_tokens[0])

            # Si el token es un operador, entra a la pila de operadores
            if(tokenType == "operador"):
                try:
                    #Tope de la pila
                    peek = pilaOperadores[-1]
                    peekPriority = prioridades.get(peek)
                    #Operador encontrado en la tabla de tokens
                    operador = tabla_tokens[0]
                    operadorPriority = prioridades.get(operador)
                    
                    if(operadorPriority > peekPriority):
                        pilaOperadores.append(tabla_tokens[0])
                    else:
                        while(operadorPriority <= peekPriority):
                            top = pilaOperadores.pop()
                            vci.append(top)

                            peek = pilaOperadores[-1]
                            peekPriority = prioridades.get(peek)
                            operador = tabla_tokens[0]
                            operadorPriority = prioridades.get(operador)

                        pilaOperadores.append(tabla_tokens[0])
                except IndexError:
                    pilaOperadores.append(tabla_tokens[0])

                # Si el token es un ;, se vacía la pila de operadores
            if(tokenType == "PyC"):  
                while(pilaOperadores):
                            top = pilaOperadores.pop()
                            vci.append(top)
            
        print("Archivos generados correctamente")

        print(vci)
        print(pilaOperadores)

            
except FileNotFoundError:
    print("Archivo no encontrado/seleccionado")



    


