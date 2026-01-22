# db_functions.py
import sqlite3

DB_FILE = 'uniform_distribution.db'

# -------------------------------
# Database setup
# -------------------------------
def init_db():
    """Initialize the SQLite database and tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Staff table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Staff (
        Staff_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Role TEXT,
        Contact_Details TEXT,
        Start_Date TEXT,
        Eligibility TEXT,
        Uniform_Issue_Date TEXT
    )
    """)

    # Uniform_Items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Uniform_Items (
        Item_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Item_Type TEXT,
        Size_Options TEXT,
        Quantity_Available INTEGER,
        Supplier TEXT
    )
    """)

    # Uniform_Issues table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Uniform_Issues (
        Issue_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Staff_ID INTEGER,
        Item_ID INTEGER,
        Quantity_Issued INTEGER,
        Issue_Date TEXT,
        Reissue_Eligible INTEGER,
        FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID),
        FOREIGN KEY (Item_ID) REFERENCES Uniform_Items(Item_ID)
    )
    """)

    # Additional_Uniform_Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Additional_Uniform_Orders (
        Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Staff_ID INTEGER,
        Item_ID INTEGER,
        Quantity_Ordered INTEGER,
        Order_Date TEXT,
        Paid_Amount REAL,
        FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID),
        FOREIGN KEY (Item_ID) REFERENCES Uniform_Items(Item_ID)
    )
    """)

    conn.commit()
    return conn, cursor


# -------------------------------
# Sample Data
# -------------------------------
def insert_sample_data(conn, cursor):
    """Insert initial sample data if table is empty."""
    cursor.execute("SELECT COUNT(*) FROM Staff")
    if cursor.fetchone()[0] == 0:

        # -------------------------------
        # Staff (5 records)
        # -------------------------------
        staff_data = [
            ('John Doe', 'Doctor', '555-1234', '2021-05-10', 'Yes', '2021-05-15'),
            ('Sarah Khan', 'Nurse', '555-2345', '2022-02-01', 'Yes', '2022-02-05'),
            ('Ali Ahmed', 'Surgeon', '555-3456', '2020-08-15', 'Yes', '2020-08-20'),
            ('Emma Wilson', 'Physiotherapist', '555-4567', '2023-01-10', 'Yes', '2023-01-15'),
            ('David Smith', 'Radiographer', '555-5678', '2021-11-01', 'No', None)
        ]

        cursor.executemany('''
            INSERT INTO Staff (Name, Role, Contact_Details, Start_Date, Eligibility, Uniform_Issue_Date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', staff_data)

        # -------------------------------
        # Uniform_Items (5 records)
        # -------------------------------
        uniform_items = [
            ('Scrub Shirt', 'XS, S, M, L, XL', 50, 'Ferreira Ltd.'),
            ('Scrub Trousers', 'XS, S, M, L, XL', 40, 'MedWear Co.'),
            ('Lab Coat', 'S, M, L, XL', 30, 'HealthPro Supplies'),
            ('Theatre Gown', 'One Size', 25, 'SterileTex'),
            ('Nurse Tunic', 'XS, S, M, L', 35, 'CareUniforms Ltd.')
        ]

        cursor.executemany('''
            INSERT INTO Uniform_Items (Item_Type, Size_Options, Quantity_Available, Supplier)
            VALUES (?, ?, ?, ?)
        ''', uniform_items)

        # -------------------------------
        # Uniform_Issues (5 records)
        # -------------------------------
        uniform_issues = [
            (1, 1, 3, '2021-05-15', 1),
            (2, 2, 2, '2022-02-05', 1),
            (3, 3, 1, '2020-08-20', 0),
            (4, 4, 2, '2023-01-15', 1),
            (1, 2, 1, '2023-06-01', 0)
        ]

        cursor.executemany('''
            INSERT INTO Uniform_Issues (Staff_ID, Item_ID, Quantity_Issued, Issue_Date, Reissue_Eligible)
            VALUES (?, ?, ?, ?, ?)
        ''', uniform_issues)

        # -------------------------------
        # Additional_Uniform_Orders (5 records)
        # -------------------------------
        additional_orders = [
            (1, 1, 2, '2023-01-20', 30.00),
            (2, 2, 1, '2023-03-10', 15.00),
            (3, 3, 1, '2022-12-05', 20.00),
            (4, 4, 2, '2023-07-18', 40.00),
            (1, 5, 1, '2024-01-12', 18.00)
        ]

        cursor.executemany('''
            INSERT INTO Additional_Uniform_Orders (Staff_ID, Item_ID, Quantity_Ordered, Order_Date, Paid_Amount)
            VALUES (?, ?, ?, ?, ?)
        ''', additional_orders)

        conn.commit()
        print("Sample data inserted successfully!")



# -------------------------------
# Query Functions
# -------------------------------
def query_uniforms_issued(cursor):
    cursor.execute('''
        SELECT Staff.Name, Uniform_Items.Item_Type, SUM(Uniform_Issues.Quantity_Issued) AS Total_Quantity
        FROM Staff
        JOIN Uniform_Issues ON Staff.Staff_ID = Uniform_Issues.Staff_ID
        JOIN Uniform_Items ON Uniform_Issues.Item_ID = Uniform_Items.Item_ID
        GROUP BY Staff.Name, Uniform_Items.Item_Type
        ORDER BY Staff.Name ASC
    ''')
    return cursor.fetchall()


def query_reissue_eligible(cursor):
    cursor.execute('''
        SELECT Staff.Name, Uniform_Items.Item_Type, Uniform_Issues.Issue_Date
        FROM Staff
        JOIN Uniform_Issues ON Staff.Staff_ID = Uniform_Issues.Staff_ID
        JOIN Uniform_Items ON Uniform_Issues.Item_ID = Uniform_Items.Item_ID
        WHERE Uniform_Issues.Reissue_Eligible = 1
        AND Uniform_Issues.Issue_Date <= DATE('now', '-24 months')
        ORDER BY Uniform_Issues.Issue_Date ASC
    ''')
    return cursor.fetchall()


def query_additional_orders(cursor):
    cursor.execute('''
        SELECT Staff.Name, Uniform_Items.Item_Type, SUM(Additional_Uniform_Orders.Quantity_Ordered) AS Total_Ordered,
               SUM(Additional_Uniform_Orders.Paid_Amount) AS Total_Paid
        FROM Staff
        JOIN Additional_Uniform_Orders ON Staff.Staff_ID = Additional_Uniform_Orders.Staff_ID
        JOIN Uniform_Items ON Additional_Uniform_Orders.Item_ID = Uniform_Items.Item_ID
        GROUP BY Staff.Name, Uniform_Items.Item_Type
        ORDER BY Staff.Name ASC
    ''')
    return cursor.fetchall()


# -------------------------------
# Add / Update Functions
# -------------------------------
def add_new_staff(cursor, conn, name, role, contact, start_date, eligibility, uniform_date):
    cursor.execute('''
        INSERT INTO Staff (Name, Role, Contact_Details, Start_Date, Eligibility, Uniform_Issue_Date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, role, contact, start_date, eligibility, uniform_date))
    conn.commit()


def issue_uniform(cursor, conn, staff_id, item_id, quantity, issue_date, reissue_eligible):
    reissue_val = 1 if reissue_eligible.lower() in ('yes', 'true', '1') else 0
    cursor.execute('''
        INSERT INTO Uniform_Issues (Staff_ID, Item_ID, Quantity_Issued, Issue_Date, Reissue_Eligible)
        VALUES (?, ?, ?, ?, ?)
    ''', (staff_id, item_id, quantity, issue_date, reissue_val))
    conn.commit()


def add_additional_order(cursor, conn, staff_id, item_id, quantity, order_date, paid_amount):
    cursor.execute('''
        INSERT INTO Additional_Uniform_Orders (Staff_ID, Item_ID, Quantity_Ordered, Order_Date, Paid_Amount)
        VALUES (?, ?, ?, ?, ?)
    ''', (staff_id, item_id, quantity, order_date, paid_amount))
    conn.commit()


def update_staff_info(cursor, conn, staff_id, name, role, contact):
    cursor.execute('''
        UPDATE Staff
        SET Name = ?, Role = ?, Contact_Details = ?
        WHERE Staff_ID = ?
    ''', (name, role, contact, staff_id))
    conn.commit()


def modify_inventory(cursor, conn, item_id, quantity, supplier):
    cursor.execute('''
        UPDATE Uniform_Items
        SET Quantity_Available = ?, Supplier = ?
        WHERE Item_ID = ?
    ''', (quantity, supplier, item_id))
    conn.commit()
