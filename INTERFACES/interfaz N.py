import tkinter as tk

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz Gráfica")
root.geometry("400x400")  # Tamaño de la ventana

# Crear un marco (frame) para cada cuadrante
frame1 = tk.Frame(root, bg='red', width=200, height=200)
frame2 = tk.Frame(root, bg='green', width=200, height=200)
frame3 = tk.Frame(root, bg='blue', width=200, height=200)
frame4 = tk.Frame(root, bg='yellow', width=200, height=200)

# Colocar los marcos en una cuadrícula 2x2
frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=1, sticky="nsew")
frame3.grid(row=1, column=0, sticky="nsew")
frame4.grid(row=1, column=1, sticky="nsew")

# Configurar la cuadrícula para que se expanda con la ventana
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Crear botones en el cuarto frame
button1 = tk.Button(frame4, text="Botón 1")
button2 = tk.Button(frame4, text="Botón 2")
button3 = tk.Button(frame4, text="Botón 3")
button4 = tk.Button(frame4, text="Botón 4")

# Colocar los botones en una cuadrícula 2x2 dentro del cuarto frame
button1.grid(row=0, column=0, sticky="nsew")
button2.grid(row=0, column=1, sticky="nsew")
button3.grid(row=1, column=0, sticky="nsew")
button4.grid(row=1, column=1, sticky="nsew")

# Configurar la cuadrícula dentro del cuarto frame para que se expanda con el tamaño del frame
frame4.grid_rowconfigure(0, weight=1)
frame4.grid_rowconfigure(1, weight=1)
frame4.grid_columnconfigure(0, weight=1)
frame4.grid_columnconfigure(1, weight=1)

# Ejecutar el bucle principal de la aplicación
root.mainloop()
