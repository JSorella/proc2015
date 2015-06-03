from PIL import Image

import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
import os


def filtroGrisesPromedio(imagen):
	x, y = imagen.shape
	px = imagen.load()
	imagenGrises = Image.new('RGB',(x,y))
	for i in range(0, x):
		for j in range(0, y):
			pixeles = px[i,j]
			prom = sum(pixeles) / 3
			imagenGrises.putpixel((i,j),(prom,prom,prom))
	return imagenGrises

def abrirImagen(ruta):
	return np.asarray(Image.open(ruta).convert(mode='L'))

def mostrarMatrizComoImagen(matriz, nroFigura):
	plt.figure(nroFigura)
	plt.imshow(matriz, cmap=plt.cm.gray)

def errorCuadraticoPuntoAPunto(matriz1, matriz2):
	suma = 0
	matriz3 = (matriz1 - matriz2)*(matriz1 - matriz2)
	
	return matriz3

def errorCuadraticoMedio(matriz1, matriz2):
	suma = 0
	m3 = errorCuadraticoPuntoAPunto(matriz1, matriz2)
	suma = np.sum(m3)
	return suma/m3.size

def espectroMatriz(matr, nroFigura):
	freq = np.fft.fft2(matr)
	plt.figure(nroFigura)
	plt.hist(np.log(freq).ravel(), bins=100)

def generarMatriz(imagen):
	x, y = imagen.shape
	p = imagen
	matriz = list()
	for j in range(0,y):
		fila = list()
		for i in range(0,x):
			fila.append(p[i,j])
		matriz.append(fila)
	n_array = np.array(matriz)
	return n_array
 
