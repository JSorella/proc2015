#!/usr/bin/env python
"""
Programa principal
"""

import numpy as np
import helper as f
import haar
import dcst
import matplotlib.pyplot as plt


def main():
  # Cargamos las imagenes
  img = f.to_float(f.load('../media/lena.png'))

  # Calculamos los coeficientes segun algortimo
  fftCoeffs = np.fft.fft2(img)
  haarCoeffs = haar.haar_2d(img)
  dctCoeffs = dcst.dct2(img)

  # Recortamos los valores despreciables
  strongFftCoeffs =  f.keep_ratio(fftCoeffs, .5)
  strongHaarCoeffs = f.keep_ratio(haarCoeffs, .5)
  strongDctCoeffs = f.keep_ratio(dctCoeffs, .5)
  
  # Antitransformamos y creamos las imagenes a partir de los coeficientes recortados
  lossyFft = np.fft.ifft2(strongFftCoeffs)
  lossyHaar = haar.ihaar_2d(strongHaarCoeffs)
  lossyDct = dcst.idct2(strongDctCoeffs)

  # Creamos las matrices a partir de imagenes
  originalMatrix = f.generarMatriz(img)
  fftMatrix = f.generarMatriz(lossyFft)
  haarMatrix = f.generarMatriz(lossyHaar)
  dctMatrix = f.generarMatriz(lossyDct)

  # Calculamos e informamos los errores cuatraticos medios
  print "ERROR CUADRATICO MEDIO"
  print "Diferencia entre FFT y original: ", f.errorCuadraticoMedio(fftMatrix,originalMatrix)
  print "Diferencia entre Haar y original: ", f.errorCuadraticoMedio(haarMatrix,originalMatrix)
  print "Diferencia entre DCT y original: ", f.errorCuadraticoMedio(dctMatrix,originalMatrix)

  # Guardamos las imagenes comprimidas
  f.save('../media/fft.png', f.from_float(lossyFft))
  f.save('../media/haar.png', f.from_float(lossyHaar))
  f.save('../media/dct.png', f.from_float(lossyDct))
  # Guardamos las imagenes con los coeficientes  
  f.save('../media/fft-coeff.png', f.bipolar(fftCoeffs))
  f.save('../media/fft-coeff-recortado.png', f.bipolar(strongFftCoeffs))
  f.save('../media/haar-coeff.png', f.bipolar(haarCoeffs))
  f.save('../media/haar-coeff-recortado.png', f.bipolar(strongHaarCoeffs))
  f.save('../media/dct-coeff.png', f.bipolar(dctCoeffs))
  f.save('../media/dct-coeff-recortado.png', f.bipolar(strongDctCoeffs))

  # Ploteamos las imagenes resultantes en pantalla, junto a sus histogramas
  f.mostrarMatrizComoImagen(f.errorCuadraticoPuntoAPunto(f.to_float(fftMatrix), originalMatrix), 1)
  f.mostrarMatrizComoImagen(f.errorCuadraticoPuntoAPunto(haarMatrix, originalMatrix), 2)
  f.mostrarMatrizComoImagen(f.errorCuadraticoPuntoAPunto(dctMatrix, originalMatrix), 3)
  f.espectroMatriz(f.errorCuadraticoPuntoAPunto(fftMatrix, originalMatrix), 4)
  f.espectroMatriz(f.errorCuadraticoPuntoAPunto(haarMatrix, originalMatrix), 5)
  f.espectroMatriz(f.errorCuadraticoPuntoAPunto(dctMatrix, originalMatrix), 6)

  plt.show()

if __name__ == '__main__':
  main()
