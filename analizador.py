import re
from Tokens import Tokens


from tkinter import filedialog

def obtener_clave_por_valor(diccionario, valor):
    for clave, v in diccionario.items():
        if v == valor:
            return clave
    return None  # Valor no encontrado en el diccionario

def checkToken(Tokens):
    ids = re.compile(r'[a-zA-Z][a-zA-Z0-9]*&|[a-zA-Z][a-zA-Z0-9]*%|[a-zA-Z][a-zA-Z0-9]*\$')
    proced = re.compile(r'[a-zA-Z][A-Za-z0-9]*@')
    constante = re.compile(r'[0-9]+')
    operador = re.compile(r'[+\-*\/%<>=!&|]+')
    pyc = re.compile(r'[;]')
    declaracion =  re.compile(r'[var]')
    inicio =  re.compile(r'[inicio]')
    fin =  re.compile(r'[fin]')
    si =  re.compile(r'[si]')
    sino =  re.compile(r'[sino]')
    pF =  re.compile(r'[)]')
    lF =  re.compile(r'[}]')

    if(bool(ids.match(Tokens.lexema))):
        tokenType = "simbolo"
        #print("Símbolo ", Tokens.lexema)
    elif(bool(proced.match(Tokens.lexema))):
        tokenType = "procedimiento"
    elif(bool(constante.match(Tokens.lexema))):
        tokenType = "constante"
    elif(bool(operador.match(Tokens.lexema))):
        tokenType = "operador"
    elif(bool(pyc.match(Tokens.lexema))):
        tokenType = "PyC"
    elif(bool(declaracion.match(Tokens.lexema))):
        tokenType = "var"
    elif(bool(inicio.match(Tokens.lexema))):
        tokenType = "inicio"
    elif(bool(fin.match(Tokens.lexema))):
        tokenType = "fin"
    elif(bool(si.match(Tokens.lexema))):
        tokenType = "si"
    elif(bool(si.match(Tokens.lexema))):
        tokenType = "sino"
    elif(bool(pF.match(Tokens.lexema))):
        tokenType = "parentesisFinal"
    elif(bool(lF.match(Tokens.lexema))):
        tokenType = "llaveFinal"
    else:
        tokenType = "Ignored"

    return tokenType
    
file_path = filedialog.askopenfilename()

try:
    with open(file_path, "r+") as archivo, open("simbolos.txt", "w") as simbolos, open("direcciones.txt", "w") as direcciones, open("vci.txt", "w") as vci_txt:
        simbolos.write("TABLA DE SÍMBOLOS \n")
        simbolos.write("ID\tTOKEN\tVALOR\tD1\tD2\tPRT\tAMBITO\n")
        simbolos.write("---\t---\t---\t---\t---\t---\t---\n")

        direcciones.write("TABLA DE DIRECCIONES \n")
        direcciones.write("ID\tTOKEN\tLINEA\tVCI \n")
        direcciones.write("---\t---\t---\t---\n")

        nlineas = 0
        simbolos_dimension = {}
        simbolos_repeticion = [] #Arreglo para almacenar los símbolos y verificar que no existan repetidos
        simbolos_dic = {} #Arreglo para almacenar los simbolos con sus ambitos
        direcciones_dic = [] #Arreglo para almacenar los direcciones
        
        prioridades = {'*':60, '/':60, '%':60, '+': 50, '-': 50, '<': 40, '>': 40, '<=':40,
                       '>=':40, '==':40, '!=':40, '!': 30, '&&': 20, '||': 10, '=': 0}
        vci = {}
        pilaDirecciones = []
        pilaOperadores = []
        pilaEstatutos = []

        inicioVar = 0
        finVar = 0
        contFin = 0
        contInicio = 0
        inicio = 0
        fin = 0
        inicioIf = 0
        inicioElse = 0
        posicionVCI = 31

        linea_actual = archivo.readline().strip()

        #Mientras nos encontremos en la línea actual
        while linea_actual:
            #Se lee la línea siguiente
            linea_siguiente = archivo.readline().strip()
            linea_actual = linea_actual.strip() + ','
            tabla_tokens = linea_actual.split(",")
            siguiente_token = linea_siguiente.split(",")
            try:
                specificToken = Tokens(tabla_tokens[0], tabla_tokens[1], tabla_tokens[2], tabla_tokens[3])

                tokenType = checkToken(specificToken)
            except IndexError:
                print("El error está en", tabla_tokens)

            if(tokenType == "simbolo" and inicioVar == 1):
                try:
                    variableN = tabla_tokens[0][:-1]
                    if(variableN in simbolos_repeticion and simbolos_dic[variableN] == ambito):
                        print("ERROR: VARIABLE", tabla_tokens[0] ,"REPETIDA EN LINEA", tabla_tokens[3], "AMBITO:", simbolos_dic[variableN])
                    else:
                        simbolos_dic[tabla_tokens[0][:-1]] = ambito

                        if siguiente_token[0] == "[":
                            dimensiones = archivo.readline().strip()
                            dimensiones_token = dimensiones.split(",")
                            d1 = dimensiones_token[0]
                            siguiente_token = archivo.readline().strip()

                            if siguiente_token[0] == ",":
                                dimensiones = archivo.readline().strip()
                                dimensiones_token = dimensiones.split(",")
                                d2 = dimensiones_token[0]
                                simbolos.write(tabla_tokens[0] +"\t" + tabla_tokens[1] + "\t0\t" + d1 + "\t" + d2 +"\t0\t" + ambito + "\n")

                                simbolos_dimension[tabla_tokens[0]] = 2
                            else:
                                simbolos.write(tabla_tokens[0] +"\t" + tabla_tokens[1] + "\t0\t" + d1 + "\t0\t0\t" + ambito + "\n")
                                simbolos_dimension[tabla_tokens[0]] = 1         
                        else: 
                            simbolos.write(tabla_tokens[0] +"\t" + tabla_tokens[1] + "\t0\t0\t0\t0\t" + ambito + "\n")
                            simbolos_dimension[tabla_tokens[0]] = 0

                        simbolos_repeticion.append(tabla_tokens[0][:-1])
                except NameError:
                    print("El error está en el " + tabla_tokens[0] +" "+ tabla_tokens[1]+" "+ tabla_tokens[2])

            elif(tokenType == "procedimiento"):
                if tabla_tokens[0] not in direcciones_dic:
                    ambito = tabla_tokens[0]
                    direcciones_dic.append(tabla_tokens[0])
                    direcciones.write(tabla_tokens[0] + "\t" + tabla_tokens[1] + "\t" + tabla_tokens[3] + "\t0" + "\n")
                    nlineas += 1

            #semantica(tabla_tokens, siguiente_token, inicio, simbolos_dimension)

            #Si el token es una constante, o bien, un ID; entra directamente al VCI
            if((tokenType == "constante" or tokenType == "simbolo") and inicio == 1):
                if(tabla_tokens[0][:-1] not in simbolos_dic and tokenType == "simbolo"):
                    print("ERROR: VARIABLE", tabla_tokens[0] ,"NO DECLARADA EN LINEA", tabla_tokens[3])
                else:
                    vci[posicionVCI] = tabla_tokens[:-1]
                    posicionVCI += 1
                    #vci.append(tabla_tokens[:-1])
                    vci_txt.write(str(obtener_clave_por_valor(vci, tabla_tokens[:-1])) + ": ")
                    for token in tabla_tokens:
                        vci_txt.write(token + "\t")
                    vci_txt.write("\n")    

            # Si el token es un operador, entra a la pila de operadores
            elif(tokenType == "operador" and inicio == 1):
                try:
                    #Tope de la pila
                    peek = pilaOperadores[-1]
                    peekPriority = prioridades.get(peek[0])
                    #Operador encontrado en la tabla de tokens
                    operador = tabla_tokens
                    operadorPriority = prioridades.get(operador[0])
                    
                    if(operadorPriority > peekPriority):
                        pilaOperadores.append(tabla_tokens)
                    else:
                        while(operadorPriority <= peekPriority):
                            top = pilaOperadores.pop()
                            vci[posicionVCI] = top
                            posicionVCI += 1
                            #vci.append(top)
                            vci_txt.write(str(obtener_clave_por_valor(vci, top)) + ": ")
                            for token in top:
                                vci_txt.write(token + "\t")
                            vci_txt.write("\n") 

                            peek = pilaOperadores[:-1]
                            print(peek)
                            peekPriority = prioridades.get(peek[0])
                            operador = tabla_tokens
                            operadorPriority = prioridades.get(operador[0])

                        pilaOperadores.append(tabla_tokens)
                except IndexError:
                    pilaOperadores.append(tabla_tokens)

            # Si el token es un ;, se vacía la pila de operadores
            elif(tokenType == "PyC"):  
                if(inicio == 1):
                    while(pilaOperadores):
                        top = pilaOperadores.pop()
                        vci[posicionVCI] = top[:-1]
                        posicionVCI += 1
                        #vci.append(top[:-1])
                        vci_txt.write(str(obtener_clave_por_valor(vci, top[:-1])) + ": ")
                        for token in top[:-1]:
                            vci_txt.write(token + "\t")
                        vci_txt.write("\n")  
                
                if(inicioVar == 1):
                    finVar = 1
                    inicioVar = 0
            
            #Si el token es 'var', da el inicio a declaración de varibales
            elif(tokenType == "var"):
                inicioVar = 1;
        
            elif(tokenType == "inicio"):
                contInicio =+ 1
                inicio = 1

            elif(tokenType == "fin"):
                contFin =+ 1
                fin = 1
            
            elif(tokenType == "si"):
                inicioIf = 1
                pilaEstatutos.append(tabla_tokens)
                        
            elif(tokenType == "parentesisFinal" and inicioIf == 1):
                while(pilaOperadores):
                    top = pilaOperadores.pop()
                    vci[posicionVCI] = top[:-1]
                    posicionVCI += 1
                    #vci.append(top[:-1])
                    vci_txt.write(str(obtener_clave_por_valor(vci, top[:-1])) + ": ")
                    for token in top[:-1]:
                        vci_txt.write(token + "\t")
                    vci_txt.write("\n")  
                vci[posicionVCI] = "Vacio\t0\t0\t0"
                pilaDirecciones.append(obtener_clave_por_valor(vci, "Vacio\t0\t0\t0"))
                print(pilaDirecciones)
                posicionVCI += 1
                #vci.append("Vacio\t0\t0\t0")
                #vci_txt.write("Vacio\t0\t0\t0\n")
                #pilaDirecciones.append(vci[])
                vci[posicionVCI] = "si\t0\t0\t0"
                vci_txt.write(str(obtener_clave_por_valor(vci, "si\t0\t0\t0")) + ": ")
                posicionVCI += 1
                #vci.append("si\t0\t0\t0")
                vci_txt.write("si\t0\t0\t0\n")
            
            elif(tokenType == "llaveFinal" and inicioIf == 1):
                pilaEstatutos.pop()
                inicioIf = 0
                if inicioElse == 0:
                    inicioElse = 1
                    direccion = pilaDirecciones.pop()
                    vci[direccion] = posicionVCI + 2
                    n_pos = posicionVCI + 2
                    vci_txt.write(str(n_pos)+"\t0\t0\t0\n")
                    pilaEstatutos.append(tabla_tokens)
                    while pilaOperadores:
                        top = pilaOperadores.pop()
                        vci[posicionVCI] = top[:-1]
                        posicionVCI += 1
                        #vci.append(top[:-1])
                        vci_txt.write(str(obtener_clave_por_valor(vci, top[:-1])) + ": ")
                        for token in top[:-1]:
                            vci_txt.write(token + "\t")
                        vci_txt.write("\n")
                    vci[posicionVCI] = "Vacio\t0\t0\t0"
                    posicionVCI += 1
                    #vci_txt.write("Vacio\t0\t0\t0\n")
                    vci[posicionVCI] = "sino\t0\t0\t0"
                    posicionVCI += 1
                    vci_txt.write(str(obtener_clave_por_valor(vci, "sino\t0\t0\t0")) + ": ")
                    vci_txt.write("sino\t0\t0\t0\n")
                    pilaEstatutos.pop()
                

            elif(tokenType == "llaveFinal" and inicioElse == 0):
                pilaEstatutos.pop()
                inicioElse = 0    
                direccion = pilaDirecciones.pop()
                vci[direccion] = posicionVCI
                vci_txt.write(str(posicionVCI)+"\t0\t0\t0\n")
                
            # procesar linea_actual y linea_siguiente aquí
            linea_actual = linea_siguiente

        print("Archivos generados correctamente")

        if(contInicio != contFin):
            print("ESTATUTO/ESTRUCTURA MAL TERMINADA. HACE FALTA UN INICIO/FIN")
        
        
        #for lineaV in vci:
         #   print(lineaV)
        # print ("\t Pila estatutos",pilaEstatutos)
        #print(simbolos_dimension)
        #print(pilaOperadores)
        #print(simbolos_dic)
        #print(simbolos_repeticion)
            
except FileNotFoundError:
    print("Archivo no encontrado/seleccionado")