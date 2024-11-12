import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def connection():
    try:
        return mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "factory"
        )
        
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Can't connect to database: {e}")
        return None
    
conn = connection()

if not connection():
    exit(1)

def add_materials():
    material = material_name.get().strip()
    quantity = material_quantity.get().strip()

    if not material or not quantity.isdigit():
        messagebox.showerror("Error", "Enter a valid name or quantity");
        return
    
    try:
        cursor = conn.cursor()
        query = "UPDATE material_inventory SET material_quantity = material_quantity + %s WHERE material_id = (SELECT material_id FROM materials WHERE materials.material_name = %s)"
        cursor.execute(query, (quantity, material))
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Info", f'Materials successfully updated')
        else:
            messagebox.showwarning("Warning", "Not found")

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f'Error updating: {e}')
    
    finally:
        cursor.close()

def check_inventory_stock():
    try:
        cursor = conn.cursor()
        query = "SELECT material_name, material_inventory.material_quantity FROM materials INNER JOIN material_inventory ON materials.material_id = material_inventory.material_id"
        cursor.execute(query)
        records = cursor.fetchall()
        stock = "\n".join([f'{name}: {quantity} units' for name, quantity in records])
        messagebox.showinfo("Inventory stock status", stock if stock else "Inventory is empty")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", e)
    finally:
        cursor.close()

root = tk.Tk()
root.title("Procurement application")
root.geometry("400x300")

style = ttk.Style()
style.configure("TLabel")
style.configure("TButton")
style.configure("TEntry")

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

ttk.Label(frame, text = "Material name: ").grid(row = 0, column = 0, sticky = tk.E, pady = 5)
material_name = ttk.Entry(frame)
material_name.grid(row = 0, column = 1, pady = 5)

ttk.Label(frame, text = "Quantity: ").grid(row = 1, column = 0, sticky = tk.E, pady = 5)
material_quantity = ttk.Entry(frame)
material_quantity.grid(row = 1, column = 1, pady = 5)

add_btn = ttk.Button(frame, text = "Add material", command = add_materials)
add_btn.grid(row = 2, column = 0, columnspan = 2, pady = 15)

status_btn = ttk.Button(frame, text = "Check inventory stock", command = check_inventory_stock)
status_btn.grid(row = 3, column = 0, columnspan = 2, pady = 10)

for child in frame.winfo_children():
    child.grid_configure(padx = 10)

root.mainloop()