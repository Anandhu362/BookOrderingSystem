import mysql.connector
import functions.database as functions
from flask import session
from flask import Flask, render_template, request, redirect, url_for, session, flash
import uuid
import re
from flask import make_response
import datetime

app = Flask(__name__)


app.secret_key = '12345678'
#app.config['SESSION_COOKIE_SECURE'] = True  # This ensures that session cookies are only sent over HTTPS


    
def connect_to_database():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Kaalan@123',
            database='bookorderingsystem'
        )
        
        return db, db.cursor()
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None, None
    
def is_logged_in():
    return session.get('logged_in', False)


@app.route('/')
def login_page():
    return render_template('index.html')  

@app.route('/adminindex')
def login_page1():
    return render_template('adminindex.html')  

@app.route('/home')
def home():
    # Check if the user is logged in
    
    if  is_logged_in():          
        db, cursor = connect_to_database()        
        books = []
        cursor.execute("select * from books")
        resultset = cursor.fetchall()
        
        for data in resultset:
            book = {
                "id":data[0],
                "title":data[1],
                "author":data[2],
                "description":data[3],
                "category":data[4],
                "price":data[5],
                "bgimgurl":data[6],
                "fgimgurl":data[7],
                "type":data[8]
            }
            books.append(book)

        all_books = books
        popularbooks=[]
        kidsbooks=[]
        magazine=[]
        students=[]
        for book in all_books:
            if book['type']=='POPULARBOOK':
                popularbooks.append(book)
            elif book['type']=='KIDS':
                kidsbooks.append(book)
            elif book['type']=='MAGAZINE':
                magazine.append(book)
            elif book['type']=='STUDENT':
                students.append(book)

        return render_template('home.html',userurl=session['user_url'], popularbooks=popularbooks,kidsbooks=kidsbooks,magazine=magazine,students=students)
    else:
        # If the user is not logged in, redirect to the login page
        flash('You need to login first.')
        return redirect(url_for('login_page'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  
        password = request.form.get('password')

        print("Attempting login with email:", email) 
        db, cursor = connect_to_database()

        query = "SELECT * FROM USERS WHERE Email = %s AND Password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            session['logged_in'] = True
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            user_id = cursor.fetchone()
            if user_id:
                session['user_id'] = user_id[0]
            print(user_id)
            cursor.execute("SELECT userurl FROM users WHERE email = %s", (email,))
            user_url = cursor.fetchone()
            if user_url:            
                session['user_url'] = user_url[0]
            #session['user_id'] = user_id  # Store the user ID in the session
            print(session['user_id'])
            if session['logged_in'] == True:
                print("User logged in successfully!")
            # Authentication successful, redirect to the home page
            return redirect(f'/home')
        else:
            # If authentication fails, redirect back to login page or handle accordingly
            flash('Invalid email or password.')
            print("User login failed.")
            return redirect(url_for('login_page'))
    
    return render_template('Bookify-signup/index.html',error='Login failed. Please check your username and password.')


@app.route('/adminlogin', methods=['POST'])
def adminlogin():
    if request.method == 'POST':
        adminid= request.form.get('adminid')  
        password = request.form.get('password')

        print("Attempting login with adminid:",adminid) 
        db, cursor = connect_to_database()
        
        if adminid == 'admin' and password == 'admin123':
            return redirect(f'/adminportal')
        else:
            flash('Invalid Admin Credentials')
        return redirect(f'/')
    

        
@app.route('/adminportal')
def adminlportal():
    
    return render_template('adminportal.html',error='Login failed. Please check your username and password.')
        


@app.route('/add_book', methods=['POST'])
def add_book():
    db, cursor = connect_to_database()
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        category = request.form.get('category')
        price = request.form.get('price')
        bgimgurl = request.form.get('bgimgurl')
        fgimgurl = request.form.get('fgimgurl')
        book_type = request.form.get('type')
        
        # Assuming you have a function to handle database insertion
        # Insert the data into the 'books' table
        cursor.execute("INSERT INTO books (TITLE, AUTHOR, DESCRIPTION, CATEGORY, PRICE, BGIMGURL, FGIMGURL, TYPE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (title, author, description, category, price, bgimgurl, fgimgurl, book_type))
        db.commit()
        
        flash('Book added successfully!', 'success')  # Flash message
        
        return render_template('adminportal.html')  # Render the admin portal page
    else:
        return "Book not added"





@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')  
        email = request.form.get('email') 
        password = request.form.get('password')
        userurl = request.form.get('userurl')  
        db, cursor = connect_to_database()

        # Check if username already exists
        cursor.execute("SELECT * FROM USERS WHERE NAME = %s", (name,))
        existing_username = cursor.fetchone()
        if existing_username:
            flash('Username already exists.')
            return redirect(url_for('login_page'))

        # Check if email is valid and already exists
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            flash('Invalid email address.')
            return redirect(url_for('login_page'))
        cursor.execute("SELECT * FROM USERS WHERE EMAIL = %s", (email,))
        existing_email = cursor.fetchone()
        if existing_email:
            flash('Email already exists.')
            return redirect(url_for('login_page'))

        # Validate password strength
        if not re.match(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$%!]).{8,}$', password):
            flash('Password must contain at least one uppercase letter, one digit, and one special character (@, #, $, %, or !), and be at least 8 characters long.')
            flash('Please provide Valid name')
            flash('Please Provide proper domain')
            return redirect(url_for('login_page'))

        # Check if userurl already exists
        cursor.execute("SELECT * FROM USERS WHERE USERURL = %s", (userurl,))
        existing_userurl = cursor.fetchone()
        if existing_userurl:
            flash('User URL already exists.')
            return redirect(url_for('login_page'))

        # Generate a unique ID using UUID
        user_id = str(uuid.uuid4())

        cursor.execute("INSERT INTO USERS (USER_ID, NAME, EMAIL, PASSWORD, USERURL) VALUES (%s, %s, %s, %s, %s)", (user_id, name, email, password, userurl))
        db.commit()

        return redirect(f'/home')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id',None)
    return redirect(url_for('login_page'))


@app.route('/description')
def book_details():
    book_id = int(request.args.get('id'))   
    db, cursor = connect_to_database() 
    books = []

    cursor.execute("select * from books")
    resultset = cursor.fetchall()
    print(resultset)
    for data in resultset:
        book = {
            "id":data[0],
            "title":data[1],
            "author":data[2],
            "description":data[3],
            "category":data[4],
            "price":data[5],
            "bgimgurl":data[6],
            "fgimgurl":data[7],
            "type":data[8]
        }
        books.append(book)

    all_books = books



    popularbooks=[]
    kidsbooks=[]
    magazine=[]
    students=[]
    user_id = session['user_id']

    for book in all_books:
        if book['type']=='POPULARBOOK':
            popularbooks.append(book)
        elif book['type']=='KIDS':
            kidsbooks.append(book)
        elif book['type']=='MAGAZINE':
            magazine.append(book)
        elif book['type']=='STUDENT':
            students.append(book)

    
    
    cursor.execute("select * from cart where user_id= %s", (user_id,))
    cartcount =  len(cursor.fetchall())



    index=0
    for book in all_books:
        if int( book['id'])== int(book_id):
            index=all_books.index(book)
    item = all_books[index]
    if item['type'] == 'MAGAZINE':
        return render_template('subdescription.html',all_books=all_books,popularbooks=popularbooks,kidsbooks=kidsbooks,magazine=magazine,students=students,item=index,id=book_id,cartcount=cartcount, userurl = session['user_url'])
    return render_template('description.html',all_books=all_books,popularbooks=popularbooks,kidsbooks=kidsbooks,magazine=magazine,students=students,item=index,id=book_id,cartcount=cartcount, userurl = session['user_url'])

@app.route('/cart')
def cart():
    user_id = session['user_id']
    db, cursor = connect_to_database()
    data = []
    cursor.execute("SELECT BOOKID FROM CART WHERE USER_ID = %s", (user_id,))
    ids = [int(book[0]) for book in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM BOOKS")#change popular name
    bookdetails = cursor.fetchall()

    for bid in ids:
        for book in bookdetails:
            if int(book[0])==int(bid):
                data.append({
                    "id":book[0],
                    "title":book[1],
                    "author":book[2],
                    "description":book[3],
                    "category":book[4],
                    "price":book[5],
                    "url":book[7],
                })
    
    
    
    cursor.execute("select * from cart where user_id= %s", (user_id,))
    cartcount = len(cursor.fetchall())



    total = 0
    for item in data:
        total+=item['price']
        
    return render_template('checkout.html',data=data,cartcount=cartcount,total=total, userurl = session['user_url'])

@app.route('/subcheckout')
def subcheckout():
    db, cursor = connect_to_database()
    book_id = request.args.get('id')
    user_id = session["user_id"]
    # cursor.execute("SELECT BOOKID FROM SUBCHECKOUT WHERE USER_ID = %s", (user_id,))
    # ids = [book[0] for book in cursor.fetchall()]
    # if book_id in ids:
    #     print("Already Subscribed")
    #     flash('Already Subscribed')
    # else:
    cursor.execute("INSERT INTO SUBCHECKOUT (bookid, user_id) VALUES (%s, %s)", (book_id, user_id))

    db.commit()
    user_id = session['user_id']
    db, cursor = connect_to_database()
    data = []
    cursor.execute("SELECT BOOKID FROM SUBCHECKOUT WHERE USER_ID = %s", (user_id,))
    ids = [book[0] for book in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM BOOKS")#change popular name
    bookdetails = cursor.fetchall()

    for bid in ids:
        for book in bookdetails:
            if book[0]==bid:
                data.append({
                    "id":book[0],
                    "title":book[1],
                    "author":book[2],
                    "description":book[3],
                    "category":book[4],
                    "price":book[5],
                    "url":book[7],
                })
    
    
    cursor.execute("select * from cart where user_id= %s", (user_id,))
    cartcount = len(cursor.fetchall())



    total = 0
    for item in data:
        total+=item['price']
        
    return render_template('subcheckout.html',data=data,cartcount=cartcount,total=total, userurl = session['user_url'])


@app.route('/addbook')
def addbook():
    book_id = request.args.get('id')
    user_id = session["user_id"]
    db, cursor = connect_to_database()
    
    cursor.execute("SELECT BOOKID FROM CART WHERE USER_ID = %s", (user_id,))
    ids = [int(book[0]) for book in cursor.fetchall()]
    if int(book_id) in ids:
        print("Already in Cart")
        flash('Already in Cart')
    else:
        cursor.execute("INSERT INTO CART (bookid, user_id) VALUES (%s, %s)", (book_id, user_id))
      
        db.commit()

    return redirect(f'/description?id={book_id}')

@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    item_id = request.form.get("item_id")
    print("Received form data:", request.form)
    print("Received item_id:", item_id)
    user_id = session['user_id']
    db, cursor = connect_to_database()

    # Check if username already exists
    sql = "DELETE FROM cart WHERE bookid = %s and user_id = %s"
    cursor.execute(sql, (item_id,user_id,))
    
    print("deleted Succesfully")
    db.commit()
    db.close()
    return redirect(url_for('cart'))


@app.route("/remove_from_subcheckout", methods=["POST"])
def remove_from_subcheckout():
    item_id = request.form.get("item_id")
    print("Received form data:", request.form)
    print("Received item_id:", item_id)
    user_id = session['user_id']
    db, cursor = connect_to_database()

    # Check if username already exists
    sql = "DELETE FROM SUBCHECKOUT WHERE bookid = %s and user_id = %s LIMIT 1"
    cursor.execute(sql, (item_id,user_id,))
    
    print("Deleted Succesfully")
    db.commit()
    db.close()
    return redirect(url_for('subcheckout'))






@app.route('/update_email', methods=['POST'])
def update_email():
    if request.method == 'POST':
        new_email = request.form.get('new_email')  # Get the new email from the form
        user_id = session.get('user_id')  # Get the user ID from the session
        
        # Check if user_id exists in the session
        if user_id:
            # Update the user's email in the database
            db, cursor = connect_to_database()
            cursor.execute("UPDATE users SET email = %s WHERE user_id = %s", (new_email, user_id))
            db.commit()  # Commit the transaction
            
            # Optionally, update the session with the new email
            session['user_email'] = new_email
            flash('Email Successfully Updated')
            # Redirect to the account page or any other appropriate page
            return redirect(url_for('account'))
        else:
            # Handle the case where the user is not logged in
            flash('User not logged in.')
            return redirect(url_for('login_page'))
        

@app.route('/update_url', methods=['POST'])
def update_url():
    if request.method == 'POST':
        new_url = request.form.get('new_url')  # Get the new email from the form
        user_id = session.get('user_id')  # Get the user ID from the session
        
        # Check if user_id exists in the session
        if user_id:
            # Update the user's email in the database
            db, cursor = connect_to_database()
            cursor.execute("UPDATE users SET userurl = %s WHERE user_id = %s", (new_url, user_id))
            db.commit()  # Commit the transaction
            
            # Optionally, update the session with the new email
            session['user_url'] = new_url
            flash('Email Successfully Updated')
            # Redirect to the account page or any other appropriate page
            return redirect(url_for('account'))
        else:
            # Handle the case where the user is not logged in
            flash('User not logged in.')
            return redirect(url_for('login_page'))




@app.route('/placeorder', methods=['POST'])
def placeorder():
    db, cursor = connect_to_database()
    if request.method == 'POST':
        address = request.form.get('address')  
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        
        
    user_id = session['user_id']
    
    
    cursor.execute(" delete from subcheckout where bookid IS NULL;")
    cursor.execute("SELECT BOOKID FROM CART")
    ids = [int(book[0]) for book in cursor.fetchall()]
    today_date = datetime.date.today().strftime('%Y-%m-%d')
    print(today_date)
    add = name + ",\n" + address + ",\n" + city + ", " + state + ",\n" + zipcode
    
    for bid in ids:
        print(bid)
        cursor.execute(f"INSERT INTO ORDERS  VALUES({bid},'{today_date}','{user_id}','{add}')")
        db.commit()
    
    cursor.execute("DELETE FROM CART")
    db.commit()

    return render_template("placed.html", userurl = session['user_url'])


@app.route('/placesub', methods=['POST'])
def placesub():
    if request.method == 'POST':
        address = request.form.get('address')  
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
    print(address)
    db, cursor = connect_to_database()
    cursor.execute(" delete from subcheckout where bookid IS NULL;")
    user_id = session['user_id']
    cursor.execute("SELECT BOOKID FROM SUBCHECKOUT")
    ids = [int(book[0]) for book in cursor.fetchall()]
    today_date = datetime.date.today().strftime('%Y-%m-%d')
    print(today_date)
    add = name + "\n" + address + "\n" + city + ", " + state + "\n" + zipcode
    print(add,user_id)
    for bid in ids:
        print(bid)
        cursor.execute("INSERT INTO SUBSCRIPTIONS (BOOKID, PURCHASEDDATE, USER_ID, ADDRESS) VALUES (%s, %s, %s, %s)",(bid, today_date, user_id, address))
        
        db.commit()
    
    cursor.execute("DELETE FROM SUBCHECKOUT")
    db.commit()
    return render_template("placed.html", userurl = session['user_url'])

@app.route('/pay', methods=['POST'])
def pay():
    
        
    return render_template("pay.html")


@app.route('/subpay', methods=['POST'])
def subpay():
    return render_template("subpay.html")


@app.route('/orders')
def orders():
    db, cursor = connect_to_database()
    user_id = session['user_id']
    
    data = []
    cursor.execute("SELECT * FROM ORDERS WHERE USER_ID = %s ", (user_id,))

    #ids = [int(book[0]) for book in cursor.fetchall()]
    orders = cursor.fetchall()
    
    cursor.execute("SELECT * FROM BOOKS")#change popular name
    bookdetails = cursor.fetchall()

    date_format = "%Y-%m-%d"

    for order in orders:
        for book in bookdetails:
            if int(book[0])==int(order[0]):
                purchased_date = order[1]#datetime.datetime.strptime(order[1], date_format)
                address = order[3]
                today = datetime.date.today()#datetime.datetime.strptime(datetime.date.today(), date_format)
                time_difference = today - purchased_date
                difference_in_days = time_difference.days

                print(difference_in_days)
                estimated_date= purchased_date + datetime.timedelta(days=7)
                if difference_in_days>=7:
                    status="Delivered"
                elif difference_in_days>=5:
                    status="Out for delivery"
                elif difference_in_days>=3:
                    status="Shipped"
                else:
                    status="Ordered"


                print(purchased_date)
                print(today)
                data.append({
                    "id":book[0],
                    "title":book[1],
                    "author":book[2],
                    "description":book[3],
                    "category":book[4],
                    "price":book[5],
                    "url":book[7],
                    "status":status,
                    "estimated_date":estimated_date,
                    "address":address,
                })

    book_data = data



    return render_template("orders.html",books_data=book_data, userurl = session['user_url'])

@app.route("/removesubscription", methods=['POST'])
def remove_subscription():
    user_id = request.form.get('userid')
    book_id = request.form.get('bookid')
    print("Hello")
    print(user_id)
    print(book_id)
    if user_id and book_id:
        db, cursor = connect_to_database()
        query = "DELETE FROM subscriptions WHERE user_id=%s AND bookid=%s LIMIT 1"
        cursor.execute(query, (user_id, book_id))
        db.commit()
        cursor.close()
        db.close()
    
    return redirect(url_for('subscriptions'))


@app.route('/subscriptions')
def subscriptions():
    user_id = session['user_id']
    
    db, cursor = connect_to_database()
    
    data = []
    cursor.execute("SELECT * FROM SUBSCRIPTIONS WHERE USER_ID  =%s",(user_id,))
    #ids = [int(book[0]) for book in cursor.fetchall()]
    orders = cursor.fetchall()
    
    cursor.execute("SELECT * FROM BOOKS")#change popular name
    bookdetails = cursor.fetchall()

    date_format = "%Y-%m-%d"

    for order in orders:
        for book in bookdetails:
            if int(book[0])==int(order[0]):
                purchased_date = order[1]#datetime.datetime.strptime(order[1], date_format)
                today = datetime.date.today()#datetime.datetime.strptime(datetime.date.today(), date_format)
                time_difference = today - purchased_date
                difference_in_days = time_difference.days

                print(difference_in_days)
                estimated_date= purchased_date + datetime.timedelta(days=7)
                if difference_in_days>=7:
                    status="Latest Edition Delivered"
                elif difference_in_days>=5:
                    status="Out for delivery"
                elif difference_in_days>=3:
                    status="Shipped"
                else:
                    status="Ordered"


                print(purchased_date)
                print(today)
                data.append({
                    "id":book[0],
                    "title":book[1],
                    "author":book[2],
                    "description":book[3],
                    "category":book[4],
                    "price":book[5],
                    "url":book[7],
                    "status":status,
                    "estimated_date":estimated_date,
                })

    


    return render_template("subscriptions.html",books_data=data, userurl = session['user_url'], user_id = session['user_id'])

@app.route('/contact')
def contact():
    return render_template('contact.html', userurl = session['user_url'])

@app.route('/featured')
def featured():
    return redirect(url_for('home'))

@app.route('/account')
def account():
    # Fetch user details from the database based on the currently logged in user or any identifier you have
    # For demonstration, I'm assuming you have a logged-in user ID stored in a variable called 'user_id'
    user_id = session['user_id']
    db, cursor = connect_to_database()
    # Fetch user details based on user ID
    print(user_id)
    cursor.execute("SELECT * FROM users WHERE USER_ID = %s", (user_id,))
    user_data = cursor.fetchone()

    # Check if user data is found
    if user_data:
        # Extract userurl from user_data
        username = user_data[1]
        useremail = user_data[2]
        userurl = user_data[4]  # Assuming 'userurl' is the column name for image URL

        # Pass user image URL to the template
        return render_template('account.html', userurl=userurl, username=username, useremail=useremail)
    else:
        # Handle if user data not found
        flash('User data not found.')
        return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
