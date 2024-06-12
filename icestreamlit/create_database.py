
import streamlit as st
import sqlite3

# Function to create a new SQLite database file
def create_database():
    with sqlite3.connect('icecream.db') as conn:
        pass  # Do nothing, connection is automatically closed

# Function to create tables in the database
def create_tables():
    with sqlite3.connect('icecream.db') as conn:
        c = conn.cursor()
    
    # Create table for seasonal flavor offerings
    c.execute('''CREATE TABLE IF NOT EXISTS flavors (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    seasonal BOOLEAN NOT NULL,
                    UNIQUE(name)
                )''')

    # Create table for ingredient inventory
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    UNIQUE(name)
                )''')

    # Create table for customer suggestions
    c.execute('''CREATE TABLE IF NOT EXISTS suggestions (
                    id INTEGER PRIMARY KEY,
                    flavor_id INTEGER NOT NULL,
                    suggestion TEXT NOT NULL,
                    FOREIGN KEY (flavor_id) REFERENCES flavors(id)
                )''')

    # Create table for allergy concerns
    c.execute('''CREATE TABLE IF NOT EXISTS allergens (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    UNIQUE(name)
                )''')

    # Create table to store relationships between flavors and allergens (many-to-many)
    c.execute('''CREATE TABLE IF NOT EXISTS flavor_allergens (
                    flavor_id INTEGER NOT NULL,
                    allergen_id INTEGER NOT NULL,
                    PRIMARY KEY (flavor_id, allergen_id),
                    FOREIGN KEY (flavor_id) REFERENCES flavors(id),
                    FOREIGN KEY (allergen_id) REFERENCES allergens(id)
                )''')

    # Create table for user's cart
    c.execute('''CREATE TABLE IF NOT EXISTS cart (
                    id INTEGER PRIMARY KEY,
                    flavor_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (flavor_id) REFERENCES flavors(id)
                )''')

    conn.commit()
    conn.close()

# Function to insert data for flavors
def insert_flavor(name, description, seasonal):
    try:
        conn = sqlite3.connect('icecream.db')
        c = conn.cursor()

        # Check if flavor with the same name already exists
        c.execute("SELECT COUNT(*) FROM flavors WHERE name = ?", (name,))
        count = c.fetchone()[0]

        if count == 0:
            # Flavor does not exist, insert new flavor
            c.execute("INSERT INTO flavors (name, description, seasonal) VALUES (?, ?, ?)", (name, description, seasonal))
            conn.commit()
            conn.close()
            st.success(f"Flavor '{name}' added successfully!")
        else:
            # Flavor with the same name already exists
            st.error(f"Flavor '{name}' already exists.")
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")

# Function to insert data for inventory items
def insert_inventory(name, quantity):
    conn = sqlite3.connect('icecream.db')
    c = conn.cursor()
    c.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (name, quantity))
    conn.commit()
    conn.close()


# Function to insert data for allergens
def insert_allergen(name):
    try:
        conn = sqlite3.connect('icecream.db')
        c = conn.cursor()

        # Check if allergen with the same name already exists
        c.execute("SELECT COUNT(*) FROM allergens WHERE name = ?", (name,))
        count = c.fetchone()[0]

        if count == 0:
            # Allergen does not exist, insert new allergen
            c.execute("INSERT INTO allergens (name) VALUES (?)", (name,))
            conn.commit()
            conn.close()
            st.success(f"Allergen '{name}' added successfully!")
        else:
            # Allergen with the same name already exists
            st.error(f"Allergen '{name}' already exists.")
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")


# Function to add flavor to the user's cart
def add_to_cart(flavor_id, quantity):
    conn = sqlite3.connect('icecream.db')
    c = conn.cursor()
    c.execute("INSERT INTO cart (flavor_id, quantity) VALUES (?, ?)", (flavor_id, quantity))
    conn.commit()
    conn.close()

# Function to remove flavor from the user's cart
def remove_from_cart(cart_id):
    conn = sqlite3.connect('icecream.db')
    c = conn.cursor()
    c.execute("DELETE FROM cart WHERE id = ?", (cart_id,))
    conn.commit()
    conn.close()

# Function to display user's cart
def display_cart():
    conn = sqlite3.connect('icecream.db')
    c = conn.cursor()
    c.execute('''SELECT cart.id, flavors.name, cart.quantity 
                 FROM cart 
                 JOIN flavors ON cart.flavor_id = flavors.id''')
    cart_items = c.fetchall()
    conn.close()
    return cart_items

# Function to display all flavors
def display_flavors():
    conn = sqlite3.connect('icecream.db')
    c = conn.cursor()
    c.execute("SELECT * FROM flavors")
    flavors = c.fetchall()
    conn.close()
    return flavors


# Streamlit application
def main():
    st.title("Ice Cream Parlor Cafe")
    st.markdown(
        """
        <style>
        .main_title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            color: #009688;
            padding: 20px;
            background-color: #f0f0f0;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .sidebar_title {
            font-size: 24px;
            font-weight: bold;
            color: #009688;
            padding: 10px;
            background-color: #f0f0f0;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .header {
            font-size: 20px;
            font-weight: bold;
            color: #009688;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .button {
            background-color: #009688;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            margin-top: 10px;
            margin-bottom: 10px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #00796b;
        }
        .success_message {
            color: #4caf50;
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .error_message {
            color: #f44336;
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;  /* Stretch from left to right */
            width: 100%;
            background-color: #009688;
            color: white;
            text-align: center;
            padding: 10px 0;
            z-index: 999;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create the database and tables
    create_database()
    create_tables()

    # Sidebar navigation
    page = st.sidebar.selectbox("Navigate", ["Add Flavor", "Add Inventory Item", "Add Allergen", "View Cart"])

    if page == "Add Flavor":
        st.markdown("<h2 class='header'>Add Flavor</h2>", unsafe_allow_html=True)
        name = st.text_input("Flavor Name")
        description = st.text_area("Description")
        seasonal = st.checkbox("Seasonal")
        if st.button("Add Flavor", key="add_flavor"):
            insert_flavor(name, description, seasonal)

    elif page == "Add Inventory Item":
        st.markdown("<h2 class='header'>Add Inventory Item</h2>", unsafe_allow_html=True)
        name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=0)
        if st.button("Add Inventory Item", key="add_inventory"):
            insert_inventory(name, quantity)

    elif page == "Add Allergen":
        st.markdown("<h2 class='header'>Add Allergen</h2>", unsafe_allow_html=True)
        name = st.text_input("Allergen Name")
        if st.button("Add Allergen", key="add_allergen"):
            insert_allergen(name)

    elif page == "View Cart":
        st.markdown("<h2 class='header'>View Cart</h2>", unsafe_allow_html=True)
        cart_items = display_cart()
        if cart_items:
            st.write("**Your Cart:**")
            for item in cart_items:
                st.write(f"- {item[1]}: {item[2]}")
                if st.button(f"Remove", key=f"remove_{item[0]}"):
                    remove_from_cart(item[0])
                    st.success("Item removed from cart.")
        else:
            st.write("Your cart is empty.")

        # Add option to add flavors to the cart
        st.markdown("<h3 class='header'>Add to Cart</h3>", unsafe_allow_html=True)
        flavors = display_flavors()
        flavor_names = [flavor[1] for flavor in flavors]
        selected_flavor = st.selectbox("Select Flavor", flavor_names)
        quantity = st.number_input("Quantity", min_value=1, value=1)
        flavor_id = flavors[flavor_names.index(selected_flavor)][0]
        if st.button("Add to Cart", key="add_to_cart"):
            add_to_cart(flavor_id, quantity)
            st.success(f"{quantity} {selected_flavor}(s) added to your cart.")

    # Footer
    st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #009688;
        color: white;
        text-align: center;
        padding: 10px 0;
        z-index: 999;
    }
    </style>
    <div class="footer">
        <p>@Deeksha</p>
        <p>Ice Cream Parlor Cafe - Enjoy your ice cream experience!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
