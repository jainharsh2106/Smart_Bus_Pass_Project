from tkinter import *
import random
import qrcode
from tkcalendar import DateEntry
from datetime import date
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import mysql.connector
from mysql.connector import Error
import io
from file import read_blob
from updatefile import update_blob
from renewresume import renew_resume
root = Tk()
root.title("smart bus pass app")
root.geometry("1000x696")
bg = PhotoImage(file="busstation.png")
l1 = Label(root, image=bg)
l1.place(x=0, y=0, relwidth=1, relheight=1)
l2 = Label(root, text="SMART BUS PASS", font=("Bell MT", 50), bg="#4bb6ee")
l2.place(x=25, y=12)
global filen, img, var3, var2, var1, var4


def signup():
    newinterface = Toplevel(root)
    newinterface.title("sign up")
    newinterface.geometry("1000x900")
    newinterface.config(bg="lightyellow")
    l3 = Label(newinterface, text="USER REGISTRATION",
               font=("Bell MT", 50), bg="lightgreen")
    l3.place(x=150, y=12)

    Label(newinterface, text="Name: ", font="Arial,25",
          bg="lightyellow").place(x=10, y=110)
    e1 = Entry(newinterface, bd=5, font="Arial,25")
    e1.place(x=190, y=110)

    Label(newinterface, text="Date of Birth: ",
          font="Arial,25", bg="lightyellow").place(x=10, y=160)
    e2 = DateEntry(newinterface, bd=5, font="Arial,25",
                   selectmode='day', date_pattern='dd-mm-yyyy')
    e2.place(x=190, y=160)

    Label(newinterface, text="Mobile No.: ", font="Arial,25",
          bg="lightyellow").place(x=10, y=210)
    e3 = Entry(newinterface, bd=5, font="Arial,25")
    e3.place(x=190, y=210)

    Label(newinterface, text="Email Id: ", font="Arial,25",
          bg="lightyellow").place(x=10, y=260)
    e4 = Entry(newinterface, bd=5, font="Arial,25", width=25)
    e4.place(x=190, y=260)

    Label(newinterface, text="Address: ", font="Arial,25",
          bg="lightyellow").place(x=10, y=310)
    e5 = Text(newinterface, bd=5, font="Arial,25", width=25, height=4)
    e5.place(x=190, y=310)

    Label(newinterface, text="Password: ", font="Arial,25",
          bg="lightyellow").place(x=10, y=430)
    e6 = Entry(newinterface, bd=5, font="Arial,25")
    e6.place(x=190, y=430)

    Label(newinterface, text="Retype Password: ",
          font="Arial,25", bg="lightyellow").place(x=10, y=480)
    e7 = Entry(newinterface, bd=5, font="Arial,25")
    e7.place(x=190, y=480)

    check = IntVar()
    tc = Checkbutton(newinterface, text="by clicking this you are agreed with our privacy policies & terms and conditions", font=(
        "times", 13), bg="lightyellow", variable=check)
    tc.place(x=10, y=530)

    def show():
        con3 = mysql.connector.connect(
            host='127.0.0.1', user='root', password='', database='smartbuspass')
        cur3 = con3.cursor()
        cur3.execute("SELECT mobile FROM `registrationdetails` ")
        list2 = cur3.fetchall()
        cur3.close()
        con3.close()

        con4 = mysql.connector.connect(
            host='127.0.0.1', user='root', password='', database='smartbuspass')
        cur4 = con4.cursor()
        cur4.execute("SELECT email FROM `registrationdetails` ")
        list3 = cur4.fetchall()
        cur4.close()
        con4.close()

        Name = e1.get()
        today = date.today()
        dt = e2.get_date()
        DOB = dt.strftime("%d-%m-%Y")
        birthyear = date(day=int(dt.strftime("%d")), month=int(
            dt.strftime("%m")), year=int(dt.strftime("%Y")))
        age = today.year - birthyear.year - \
            ((today.month, today.day) < (birthyear.month, birthyear.day))
        Mob_no = e3.get()
        Email_1 = e4.get()
        Address = e5.get('0.0', "200.0")
        Pass = e6.get()
        Repass = e7.get()
        lmob = list(Mob_no)
        count = 0
        for x in lmob:
            count += 1
        chk = check.get()

        if Name == "":
            messagebox.showerror("Error", "Please Enter the name")
        elif age <= 16:
            messagebox.showerror("Error", "User must be 16+")
        elif Mob_no == "":
            messagebox.showerror("Error", "Please Enter the Mobile Number")
        elif Mob_no > "a" and Mob_no < "z" or Mob_no > "A" and Mob_no < "B":
            messagebox.showerror("Error", "Please Enter valid number digits")
        elif count < 10 or count > 10:
            messagebox.showerror(
                "Validation Error", "Please Enter valid Mobile Number\n10 digit mobile number")
        elif (Mob_no,) in list2:
            messagebox.showerror("Alert", "Mobile number Already used")
        elif Email_1 == "":
            messagebox.showerror("Error", "Please Enter the Email")
        elif (Email_1,) in list3:
            messagebox.showerror("Alert", "Email Already used")
        elif Address == "":
            messagebox.showerror("Error", "Please Enter the Address")
        elif Pass == "":
            messagebox.showerror("Error", "Please Enter the Password")
        elif Repass == "" or Repass != Pass:
            messagebox.showerror(
                "Error", "Password Did Not Matched! Enter AGAIN")
        elif chk == 0:
            messagebox.showerror("Error", "please check the policy")
        else:
            m = messagebox.askokcancel("Confirmation", "Submit or Not?")
            if m == True:

                l7.config(text="User Successfully registered", fg="Green")

                con = mysql.connector.connect(
                    host='127.0.0.1', user='root', password='', database='smartbuspass')

                cur = con.cursor()

                cur.execute(
                    "insert into registrationdetails (name,dob,mobile,email,address,password) value ('{}','{}','{}','{}','{}','{}')".format(
                        Name, DOB, Mob_no, Email_1, Address, Pass))
                con.commit()
            else:
                l7.config(text="Please check Your Details", fg="red")

    def clear():
        if messagebox.askyesno("Alert!", "Clear all details"):
            e1.delete(0, END)
            e2.delete(0, 'end')
            e3.delete(0, END)
            e4.delete(0, END)
            e5.delete("0.0", "end")
            e6.delete(0, END)
            e7.delete(0, END)
            tc.deselect()
    Label(newinterface, text="Output ", font="Arial,20,BOLD",
          fg="brown", bg="lightyellow").place(x=10, y=570)
    Button(newinterface, text="Submit", bg="sky blue",
           command=show, font="Arial,25").place(x=500, y=720)
    Button(newinterface, text="Clear", bg="red",
           command=clear, font="Arial,25").place(x=580, y=720)
    l7 = Label(newinterface, bg="lightyellow")
    l7.place(x=160, y=640)
    newinterface.mainloop()


Button(root, text="Sign UP", command=signup, font=(
    "times", 22), bg="#645b49").place(x=55, y=580)


def signin():
    newinterface2 = Toplevel(root)
    newinterface2.geometry("1000x696")
    newinterface2.title("sign in")
    bg2 = PhotoImage(file="buslogin.png")
    l4 = Label(newinterface2, image=bg2)
    l4.place(x=0, y=0, relwidth=1, relheight=1)
    Label(newinterface2, text="Email Id: ",
          font="Arial,35", bg="#c9af7c").place(x=140, y=225)
    e8 = Entry(newinterface2, bd=5, font="Arial,35")
    e8.place(x=280, y=225)
    
    Label(newinterface2, text="Password: ",
          font="Arial,35", bg="#eca73f").place(x=140, y=320)
    e9 = Entry(newinterface2, bd=5, font="Arial,35",show="*")
    e9.place(x=280, y=320)
    def show_pswrd():
        if e9.cget('show')=='*':
            e9.config(show="")
        else:
            e9.config(show="*")
    showpswrd=Checkbutton(newinterface2,text="show password",command=show_pswrd, bg="#f4b902")
    showpswrd.place(x=280, y=380)
    def login():
        user = e8.get()
        pswrd = e9.get()
        con2 = mysql.connector.connect(
            host='127.0.0.1', user='root', password='', database='smartbuspass')
        cur2 = con2.cursor()
        cur2.execute("SELECT email,password FROM `registrationdetails` ")
        list1 = cur2.fetchall()
        cur2.close()
        con2.close()
        if (user, pswrd) in list1:
            newinterface3 = Toplevel(newinterface2)
            newinterface3.geometry("696x800")
            newinterface3.title("log in")
            bg3 = PhotoImage(file="passes.png")
            l3 = Label(newinterface3, image=bg3)
            l3.place(x=0, y=0, relwidth=1, relheight=1)

            def renewpass():
                con15 = mysql.connector.connect(
                            host='127.0.0.1', user='root', password='', database='smartbuspass')
                cur15 = con15.cursor()
                query = "SELECT * FROM `newpass` WHERE email = %s limit 0,5"
                cur15.execute(query, (user,))
                list14 = cur15.fetchall()            
                newinterface7 = Toplevel(newinterface3)
                newinterface7.geometry("1000x696")
                newinterface7.title("Renew pass")
                newinterface7.config(bg="aqua")
                l = Label(newinterface7, text="Your Applied Bus Passes\n Are Here!!", font=("Bell MT", 30), bg="aqua")
                l.place(x=250, y=435)
                l1=Label(newinterface7, text='ID', bg="aqua") 
                l1.grid(row=6,column=1) 

                l2=Label(newinterface7, text='Name', bg="aqua") 
                l2.grid(row=6,column=2) 

                l3=Label(newinterface7, text='DOB', bg="aqua") 
                l3.grid(row=6,column=3)

                l4=Label(newinterface7, text='Mobile', bg="aqua") 
                l4.grid(row=6,column=4) 

                l5=Label(newinterface7, text='From', bg="aqua") 
                l5.grid(row=6,column=5) 

                l6=Label(newinterface7, text='To', bg="aqua") 
                l6.grid(row=6,column=6)

                l7=Label(newinterface7, text='Pass From', bg="aqua") 
                l7.grid(row=6,column=7) 

                l8=Label(newinterface7, text='Pass Till', bg="aqua") 
                l8.grid(row=6,column=8) 
                
                l9=Label(newinterface7, text='Profile', bg="aqua") 
                l9.grid(row=6,column=9) 

                l10=Label(newinterface7, text='Update Details', bg="aqua") 
                l10.grid(row=6,column=10) 
                
                i=7 # data starts from row 1 
                images = [] # to manage garbage collection. 
                def updatemypass():
                    query = "SELECT newpass.passid, registrationdetails.password FROM newpass INNER JOIN registrationdetails ON newpass.email=registrationdetails.email"
                    con16 = mysql.connector.connect(
                            host='127.0.0.1', user='root', password='', database='smartbuspass')
                    cur16 = con16.cursor()
                    cur16.execute(query)
                    list15 = cur16.fetchall()
                    newinterface8 = Toplevel(newinterface7)
                    newinterface8.geometry("456x316")
                    newinterface8.title("confirm password")
                    newinterface8.config(bg="#eff7dc")
                    l5 = Label(newinterface8, text="Confirm user Mobile & password", font=("Bell MT", 15), bg="#eff7dc")
                    l5.place(x=105, y=1)
                    Label(newinterface8, text="Mobile: ", font="Arial,15", bg="#eff7dc").place(x=30, y=40)
                    e18 = Entry(newinterface8, bd=5, font="Arial,15",bg="#eff7dc")
                    e18.place(x=180, y=40)
                    Label(newinterface8, text="Password: ", font="Arial,15", bg="#eff7dc").place(x=30, y=100)
                    e19 = Entry(newinterface8, bd=5, font="Arial,15",bg="#eff7dc",show="*")
                    e19.place(x=180, y=100)
                    def show_pswrd():
                        if e19.cget('show')=='*':
                            e19.config(show="")
                        else:
                            e19.config(show="*")
                    showpswrd=Checkbutton(newinterface8,text="show password",command=show_pswrd, bg="#eff7dc")
                    showpswrd.place(x=180, y=150)
                    def confirmpass():
                        cnfrmpass=e19.get()
                        cnfrmmob=e18.get()

                        query = "SELECT * FROM `newpass` WHERE mobile = %s"

                        try:
                            con19 = mysql.connector.connect(
                                host='127.0.0.1', user='root', password='', database='smartbuspass')
                            cur19 = con19.cursor()
                            cur19.execute(query, (cnfrmmob,))
                            list18 = cur19.fetchall()
                            text=list18[0][13]

                        except Error as e:
                            print(e)

                        finally:
                            cur19.close()
                            con19.close()
                        
                        if (text, cnfrmpass) in list15:
                            newinterface9 = Toplevel(newinterface8)
                            newinterface9.geometry("1300x396")
                            newinterface9.title("update details")
                            newinterface9.config(bg="lightyellow")
                            query = "SELECT * FROM `newpass` WHERE passid = %s"

                            try:
                                con19 = mysql.connector.connect(
                                    host='127.0.0.1', user='root', password='', database='smartbuspass')
                                cur19 = con19.cursor()
                                cur19.execute(query, (text,))
                                list18 = cur19.fetchall()

                            except Error as e:
                                print(e)

                            finally:
                                cur19.close()
                                con19.close()

                            l1=Label(newinterface9, text='ID', bg="lightyellow") 
                            l1.grid(row=1,column=1) 
                            e = Label(newinterface9, text=text, bg="lightyellow") 
                            e.grid(row=2,column=1,ipadx=15) 
                            l2=Label(newinterface9, text='Name', bg="lightyellow") 
                            l2.grid(row=1,column=2) 
                            e = Label(newinterface9, text=list18[0][2], bg="lightyellow") 
                            e.grid(row=2,column=2,ipadx=20)
                            l3=Label(newinterface9, text='DOB', bg="lightyellow") 
                            l3.grid(row=1,column=3)
                            edob = DateEntry(newinterface9, bd=5,selectmode='day', date_pattern='dd-mm-yyyy')
                            edob.grid(row=2,column=3,ipadx=20)
                            l4=Label(newinterface9, text='Mobile', bg="lightyellow") 
                            l4.grid(row=1,column=4) 
                            e = Label(newinterface9, text=list18[0][5], bg="lightyellow") 
                            e.grid(row=2,column=4,ipadx=20) 
                            l5=Label(newinterface9, text='From', bg="lightyellow") 
                            l5.grid(row=1,column=5) 
                            optionsfrom = ["Meerut", "Modinagar", "Muradnagar",
                                "Ghaziabad", "Mohannagar", "Noida", "Delhi"]
                            global var1
                            var1 = StringVar()
                            var1.set("From")
                            OptionMenu(newinterface9, var1, *
                                    optionsfrom).grid(row=2,column=5,ipadx=20) 
                            
                            l6=Label(newinterface9, text='To', bg="lightyellow") 
                            l6.grid(row=1,column=6)
                            optionsto = ["Meerut", "Modinagar", "Muradnagar",
                                        "Ghaziabad", "Mohannagar", "Noida", "Delhi"]
                            global var2
                            var2 = StringVar()
                            var2.set("Destination")
                            OptionMenu(newinterface9, var2, *optionsto).grid(row=2,column=6,ipadx=20) 

                            l7=Label(newinterface9, text='Pass From', bg="lightyellow") 
                            l7.grid(row=1,column=7) 
                            dt3 = date.today()
                            calfrm = DateEntry(newinterface9, bd=5,
                                            selectmode='day', date_pattern='dd-mm-yyyy', mindate=dt3)
                            calfrm.grid(row=2,column=7,ipadx=20)
                            
                            l8=Label(newinterface9, text='Pass Till', bg="lightyellow") 
                            l8.grid(row=1,column=8) 
                            calto = DateEntry(newinterface9, bd=5,
                                            selectmode='day', date_pattern='dd-mm-yyyy', mindate=dt3)
                            calto.grid(row=2,column=8,ipadx=20)
                            
                            l9=Label(newinterface9, text='Profile', bg="lightyellow") 
                            l9.grid(row=1,column=9)
                            stream = io.BytesIO(list18[0][12])
                            img=Image.open(stream)
                            img = img.resize((70, 70))
                            img = ImageTk.PhotoImage(img)
                            e = Label(newinterface9, image=img, bg="lightyellow") 
                            e.grid(row=2, column=9,ipady=7)

                            l10=Label(newinterface9, text='Upload image', bg="lightyellow") 
                            l10.grid(row=1,column=10)
                            def uploadimage():
                                global filen
                                f_types = [('JPG', '*.jpg'), ('PNG', '*.png'),
                                ('JPEG', '*.jpeg')]
                                filen = filedialog.askopenfilename(filetypes=f_types)
                                Label(newinterface9, text=filen, bg="lightyellow").grid(row=4, column=10,ipadx=15)
                            Button(newinterface9, text="upload", font=("times", 10),
                            bg="lightgreen", command=uploadimage).grid(row=2, column=10,ipadx=15)
                            
                            def renewmypass():
                                dtob = edob.get_date()
                                frm=var1.get()
                                to=var2.get()
                                pfrm=calfrm.get_date()
                                pto=calto.get_date()
                                pic=filen
                                uname=list18[0][2]
                                today2 = date.today()
                                days = (calto.get_date()-calfrm.get_date()).days
                                datee = dtob.strftime("%d-%m-%Y")
                                birthyear2 = date(day=int(dtob.strftime("%d")), month=int(dtob.strftime("%m")),
                                                year=int(dtob.strftime("%Y")))
                                agepsg = today2.year - birthyear2.year - \
                                    ((today2.month, today2.day) <
                                    (birthyear2.month, birthyear2.day))
                                if pto is list18[0][11] and frm is list18[0][8] and to is list18[0][9]:
                                    renew_resume(str(dtob),str(frm),str(to),str(pfrm),str(pto),str(pic),str(uname))
                                    l = Label(newinterface7, text="Details Updated Successfully!!", font=("Bell MT", 15), bg="lightyellow")
                                    l.place(x=250, y=235)
                                else:
                                    newinterface10 = Toplevel(newinterface9)
                                    newinterface10.geometry("1000x696")
                                    newinterface10.title("payment")
                                    Label(newinterface10, text="Name:-",
                                        font=("Bell MT", 22)).place(x=10, y=12)
                                    Label(newinterface10, text=uname, font=(
                                        "times", 22)).place(x=150, y=12)
                                    Label(newinterface10, text="Place:-",
                                        font=("Bell MT", 22)).place(x=10, y=62)
                                    Label(newinterface10, text=frm + " to " +
                                        to, font=("times", 22)).place(x=150, y=62)
                                    Label(newinterface10, text="Pass Limit is of:-",
                                        font=("Bell MT", 22)).place(x=10, y=112)
                                    Label(newinterface10, text=str(days)+" Days",
                                        font=("times", 22)).place(x=250, y=112)
                                    Label(newinterface10, text="Amount:-",
                                        font=("Bell MT", 22)).place(x=10, y=162)
                                    if frm == to:
                                        amount = 0.0*days
                                    elif frm == "Meerut" and to == "Modinagar" or frm == "Modinagar" and to == "Meerut":
                                        amount = 20.0*(days-3)
                                    elif frm == "Meerut" and to == "Muradnagar" or frm == "Muradnagar" and to == "Meerut":
                                        amount = 35.0*(days-3)
                                    elif frm == "Meerut" and to == "Ghaziabad" or frm == "Ghaziabad" and to == "Meerut":
                                        amount = 50.0*(days-3)
                                    elif frm == "Meerut" and to == "Mohannagar" or frm == "Mohannagar" and to == "Meerut":
                                        amount = 65.0*(days-3)
                                    elif frm == "Meerut" and to == "Noida" or frm == "Noida" and to == "Meerut":
                                        amount = 80.0*(days-3)
                                    elif frm == "Meerut" and to == "Delhi" or frm == "Delhi" and to == "Meerut":
                                        amount = 95.0*(days-3)
                                    elif frm == "Modinagar" and to == "Muradnagar" or frm == "Muradnagar" and to == "Modinagar":
                                        amount = 15.0*(days-3)
                                    elif frm == "Modinagar" and to == "Ghaziabad" or frm == "Ghaziabad" and to == "Modinagar":
                                        amount = 30.0*(days-3)
                                    elif frm == "Modinagar" and to == "Mohannagar" or frm == "Mohannagar" and to == "Modinagar":
                                        amount = 45.0*(days-3)
                                    elif frm == "Modinagar" and to == "Noida" or frm == "Noida" and to == "Modinagar":
                                        amount = 75.0*(days-3)
                                    elif frm == "Modinagar" and to == "Delhi" or frm == "Delhi" and to == "Modinagar":
                                        amount = 90.0*(days-3)
                                    elif frm == "Muradnagar" and to == "Ghaziabad" or frm == "Ghaziabad" and to == "Muradnagar":
                                        amount = 17.0*(days-3)
                                    elif frm == "Muradnagar" and to == "Mohannagar" or frm == "Muradnagar" and to == "Modinagar":
                                        amount = 32.0*(days-3)
                                    elif frm == "Muradnagar" and to == "Noida" or frm == "Noida" and to == "Muradnagar":
                                        amount = 48.0*(days-3)
                                    elif frm == "Muradnagar" and to == "Delhi" or frm == "Delhi" and to == "Muradnagar":
                                        amount = 63.0 * (days - 3)
                                    elif frm == "Ghaziabad" and to == "Mohannagar" or frm == "Muradnagar" and to == "Ghaziabad":
                                        amount = 15.0*(days-3)
                                    elif frm == "Ghaziabad" and to == "Noida" or frm == "Noida" and to == "Ghaziabad":
                                        amount = 35.0*(days-3)
                                    elif frm == "Ghaziabad" and to == "Delhi" or frm == "Delhi" and to == "Ghaziabad":
                                        amount = 55.0*(days-3)
                                    elif frm == "Mohannagar" and to == "Noida" or frm == "Noida" and to == "Mohannagar":
                                        amount = 20.0*(days-3)
                                    elif frm == "Mohannagar" and to == "Delhi" or frm == "Delhi" and to == "Mohannagar":
                                        amount = 40.0*(days-3)
                                    else:
                                        amount = 0.0*(days-3)
                                    Label(newinterface10, text=amount, font=(
                                        "times", 22)).place(x=150, y=162)
                                    paypic = PhotoImage(file="payment.png")
                                    paymentpic = Label(
                                        newinterface10, image=paypic, width=400, height=400)
                                    paymentpic.place(x=190, y=212)

                                    def mypass():
                                        image = Image.new(
                                            'RGB', (880, 500), (81, 191, 232))
                                        draw = ImageDraw.Draw(image)
                                        draw.rectangle(
                                            xy=[(0, 0), (880, 80)], fill='#e86d51', outline='#e86d51', width=880)
                                        img1 = Image.open('./aprove.png')
                                        img1 = img1.resize((350, 350))
                                        image.paste(img1, (300, 150))

                                        (x, y) = (10, 10)
                                        company = str("SMART BUS PASS")
                                        color = 'rgb(0, 0, 0)'  # black color
                                        font = ImageFont.truetype(
                                            'arial.ttf', size=60)
                                        draw.text((x, y), company,
                                                fill=color, font=font)

                                        (x, y) = (580, 20)
                                        message = str('ID: ' + str(text))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        font = ImageFont.truetype(
                                            'arial.ttf', size=60)
                                        draw.text((x, y), message,
                                                fill=color, font=font)

                                        (x, y) = (180, 100)
                                        fname = str('Name: ' + str(uname))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        font = ImageFont.truetype(
                                            'arial.ttf', size=35)
                                        draw.text((x, y), fname,
                                                fill=color, font=font)

                                        (x, y) = (180, 150)
                                        fage = str('Age: ' + str(agepsg))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        draw.text((x, y), fage,
                                                fill=color, font=font)

                                        (x, y) = (400, 150)
                                        fgender = str('Gender: ' + str(list18[0][4]))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        draw.text((x, y), fgender,
                                                fill=color, font=font)

                                        (x, y) = (180, 200)
                                        fNo = str('Mobile Number: ' + str(list18[0][5]))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        draw.text(
                                            (x, y), fNo, fill=color, font=font)

                                        (x, y) = (10, 250)
                                        famount = str('Amount: ' + str(amount))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        draw.text((x, y), famount,
                                                fill=color, font=font)

                                        (x, y) = (10, 300)
                                        froute = str(
                                            'Route: ' + str(frm) + " to " + str(to))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        draw.text((x, y), froute,
                                                fill=color, font=font)

                                        (x, y) = (10, 350)
                                        flimit = str(
                                            'Validity: ' + str(pfrm) + " to " + str(pto))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        draw.text((x, y), flimit,
                                                fill=color, font=font)

                                        update_blob(text, filen)
                                        read_blob(text,"read.jpg")
                                        renew_resume(str(dtob),str(frm),str(to),str(pfrm),str(pto),str(pic),str(uname))
                                        img4 = Image.open('read.jpg')
                                        img4 = img4.resize((150, 150))
                                        image.paste(img4, (10, 90))

                                        qr = qrcode.QRCode(
                                            version=12,
                                            error_correction=qrcode.constants.ERROR_CORRECT_H,
                                            box_size=3,
                                            border=0
                                        )
                                        qr.add_data(str(text) + '\n' + str(uname) + '\n' + str(datee) + '\t' + str(
                                            agepsg) + '\n' + str(list18[0][4]) + '\n' + str(list18[0][5]) + '\n' + str(
                                            list18[0][6]) + '\n' + str(list18[0][7]) + '\n' + str(frm) + " to " + str(
                                            to) + '\n' + str(pfrm) + " to " + str(pto))
                                        qr.make()
                                        QR = qr.make_image(
                                            fill_color="black", back_color="#51bfe8")
                                        image.paste(QR, (650, 200))

                                        image.save(str(uname) + str(text) + '.png')
                                        newinterface11 = Toplevel(newinterface10)
                                        newinterface11.geometry("1000x696")
                                        newinterface11.title("My Pass")
                                        passtemp = Image.open(
                                            str(uname) + str(text) + '.png')
                                        passtemp = passtemp.resize((880, 500))
                                        passtemp = ImageTk.PhotoImage(passtemp)
                                        Label(newinterface11, image=passtemp).place(
                                            x=60, y=60)
                                        pt1 = Label(
                                            newinterface11, text="BUS PASS Successfully Genrated")
                                        pt1.place(x=25, y=12)

                                        newinterface11.mainloop()
                                    Button(newinterface10, text="Generate Pass", bg="lightgreen", command=mypass,
                                        font="Arial,25").place(x=560, y=600)
                                    newinterface10.mainloop()
                            Button(newinterface9, text="Renew Pass", font=("times", 15),
                            bg="lightgreen", command=renewmypass).place(x=370, y=160)

                            newinterface9.mainloop()
                        else:
                            messagebox.showerror("Details did not match",
                                 "Please Enter Valid Mobile number or Password")
                            
            
                    Button(newinterface8, text="Enter", font=("times", 18), bg="#eff7dc", command=confirmpass).place(x=170, y=210)
                    newinterface8.mainloop()

                for passenger in list14: 
                    stream = io.BytesIO(passenger[12])
                    img=Image.open(stream)
                    img = img.resize((70, 70))
                    img = ImageTk.PhotoImage(img)    
                    e = Label(newinterface7, text=passenger[13], bg="aqua") 
                    e.grid(row=i,column=1,ipadx=15) 
                    e = Label(newinterface7, text=passenger[2], bg="aqua") 
                    e.grid(row=i,column=2,ipadx=20) 
                    e = Label(newinterface7, text=passenger[3], bg="aqua") 
                    e.grid(row=i,column=3,ipadx=20) 
                    e = Label(newinterface7, text=passenger[5], bg="aqua") 
                    e.grid(row=i,column=4,ipadx=20) 
                    e = Label(newinterface7, text=passenger[8], bg="aqua") 
                    e.grid(row=i,column=5,ipadx=20) 
                    e = Label(newinterface7, text=passenger[9], bg="aqua") 
                    e.grid(row=i,column=6,ipadx=20) 
                    e = Label(newinterface7, text=passenger[10], bg="aqua") 
                    e.grid(row=i,column=7,ipadx=20)
                    e = Label(newinterface7, text=passenger[11], bg="aqua") 
                    e.grid(row=i,column=8,ipadx=20) 
                    e = Label(newinterface7, image=img, bg="aqua") 
                    e.grid(row=i, column=9,ipady=7)  
                    Button(newinterface7, text="update", font=("times", 10),
                    bg="lightgreen", command=updatemypass).grid(row=i, column=10,ipadx=15)
                    images.append(img) # garbage collection 
                    i=i+1 

                cur15.close()
                con15.close()
                newinterface7.mainloop()
            Button(newinterface3, text="Renew Pass", font=("times", 30),
                   bg="orange", command=renewpass).place(x=250, y=450)

            def newpass():
                query = "SELECT COUNT(email) FROM `newpass` WHERE email = %s"

                try:
                    con19 = mysql.connector.connect(
                        host='127.0.0.1', user='root', password='', database='smartbuspass')
                    cur19 = con19.cursor()
                    cur19.execute(query, (user,))
                    list18 = cur19.fetchall()

                except Error as e:
                    print(e)

                finally:
                    cur19.close()
                    con19.close()
                
                if (5,) not in list18:
                    newinterface4 = Toplevel(newinterface3)
                    newinterface4.geometry("1000x696")
                    newinterface4.title("new pass")
                    newinterface4.config(bg="aqua")

                    global filen, img
                    l5 = Label(newinterface4, text="APPLY NEW PASS",
                            font=("Bell MT", 50), bg="lightblue")
                    l5.place(x=210, y=12)

                    Label(newinterface4, text="Name: ",
                        font="Arial,25", bg="aqua").place(x=10, y=110)
                    e10 = Entry(newinterface4, bd=5, font="Arial,25")
                    e10.place(x=190, y=110)

                    Label(newinterface4, text="Date of Birth: ",
                        font="Arial,25", bg="aqua").place(x=10, y=160)
                    e11 = DateEntry(newinterface4, bd=5, font="Arial,25",
                                    selectmode='day', date_pattern='dd-mm-yyyy')
                    e11.place(x=190, y=160)

                    Label(newinterface4, text="Category: ",
                        font="Arial,25", bg="aqua").place(x=10, y=210)
                    global var3
                    var3 = StringVar()
                    Radiobutton(newinterface4, text="Male", variable=var3,
                                value="male", bg="aqua", font="Arial,25").place(x=190, y=210)
                    Radiobutton(newinterface4, text="Female", variable=var3,
                                value="female", bg="aqua", font="Arial,25").place(x=270, y=210)

                    Label(newinterface4, text="Mobile No.: ",
                        font="Arial,25", bg="aqua").place(x=10, y=260)
                    e12 = Entry(newinterface4, bd=5, font="Arial,25")
                    e12.place(x=190, y=260)

                    Label(newinterface4, text="AADHAR Card No.: ",
                        font="Arial,25", bg="aqua").place(x=10, y=310)
                    e13 = Entry(newinterface4, bd=5, font="Arial,25", width=25)
                    e13.place(x=190, y=310)

                    Label(newinterface4, text="Address: ",
                        font="Arial,25", bg="aqua").place(x=10, y=360)
                    e14 = Text(newinterface4, bd=5,
                            font="Arial,25", width=25, height=4)
                    e14.place(x=190, y=360)

                    ig = ImageTk.PhotoImage(file="profile.png")
                    profile = Label(newinterface4, image=ig, width=250, height=250)
                    profile.place(x=610, y=125)

                    Label(newinterface4, text="Location from: ",
                        font="Arial,25", bg="aqua").place(x=10, y=480)
                    optionsfrom = ["Meerut", "Modinagar", "Muradnagar",
                                "Ghaziabad", "Mohannagar", "Noida", "Delhi"]
                    global var1
                    var1 = StringVar()
                    var1.set("From")
                    OptionMenu(newinterface4, var1, *
                            optionsfrom).place(x=190, y=480)
                    Label(newinterface4, text="Location to: ",
                        font="Arial,25", bg="aqua").place(x=10, y=530)
                    optionsto = ["Meerut", "Modinagar", "Muradnagar",
                                "Ghaziabad", "Mohannagar", "Noida", "Delhi"]
                    global var2
                    var2 = StringVar()
                    var2.set("Destination")
                    OptionMenu(newinterface4, var2, *optionsto).place(x=190, y=530)

                    Label(newinterface4, text="PASS LIMIT: ",
                        font="Arial,25", bg="aqua").place(x=10, y=580)
                    dt3 = date.today()
                    calfrm = DateEntry(newinterface4, bd=5, font="Arial,25",
                                    selectmode='day', date_pattern='dd-mm-yyyy', mindate=dt3)
                    calfrm.place(x=190, y=580)
                    calto = DateEntry(newinterface4, bd=5, font="Arial,25",
                                    selectmode='day', date_pattern='dd-mm-yyyy', mindate=dt3)
                    calto.place(x=350, y=580)

                    def uploadimg():
                        global filen, img
                        f_types = [('JPG', '*.jpg'), ('PNG', '*.png'),
                                ('JPEG', '*.jpeg')]
                        filen = filedialog.askopenfilename(filetypes=f_types)
                        img = Image.open(filen)
                        img = img.resize((250, 250))
                        img = ImageTk.PhotoImage(img)
                        Label(newinterface4, image=img).place(x=610, y=125)
                    Button(newinterface4, text="Upload Photo", font=(
                        "times", 20), bg="yellow", command=uploadimg).place(x=650, y=410)

                    def submit():

                        con5 = mysql.connector.connect(
                            host='127.0.0.1', user='root', password='', database='smartbuspass')
                        cur5 = con5.cursor()
                        cur5.execute("SELECT aadhar FROM `newpass` ")
                        list4 = cur5.fetchall()
                        cur5.close()
                        con5.close()
                        con6 = mysql.connector.connect(
                            host='127.0.0.1', user='root', password='', database='smartbuspass')
                        cur6 = con6.cursor()
                        cur6.execute("SELECT mobile FROM `newpass` ")
                        list5 = cur6.fetchall()
                        cur6.close()
                        con6.close()
                        global var5, r1, r2, filen
                        Namee = e10.get()
                        today2 = date.today()
                        dt2 = e11.get_date()
                        datee = dt2.strftime("%d-%m-%Y")
                        birthyear2 = date(day=int(dt2.strftime("%d")), month=int(dt2.strftime("%m")),
                                        year=int(dt2.strftime("%Y")))
                        agepsg = today2.year - birthyear2.year - \
                            ((today2.month, today2.day) <
                            (birthyear2.month, birthyear2.day))
                        category = var3.get()
                        Mobno = e12.get()
                        aadhar = e13.get()
                        Adress = e14.get('0.0', "200.0")
                        locfrom = var1.get()
                        locto = var2.get()
                        idno = random.randint(100000, 900000)
                        con9 = mysql.connector.connect(
                            host='127.0.0.1', user='root', password='', database='smartbuspass')
                        cur9 = con9.cursor()
                        cur9.execute("SELECT passid FROM `newpass` ")
                        list8 = cur9.fetchall()
                        cur9.close()
                        con9.close()
                        passfrom = calfrm.get_date()
                        passto = calto.get_date()
                        days = (calto.get_date()-calfrm.get_date()).days

                        laadhar = list(aadhar)
                        count1 = 0
                        for x in laadhar:
                            count1 += 1
                        lmobi = list(Mobno)
                        count2 = 0
                        for x in lmobi:
                            count2 += 1
                        if Namee == "":
                            messagebox.showerror("Error", "Please Enter the name")
                        elif agepsg <= 16:
                            messagebox.showerror("Error", "User must be 16+")
                        elif category == "" or category == "MaleFemaleChild":
                            messagebox.showerror(
                                "Error", "Please select the Category")
                        elif Mobno == "":
                            messagebox.showerror(
                                "Error", "Please Enter the Mobile Number")
                        elif Mobno > "a" and Mobno < "z" or Mobno > "A" and Mobno < "B":
                            messagebox.showerror(
                                "Error", "Please Enter valid number digits")
                        elif count2 < 10 or count2 > 10:
                            messagebox.showerror("Validation Error",
                                                "Please Enter valid Mobile Number\n10 digit mobile number")
                        elif (Mobno,) in list5:
                            messagebox.showerror(
                                "Alert", "Mobile number Already used")
                        elif aadhar == "":
                            messagebox.showerror(
                                "Error", "Please Enter the Aadhar Number")
                        elif count1 < 12 or count1 > 12:
                            messagebox.showerror("Validation Error",
                                                "Please Enter valid aadhar number\n12 digit AADHAR Number")
                        elif (aadhar,) in list4:
                            messagebox.showerror(
                                "Alert", "Bus pass exist on this Aadhar no.")
                        elif Adress == "":
                            messagebox.showerror(
                                "Error", "Please Enter the Address")
                        elif locfrom == "From":
                            messagebox.showerror(
                                "Error", "Please choose your location")
                        elif locto == "Destination":
                            messagebox.showerror(
                                "Error", "Please choose destination ")
                        elif days < 30 or days > 365:
                            messagebox.showerror(
                                "Error", "Pass Limit Can Only Be \nMonthly and Yearly ")
                        elif (idno,) in list8:
                            idno = random.randint(100000, 900000)
                        else:
                            m = messagebox.askokcancel(
                                "Confirmation", "Submit or Not?")
                            if m == True:

                                l7.config(
                                    text="Details submitted succesfully!\ntap payment for transaction process", fg="Green", font="Arial,15")

                                con3 = mysql.connector.connect(
                                    host='127.0.0.1', user='root', password='', database='smartbuspass')
                                cur3 = con3.cursor()
                                cur3.execute(
                                    "insert into newpass (email,name,dobb,category,mobile,aadhar,address,fromloc,toloc,passfrom,passto,profile,passid) value ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                                        user, Namee, datee, category, Mobno, aadhar, Adress, locfrom, locto, passfrom, passto, img, idno))
                                con3.commit()

                                def payment():
                                    newinterface5 = Toplevel(newinterface4)
                                    newinterface5.geometry("1000x696")
                                    newinterface5.title("payment")
                                    Label(newinterface5, text="Name:-",
                                        font=("Bell MT", 22)).place(x=10, y=12)
                                    Label(newinterface5, text=Namee, font=(
                                        "times", 22)).place(x=150, y=12)
                                    Label(newinterface5, text="Place:-",
                                        font=("Bell MT", 22)).place(x=10, y=62)
                                    Label(newinterface5, text=locfrom + " to " +
                                        locto, font=("times", 22)).place(x=150, y=62)
                                    Label(newinterface5, text="Pass Limit is of:-",
                                        font=("Bell MT", 22)).place(x=10, y=112)
                                    Label(newinterface5, text=str(days)+" Days",
                                        font=("times", 22)).place(x=250, y=112)
                                    Label(newinterface5, text="Amount:-",
                                        font=("Bell MT", 22)).place(x=10, y=162)
                                    if locfrom == locto:
                                        amount = 0.0*days
                                    elif locfrom == "Meerut" and locto == "Modinagar" or locfrom == "Modinagar" and locto == "Meerut":
                                        amount = 20.0*(days-3)
                                    elif locfrom == "Meerut" and locto == "Muradnagar" or locfrom == "Muradnagar" and locto == "Meerut":
                                        amount = 35.0*(days-3)
                                    elif locfrom == "Meerut" and locto == "Ghaziabad" or locfrom == "Ghaziabad" and locto == "Meerut":
                                        amount = 50.0*(days-3)
                                    elif locfrom == "Meerut" and locto == "Mohannagar" or locfrom == "Mohannagar" and locto == "Meerut":
                                        amount = 65.0*(days-3)
                                    elif locfrom == "Meerut" and locto == "Noida" or locfrom == "Noida" and locto == "Meerut":
                                        amount = 80.0*(days-3)
                                    elif locfrom == "Meerut" and locto == "Delhi" or locfrom == "Delhi" and locto == "Meerut":
                                        amount = 95.0*(days-3)
                                    elif locfrom == "Modinagar" and locto == "Muradnagar" or locfrom == "Muradnagar" and locto == "Modinagar":
                                        amount = 15.0*(days-3)
                                    elif locfrom == "Modinagar" and locto == "Ghaziabad" or locfrom == "Ghaziabad" and locto == "Modinagar":
                                        amount = 30.0*(days-3)
                                    elif locfrom == "Modinagar" and locto == "Mohannagar" or locfrom == "Mohannagar" and locto == "Modinagar":
                                        amount = 45.0*(days-3)
                                    elif locfrom == "Modinagar" and locto == "Noida" or locfrom == "Noida" and locto == "Modinagar":
                                        amount = 75.0*(days-3)
                                    elif locfrom == "Modinagar" and locto == "Delhi" or locfrom == "Delhi" and locto == "Modinagar":
                                        amount = 90.0*(days-3)
                                    elif locfrom == "Muradnagar" and locto == "Ghaziabad" or locfrom == "Ghaziabad" and locto == "Muradnagar":
                                        amount = 17.0*(days-3)
                                    elif locfrom == "Muradnagar" and locto == "Mohannagar" or locfrom == "Muradnagar" and locto == "Modinagar":
                                        amount = 32.0*(days-3)
                                    elif locfrom == "Muradnagar" and locto == "Noida" or locfrom == "Noida" and locto == "Muradnagar":
                                        amount = 48.0*(days-3)
                                    elif locfrom == "Muradnagar" and locto == "Delhi" or locfrom == "Delhi" and locto == "Muradnagar":
                                        amount = 63.0 * (days - 3)
                                    elif locfrom == "Ghaziabad" and locto == "Mohannagar" or locfrom == "Muradnagar" and locto == "Ghaziabad":
                                        amount = 15.0*(days-3)
                                    elif locfrom == "Ghaziabad" and locto == "Noida" or locfrom == "Noida" and locto == "Ghaziabad":
                                        amount = 35.0*(days-3)
                                    elif locfrom == "Ghaziabad" and locto == "Delhi" or locfrom == "Delhi" and locto == "Ghaziabad":
                                        amount = 55.0*(days-3)
                                    elif locfrom == "Mohannagar" and locto == "Noida" or locfrom == "Noida" and locto == "Mohannagar":
                                        amount = 20.0*(days-3)
                                    elif locfrom == "Mohannagar" and locto == "Delhi" or locfrom == "Delhi" and locto == "Mohannagar":
                                        amount = 40.0*(days-3)
                                    else:
                                        amount = 0.0*(days-3)
                                    Label(newinterface5, text=amount, font=(
                                        "times", 22)).place(x=150, y=162)
                                    paypic = PhotoImage(file="payment.png")
                                    paymentpic = Label(
                                        newinterface5, image=paypic, width=400, height=400)
                                    paymentpic.place(x=190, y=212)

                                    def mypass():
                                        image = Image.new(
                                            'RGB', (880, 500), (81, 191, 232))
                                        draw = ImageDraw.Draw(image)
                                        draw.rectangle(
                                            xy=[(0, 0), (880, 80)], fill='#e86d51', outline='#e86d51', width=880)
                                        img1 = Image.open('./aprove.png')
                                        img1 = img1.resize((350, 350))
                                        image.paste(img1, (300, 150))

                                        (x, y) = (10, 10)
                                        company = str("SMART BUS PASS")
                                        color = 'rgb(0, 0, 0)'  # black color
                                        font = ImageFont.truetype(
                                            'arial.ttf', size=60)
                                        draw.text((x, y), company,
                                                fill=color, font=font)

                                        (x, y) = (580, 20)
                                        message = str('ID: ' + str(idno))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        font = ImageFont.truetype(
                                            'arial.ttf', size=60)
                                        draw.text((x, y), message,
                                                fill=color, font=font)

                                        (x, y) = (180, 100)
                                        fname = str('Name: ' + str(Namee))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        font = ImageFont.truetype(
                                            'arial.ttf', size=35)
                                        draw.text((x, y), fname,
                                                fill=color, font=font)

                                        (x, y) = (180, 150)
                                        fage = str('Age: ' + str(agepsg))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        draw.text((x, y), fage,
                                                fill=color, font=font)

                                        (x, y) = (400, 150)
                                        fgender = str('Gender: ' + str(category))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        draw.text((x, y), fgender,
                                                fill=color, font=font)

                                        (x, y) = (180, 200)
                                        fNo = str('Mobile Number: ' + str(Mobno))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        draw.text(
                                            (x, y), fNo, fill=color, font=font)

                                        (x, y) = (10, 250)
                                        famount = str('Amount: ' + str(amount))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        draw.text((x, y), famount,
                                                fill=color, font=font)

                                        (x, y) = (10, 300)
                                        froute = str(
                                            'Route: ' + str(locfrom) + " to " + str(locto))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        draw.text((x, y), froute,
                                                fill=color, font=font)

                                        (x, y) = (10, 350)
                                        flimit = str(
                                            'Validity: ' + str(passfrom) + " to " + str(passto))
                                        color = 'rgb(0, 0, 0)'  # black color
                                        draw.text((x, y), flimit,
                                                fill=color, font=font)

                                        update_blob(idno, filen)
                                        read_blob(idno,"read.jpg")
                                        img4 = Image.open('read.jpg')
                                        img4 = img4.resize((150, 150))
                                        image.paste(img4, (10, 90))

                                        qr = qrcode.QRCode(
                                            version=12,
                                            error_correction=qrcode.constants.ERROR_CORRECT_H,
                                            box_size=3,
                                            border=0
                                        )
                                        qr.add_data(str(idno) + '\n' + str(Namee) + '\n' + str(datee) + '\t' + str(
                                            agepsg) + '\n' + str(category) + '\n' + str(Mobno) + '\n' + str(
                                            aadhar) + '\n' + str(Adress) + '\n' + str(locfrom) + " to " + str(
                                            locto) + '\n' + str(passfrom) + " to " + str(passto))
                                        qr.make()
                                        QR = qr.make_image(
                                            fill_color="black", back_color="#51bfe8")
                                        image.paste(QR, (650, 200))

                                        image.save(str(Namee) + str(idno) + '.png')
                                        newinterface6 = Toplevel(newinterface5)
                                        newinterface6.geometry("1000x696")
                                        newinterface6.title("My Pass")
                                        passtemp = Image.open(
                                            str(Namee) + str(idno) + '.png')
                                        passtemp = passtemp.resize((880, 500))
                                        passtemp = ImageTk.PhotoImage(passtemp)
                                        Label(newinterface6, image=passtemp).place(
                                            x=60, y=60)
                                        pt1 = Label(
                                            newinterface6, text="BUS PASS Successfully Genrated")
                                        pt1.place(x=25, y=12)

                                        newinterface6.mainloop()
                                    Button(newinterface5, text="Generate Pass", bg="lightgreen", command=mypass,
                                        font="Arial,25").place(x=560, y=600)
                                    newinterface5.mainloop()

                                Button(newinterface4, text="PAYMENT", bg="lightgreen",
                                    command=payment, font="Arial,25").place(x=660, y=480)
                            else:
                                l7.config(
                                    text="Please check Your Details", fg="red")

                    def cleard():
                        if messagebox.askyesno("Alert!", "Clear all details"):
                            e10.delete(0, END)
                            e11.delete(0, 'end')
                            e12.delete(0, END)
                            e13.delete(0, END)
                            e14.delete("0.0", "end")
                            calfrm.delete(0, 'end')
                            calto.delete(0, 'end')

                    Button(newinterface4, text="Submit", bg="lightyellow",
                        command=submit, font="Arial,25").place(x=550, y=580)
                    Button(newinterface4, text="Clear", bg="red",
                        command=cleard, font="Arial,25").place(x=630, y=580)
                    l7 = Label(newinterface4, bg="aqua")
                    l7.place(x=170, y=630)
                    newinterface4.mainloop()
                else:
                    messagebox.showerror("Pass limit exceed",
                                        "Please use another email You have created 5 passes")
            Button(newinterface3, text="New Pass", command=newpass,
                   font=("times", 30), bg="orange").place(x=250, y=350)
            newinterface3.mainloop()
        else:
            messagebox.showerror("Authentication Failed",
                                 "Please Enter Valid Username or Password")

    Button(newinterface2, text="Login", command=login,
           font=("times", 22), bg="green").place(x=450, y=450)
    newinterface2.config(bg="white")
    newinterface2.mainloop()


Button(root, text="Sign IN", font=("times", 22),
       command=signin, bg="#645b49").place(x=175, y=580)
root.mainloop()
