from tkinter import *

# 1. Crear la ventana principal (Raíz)
root = Tk()
root.title("Práctica con Label - Video 3")

# 2. Crear y empaquetar el Frame contenedor
miFrame = Frame(root, width=400, height=400)
miFrame.pack()

# 3. Crear el Label de texto
Label(
    miFrame, 
    text="Hola lemonardo", 
    fg="purple", 
    font=("Comic Sans MS", 18)
).place(x=100, y=200)

# 4. Bucle principal para mantener la ventana en ejecución
root.mainloop()