from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
from foodapp.forms import LoginForm
import sqlite3

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        access_to_buttons = check_user_access(username,password)
        return render(request, 'home.html', {'access_to_buttons': access_to_buttons})
    else:    
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def check_user_access(username,password):
    index = 1
    access_to_buttons = []
    if username == 'Admin':
        access_to_buttons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,32]
        return access_to_buttons
    else:    
        con = sqlite3.connect("User.db")
        cur = con.cursor()
        result = cur.execute("SELECT AccessCode FROM Details WHERE Name=? AND Password=?", (username,password))
        access_code = result.fetchall()
        access_decode = "{:032b}".format(int(access_code[0][0]))
        for i in access_decode:
            if i in "1":
                access_to_buttons.append(index)
            index += 1
        print(access_to_buttons) 
        return access_to_buttons


    




