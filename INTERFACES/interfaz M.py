import tkinter as tk

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz Gráfica")
root.geometry("400x400")  # Tamaño inicial de la ventana

# Configurar la cuadrícula principal (2x2) para que se expanda con la ventana
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Ejecutar el bucle principal de la aplicación
root.mainloop()
