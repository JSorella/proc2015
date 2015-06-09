#!/usr/bin/env python
"""
Compresion Lossy de la imagen usando la transformada wavelet de Haar.
"""
import numpy as np

scale = np.sqrt(2.)

def haar(a):
  if len(a) == 1:
    return a.copy()
  #assert len(a) % 2 == 0, "length needs to be even"
  b = a
  if(len(a[0::2] ) > len(a[1::2])):
    b = np.append(a, [0])
  mid = (b[0::2] + b[1::2]) / scale
  side = (b[0::2] - b[1::2]) / scale
  if(len(a[0::2] ) > len(a[1::2])):
    mid = np.delete(mid, len(mid)-1)
    #side = np.delete(side, len(side)-1)
  return np.hstack((haar(mid), side))

def ihaar(a):
  if len(a) == 1:
    return a.copy()
  #assert len(a) % 2 == 0, "length needs to be even"
  b = a
  if(len(a[0::2] ) > len(a[1::2])):
    b = np.delete(a, len(a)-1)
  mid = ihaar(b[0:len(b)/2]) * scale
  side = b[len(b)/2:] * scale
  
  out = np.zeros(len(b), dtype=float)
  if(len(mid) < len(side)):
    mid = np.append(mid, [0])
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
    ihaarResult = ihaar(haarCoeffs[:,x])
    if (len(ihaarResult) < len(cols[:,x])):
      ihaarResult = np.append(ihaarResult,[0])
    cols[:,x] = ihaarResult
  rows = np.zeros(haarCoeffs.shape, dtype=float)
  for y in range(h):
    ihaarResult = ihaar(cols[y])
    if (len(ihaarResult) < len(rows[y])):
      ihaarResult = np.append(ihaarResult,[0])
    rows[y] = ihaarResult
  return rows
