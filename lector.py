import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

with open(file_path, "r") as archivoEntrada:
    linea = archivoEntrada.readline()
    nlineas = 0

    while linea:
        nlineas += 1
        linea = archivoEntrada.readline()

print("Numero de lineas: " + str(nlineas))

# Nota: La clase "File" y "FileReader" no son necesarias en Python
# ya que se puede abrir el archivo directamente con la
# función "open". También es importante cerrar el archivo
# después de leerlo, lo cual se hace usando el método "close".
# En Python, la condición "while(linea != null)" se cambia
# por "while linea", ya que Python considera una cadena
# vacía como False y una cadena no vacía como True.
# Además, la función "readLine()" se convierte en "readline()"
# en Python. Por último, el operador "+" se usa para
# concatenar cadenas en Python, y se debe convertir
# nlineas a una cadena antes de concatenarlo con la cadena
# de texto usando la función "str()".
