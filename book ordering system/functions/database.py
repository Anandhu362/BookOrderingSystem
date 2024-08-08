import mysql.connector
import datetime
from flask import flash


try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Kaalan@123',
        database='bookorderingsystem'
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")



# def getAllBooks():
#     books = []

#     cursor.execute("select * from books")
#     resultset = cursor.fetchall()
#     print(resultset)
#     for data in resultset:
#         book = {
#             "id":data[0],
#             "title":data[1],
#             "author":data[2],
#             "description":data[3],
#             "category":data[4],
#             "price":data[5],
#             "bgimgurl":data[6],
#             "fgimgurl":data[7],
#             "type":data[8]
#         }
#         books.append(book)

#     return books

# def addToCart(bookid,userid):
    
#     cursor.execute("SELECT BOOKID FROM CART WHERE USER_ID = %s", (userid,))
#     ids = [int(book[0]) for book in cursor.fetchall()]
#     if int(bookid) in ids:
#         print("Already in Cart")
#         flash('Already in Cart')
#     else:
#         cursor.execute("INSERT INTO CART (bookid, user_id) VALUES (%s, %s)", (bookid, userid))

        
#         db.commit()



# def addToSubcheckout(bookid,userid):
     
    
#     cursor.execute("INSERT INTO SUBCHECKOUT (bookid, user_id) VALUES (%s, %s)", (bookid, userid))

#     db.commit()

# def getCartCount(userid):
#     cursor.execute("select * from cart where user_id= %s", (userid,))
#     return len(cursor.fetchall())



# def getCartDetails(userid):
#     data = []
#     cursor.execute("SELECT BOOKID FROM CART WHERE USER_ID = %s", (userid,))
#     ids = [int(book[0]) for book in cursor.fetchall()]
    
#     cursor.execute("SELECT * FROM BOOKS")#change popular name
#     bookdetails = cursor.fetchall()

#     for bid in ids:
#         for book in bookdetails:
#             if int(book[0])==int(bid):
#                 data.append({
#                     "id":book[0],
#                     "title":book[1],
#                     "author":book[2],
#                     "description":book[3],
#                     "category":book[4],
#                     "price":book[5],
#                     "url":book[7],
#                 })

#     return data



# def getOrders(user_id):
#     data = []
#     cursor.execute("SELECT * FROM ORDERS WHERE USER_ID  =%s",(user_id,))
#     #ids = [int(book[0]) for book in cursor.fetchall()]
#     orders = cursor.fetchall()
    
#     cursor.execute("SELECT * FROM BOOKS")#change popular name
#     bookdetails = cursor.fetchall()

#     date_format = "%Y-%m-%d"

#     for order in orders:
#         for book in bookdetails:
#             if int(book[0])==int(order[0]):
#                 purchased_date = order[1]#datetime.datetime.strptime(order[1], date_format)
#                 address = order[3]
#                 today = datetime.date.today()#datetime.datetime.strptime(datetime.date.today(), date_format)
#                 time_difference = today - purchased_date
#                 difference_in_days = time_difference.days

#                 print(difference_in_days)
#                 estimated_date= purchased_date + datetime.timedelta(days=7)
#                 if difference_in_days>=7:
#                     status="Delivered"
#                 elif difference_in_days>=5:
#                     status="Out for delivery"
#                 elif difference_in_days>=3:
#                     status="Shipped"
#                 else:
#                     status="Ordered"


#                 print(purchased_date)
#                 print(today)
#                 data.append({
#                     "id":book[0],
#                     "title":book[1],
#                     "author":book[2],
#                     "description":book[3],
#                     "category":book[4],
#                     "price":book[5],
#                     "url":book[7],
#                     "status":status,
#                     "estimated_date":estimated_date,
#                     "address":address,
#                 })

#     return data


# def getSubscriptions(user_id):
#     data = []
#     cursor.execute("SELECT * FROM SUBSCRIPTIONS WHERE USER_ID  =%s",(user_id,))
#     #ids = [int(book[0]) for book in cursor.fetchall()]
#     orders = cursor.fetchall()
    
#     cursor.execute("SELECT * FROM BOOKS")#change popular name
#     bookdetails = cursor.fetchall()

#     date_format = "%Y-%m-%d"

#     for order in orders:
#         for book in bookdetails:
#             if int(book[0])==int(order[0]):
#                 purchased_date = order[1]#datetime.datetime.strptime(order[1], date_format)
#                 today = datetime.date.today()#datetime.datetime.strptime(datetime.date.today(), date_format)
#                 time_difference = today - purchased_date
#                 difference_in_days = time_difference.days

#                 print(difference_in_days)
#                 estimated_date= purchased_date + datetime.timedelta(days=7)
#                 if difference_in_days>=7:
#                     status="Latest Edition Delivered"
#                 elif difference_in_days>=5:
#                     status="Out for delivery"
#                 elif difference_in_days>=3:
#                     status="Shipped"
#                 else:
#                     status="Ordered"


#                 print(purchased_date)
#                 print(today)
#                 data.append({
#                     "id":book[0],
#                     "title":book[1],
#                     "author":book[2],
#                     "description":book[3],
#                     "category":book[4],
#                     "price":book[5],
#                     "url":book[7],
#                     "status":status,
#                     "estimated_date":estimated_date,
#                 })

#     return data


# def checkout(user_id, address, name, city, state, zipcode):
#     cursor.execute(" delete from subcheckout where bookid IS NULL;")
#     cursor.execute("SELECT BOOKID FROM CART")
#     ids = [int(book[0]) for book in cursor.fetchall()]
#     today_date = datetime.date.today().strftime('%Y-%m-%d')
#     print(today_date)
#     add = name + "\n" + address + "\n" + city + ", " + state + "\n" + zipcode
    
#     for bid in ids:
#         cursor.execute(f"INSERT INTO ORDERS  VALUES({bid},'{today_date}','{user_id}','{add}')")
#         db.commit()
    
#     cursor.execute("DELETE FROM CART")
#     db.commit()


# def subcheckout(user_id, address, name, city, state, zipcode):
#     cursor.execute("SELECT BOOKID FROM SUBCHECKOUT")
#     ids = [int(book[0]) for book in cursor.fetchall()]
#     today_date = datetime.date.today().strftime('%Y-%m-%d')
#     print(today_date)
#     add = name + "\n" + address + "\n" + city + ", " + state + "\n" + zipcode
#     print(add,user_id)
#     for bid in ids:
#         print(bid)
#         cursor.execute(f"INSERT INTO SUBSCRIPTIONS  VALUES({bid},'{today_date}','{user_id}','{add}')")
#         db.commit()
    
#     cursor.execute("DELETE FROM SUBCHECKOUT")
#     db.commit()

    