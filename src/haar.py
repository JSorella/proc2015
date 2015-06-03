#!/usr/bin/env python
"""
Lossy image compression using the Haar Wavelet Transform.
"""

import Image
import numpy as np
import funcion
import matplotlib.pyplot as plt

def main():
  img = to_float(load('lena.png'))
  imgF = to_float(load('lena.png'))
  coeffsF = np.fft.fft2(imgF)
  coeffs = haar_2d(img)
  strong_coeffsFFT =  keep_ratio(coeffsF, .5)
  strong_coeffs = keep_ratio(coeffs, .5)
 
  lossy = ihaar_2d(strong_coeffs)
  lossyF = np.fft.ifft2(strong_coeffsFFT)
  ml=funcion.generarMatriz(lossy)
  mlf=funcion.generarMatriz(lossyF)
  mi=funcion.generarMatriz(img)
  mif=funcion.generarMatriz(imgF)


  print "diferencia entre FFT y original", funcion.errorCuadraticoMedio(mlf,mif)
  print "diferencia entre Haar y original", funcion.errorCuadraticoMedio(ml,mi)

  funcion.mostrarMatrizComoImagen(funcion.errorCuadraticoPuntoAPunto(to_float(mlf), mif),2)
  funcion.mostrarMatrizComoImagen(funcion.errorCuadraticoPuntoAPunto(ml, mi),1)
  plt.show()
  

  save('Haar-coeff.png', bipolar(coeffs))
  save('Haar-coeff-Recortado.png', bipolar(strong_coeffs))
  save('fft-coeff.png', bipolar(coeffsF))
  save('fft-coeff-Recortado.png', bipolar(strong_coeffsFFT))
  save('Haar-output.png', from_float(lossy))
  save('FFT-output.png', from_float(lossyF))

# --- haar-related code:

scale = np.sqrt(2.)

def haar(a):
  if len(a) == 1:
    return a.copy()
  assert len(a) % 2 == 0, "length needs to be even"
  mid = (a[0::2] + a[1::2]) / scale
  side = (a[0::2] - a[1::2]) / scale
  return np.hstack((haar(mid), side))

def ihaar(a):
  if len(a) == 1:
    return a.copy()
  assert len(a) % 2 == 0, "length needs to be even"
  mid = ihaar(a[0:len(a)/2]) * scale
  side = a[len(a)/2:] * scale
  out = np.zeros(len(a), dtype=float)
  out[0::2] = (mid + side) / 2.
  out[1::2] = (mid - side) / 2.
  return out

def haar_2d(img):
  h,w = img.shape
  rows = np.zeros(img.shape, dtype=float)
  for y in range(h):
    rows[y] = haar(img[y])
  cols = np.zeros(img.shape, dtype=float)
  for x in range(w):
    cols[:,x] = haar(rows[:,x])
  return cols

def ihaar_2d(coeffs):
  h,w = coeffs.shape
  cols = np.zeros(coeffs.shape, dtype=float)
  for x in range(w):
    cols[:,x] = ihaar(coeffs[:,x])
  rows = np.zeros(coeffs.shape, dtype=float)
  for y in range(h):
    rows[y] = ihaar(cols[y])
  return rows

def keep_ratio(a, ratio):
  """
  Keep only the strongest values.
  """
  magnitude = sorted(np.abs(a.flatten()))
  idx = int((len(magnitude) - 1) * (1. - ratio))
  return np.where(np.abs(a) > magnitude[idx], a, 0)

# --- graphics-related code:

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

def load(fn):
  return np.asarray(Image.open(fn).convert(mode='L'))

def save(fn, img):
  assert img.dtype == np.uint8
  Image.fromarray(img).save(fn)
  print 'wrote', fn

if __name__ == '__main__':
  main()

# vim:set ts=2 sw=2 et:
