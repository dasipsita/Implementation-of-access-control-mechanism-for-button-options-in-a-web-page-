from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
from foodapp.forms import show_access_form, add_access_form, remove_access_form, check_access_form, add_superuser_form, remove_user_form
import sqlite3

def home(request):
    if request.method == 'POST':
        formID = request.POST['formID']
        if formID == "show_access_form":
            userID = request.POST['userID']
            access_to_buttons = show_access(userID)
            if type(access_to_buttons) == str:
                return render(request, 'home.html', {'statement': statement})
            else:    
                return render(request, 'home.html', {'access_to_buttons': access_to_buttons})
        elif formID == "add_access_form":
            userID = request.POST['userID']
            menuitem = request.POST['MenuID']
            statement = add_access(userID,menuitem)
            return render(request, 'home.html', {'statement': statement}) 
        elif formID == "remove_access_form": 
            userID = request.POST['userID']
            menuitem = request.POST['MenuID']
            statement = remove_access(userID,menuitem)
            return render(request, 'home.html', {'statement': statement})
        elif formID == "add_superuser_form":
            userID = request.POST['userID']
            statement = add_superuser(userID)
            return render(request, 'home.html', {'statement': statement})
        elif formID == "remove_user_form":
            userID = request.POST['userID']
            statement = delete_user(userID)
            return render(request, 'home.html', {'statement': statement})
        elif formID == "check_access_form": 
            userID = request.POST['userID']
            menuitem = request.POST['MenuID']
            statement = check_access(userID,menuitem)
            return render(request, 'home.html', {'statement': statement})         
    else:    
        context = {
            'show_access_form' :  show_access_form,
            'add_access_form' : add_access_form,
            'remove_access_form' : remove_access_form,
            'check_access_form' : check_access_form,
            'add_superuser_form' : add_superuser_form,
            'remove_user_form' : remove_user_form
        }
        return render(request, 'base.html', context = context)


def show_access(userID):
    user_exist = if_user_exist(userID)
    if type(user_exist) == str: 
        statement = "User does not exist" 
        return statement
    else:    
        index = 1
        access_to_buttons = []
        con = sqlite3.connect("User.db")
        cur = con.cursor()
        result = cur.execute("SELECT AccessCode FROM Details WHERE UserID=?;", [userID])
        access_code = result.fetchall()
        access_decode = "{:032b}".format(int(access_code[0][0]))
        for i in access_decode:
            if i in "1":
                access_to_buttons.append(index)
            index += 1
        # print(access_to_buttons) 
        return access_to_buttons

def add_access(userID,menuitem):
    menuitem = int(menuitem)
    user_exist = if_user_exist(userID)
    con = sqlite3.connect("User.db")
    cur = con.cursor()
    if type(user_exist) == str: 
        temp_accesscode = ['0']*32
        temp_accesscode[menuitem-1] = '1'
        accesscode = binary_to_decimal(temp_accesscode)
        print ("accesscode1 ", accesscode)
        cur.execute(" INSERT INTO Details (UserID, AccessCode) VALUES(?, ?)",(userID, accesscode))
        con.commit()
        statement = "Access added for " + userID
        return statement
    else:
        temp_accesscode1 = user_exist
        temp_accesscode1 = "{:032b}".format(temp_accesscode1)
        print ("temp_accesscode1:",temp_accesscode1)
        if '0' not in temp_accesscode1:
            statement = "As Super User has access to all Buttons"
            return statement
        else:    
            temp_accesscode1 = user_exist
            temp_accesscode1 = "{:032b}".format(temp_accesscode1)
            temp_accesscode2 = []
            temp_accesscode2[:0] = temp_accesscode1
            temp_accesscode2[menuitem-1] = '1'
            accesscode = binary_to_decimal(temp_accesscode2)
            print ("accesscode2 ", accesscode)
            cur.execute("UPDATE Details SET AccessCode=? WHERE UserID=?;" ,[accesscode,userID])
            con.commit()
            statement = "Access added for " + userID
            return statement 

def remove_access(userID,menuitem):
    menuitem = int(menuitem)
    con = sqlite3.connect("User.db")
    cur = con.cursor()
    user_exist = if_user_exist(userID)
    if type(user_exist) == str:
        statement = "User does not exist" 
        return statement
    else:
        temp_accesscode1 = user_exist
        temp_accesscode1 = "{:032b}".format(temp_accesscode1)
        if '0' not in temp_accesscode1:
            statement = "Can not remove access for Super User"
            return statement
        else:    
            temp_accesscode2[menuitem-1] = '0'
            accesscode = binary_to_decimal(temp_accesscode2)
            cur.execute("UPDATE Details SET AccessCode=? WHERE UserID=?;" ,[accesscode,userID])
            con.commit()
            statement = "Access removed for " + userID
            return statement 
    

def check_access(userID,menuitem):
    menuitem = int(menuitem)
    con = sqlite3.connect("User.db")
    cur = con.cursor()
    user_exist = if_user_exist(userID)
    if type(user_exist) == str:
        statement = "User does not exist" 
        return statement
    else:
        temp_accesscode1 = user_exist
        temp_accesscode1 = "{:032b}".format(temp_accesscode1)
        temp_accesscode2 = []
        temp_accesscode2[:0] = temp_accesscode1
        current_access = temp_accesscode2[menuitem-1]
        if current_access == '1':
            statement =  userID + " has access for the Button "
        else: 
            statement =  userID + " does not have access for the Button "   
        return statement 

def add_superuser(userID):
    con = sqlite3.connect("User.db")
    cur = con.cursor()
    user_exist = if_user_exist(userID)
    if type(user_exist) == str: 
        con = sqlite3.connect("User.db")
        cur = con.cursor()
        temp_accesscode = ['1']*32
        accesscode = binary_to_decimal(temp_accesscode)
        print ("userID", userID)
        cur.execute(" INSERT INTO Details (UserID, AccessCode) VALUES(?, ?)",(userID, accesscode))
        con.commit()
    else:
        temp_accesscode = ['1']*32
        accesscode = binary_to_decimal(temp_accesscode)
        cur.execute("UPDATE Details SET AccessCode=? WHERE UserID=?;" ,[accesscode,userID])
        con.commit()
    statement = userID + " is now a Super User"
    return statement 

def delete_user(userID):
    con = sqlite3.connect("User.db")
    cur = con.cursor()
    user_exist = if_user_exist(userID)
    if type(user_exist) == str: 
        statement = "User does not exist"
    else:    
        con = sqlite3.connect("User.db")
        cur = con.cursor()
        cur.execute("DELETE FROM Details WHERE UserID=?;" ,[userID])
        con.commit()
        statement = userID + " is removed"
        return statement

def if_user_exist(userID):
    con = sqlite3.connect("User.db")
    cur = con.cursor()
    print (userID)
    result = cur.execute("SELECT AccessCode FROM Details WHERE UserID=?;", [userID])
    con.commit()
    access_code = result.fetchall()
    print (access_code)
    if access_code == []:
        return "Create User"  
    else:
        print (access_code[0][0])
        return int(access_code[0][0])
          
def binary_to_decimal(binary_num_list):
    num = 0
    length = len(binary_num_list)-1
    for i in range(length):
      sum = int(binary_num_list[i])*(2**(length-i))
      print ("sum:",sum)
      num += sum
    print (num)
    return num

    




