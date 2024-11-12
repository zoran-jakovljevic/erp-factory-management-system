import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="factory"
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Can't connect to database: {e}")
        exit(1)

conn = connection()

def check_stock():
    try:
        cursor = conn.cursor()
        query = "SELECT product_id, product_quantity FROM product_inventory"
        cursor.execute(query)
        records = cursor.fetchall()

        for item in tree_stock.get_children():
            tree_stock.delete(item)

        for productId, quantity in records:
            tree_stock.insert("", "end", values=(productId, quantity))

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error: {e}")

def show_value():
    try:
        cursor = conn.cursor()
        query = """
        SELECT products.name, product_inventory.product_quantity, products.selling_price 
        FROM products 
        INNER JOIN product_inventory 
        ON products.product_id = product_inventory.product_id
        """
        cursor.execute(query)
        records = cursor.fetchall()

        for item in tree_value.get_children():
            tree_value.delete(item)

        for name, quantity, price in records:
            totalValue = quantity * price
            tree_value.insert("", "end", values=(name, quantity, price, totalValue))

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f'Error: {e}')

def fill_products():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM products")
    return [row[0] for row in cursor.fetchall()]

def produce():
    chosen_product = combo_products.get()
    if not chosen_product:
        messagebox.showwarning("Warning", "Please choose a product")
        return

    try:
        cursor = conn.cursor()
        query = """
        SELECT materials.material_name, material_products.required_quantity 
        FROM materials 
        INNER JOIN material_products 
        ON materials.material_id = material_products.material_id 
        WHERE material_products.product_id = (SELECT product_id FROM products WHERE name = %s)
        """
        cursor.execute(query, (chosen_product,))
        result = cursor.fetchall()

        if not result:
            messagebox.showerror("Error", f'Production of this product is not allowed')
            return

        for material, quantity in result:
            query_stock = """
            UPDATE material_inventory 
            SET material_quantity = material_quantity - %s 
            WHERE material_id = (SELECT material_id FROM materials WHERE material_name = %s) 
            AND material_quantity >= %s
            """
            cursor.execute(query_stock, (quantity, material, quantity))

            if cursor.rowcount <= 0:
                messagebox.showerror("Error", f'Not enough {material} in inventory')
                conn.rollback()
                return

        query_addProduct = """
        UPDATE product_inventory 
        SET product_quantity = product_quantity + 1 
        WHERE product_id = (SELECT product_id FROM products WHERE name = %s)
        """
        cursor.execute(query_addProduct, (chosen_product,))

        messagebox.showinfo("Info", f'Successfully produced {chosen_product}')
        conn.commit()
        show_value()

    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Error", e)

root = tk.Tk()
root.title("Production application")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

frame_stock = ttk.Frame(notebook)
notebook.add(frame_stock, text="Stock level")

tree_stock = ttk.Treeview(frame_stock, columns=("Product ID", "Quantity"), show='headings')
tree_stock.heading("Product ID", text="Product ID")
tree_stock.heading("Quantity", text="Quantity")
tree_stock.pack(expand=True, fill='both')

refresh_btn = ttk.Button(frame_stock, text="Refresh", command=check_stock)
refresh_btn.pack(pady=10)

frame_value = ttk.Frame(notebook)
notebook.add(frame_value, text="Total value of product")

tree_value = ttk.Treeview(frame_value, columns=['Name', 'Quantity', 'Price', 'Total value'], show='headings')
tree_value.heading('Name', text='Product name')
tree_value.heading('Quantity', text="Quantity")
tree_value.heading('Price', text="Price (eur)")
tree_value.heading('Total value', text='Total value (eur)')
tree_value.pack(expand=True, fill='both')

showValue_btn = ttk.Button(frame_value, text="Show value", command=show_value)
showValue_btn.pack(pady=10)

frame_production = ttk.Frame(notebook)
notebook.add(frame_production, text="Production")

ttk.Label(frame_production, text="Choose product: ").pack()
combo_products = ttk.Combobox(frame_production, values=fill_products(), state="readonly")
combo_products.pack()

produce_btn = ttk.Button(frame_production, text="Produce", command=produce)
produce_btn.pack(pady=10)

root.mainloop()

conn.close()
