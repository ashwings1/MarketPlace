from flask import Flask, render_template, request, session
import sqlite3 as sql
import hashlib
import uuid
import random

app = Flask(__name__)
app.secret_key = "super secret key"
# Main page user sees
@app.route('/')
def main():
    return render_template('main.html')

# Login check 
@app.route('/login',methods=['GET','POST'])
def check_login():
    errormess = ''
    connection = sql.connect('sqlite (3).db')

    # Check for request by user
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Get the username and password values
        username=request.form['username']
        password=request.form['password']

        # Use hash and salt to protect user passwords
        salt = uuid.uuid4().hex
        hashPassword=hashlib.sha512((password + salt).encode('utf-8'))
        print('Hash',hashPassword.hexdigest())

        # Check if account exists
        cursor=connection.execute('SELECT * FROM Users WHERE email = ? AND password = ?', (username, password,))

        # To check if whether account exists or not
        account = cursor.fetchone()
        if account:
            session['login'] = True
            session['username'] = account[0]
            session['password'] = account[1]

            cursorCheck = connection.execute('SELECT * FROM Sellers WHERE email = ?', (username,))

            # Check if seller or buyer
            if cursorCheck.fetchone():
                return render_template('checkseller.html', username=session['username'])
            else:
                return render_template('checkinfo.html', username=session['username'])
        else:
            errormess = 'Incorrect email or password'
            return errormess

# Find correct information for user
def show_info():
    username = session['username']

    connection = sql.connect('sqlite (3).db')
    cursor = connection.execute('SELECT * FROM Buyers WHERE email=?;', (username,))
    return cursor.fetchall()

# Find correct credit card for user
def show_card():
    username = session['username']

    connection = sql.connect('sqlite (3).db')
    cursor = connection.execute('SELECT SUBSTR(credit_card_num,1,4) FROM Credit_Cards WHERE owner_email=?;', (username,))
    return cursor.fetchall()

# Show buyer info
@app.route('/checkinfo',methods=['GET','POST'])
def check_info():
    result = show_info()
    result2 = show_card()
    return render_template('checkinfo.html', result=result, result2=result2)

# Show seller info
@app.route('/checkinfoseller',methods=['GET','POST'])
def check_infoseller():
    result = show_info()
    result2 = show_card()
    return render_template('checkseller.html', result=result, result2=result2)

# Change password
@app.route('/changepass',methods=['GET','POST'])
def change_pass():
    username = session['username']
    password = request.form['password']

    connection = sql.connect('sqlite (3).db')
    connection.execute('UPDATE Users SET Password = ? WHERE email = ?', (password, username))
    connection.commit()
    return 'Password successfully changed'

# Go to Products page
@app.route('/gotoproducts')
def go_product():
    return render_template('products.html')

# Go to Publish Seller page
@app.route('/publishproducts')
def go_publishseller():
    return render_template('publishseller.html')

# Publish Products
@app.route('/publishproduct',methods=['GET','POST'])
def publish_product():
    username = session['username']
    if request.method == 'POST' and 'category' in request.form and 'title' in request.form and 'name' in request.form and 'description' in request.form and 'price' in request.form and 'quantity' in request.form:
        # Get values from input fields
        categoryProd = request.form['category']
        titleProd = request.form['title']
        nameProd = request.form['name']
        descriptionProd = request.form['description']
        priceProd = request.form['price']
        quantityProd = request.form['quantity']

        listid = random.randint(1, 1000)

        connection = sql.connect('sqlite (3).db')
        cursor = connection.execute('INSERT INTO Product_Listings (seller_email, listing_id, category, title, product_name, product_description, price, quantity) VALUES (?,?,?,?,?,?,?,?);',(username, listid, categoryProd, titleProd, nameProd, descriptionProd, priceProd, quantityProd,))
        checklisting = cursor.fetchall()
        connection.commit()
        if checklisting != None:
            result = show_product()
            if result:
                return render_template('publishseller.html', result=result)
        else:
            return 'Product error'

# Shows product information in a table
@app.route('/showproduct',methods=['GET','POST'])
def show_table():
    result = show_product()
    if result:
        return render_template('publishseller.html', result=result)

# Select Seller Products
def show_product():
    username = session['username']

    connection = sql.connect('sqlite (3).db')
    cursor = connection.execute('SELECT * FROM Product_Listings WHERE Active=TRUE and Seller_Email=?;', (username,))
    return cursor.fetchall()

# Select parent catalog of products
def show_catalog():
    connection = sql.connect('sqlite (3).db')
    cursor = connection.execute('SELECT DISTINCT parent_category FROM Categories;')
    return cursor.fetchall()

# View catalog of products
@app.route('/viewcatalog',methods=['GET','POST'])
def view_catalog():
    result = show_catalog()
    if result:
        return render_template('products.html', result=result)

# Select subcatalog of Parent
def show_subcatalog():
    parentcategoryProd = request.form['parentCategory']
    connection = sql.connect('sqlite (3).db')
    cursor = connection.execute('SELECT category_name FROM Categories WHERE parent_category=?;', (parentcategoryProd,))
    return cursor.fetchall()

# View subcatalog of products
@app.route('/viewsubcatalog',methods=['GET','POST'])
def view_subcatalog():
    result = show_subcatalog()
    if result:
        return render_template('products.html', result=result)
    else:
        return "Empty"

# Show correct products of subcatalog
def show_correctproduct():
    parentcategoryProd = request.form['subCategory']

    connection = sql.connect('sqlite (3).db')

    cursor = connection.execute('SELECT seller_email, category, title, product_name, product_description, price, quantity FROM Product_Listings WHERE Active=TRUE and Category=? COLLATE NOCASE;',(parentcategoryProd,))
    return cursor.fetchall()

# View correct products subcatalog
@app.route('/correctproducts',methods=['GET','POST'])
def view_correctproduct():
    result = show_correctproduct()
    if result:
        return render_template('checkProd.html', result=result)
    else:
        return "Empty"

# Delete Products
@app.route('/deleteproduct',methods=['GET','POST'])
def delete_product():
    username = session['username']
    if request.method == 'POST' and 'deleteID' in request.form:

        listid = request.form['deleteID']

        connection = sql.connect('sqlite (3).db')

        # Update Active column to False when removing product
        connection.execute('UPDATE Product_Listings SET ACTIVE=FALSE WHERE Seller_Email=? AND Listing_ID=?',
                           (username, listid))
        connection.commit()
        result = show_product()
        if result:
            return render_template('publishseller.html', result=result)

# Select inactive product
def show_inactive():
    username = session['username']

    connection = sql.connect('sqlite (3).db')
    cursor = connection.execute('SELECT * FROM Product_Listings WHERE Active=FALSE and Seller_Email=?;', (username,))
    return cursor.fetchall()

# Show inactive product
@app.route('/showinactive',methods=['GET','POST'])
def show_inactivetable():
    result = show_inactive()
    if result:
        return render_template('publishseller.html', result=result)

# Goes back to User information page
@app.route('/back')
def backpage():
    return render_template('checkseller.html')

# Logs out user
@app.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('username', None)
    session.pop('password', None)
    return render_template('main.html')

if __name__ == '__main__':

    app.run()

