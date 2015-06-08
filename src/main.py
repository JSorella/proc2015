#!/usr/bin/env python
"""
Programa principal
"""

import numpy as np
import helper as f
import haar
import matplotlib.pyplot as plt


def main():
  # Cargamos las imagenes
  img = f.to_float(f.load('../media/lena.png'))

  # Calculamos los coeficientes segun algortimo
  fftCoeffs = np.fft.fft2(img)
  haarCoeffs = haar.haar_2d(img)

  # Recortamos los valores despreciables
  strongFftCoeffs =  f.keep_ratio(fftCoeffs, .5)
  strongHaarCoeffs = f.keep_ratio(haarCoeffs, .5)
  
  # Antitransformamos y creamos las imagenes a partir de los coeficientes recortados
  lossyFft = np.fft.ifft2(strongFftCoeffs)
  lossyHaar = haar.ihaar_2d(strongHaarCoeffs)

  # Creamos las matrices a partir de imagenes
  mif = f.generarMatriz(img)
  mlf = f.generarMatriz(lossyFft)
  ml = f.generarMatriz(lossyHaar)

  # Calculamos e informamos los errores cuatraticos medios
  print "ERROR CUADRATICO MEDIO"
  print "Diferencia entre FFT y original: ", f.errorCuadraticoMedio(mlf,mif)
  print "Diferencia entre Haar y original: ", f.errorCuadraticoMedio(ml,mif)

  # Guardamos las imagenes
  f.save('../media/Haar-coeff.png', f.bipolar(haarCoeffs))
  f.save('../media/Haar-coeff-Recortado.png', f.bipolar(strongHaarCoeffs))
  f.save('../media/fft-coeff.png', f.bipolar(fftCoeffs))
  f.save('../media/fft-coeff-Recortado.png', f.bipolar(strongFftCoeffs))
  f.save('../media/Haar-output.png', f.from_float(lossyHaar))
  f.save('../media/FFT-output.png', f.from_float(lossyFft))

  # Ploteamos las imagenes resultantes en pantalla, junto a sus histogramas
  f.mostrarMatrizComoImagen(f.errorCuadraticoPuntoAPunto(f.to_float(mlf), mif), 1)
  f.espectroMatriz(f.errorCuadraticoPuntoAPunto(mlf, mif), 2)
  f.mostrarMatrizComoImagen(f.errorCuadraticoPuntoAPunto(ml, mif), 3)
  f.espectroMatriz(f.errorCuadraticoPuntoAPunto(ml, mif), 4)
  plt.show()

if __name__ == '__main__':
  main()
