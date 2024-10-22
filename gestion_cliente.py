import psycopg2
import tkinter as tk
from tkinter import messagebox, ttk

# Configuración de la conexión
def conectar_db():
    return psycopg2.connect(
        dbname="clinica_db",
        user="postgres",
        password="clinica",
        host="127.0.0.1",
        port="5432"
    )

# Función para agregar un cliente
def agregar_cliente(nombre, apellido, email, telefono):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nombre, apellido, email, telefono)
        VALUES (%s, %s, %s, %s);
    """, (nombre, apellido, email, telefono))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Éxito", "Cliente agregado con éxito.")
    mostrar_clientes()
    limpiar_formulario()  # Limpiar el formulario después de agregar

# Función para consultar clientes
def consultar_clientes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes;")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return clientes

# Función para actualizar un cliente
def actualizar_cliente(id, nombre, apellido, email, telefono):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes
        SET nombre = %s, apellido = %s, email = %s, telefono = %s
        WHERE id = %s;
    """, (nombre, apellido, email, telefono, id))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Éxito", "Cliente actualizado con éxito.")
    mostrar_clientes()
    limpiar_formulario()  # Limpiar el formulario después de actualizar

# Función para eliminar un cliente
def eliminar_cliente(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s;", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Éxito", "Cliente eliminado con éxito.")
    mostrar_clientes()
    limpiar_formulario()  # Limpiar el formulario después de eliminar

# Función para agregar un cliente desde la interfaz
def agregar_cliente_ui():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    email = entry_email.get()
    telefono = entry_telefono.get()
    agregar_cliente(nombre, apellido, email, telefono)

# Función para seleccionar un cliente de la lista
def seleccionar_cliente(event):
    selected_item = tree.selection()
    if not selected_item:  # Verifica si hay un elemento seleccionado
        print("No hay ningún cliente seleccionado.")  # Mensaje de depuración
        return

    selected_item = selected_item[0]  # Obtener el ID del cliente seleccionado
    cliente = tree.item(selected_item, 'values')
    
    entry_id.config(state='normal')  # Habilitar la entrada del ID para mostrar
    entry_id.delete(0, tk.END)
    entry_id.insert(0, cliente[0])  # ID
    entry_id.config(state='readonly')  # Dejar la entrada del ID en modo solo lectura

    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, cliente[1])  # Nombre
    entry_apellido.delete(0, tk.END)
    entry_apellido.insert(0, cliente[2])  # Apellido
    entry_email.delete(0, tk.END)
    entry_email.insert(0, cliente[3])  # Email
    entry_telefono.delete(0, tk.END)
    entry_telefono.insert(0, cliente[4])  # Teléfono

    habilitar_botones()  # Habilitar botones al seleccionar cliente

# Función para habilitar o deshabilitar botones
def habilitar_botones():
    selected_item = tree.selection()
    if selected_item:
        btn_actualizar.config(state=tk.NORMAL)
        btn_eliminar.config(state=tk.NORMAL)
    else:
        btn_actualizar.config(state=tk.DISABLED)
        btn_eliminar.config(state=tk.DISABLED)

# Función para mostrar todos los clientes en la tabla
def mostrar_clientes():
    for row in tree.get_children():
        tree.delete(row)
    
    clientes = consultar_clientes()
    for cliente in clientes:
        tree.insert("", tk.END, values=cliente)

# Función para actualizar cliente desde la interfaz
def actualizar_cliente_ui():
    id = entry_id.get()
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    email = entry_email.get()
    telefono = entry_telefono.get()

    if id:  # Verifica que el ID no esté vacío
        actualizar_cliente(id, nombre, apellido, email, telefono)
    else:
        messagebox.showwarning("Advertencia", "Por favor, seleccione un cliente para actualizar.")

# Función para eliminar cliente desde la interfaz
def eliminar_cliente_ui():
    id = entry_id.get()
    if id:  # Verifica que el ID no esté vacío
        eliminar_cliente(id)
    else:
        messagebox.showwarning("Advertencia", "Por favor, seleccione un cliente para eliminar.")

# Función para limpiar el formulario
def limpiar_formulario():
    entry_id.config(state='normal')  # Habilitar el campo ID para limpiar
    entry_id.delete(0, tk.END)
    entry_id.config(state='readonly')  # Dejar el campo ID en modo solo lectura
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    habilitar_botones()  # Deshabilitar botones después de limpiar

# Función para mostrar la interfaz
def mostrar_interfaz():
    global entry_nombre, entry_apellido, entry_email, entry_telefono, entry_id, tree
    global btn_actualizar, btn_eliminar

    window = tk.Tk()
    window.title("Gestión de Clientes")

    # Labels
    tk.Label(window, text="ID:").grid(row=0, column=0)
    tk.Label(window, text="Nombre:").grid(row=1, column=0)
    tk.Label(window, text="Apellido:").grid(row=2, column=0)
    tk.Label(window, text="Email:").grid(row=3, column=0)
    tk.Label(window, text="Teléfono:").grid(row=4, column=0)

    # Entradas
    entry_id = tk.Entry(window, state='readonly')  # ID solo para lectura
    entry_nombre = tk.Entry(window)
    entry_apellido = tk.Entry(window)
    entry_email = tk.Entry(window)
    entry_telefono = tk.Entry(window)

    entry_id.grid(row=0, column=1)
    entry_nombre.grid(row=1, column=1)
    entry_apellido.grid(row=2, column=1)
    entry_email.grid(row=3, column=1)
    entry_telefono.grid(row=4, column=1)

    # Botones
    btn_agregar = tk.Button(window, text="Agregar Cliente", command=agregar_cliente_ui)
    btn_agregar.grid(row=5, column=0, columnspan=2)

    btn_actualizar = tk.Button(window, text="Actualizar Cliente", command=actualizar_cliente_ui, state=tk.DISABLED)
    btn_actualizar.grid(row=6, column=0, columnspan=2)

    btn_eliminar = tk.Button(window, text="Eliminar Cliente", command=eliminar_cliente_ui, state=tk.DISABLED)
    btn_eliminar.grid(row=7, column=0, columnspan=2)

    # Tabla para mostrar clientes
    tree = ttk.Treeview(window, columns=("ID", "Nombre", "Apellido", "Email", "Teléfono"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Apellido", text="Apellido")
    tree.heading("Email", text="Email")
    tree.heading("Teléfono", text="Teléfono")
    tree.grid(row=8, column=0, columnspan=2)

    # Evento de selección en la tabla
    tree.bind("<<TreeviewSelect>>", seleccionar_cliente)

    # Mostrar clientes al inicio
    mostrar_clientes()

    # Mostrar ventana
    window.mainloop()

# Ejecutar la interfaz
if __name__ == "__main__":
    mostrar_interfaz()
