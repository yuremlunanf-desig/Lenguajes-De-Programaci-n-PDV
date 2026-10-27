from tkinter import *
from tkinter import ttk  # menú desplegable
from datetime import datetime
import os

IVA = 0.16
NEGOCIO = "MI TIENDA"
USUARIOS = {"1234": "Cajero 1", "5678": "Cajero 2"}

# PRODUCTOS 
INVENTARIO = {
    "refresco": [18.50, 30],
    "papas": [22.00, 25],
    "galletas": [15.00, 40],
    "agua": [12.00, 50],
    "pan": [8.50, 60],
    "chocolate": [25.00, 35],
    "cafe": [30.00, 20],
    "yogurt": [20.00, 28],
    "jugos": [17.50, 22],
    "tortillas": [14.00, 18],
    "botana": [27.00, 16],
}

# ---------- ARCHIVOS TXT ----------
def leer(archivo):
    if not os.path.exists(archivo):
        return []
    return [l.strip().split("|") for l in open(archivo, encoding="utf-8") if l.strip()]

def agregarLinea(archivo, *campos):
    with open(archivo, "a", encoding="utf-8") as f:
        f.write("|".join(campos) + "\n")

def guardarInventario():
    with open("inventario.txt", "w", encoding="utf-8") as f:
        for n, (p, s) in inventario.items():
            f.write(f"{n}|{p}|{s}\n")

inventario = INVENTARIO
clientes = {n: t for n, t in leer("clientes.txt")}
guardarInventario()
carrito = {}
cajero = ""

#  LOGICA 
def mensaje(texto, color="#c0392b"):
    labelMensaje.config(text=texto, fg=color)

def calcular():
    total = round(sum(inventario[n][0] * c for n, c in carrito.items()), 2)
    sub = round(total / (1 + IVA), 2)
    iva = round(total - sub, 2)
    return sub, iva, total

def actualizar():
    lineas = [f"{c} x {n.capitalize()}  ${inventario[n][0] * c:.2f}" for n, c in carrito.items()]
    labelCarrito.config(text="\n".join(lineas[-6:]) or "Carrito vacío")
    labelTotal.config(text=f"TOTAL: ${calcular()[2]:.2f}")

def al_seleccionar_producto(event):
    nombre = cuadroProducto.get().lower()
    if nombre in inventario:
        cuadroPrecio.delete(0, END)
        cuadroPrecio.insert(0, f"{inventario[nombre][0]:.2f}")

def agregar(event=None):
    nombre = cuadroProducto.get().strip().lower()
    if not nombre or nombre not in inventario:
        return mensaje("Selecciona un producto válido")
    if not cuadroCantidad.get().isdigit() or int(cuadroCantidad.get()) == 0:
        return mensaje("Cantidad inválida")
    cant = int(cuadroCantidad.get())
    if carrito.get(nombre, 0) + cant > inventario[nombre][1]:
        return mensaje(f"Stock insuficiente (quedan {inventario[nombre][1]})")

    carrito[nombre] = carrito.get(nombre, 0) + cant
    cuadroPrecio.delete(0, END)
    cuadroProducto.set('') 
    cuadroCantidad.delete(0, END)
    cuadroCantidad.insert(0, "1")
    mensaje("Producto agregado", "#27ae60")
    actualizar()

def vaciar():
    carrito.clear()
    actualizar()
    mensaje("")

def registrarCliente():
    n = cuadroCliente.get().strip().replace("|", "")
    if not n:
        return mensaje("Escribe el nombre del cliente")
    if n in clientes:
        return mensaje("Ese cliente ya está registrado")
    clientes[n] = cuadroTelefono.get().strip().replace("|", "")
    agregarLinea("clientes.txt", n, clientes[n])
    mensaje("Cliente registrado", "#27ae60")

def cobrar(event=None):
    if not carrito:
        return mensaje("El carrito está vacío")

    try:
        pago = float(cuadroPago.get())
    except ValueError:
        return mensaje("Ingresa una cantidad de pago válida")

    sub, iva, total = calcular()

    if pago < total:
        return mensaje(f"Pago insuficiente. Faltan ${total - pago:.2f}")

    cambio = pago - total

    folio = len(leer("ventas.txt")) + 1
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    cliente = cuadroCliente.get().strip()
    if cliente not in clientes:
        cliente = "Público general"

    t = [
        NEGOCIO.center(34),
        "TICKET DE VENTA".center(34),
        f"Folio:   {folio:04d}",
        f"Fecha:   {fecha}",
        f"Cajero:  {cajero}",
        f"Cliente: {cliente}",
        "-" * 34,
    ]
    
    # DESGLOSE DE IVA 
    for n, c in carrito.items():
        precio_total_prod = inventario[n][0] * c
        iva_prod = precio_total_prod - (precio_total_prod / (1 + IVA))
        t.append(f"{c:>3} {n.capitalize()[:18]:<18}{precio_total_prod:>11.2f}")
        t.append(f"    (Incluye IVA: ${iva_prod:.2f})")

    t += [
        "-" * 34,
        f"{'SUBTOTAL':<24}{sub:>10.2f}",
        f"{f'IVA ({IVA:.0%})':<24}{iva:>10.2f}",
        f"{'TOTAL':<24}{total:>10.2f}",
        "-" * 34,
        f"{'PAGÓ CON:':<24}{pago:>10.2f}",
        f"{'SU CAMBIO:':<24}{cambio:>10.2f}",
        "",
        "Gracias por su compra".center(34),
    ]

    agregarLinea(
        "ventas.txt",
        f"{folio:04d}",
        fecha,
        cajero,
        cliente,
        f"{sub:.2f}",
        f"{iva:.2f}",
        f"{total:.2f}",
        "; ".join(f"{n} x{c}" for n, c in carrito.items()),
    )

    for n, c in carrito.items():
        inventario[n][1] -= c
    guardarInventario()

    ticketLabel.config(text="\n".join(t))
    carrito.clear()
    cuadroPago.delete(0, END)
    actualizar()
    mensaje(f"Venta registrada. Cambio: ${cambio:.2f}", "#27ae60")

def verInventario():
    l = ["INVENTARIO".center(34), f"{'Producto':<16}{'Precio':>9}{'Stock':>8}", "-" * 34]
    ticketLabel.config(
        text="\n".join(l + [f"{n.capitalize():<16}{p:>9.2f}{s:>8}" for n, (p, s) in inventario.items()])
    )

def verClientes():
    l = ["CLIENTES".center(34), f"{'Nombre':<20}{'Teléfono':>14}", "-" * 34]
    ticketLabel.config(text="\n".join(l + [f"{n[:20]:<20}{t:>14}" for n, t in clientes.items()][:25]))

def verHistorial():
    ventas = leer("ventas.txt")
    l = ["HISTORIAL DE VENTAS".center(34), f"{'Folio Fecha Cliente':<28}{'Total':>6}", "-" * 34]
    l += [f"{v[0]} {v[1][:5]} {v[3][:12]:<12}{float(v[6]):>10.2f}" for v in ventas[-15:]]
    l += ["-" * 34, f"{len(ventas)} ventas   Total: ${sum(float(v[6]) for v in ventas):.2f}"]
    ticketLabel.config(text="\n".join(l))

def entrar(event=None):
    global cajero
    if cuadroCajero.get() in USUARIOS:
        cajero = USUARIOS[cuadroCajero.get()]
        login.destroy()
        raiz.geometry("980x680")
        labelCajero.config(text="Cajero: " + cajero)
        miFrame.pack(side="left", fill="y", padx=20, pady=20)
        ticketLabel.pack(side="right", fill="y", padx=(0, 20), pady=20)
    else:
        cuadroCajero.delete(0, END)
        labelLogin.config(text="Clave incorrecta")

#  INTERFAZ 
raiz = Tk()
raiz.title("Sistema de Punto de Venta - Tkinter")
raiz.geometry("420x330")
raiz.resizable(False, False)

BG_APP = "#2c3e50"
CARD_BG = "#ecf0f1"
CARD_EDGE = "#d0d7de"
ACCENT = "#27ae60"
ACCENT_DARK = "#1e8e4e"
DANGER = "#c0392b"

raiz.config(bg=BG_APP)

style = ttk.Style(raiz)
try:
    style.theme_use("clam")
except:
    pass

style.configure("TCombobox",
                fieldbackground=CARD_BG,
                background=CARD_BG,
                foreground="#2c3e50",
                bordercolor=CARD_EDGE)
style.configure("TButton",
                padding=(8, 4),
                font=("Arial", 10, "bold"))

# Inicio de sesión
login = Frame(raiz, bg=CARD_BG, bd=10, relief="groove")
login.pack(fill="both", expand=True, padx=20, pady=20)

Label(login, text=" PUNTO DE VENTA", fg=BG_APP, bg=CARD_BG, font=("Arial", 18, "bold")).pack(pady=(25, 12))

Label(login, text="Clave Cajero:", bg=CARD_BG, fg=BG_APP, font=("Arial", 10, "bold")).pack()

cuadroCajero = Entry(login, bd=2, relief="groove", justify="center")
cuadroCajero.pack(pady=8)
cuadroCajero.config(show="*", justify="center")
cuadroCajero.bind("<Return>", entrar)

Button(login, text="ENTRAR", command=entrar, bg=ACCENT, fg="white",
    activebackground=ACCENT_DARK, activeforeground="white",
    relief="flat", padx=18, pady=6).pack(pady=8)

labelLogin = Label(login, text="", fg=DANGER, bg=CARD_BG, font=("Arial", 10, "bold"))
labelLogin.pack(pady=(4, 0))

# Pantalla de venta
miFrame = Frame(raiz, bg=CARD_BG, bd=10, relief="groove")

Label(miFrame, text=" PUNTO DE VENTA", fg=BG_APP, bg=CARD_BG,
    font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(6, 0))

labelCajero = Label(miFrame, text="", bg=CARD_BG, fg="#7f8c8d", font=("Arial", 10, "italic"))
labelCajero.grid(row=1, column=0, columnspan=2, pady=(0, 10))

def campo(texto, fila, **cfg):
    Label(miFrame, text=texto, bg=CARD_BG, fg=BG_APP, font=("Arial", 10, "bold")).grid(
        row=fila, column=0, sticky="e", padx=10, pady=6
    )
    e = Entry(miFrame, bd=2, relief="groove", **cfg)
    e.grid(row=fila, column=1, padx=10, pady=6)
    return e

# Producto 
Label(miFrame, text="Producto:", bg=CARD_BG, fg=BG_APP, font=("Arial", 10, "bold")).grid(
    row=2, column=0, sticky="e", padx=10, pady=6
)

cuadroProducto = ttk.Combobox(
    miFrame,
    values=[n.capitalize() for n in inventario.keys()],
    state="readonly",
    width=18
)
cuadroProducto.grid(row=2, column=1, padx=10, pady=6)
cuadroProducto.bind("<<ComboboxSelected>>", al_seleccionar_producto)

cuadroPrecio = campo("Precio ($):", 3, justify="right")
cuadroCantidad = campo("Cantidad:", 4, justify="center")

cuadroCliente = campo("Cliente:", 5)
cuadroTelefono = campo("Teléfono:", 6)
cuadroPago = campo("Paga con ($):", 7, justify="right", fg=DANGER)  # Nuevo campo de pago

cuadroCantidad.insert(0, "1")
cuadroCantidad.bind("<Return>", agregar)

def botones(fila, lista, color=BG_APP):
    f = Frame(miFrame, bg=CARD_BG)
    f.grid(row=fila, column=0, columnspan=2, pady=6)
    for texto, comando in lista:
        Button(
            f, text=texto, command=comando,
            bg=color, fg="white",
            activebackground=("#22313f" if color == BG_APP else color),
            relief="flat", padx=10, pady=6,
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=4)

botones(8, [("Agregar", agregar), ("Vaciar carrito", vaciar), ("Registrar cliente", registrarCliente)])

#  Carrito 
labelCarrito = Label(
    miFrame,
    text="Carrito vacío",
    bg="#ffffff",
    fg=BG_APP,
    font=("Courier", 10),
    justify="left",
    anchor="nw",
    width=38,
    height=7,
    bd=1,
    relief="solid"
)
labelCarrito.grid(row=9, column=0, columnspan=2, pady=8)

Label(miFrame, text="Resumen de Cobro", bg=CARD_BG, fg="#7f8c8d",
    font=("Arial", 11, "italic")).grid(row=10, column=0, columnspan=2, pady=(10, 2))

labelTotal = Label(
    miFrame,
    text="TOTAL: $0.00",
    fg=ACCENT,
    bg=CARD_BG,
    font=("Comic Sans MS", 20, "bold"),
    cursor="hand2",
    pady=2
)
labelTotal.grid(row=11, column=0, columnspan=2, pady=5)
labelTotal.bind("<Button-1>", cobrar)

botones(12, [("COBRAR", cobrar)], ACCENT)

botones(13, [("Inventario", verInventario), ("Clientes", verClientes), ("Historial", verHistorial)], BG_APP)

labelMensaje = Label(miFrame, text="", bg=CARD_BG, font=("Arial", 10, "bold"), fg=DANGER)
labelMensaje.grid(row=14, column=0, columnspan=2, pady=(8, 0))

# Ticket 
ticketLabel = Label(
    raiz,
    text="\nEl ticket aparecerá aquí",
    bg="#ffffff",
    fg=BG_APP,
    font=("Courier", 10),
    justify="left",
    anchor="nw",
    width=50,
    height=20,
    bd=1,
    relief="solid",
    padx=10,
    pady=10
)

raiz.mainloop()