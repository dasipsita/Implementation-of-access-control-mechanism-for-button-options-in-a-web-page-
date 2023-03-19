import sqlite3

con = sqlite3.connect("User.db")
cur = con.cursor()
#create table
cur.execute("CREATE TABLE Details(UserID varchar, AccessCode int)")
# cur.execute("DROP TABLE Details")

#add users
cur.execute(""" 
INSERT INTO Details VALUES
    ('Rahul12', 3300),
    ('Geetha21', 2500)
""")

con.commit()

  