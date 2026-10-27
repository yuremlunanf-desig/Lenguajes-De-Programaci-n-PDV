from tkinter import *

# 1. Crear la ventana principal (Raíz)
root = Tk()
root.title("Práctica con Label e Imagen - Video 3")

# 2. Crear y empaquetar el Frame contenedor
miFrame = Frame(root, width=800, height=800)
miFrame.pack()

# 3. Cargar la imagen desde el directorio de trabajo
# Soporta formatos nativos como PNG y GIF
miImagen = PhotoImage(file="Snorlax-Pokemon-Download-Free-PNG.png")

# 4. Crear el Label asignando la variable de la imagen
Label(miFrame, image=miImagen).place(x=50, y=50)

# 5. Bucle principal para mantener la ventana en ejecución
root.mainloop()