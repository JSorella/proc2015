# TP Compresión de Imágenes
#### Procesamiento de Señales - 1c 2015 - UTN FRBA
##### Grupo 2
---------------------

## Instalación

Se necesitan los siguientes pre-requisitos para correr el aplicativo:

1) Instalar python

2) Instalar las siguientes dependencias:
>**Scipy:**
>sudo apt-get install python-scipy

>**Matplotlib:**
>sudo apt-get install python-matplotlib

>**Tkinter:**
>sudo apt-get install python-tk

---------------------

## Ejecución

Dentro de la carpeta "src", ejecutar bajo la directiva:

>```bash
python main.py -i <nombreArchivoAProcesar>
```

... Si no se adjunta ningún argumento, por defecto procesa la imágen media/lena.png

---------------------

## To do:
- [ ] Mejorar Haar
- [ ] Crear tests
- [x] Parametrizar el Ratio
- [x] Verificar que es eso de que las imágenes que se cargan tienen que tener "valor par"
- [x] Pasar por parámetro ruta a la imágen a cargar
- [x] Averiguar porque la imágen gira 90 grados
- [x] Mostrar la diferencia de error entre original y algoritmos
- [x] Desarrollar el algoritmo por transformada discreta del coseno (DCT)
- [x] Terminar de configurar el entorno
- [x] Mejorar el formato del código
- [x] Commitear los archivos de Carlos
- [x] Crear repositorio
