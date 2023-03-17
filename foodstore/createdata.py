import sqlite3

con = sqlite3.connect("User.db")
cur = con.cursor()
#create table
cur.execute("CREATE TABLE Details(UserID varchar, Name varchar, Password varchar, AccessCode int)")

#add users
cur.execute(""" 
INSERT INTO Details VALUES
    ('1', 'Rahul', 'Rahul1', 3300),
    ('2', 'Geetha', 'Geetha2', 2500),
    ('3', 'Krish', 'Krish3', 40204) 
""")

#add superuser
cur.execute(""" 
INSERT INTO Details VALUES
    ('4', 'Admin', 'SuperUser', 1) 
""")

con.commit()

  