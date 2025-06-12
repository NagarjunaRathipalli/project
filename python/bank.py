from tkinter import *
from tkinter import messagebox
from tkinter import ttk
root=Tk()
root.geometry("300x400")
root.title('bank')

# created a login page
def login():
    ob=Toplevel(root)
    ob.title("login")
    ob.geometry("300x400")
 
    #create a login deatils
    login_label=Label(ob, text="PHONE NUMBER")
    login_label.pack()
    login_entry=Entry(ob)
    login_entry.pack()

    # create pin for login
    login_pin=Label(ob, text="4 DIGITS PIN")
    login_pin.pack()
    login_entry2=Entry(ob)
    login_entry2.pack()
    
    #created login button
    login_button=Button(ob, text="LOGIN")
    login_button.pack()

def signup():
    bj=Toplevel()
    bj.geometry("600x600")
    bj.title("signup")

    #create a signup deatils
    signup_label=Label(bj, text="USER NAME")
    signup_label.pack()
    signup_entry=Entry(bj)
    signup_entry.pack()

    signup_label1=Label(bj, text="NAME")
    signup_label1.pack()
    signup_entry1=Entry(bj)
    signup_entry1.pack()

    signup_label2=Label(bj, text="PHONE NUMBER")
    signup_label2.pack()
    signup_entry2=Entry(bj)
    signup_entry2.pack()

    signup_label3=Label(bj, text="EMAIL")
    signup_label3.pack()
    signup_entry3=Entry(bj)
    signup_entry3.pack()

    signup_label=Label(bj, text="ADDRESS")
    signup_label.pack()
    signup_entry=Entry(bj)
    signup_entry.pack()

    signup_button=Button(bj, text="SIGN UP")
    signup_button.pack()

def tq():
    messagebox.showinfo("Hushhh","Thank!For visting ")

frame=Frame(root)
frame.pack()
buttonframe=Frame(root)
buttonframe.pack(side=BOTTOM)

redbutton=Button(frame, text="ANAND", fg="red", command=tq)
redbutton.pack(side=LEFT)

greenbutton=Button(frame, text="BANK", fg="green", command=tq)
greenbutton.pack(side=RIGHT)

bluebutton=Button(frame, text="LOGIN", fg="blue" , command=login)
bluebutton.pack(side=BOTTOM)

bluebutton=Button(frame, text="SIGN UP", fg="blue" , command=signup)
bluebutton.pack(side=BOTTOM)


nootbook=ttk.Notebook(root)
nootbook.pack(expand=True, fill="both", padx=10 , pady=10)

login=ttk.Frame(nootbook)
nootbook.add(login, text='DEATILS')

customer=Label(login, text="customer id")
customer.grid(row=0, column=0 ,padx=20, pady=5)
l1=Entry(login)
l1.grid(row=0,column=1,padx=2, pady=10)

name=Label(login,text="NAME").grid(row=1,column=0)
l2=Entry(login).grid(row=1,column=1,padx=2, pady=10)

phone=Label(login, text="phone number")
phone.grid(row=2,column=0)
l3=Entry(login)
l3.grid(row=2,column=1,padx=2, pady=10)

email=Label(login,text="EMAIL").grid(row=3,column=0)
l4=Entry(login).grid(row=3,column=1,padx=2, pady=10)

address=Label(login,text="ADDRESS").grid(row=4,column=0)
l5=Entry(login).grid(row=4,column=1,padx=2, pady=10)

#create a deposite module
deposit=ttk.Frame(nootbook)
nootbook.add(deposit,text="DEPOSIT")

amount=Label(deposit,text="Amount Deposit")
amount.grid(row=0,column=0)
l1=Entry(deposit)
l1.grid(row=0,column=1)

Enter=Button(deposit, text="DEPOSIT")
Enter.grid(row=1)

#create a withdrawl module
withdrawl=ttk.Frame(nootbook)
nootbook.add(withdrawl,text="WITHDRAWL")

amount=Label(withdrawl, text="Amount")
amount.grid(row=0,column=0)
l1=Entry(withdrawl)
l1.grid(row=0,column=1)

Enter1=Button(withdrawl, text="WITHDRAWL")
Enter1.grid(row=1)

# create cheak balance 
balance=ttk.Frame(nootbook)
nootbook.add(balance,text="BALANCE")

id=Label(balance,text="USER ID ")
id.grid(row=0,column=0)
e3=Entry(balance)
e3.grid(row=0,column=1)

check=Button(balance,text="check balance")
check.grid()

checkbalance=Label(balance,text="CHEAK BALANCE")
checkbalance.grid(row=2,column=0)
e4=Entry(balance)
e4.grid(row=2, column=1)
root.mainloop()