from PIL import Image

import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
import os

def abrirImagen(ruta):
	return np.asarray(Image.open(ruta).convert(mode='L'))

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

def load(fn):
  return np.asarray(Image.open(fn).convert(mode='L'))

def save(fn, img):
  assert img.dtype == np.uint8
  Image.fromarray(img).save(fn)
  print 'wrote', fn


# ------ graphics-related code: ------

def to_float(img, gamma=2.2):
  """
  Convert uint8 image to linear floating point values.
  """
  return np.power(img.astype(float) / 255, gamma)

def from_float(img, gamma=2.2):
  """
  Convert from floating point, doing gamma conversion and 0,255 saturation,
  into a byte array.
  """
  out = np.power(img.astype(float), 1.0 / gamma)
  out = np.round(out * 255).clip(0, 255)
  return out.astype(np.uint8)

def bipolar(img):
  """
  Negative values are red, positive blue, and zero is black.
  """
  h,w = img.shape
  img = img.copy()
  img /= np.abs(img).max()
  out = np.zeros((h, w, 3), dtype=float)
  a = .005
  b = 1. - a
  c = .5
  out[:,:,0] = np.where(img < 0, a + b * np.power(img / (img.min() - 0.001), c), 0)
  out[:,:,2] = np.where(img > 0, a + b * np.power(img / (img.max() + 0.001), c), 0)
  return from_float(out)
 
def keep_ratio(a, ratio):
  """
  Keep only the strongest values.
  """
  magnitude = sorted(np.abs(a.flatten()))
  idx = int((len(magnitude) - 1) * (1. - ratio))
  return np.where(np.abs(a) > magnitude[idx], a, 0)
