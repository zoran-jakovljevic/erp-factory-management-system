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

def show_product_stock():
    try:
        cursor = conn.cursor()
        query = "SELECT name, product_inventory.product_quantity FROM products INNER JOIN product_inventory ON products.product_id = product_inventory.product_id"
        cursor.execute(query)
        records = cursor.fetchall()

        for item in tree_stock.get_children():
            tree_stock.delete(item)

        for name, quantity in records:
            tree_stock.insert("", "end", values=(name, quantity))

        cursor.close()

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f'Error: {e}')

def show_profit():
    try:
        cursor = conn.cursor()
        query = "SELECT products.name, SUM(products.selling_price - materials.purchase_price) AS profit FROM sales JOIN products ON sales.product_id = products.product_id JOIN product_inventory ON product_inventory.product_id = sales.product_id JOIN material_products ON sales.product_id = material_products.product_id JOIN materials ON material_products.material_id = materials.material_id GROUP BY products.name"
        cursor.execute(query)
        records = cursor.fetchall()

        for item in tree_profit.get_children():
            tree_profit.delete(item)
        
        for name, profit in records:
            tree_profit.insert("", "end", values=(name, profit))

        cursor.close()

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f'Error: {e}')

def products_sale():
    try:
        chosen_product = combo_products.get()
        quantity = quantity_material.get()

        if not chosen_product or not quantity.isdigit():
            messagebox.showerror("Error", "Choose product and enter valid quantity")
            return
        
        quantity = int(quantity)

        cursor = conn.cursor()

        query_decrease_products = "UPDATE product_inventory SET product_quantity = product_quantity - %s WHERE product_id = (SELECT product_id FROM products WHERE name = %s)"
        cursor.execute(query_decrease_products, (quantity, chosen_product))

        query_add_transaction = "INSERT INTO sales (product_id, product_quantity, transaction_date) VALUES ((SELECT product_id FROM products WHERE name = %s), %s, NOW())"
        cursor.execute(query_add_transaction, (chosen_product, quantity))

        conn.commit()
        messagebox.showinfo("Info", "Transaction completed successfully")

        cursor.close()
        show_product_stock()
    
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error: {e}")


root = tk.Tk()
root.title("Sales application")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

frame_stock = ttk.Frame(notebook)
notebook.add(frame_stock, text="Stock level")

tree_stock = ttk.Treeview(frame_stock, columns=("Name", "Quantity"), show="headings")
tree_stock.heading("Name", text="Product name")
tree_stock.heading("Quantity", text="Quantity")
tree_stock.pack(expand=True, fill="both")

refresh_btn = ttk.Button(frame_stock, text = "Refresh", command=show_product_stock)
refresh_btn.pack(pady=10)

frame_profit = ttk.Frame(notebook)
notebook.add(frame_profit, text = "Profit per product")

tree_profit = ttk.Treeview(frame_profit, columns=("Name", "Profit"), show="headings")
tree_profit.heading("Name", text="Product name")
tree_profit.heading("Profit", text="Profit (eur)")
tree_profit.pack(expand=True, fill="both")

showProfit_btn = ttk.Button(frame_profit, text="Show profit", command=show_profit)
showProfit_btn.pack(pady=10)

frame_sales = ttk.Frame(notebook)
notebook.add(frame_sales, text="Products sale")

ttk.Label(frame_sales, text="Choose product:").pack(pady=5)
cursor = conn.cursor()
cursor.execute("SELECT name FROM products")
products = [row[0] for row in cursor.fetchall()]
combo_products = ttk.Combobox(frame_sales, values=products, state="readonly")
combo_products.pack()

ttk.Label(frame_sales, text="Enter quantity: ").pack(pady=5)
quantity_material = ttk.Entry(frame_sales)
quantity_material.pack()

sales_btn = ttk.Button(frame_sales, text="Sell", command=products_sale)
sales_btn.pack(pady=10)

root.mainloop()