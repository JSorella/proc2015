import funcion as f
import matplotlib.pyplot as plt

a = f.abrirImagen("../media/lena.png")
b = f.abrirImagen("../media/lenaTest1.jpg")


ar1 = f.generarMatriz(a)
ar2 = f.generarMatriz(b)

ar3 = f.errorCuadraticoPuntoAPunto(ar1,ar2)

mrs = f.errorCuadraticoMedio(ar1,ar2)
print  " El error medio es ", mrs
f.mostrarMatrizComoImagen(ar1,3)
f.espectroMatriz(ar1,4)
f.mostrarMatrizComoImagen(ar3,1)
f.espectroMatriz(ar3,2)

plt.show()
# Las funciones arman las figuras, pero hay que darle show para mostrarlas.
