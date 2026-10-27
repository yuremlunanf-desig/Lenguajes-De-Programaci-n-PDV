from tkinter import *

# 1. Crear la raíz o ventana principal (Contenedor general)
raiz = Tk()
raiz.title("Ventana con Frame - Video 2")
raiz.config(bg="blue")

raiz.config(bd=15)
raiz.config(relief="sunken")
raiz.config(cursor="hand2")

# 2. Crear el Frame (Lienzo o contenedor interno)
miFrame = Frame(raiz)

# 3. Empaquetar el Frame dentro de la raíz
miFrame.pack(fill="both", expand=True)

# 4. Definir las dimensiones y características visuales del Frame

miFrame.config(bg="red")            
miFrame.config(width=650, height=350) 

# Configuración del borde y cursor dentro del Frame
miFrame.config(bd=25)               
miFrame.config(relief="groove")      
miFrame.config(cursor="pirate")     

# 5. Bucle de ejecución principal (mantiene la ventana abierta)
raiz.mainloop()