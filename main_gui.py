import tkinter as tk
from tkinter import messagebox
from db_functions import init_db, insert_sample_data
from db_functions import add_new_staff, issue_uniform, add_additional_order, update_staff_info, modify_inventory
from db_functions import query_uniforms_issued, query_reissue_eligible, query_additional_orders

# -------------------------------
# Database Initialization
# -------------------------------
conn, cursor = init_db()
insert_sample_data(conn, cursor)

# -------------------------------
# GUI Wrapper Functions
# -------------------------------
def add_staff_gui():
    add_new_staff(cursor, conn,
                  name_entry.get(),
                  role_entry.get(),
                  contact_details_entry.get(),
                  start_date_entry.get(),
                  eligibility_entry.get(),
                  uniform_issue_date_entry.get())
    messagebox.showinfo("Success", "New staff added successfully.")

def issue_uniform_gui():
    issue_uniform(cursor, conn,
                  staff_id_issue_entry.get(),
                  item_id_entry.get(),
                  quantity_entry.get(),
                  issue_date_entry.get(),
                  reissue_eligible_entry.get())
    messagebox.showinfo("Success", "Uniform issued successfully.")

def add_order_gui():
    add_additional_order(cursor, conn,
                         staff_id_order_entry.get(),
                         item_id_order_entry.get(),
                         quantity_order_entry.get(),
                         order_date_entry.get(),
                         paid_amount_entry.get())
    messagebox.showinfo("Success", "Additional uniform order added successfully.")

def update_staff_gui():
    update_staff_info(cursor, conn,
                      staff_id_update_entry.get(),
                      name_update_entry.get(),
                      role_update_entry.get(),
                      contact_details_update_entry.get())
    messagebox.showinfo("Success", "Staff information updated successfully.")

def modify_inventory_gui():
    modify_inventory(cursor, conn,
                     item_id_inventory_entry.get(),
                     quantity_inventory_entry.get(),
                     supplier_inventory_entry.get())
    messagebox.showinfo("Success", "Uniform inventory updated successfully.")

def report_uniforms():
    results = query_uniforms_issued(cursor)
    if results:
        output = "\n".join([f"{row[0]} | {row[1]} | Total Qty: {row[2]}" for row in results])
        messagebox.showinfo("Uniforms Issued", output)
    else:
        messagebox.showinfo("Uniforms Issued", "No uniforms issued yet.")

def report_reissue():
    results = query_reissue_eligible(cursor)
    if results:
        output = "\n".join([f"{row[0]} | {row[1]} | Issued: {row[2]}" for row in results])
        messagebox.showinfo("Reissue Eligible", output)
    else:
        messagebox.showinfo("Reissue Eligible", "No items eligible for reissue.")

def report_additional():
    results = query_additional_orders(cursor)
    if results:
        output = "\n".join([f"{row[0]} | {row[1]} | Total Qty: {row[2]} | Total Paid: ${row[3]:.2f}" for row in results])
        messagebox.showinfo("Additional Orders", output)
    else:
        messagebox.showinfo("Additional Orders", "No additional orders found.")

# -------------------------------
# Tkinter GUI
# -------------------------------
root = tk.Tk()
root.title("Uniform Distribution System")

# Set window size and background color
root.geometry("600x650")
root.config(bg="#F4F4F4")

# Font styles for buttons and labels
label_font = ("Helvetica", 12, "bold")
button_font = ("Helvetica", 10)

# --- Scrollable Frame ---
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# Configure the canvas and scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Update scrollable area when the content changes
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_frame_configure)

# --- Staff section ---
staff_frame = tk.Frame(scrollable_frame, bg="#F4F4F4")
staff_frame.grid(row=0, column=0, pady=10, padx=10, sticky="w")

tk.Label(staff_frame, text="Add New Staff", font=("Helvetica", 14, "bold"), bg="#F4F4F4").grid(row=0, column=0, pady=5, columnspan=2)
tk.Label(staff_frame, text="Name", font=label_font, bg="#F4F4F4").grid(row=1, column=0, sticky="w")
name_entry = tk.Entry(staff_frame, font=("Helvetica", 12), width=30)
name_entry.grid(row=1, column=1, pady=5)

tk.Label(staff_frame, text="Role", font=label_font, bg="#F4F4F4").grid(row=2, column=0, sticky="w")
role_entry = tk.Entry(staff_frame, font=("Helvetica", 12), width=30)
role_entry.grid(row=2, column=1, pady=5)

tk.Label(staff_frame, text="Contact Details", font=label_font, bg="#F4F4F4").grid(row=3, column=0, sticky="w")
contact_details_entry = tk.Entry(staff_frame, font=("Helvetica", 12), width=30)
contact_details_entry.grid(row=3, column=1, pady=5)

tk.Label(staff_frame, text="Start Date", font=label_font, bg="#F4F4F4").grid(row=4, column=0, sticky="w")
start_date_entry = tk.Entry(staff_frame, font=("Helvetica", 12), width=30)
start_date_entry.grid(row=4, column=1, pady=5)

tk.Label(staff_frame, text="Eligibility", font=label_font, bg="#F4F4F4").grid(row=5, column=0, sticky="w")
eligibility_entry = tk.Entry(staff_frame, font=("Helvetica", 12), width=30)
eligibility_entry.grid(row=5, column=1, pady=5)

tk.Label(staff_frame, text="Uniform Issue Date", font=label_font, bg="#F4F4F4").grid(row=6, column=0, sticky="w")
uniform_issue_date_entry = tk.Entry(staff_frame, font=("Helvetica", 12), width=30)
uniform_issue_date_entry.grid(row=6, column=1, pady=5)

tk.Button(staff_frame, text="Add New Staff", font=button_font, bg="#4CAF50", fg="white", command=add_staff_gui).grid(row=7, column=0, columnspan=2, pady=10)

# --- Issue Uniform section ---
issue_uniform_frame = tk.Frame(scrollable_frame, bg="#F4F4F4")
issue_uniform_frame.grid(row=1, column=0, pady=10, padx=10, sticky="w")

tk.Label(issue_uniform_frame, text="Issue Uniform", font=("Helvetica", 14, "bold"), bg="#F4F4F4").grid(row=0, column=0, pady=5, columnspan=2)
tk.Label(issue_uniform_frame, text="Staff ID", font=label_font, bg="#F4F4F4").grid(row=1, column=0, sticky="w")
staff_id_issue_entry = tk.Entry(issue_uniform_frame, font=("Helvetica", 12), width=30)
staff_id_issue_entry.grid(row=1, column=1, pady=5)

tk.Label(issue_uniform_frame, text="Item ID", font=label_font, bg="#F4F4F4").grid(row=2, column=0, sticky="w")
item_id_entry = tk.Entry(issue_uniform_frame, font=("Helvetica", 12), width=30)
item_id_entry.grid(row=2, column=1, pady=5)

tk.Label(issue_uniform_frame, text="Quantity", font=label_font, bg="#F4F4F4").grid(row=3, column=0, sticky="w")
quantity_entry = tk.Entry(issue_uniform_frame, font=("Helvetica", 12), width=30)
quantity_entry.grid(row=3, column=1, pady=5)

tk.Label(issue_uniform_frame, text="Issue Date", font=label_font, bg="#F4F4F4").grid(row=4, column=0, sticky="w")
issue_date_entry = tk.Entry(issue_uniform_frame, font=("Helvetica", 12), width=30)
issue_date_entry.grid(row=4, column=1, pady=5)

tk.Label(issue_uniform_frame, text="Reissue Eligible (Yes/No)", font=label_font, bg="#F4F4F4").grid(row=5, column=0, sticky="w")
reissue_eligible_entry = tk.Entry(issue_uniform_frame, font=("Helvetica", 12), width=30)
reissue_eligible_entry.grid(row=5, column=1, pady=5)

tk.Button(issue_uniform_frame, text="Issue Uniform", font=button_font, bg="#4CAF50", fg="white", command=issue_uniform_gui).grid(row=6, column=0, columnspan=2, pady=10)

# --- Additional Uniform Orders section ---
add_order_frame = tk.Frame(scrollable_frame, bg="#F4F4F4")
add_order_frame.grid(row=2, column=0, pady=10, padx=10, sticky="w")

tk.Label(add_order_frame, text="Add Additional Order", font=("Helvetica", 14, "bold"), bg="#F4F4F4").grid(row=0, column=0, pady=5, columnspan=2)
tk.Label(add_order_frame, text="Staff ID", font=label_font, bg="#F4F4F4").grid(row=1, column=0, sticky="w")
staff_id_order_entry = tk.Entry(add_order_frame, font=("Helvetica", 12), width=30)
staff_id_order_entry.grid(row=1, column=1, pady=5)

tk.Label(add_order_frame, text="Item ID", font=label_font, bg="#F4F4F4").grid(row=2, column=0, sticky="w")
item_id_order_entry = tk.Entry(add_order_frame, font=("Helvetica", 12), width=30)
item_id_order_entry.grid(row=2, column=1, pady=5)

tk.Label(add_order_frame, text="Quantity Ordered", font=label_font, bg="#F4F4F4").grid(row=3, column=0, sticky="w")
quantity_order_entry = tk.Entry(add_order_frame, font=("Helvetica", 12), width=30)
quantity_order_entry.grid(row=3, column=1, pady=5)

tk.Label(add_order_frame, text="Order Date", font=label_font, bg="#F4F4F4").grid(row=4, column=0, sticky="w")
order_date_entry = tk.Entry(add_order_frame, font=("Helvetica", 12), width=30)
order_date_entry.grid(row=4, column=1, pady=5)

tk.Label(add_order_frame, text="Paid Amount", font=label_font, bg="#F4F4F4").grid(row=5, column=0, sticky="w")
paid_amount_entry = tk.Entry(add_order_frame, font=("Helvetica", 12), width=30)
paid_amount_entry.grid(row=5, column=1, pady=5)

tk.Button(add_order_frame, text="Add Additional Order", font=button_font, bg="#4CAF50", fg="white", command=add_order_gui).grid(row=6, column=0, columnspan=2, pady=10)

# --- Report Buttons --- 
report_frame = tk.Frame(scrollable_frame, bg="#F4F4F4")
report_frame.grid(row=3, column=0, pady=10, padx=10, sticky="w")

tk.Label(report_frame, text="Reports", font=("Helvetica", 14, "bold"), bg="#F4F4F4").grid(row=0, column=0, pady=5)

tk.Button(report_frame, text="Uniforms Issued", font=button_font, bg="#007BFF", fg="white", command=report_uniforms).grid(row=1, column=0, pady=5)
tk.Button(report_frame, text="Reissue Eligibility", font=button_font, bg="#007BFF", fg="white", command=report_reissue).grid(row=2, column=0, pady=5)
tk.Button(report_frame, text="Additional Orders", font=button_font, bg="#007BFF", fg="white", command=report_additional).grid(row=3, column=0, pady=5)

# --- Start GUI ---
root.mainloop()

# Close DB connection on exit
conn.close()
