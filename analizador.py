import re

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

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
        for linea in archivo:
            tokens = linea.split(",")

            t_simb = re.compile(r'[A-Z&|%]')
            t_dir = re.compile(r'[A-Za-z]+@$')

            if(bool(t_simb.match(tokens[0]))):
                 simbolos.write(tokens[0] +"\t" + tokens[1] + "\t0\t0\t0\t0\t" + ambito + "\n")
                 nlineas += 1
            elif(bool(t_dir.match(tokens[0]))):
                direcciones.write(tokens[0] + "\t" + tokens[1] + "\t" + tokens[3] + "\t0" + "\n")
                nlineas += 1
                ambito = tokens[0]
        print("Archivos generados correctamente")
            
except FileNotFoundError:
    print("Archivo no encontrado/seleccionado")
