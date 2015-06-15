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
import gzip

def main(argv):
  # Archivo por defecto (si no hay argumentos)
  fileName = '../media/lena.png'
  ratio = .1
  rar = '.1'

  # Verificamos que se esta pasando un nombre de archivo por argumento
  try:
    opts, args = getopt.getopt(argv,"oi:r:h",["file=","ratio=","help"])
  except getopt.GetoptError:
    print 'main.py -i <inputfile> -r <ratio>'
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      print 'main.py -i <inputfile> -r <ratio>'
      sys.exit()
    elif opt in ("-i", "--file"):
      fileName = arg
    elif opt in ("-r", "--ratio"):
      ratio = float(arg)
      rar = arg

  # Cargamos la imagen a procesar
  img = f.to_float(f.load(fileName))

  # Calculamos los coeficientes segun algortimo
  fftCoeffs = np.fft.fft2(img)
  haarCoeffs = haar.haar_2d(img)
  dctCoeffs = dcst.dct2(img)

  # Recortamos los valores despreciables
  strongFftCoeffs =  f.keep_ratio(fftCoeffs,ratio)
  strongHaarCoeffs = f.keep_ratio(haarCoeffs,ratio)
  strongDctCoeffs = f.keep_ratio(dctCoeffs,ratio)
  
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
  print "\nERROR CUADRATICO MEDIO"
  print "Diferencia entre FFT y original:  ", f.to_float(f.errorCuadraticoMedio(fftMatrix,originalMatrix))
  print "Diferencia entre Haar y original: ", f.errorCuadraticoMedio(haarMatrix,originalMatrix)
  print "Diferencia entre DCT y original:  ", f.errorCuadraticoMedio(dctMatrix,originalMatrix)
  print "\n"

  # Creamos las matrices de error cuadratico punto a punto
  errorFftMatrix = f.errorCuadraticoPuntoAPunto(fftMatrix,originalMatrix)
  errorHaarMatrix = f.errorCuadraticoPuntoAPunto(haarMatrix,originalMatrix)
  errorDctMatrix = f.errorCuadraticoPuntoAPunto(dctMatrix,originalMatrix)  
  print '../media/compressed-fft_%s.png' % rar
  # Guardamos las imagenes comprimidas
  f.save('../media/compressed-fft_%s.png' % rar, f.from_float(lossyFft))
  f.save('../media/compressed-haar_%s.png' % rar, f.from_float(lossyHaar))
  f.save('../media/compressed-dct_%s.png' % rar, f.from_float(lossyDct))
  # Guardamos las imagenes con los coeficientes  
  f.save('../media/coeff-fft_%s.png' % rar, f.bipolar(fftCoeffs))
  f.save('../media/coeff-fft-recortado_%s.png' % rar, f.bipolar(strongFftCoeffs))
  f.save('../media/coeff-haar_%s.png' % rar, f.bipolar(haarCoeffs))
  f.save('../media/coeff-haar-recortado_%s.png' % rar, f.bipolar(strongHaarCoeffs))
  f.save('../media/coeff-dct_%s.png' % rar, f.bipolar(dctCoeffs))
  f.save('../media/coeff-dct-recortado_%s.png' % rar, f.bipolar(strongDctCoeffs))
  # Guardamos las imagenes que muestran la diferencia de error entre algoritmo y original
  f.save('../media/error-fft_%s.png' % rar, f.bipolar(errorFftMatrix))
  f.save('../media/error-haar_%s.png' % rar, f.bipolar(errorHaarMatrix))
  f.save('../media/error-dct_%s.png' % rar, f.bipolar(errorDctMatrix))

  # Guardamos los coeficientes comprimidos
  fin = open('haarCoeffs_%s.raw' % rar, 'w+')
  fin.write(haarCoeffs)
  fin = open('strongHaarCoeffs_%s.raw' % rar, 'w+')
  fin.write(strongHaarCoeffs)
  fin = open('strongFftCoeffs_%s.raw' % rar, 'w+')
  fin.write(strongFftCoeffs)
  fin = open('fftCoeffs_%s.raw' % rar, 'w+')
  fin.write(fftCoeffs)
  fin = open('dctCoeffs_%s.raw' % rar, 'w+')
  fin.write(dctCoeffs)
  fin = open('strongDctCoeffs_%s.raw' % rar, 'w+')
  fin.write(strongDctCoeffs)
  fin.close()

  # Ploteamos las imagenes resultantes en pantalla
  #f.mostrarMatrizComoImagen(f.errorCuadraticoPuntoAPunto(f.to_float(fftMatrix), originalMatrix), 1)
  #f.mostrarMatrizComoImagen(errorHaarMatrix, 2)
  #f.mostrarMatrizComoImagen(errorDctMatrix, 3)
  # Ploteamos los histogramas de las imagenes
  #f.espectroMatriz(errorFftMatrix, 4)
  #f.espectroMatriz(errorHaarMatrix, 5)
  #f.espectroMatriz(errorDctMatrix, 6)

  #plt.show()

if __name__ == '__main__':
  main(sys.argv[1:])
