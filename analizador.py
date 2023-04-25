import re

from tkinter import filedialog

file_path = filedialog.askopenfilename()

try:
    with open(file_path, "r") as archivo, open("simbolos.txt", "w") as simbolos, open("direcciones.txt", "w") as direcciones:
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
        direcciones_VCI = []
        operadores_VCI = []
        estatutos_VCI = []

        for linea in archivo:
            tokens = linea.split(",")

            t_simb = re.compile(r'[A-Z&|%]')
            t_dir = re.compile(r'[A-Za-z]+@$')
            constante = re.compile(r'[0-9]+')
            operador = re.compile(r'[+\-*\/%<>=!&|]++')

            if(bool(t_simb.match(tokens[0]))):
                if tokens[0] not in simbolos_dic or simbolos_dic[tokens[0]] != ambito:
                    simbolos_dic[tokens[0]] = ambito
                    simbolos.write(tokens[0] +"\t" + tokens[1] + "\t0\t0\t0\t0\t" + ambito + "\n")
                    nlineas += 1

            elif(bool(t_dir.match(tokens[0]))):
                direcciones.write(tokens[0] + "\t" + tokens[1] + "\t" + tokens[3] + "\t0" + "\n")
                nlineas += 1
                ambito = tokens[0]

            # Si el token es una constante, o bien, un ID; entra directamente al VCI
            if(bool(t_simb.match(tokens[0])) or bool(constante.match(tokens[0]))):
                vci.append(tokens[0])
                
            # Si el token es un operador, entra a la pila de operadores
            if(bool(operador.match(tokens[0]))):
                try:
                    peek = operadores_VCI[-1]
                    value = prioridades[peek].values()
                    if():
                        print(peek)
                except:
                    operadores_VCI.append(tokens[0])             
                
        print("Archivos generados correctamente")

        print(vci)
        #print(operadores_VCI)

            
except FileNotFoundError:
    print("Archivo no encontrado/seleccionado")


