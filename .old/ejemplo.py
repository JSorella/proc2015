import funcion as f
import matplotlib.pyplot as plt

# Cargamos las imágenes
a = f.abrirImagen("../media/lena.png")
b = f.abrirImagen("../media/lenaTest1.jpg")

# Creamos las matrices a partir de imágenes
imageOneMatrix = f.generarMatriz(a)
imageTwoMatrix = f.generarMatriz(b)

# Calculamos el error cuadrático medio
mrs = f.errorCuadraticoMedio(imageOneMatrix, imageTwoMatrix)
print  " El error medio es ", mrs

# Creamos las matriz de error cuadrático
errorMatrix = f.errorCuadraticoPuntoAPunto(imageOneMatrix, imageTwoMatrix)

# Cargamos imágenes y espectros
f.mostrarMatrizComoImagen(imageOneMatrix, 3)
f.espectroMatriz(imageOneMatrix, 4)
f.mostrarMatrizComoImagen(errorMatrix, 1)
f.espectroMatriz(errorMatrix, 2)

# Mostramos los resultados
plt.show()
