#!/usr/bin/env python
"""
Programa Principal
"""
import numpy as np
import helper as f
import haar
import dcst
import matplotlib.pyplot as plt
import sys, getopt

def main(argv):
  # Archivo por defecto (si no hay argumentos)
  fileName = '../media/lena.png'
  ratio = .1

  # Verificamos que se esta pasando un nombre de archivo por argumento
  try:
    opts, args = getopt.getopt(argv,"hi:r:o",["ifile=","ratio="])
  except getopt.GetoptError:
    print 'main.py -i <inputfile> -r <ratio>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'test.py -i <inputfile> -r <ratio>'
      sys.exit()
    elif opt in ("-i", "--ifile"):
      fileName = arg
    elif opt in ("-r", "--ratio"):
      ratio = arg

  # Cargamos la imagen a procesar
  img = f.to_float(f.load(fileName))

  # Calculamos los coeficientes segun algortimo
  fftCoeffs = np.fft.fft2(img)
  haarCoeffs = haar.haar_2d(img)
  dctCoeffs = dcst.dct2(img)

  # Recortamos los valores despreciables
  strongFftCoeffs =  f.keep_ratio(fftCoeffs, .075)
  strongHaarCoeffs = f.keep_ratio(haarCoeffs, .075)
  strongDctCoeffs = f.keep_ratio(dctCoeffs, .075)
  
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

  # Creamos las matrices de error cuadratico punto a punto
  errorFftMatrix = f.errorCuadraticoPuntoAPunto(fftMatrix,originalMatrix)
  errorHaarMatrix = f.errorCuadraticoPuntoAPunto(haarMatrix,originalMatrix)
  errorDctMatrix = f.errorCuadraticoPuntoAPunto(dctMatrix,originalMatrix)

  # Guardamos las imagenes comprimidas
  f.save('../media/compressed-fft.png', f.from_float(lossyFft))
  f.save('../media/compressed-haar.png', f.from_float(lossyHaar))
  f.save('../media/compressed-dct.png', f.from_float(lossyDct))
  # Guardamos las imagenes con los coeficientes  
  f.save('../media/coeff-fft.png', f.bipolar(fftCoeffs))
  f.save('../media/coeff-fft-recortado.png', f.bipolar(strongFftCoeffs))
  f.save('../media/coeff-haar.png', f.bipolar(haarCoeffs))
  f.save('../media/coeff-haar-recortado.png', f.bipolar(strongHaarCoeffs))
  f.save('../media/coeff-dct.png', f.bipolar(dctCoeffs))
  f.save('../media/coeff-dct-recortado.png', f.bipolar(strongDctCoeffs))
  # Guardamos las imagenes que muestran la diferencia de error entre algoritmo y original
  f.save('../media/error-fft.png', f.bipolar(errorFftMatrix))
  f.save('../media/error-haar.png', f.bipolar(errorHaarMatrix))
  f.save('../media/error-dct.png', f.bipolar(errorDctMatrix))

  # Ploteamos las imagenes resultantes en pantalla, junto a sus histogramas
  f.mostrarMatrizComoImagen(f.errorCuadraticoPuntoAPunto(f.to_float(fftMatrix), originalMatrix), 1)
  f.mostrarMatrizComoImagen(errorHaarMatrix, 2)
  f.mostrarMatrizComoImagen(errorDctMatrix, 3)
  f.espectroMatriz(errorFftMatrix, 4)
  f.espectroMatriz(errorHaarMatrix, 5)
  f.espectroMatriz(errorDctMatrix, 6)

  plt.show()

if __name__ == '__main__':
  main(sys.argv[1:])
