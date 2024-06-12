#ICE CREAM PARLOR CAFE

Welcome to the Ice Cream Parlor Cafe! This Streamlit application lets you manage your ice cream parlor's flavor options, inventory items, allergens, and user carts.

## FEATURES

-Add Flavor: Easily add new ice cream flavors with descriptions and seasonal availability.
-Add Inventory Item: Keep track of your inventory by adding new items and their quantities.
-Add Allergen: Manage allergens by adding new allergens to your system.
-View Cart: View and manage user carts, allowing them to add flavors and quantities.

## SETUP

-Clone this repository to your local machine:
```
git clone <repository>
```

-Run the Streamlit application:
```
streamlit run create_database.py
```

## DEPENDENCIES

-Streamlit: Open-source app framework for Machine Learning and Data Science projects.
-SQLite: Self-contained, serverless, zero-configuration, transactional SQL database engine.
-Python: Programming language used to develop the application.

## DOCKER COMMANDS

```
docker build -t ice-cream-app .
```
```
docker run -it -p 8501:8501 ice-cream-app
```

## VIEW STREAMLIT APP IN BROWSER

Local URL: http://localhost:8501
Network URL: http://172.17.0.2:8501
External URL: http://157.45.142.4:8501
