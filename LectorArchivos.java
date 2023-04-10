/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package lectorarchivos;

import java.io.*;
/**
 *
 * @author Chetx
 */
public class LectorArchivos {

    public static void main(String [] args) throws FileNotFoundException, IOException
	{
		File archivoEntrada = new File("C:\\Users\\js98v\\Desktop\\archivo.txt");
		FileReader lectorArchivo = new FileReader(archivoEntrada);
		BufferedReader buferLectura = new BufferedReader(lectorArchivo);
		int nlineas = 0;
		String linea = "";
		while(linea != null)
		{
			linea = buferLectura.readLine();
			if(linea != null)
			{
				nlineas++;
			}
		}
		buferLectura.close();
                System.out.println("Numero de lineas: "+nlineas);
	}
}
