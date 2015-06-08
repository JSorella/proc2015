#!/usr/bin/env python
"""
Compresion Lossy de la imagen usando la transformada wavelet de Haar.
"""
import numpy as np

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

def ihaar_2d(haarCoeffs):
  h,w = haarCoeffs.shape
  cols = np.zeros(haarCoeffs.shape, dtype=float)
  for x in range(w):
    cols[:,x] = ihaar(haarCoeffs[:,x])
  rows = np.zeros(haarCoeffs.shape, dtype=float)
  for y in range(h):
    rows[y] = ihaar(cols[y])
  return rows
