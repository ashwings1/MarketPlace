# MarketPlace

# Flask E-Commerce Platform
This is a Flask-based web application for an e-commerce platform. Users can register, log in, view products, publish products (if they're sellers), and perform various other actions related to managing their account and products.

## Setup
Clone this repository to your local machine.
Make sure Python has been installed.
Install Flask using 
```
pip install Flask
```

## Dependencies
- Flask
- SQLite3

## Usage
Run the following command in your terminal:
```
python3 app.py
```
Access the application through a web browser at http://localhost:5000.

## File Structure
- main.html: Main landing page HTML template.

- checkseller.html: HTML template for seller information page.

- checkinfo.html: HTML template for user information page.

- products.html: HTML template for displaying products.

- publishseller.html: HTML template for sellers to publish products.

- app.py: Main Flask application file containing all the routes and logic.

## Note
Passwords are hashed and salted for security.
The application uses SQLite for the database.
