from tkinter import Tk,Label,Frame,Entry,Button,messagebox,filedialog
from tkinter.ttk import Combobox
import time
import os,shutil
from PIL import Image,ImageTk
import random
import project_tables
import sqlite3
import projects_mail


#Captcha Generator :
def generate_captcha():
    captcha=[]
    for i in range(3):
        c=chr(random.randint(65,90))
        captcha.append(c)
        
        n=random.randint(0,9)
        captcha.append(str(n)) 
        
    random.shuffle(captcha)
    captcha=' '.join(captcha)
    return captcha

def refresh():
    captcha = generate_captcha()
    captcha_lbl.configure(text=captcha)
       
     
    

root=Tk()               
root.state("zoomed")                        #To get full size screen
root.config(bg='#0288d1')               #To set a background Colour
root.title('Banking Automation System')     #To give Title
root.resizable(width=False,height=False)

#Banking Automation 
title_lbl=Label(root,text='Banking Automation',bg="#0288d1",font=('algerian',50,"bold","underline"))
title_lbl.pack()
#Date & Time 
today_lbl=Label(root,text=time.strftime("%A,%d %B %Y"),bg="#0288d1",font=('arial',15,"bold"),fg='yellow')
today_lbl.pack(pady=10)

#Banking logo
img1 = Image.open("images/bank_logo.png").resize((250,150))
img_bitmap=ImageTk.PhotoImage(img1,master=root)

logo_lbl1=Label(root,image=img_bitmap)
logo_lbl1.place(relx=0.01,rely=0.01)

#Footer
footer_lbl=Label(root,text='Developed by : Kamrann_03',font='Algerian',bg='#0288d1', fg='yellow')
footer_lbl.pack(side='bottom',pady=10)

#separate window/frame
def main_screen():
    def forgot():       #forgot command
        frm.destroy()
        forgot_screen()

    def login():
        uacn=acn_entry.get()
        upass=pass_entry.get()
        ucap=inputcap_entry.get()
        utype=user_combo.get()
        actual_cap=captcha_lbl.cget('text')
        actual_cap=actual_cap.replace(" ",'')
        

        if utype=='Admin':
            if uacn=='0' and upass=='admin' :
                if ucap==actual_cap:
                    frm.destroy()
                    admin_screen()
                else: 
                    messagebox.showerror('Login', f"Invalid Captcha")
            else:
                messagebox.showerror("Login","Invalid ACN/PASS/TYPE")  
        elif utype=='User':
            if ucap==actual_cap:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where accounts_acno=? and account_pass=?'
                curobj.execute(query,(uacn,upass))
            
                tuple=curobj.fetchone()
                conobj.close() 
                if tuple==None:
                    messagebox.showerror("User Login ","Invalid Acn/Pass")
                else:
                    frm.destroy()
                    user_screen(uacn)

                      
            else: 
                messagebox.showerror('Login', f"Invalid Captcha")
                   
        else:
            messagebox.showerror("login", 'kindly Select VAlid user type')

            user_screen()

        #     else:
        #         messagebox.showerror('Login', 'Invalid Captcha')
        # else:
        #     messagebox.showerror('Login','Invalid ACN / Password / TYPE')

    frm=Frame(root)
    frm.config(bg='#f39c12')
    frm.place(relx=0,rely=.2,relwidth=1,relheight=0.75)
    
    user_lbl=Label(frm,text='User Type',bg='#f39c12',font=('arial',18,'bold'))
    user_lbl.place(relx=.36,rely=.1)
    #Combobox ( - To select User types)
    user_combo=Combobox(frm,values=['---select---','Admin','User'],font=('algerian',15,'bold'),state='readonly')
    user_combo.current(0)
    user_combo.place(relx=.45,rely=.1)
    #Label & Entry for ACN:
    acn_lbl=Label(frm,text='ACN',bg='#f39c12',font=('arial',18,'bold'))
    acn_lbl.place(relx=0.36,rely=0.2)
    
    acn_entry=Entry(frm,font=('arial',18),bd = 5,)
    acn_entry.place(relx=.45,rely=.2)
    acn_entry.focus()
    #Label and Entry for Password:
    acn_password=Label(frm,text='Password',bg='#f39c12',font=('arial',18,'bold'))
    acn_password.place(relx=0.36,rely=0.3)
    
    pass_entry=Entry(frm,font=('arial',18),bd = 5,show='*')
    pass_entry.place(relx=.45,rely=.3)
    
    #Captcha Entry & Captcha Calling
    global captcha_lbl
    inputcap_lbl1=Label(frm,text='Captcha :',font=('arial',18,'bold'),bg='#f39c12')
    inputcap_lbl1.place(relx=.36,rely=.5)
    
    captcha_lbl=Label(frm,text=generate_captcha(),bg='white',font=('arial',17,'bold'))
    captcha_lbl.place(relx=0.45,rely=0.4)
    
    #refresh Button for captcha
    refresh_btn=Button(frm,text="refresh",bd=5,bg='white',fg='black',font=('Arial',12,'bold'),width=8,height=1,command=refresh)
    refresh_btn.place(relx=.55,rely=.4)
    
    inputcap_entry=Entry(frm,font=('arial',18),bd=5)
    inputcap_entry.place(relx=.45,rely=.5)
    
    # Login button , Reset Button, & Forgot Button
    login_btn=Button(frm,text='login',bg='#0288d1',font=('arial',17,'bold'),bd=5,command=login)
    login_btn.place(relx=0.48,rely=0.6)
    
    Reset_btn=Button(frm,text='reset',bg='#0288d1',font=('arial',17,'bold'),bd=5)
    Reset_btn.place(relx=0.54,rely=0.6)
    
    forgot_btn=Button(frm,width=18,text='Fogot Password',bg='#0288d1',font=('arial',17,'bold'),bd=5,command=forgot)
    forgot_btn.place(relx=0.45,rely=0.7)
   #after Jump from 1st screen to 2nd one: 
def admin_screen():
    def open_acn():
        def open_acn_db():
            uname=name_entry.get()
            uemail=email_entry.get()
            umob=Mobile_entry.get()
            ugender=gender_combo.get()
            ubal=0.0
            uopendate=time.strftime("%A,%d %B %Y")
            upass=generate_captcha().replace(' ','')

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
 
            query='insert into accounts values(null,?,?,?,?,?,?,?)'
            curobj.execute(query,(uname,upass,uemail,umob,ugender,uopendate,ubal))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("open account", 'account opened successfully')
            print('Acn Created')
            
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()

            query='select max(accounts_acno) from accounts'
            curobj.execute(query)
            
            uacno=curobj.fetchone()[0]
            conobj.close()
            
            try:
                projects_mail.send_mail_for_openacn(uemail,uacno,uname,upass,uopendate)
                msg=f'Account opened with ACN {uacno} and mail sent to {uemail},kindly check spam also'

                messagebox.showinfo('Open Accounts',msg )    
            
            except Exception as msg:
                messagebox.showerror("open account",msg)
                
    # Reset Function at Login Page:
        def reset():
            name_entry.delete(0,"end")
            email_entry.delete(0,"end")
            Mobile_entry.delete(0,"end")
            gender_combo.current(0)
            name_entry.focus()
       
            
        i_frm=Frame(bd=5, relief='ridge')
        i_frm.configure(bg='white',)
        i_frm.place(relx=.25,rely=.22,relwidth=.6,relheight=.65)

        name_lbl=Label(i_frm,text='This is open account Screen',font=('arial',20,'bold'),bg='white',)
        name_lbl.pack()
        #Name
        acn_lbl=Label(i_frm,text='Name',bg='white',font=('arial',18,'bold'))
        acn_lbl.place(relx=0.1,rely=0.1)
        
        name_entry=Entry(i_frm,font=('arial',18),bd = 5,)
        name_entry.place(relx=.1,rely=.18)
        name_entry.focus()
        #E-mail
        email_lbl=Label(i_frm,text='Email',bg='white',font=('arial',20,'bold'))
        email_lbl.place(relx=.1,rely=.4)
        
        email_entry=Entry(i_frm,font=('arial',18),bd = 5,)
        email_entry.place(relx=.1,rely=.48)
        #Mobile
        Mobile_lbl=Label(i_frm,text='Mobile',bg='white',font=('arial',18,'bold'))
        Mobile_lbl.place(relx=.55,rely=0.1)
        
        Mobile_entry=Entry(i_frm,font=('arial',18),bd = 5,)
        Mobile_entry.place(relx=.55,rely=.18)
        #Gender
        Gender_lbl=Label(i_frm,text='Gender',bg='white',font=('arial',18,'bold'))
        Gender_lbl.place(relx=.55,rely=0.4)
        
        gender_combo=Combobox(i_frm,values=['Select','Male','Female','Others'],font=('Arial',18,'bold'),state='readonly')
        gender_combo.current(0)
        gender_combo.place(relx=.55,rely=.48)
        #Open account & Reset Button
        open_btn=Button(i_frm,text="Open ACN",bd=5,fg='black',bg='#f39c12',font=('Arial',12,'bold'),width=10,height=1,command=open_acn_db)
        open_btn.place(relx=.30,rely=.6,relheight=.08,relwidth=.17)

        Reset_btn=Button(i_frm,command=reset,text="Reset",bd=5,fg='black',bg='#f39c12',font=('Arial',12,'bold'),width=10,height=1)
        Reset_btn.place(relx=.50,rely=.6,relheight=.08,relwidth=.17)
        
    # Delete func by Admin Side : 
    def delete_acn():
        def send_otp():
            uacn=acn_entry.get()
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(uacn))
            
            tuple=curobj.fetchone()
            conobj.close() 
            if tuple==None:
                messagebox.showerror("Delete Account","Record not Found")
            else:
                otp=str(random.randint(1000,9999))
                projects_mail.send_otp(tuple[3],tuple[1],otp)
                messagebox.showinfo("Delete Account", "OTP sent to registred mail ID")

                otp_entry=Entry(i_frm,font=('arial',18),bd=6)
                otp_entry.place(relx=.39,rely=.5)
                #to verify OTP at forgot password screen  and to forget password
                def verify():
                    uotp=otp_entry.get()
                    if otp==uotp:
                        resp=messagebox.askyesno("Delete Account", f"Do you want to delete")
                        if not resp:
                            frm.destroy()
                            admin_screen()


                            return

                        conobj=sqlite3.connect(database='bank.sqlite')
                        curobj=conobj.cursor()
                        query='delete from accounts where accounts_acno=?'
                        curobj.execute(query,(uacn))
                        conobj.commit()
                        conobj.close()
                        messagebox.showinfo("Delete Account",f"Account Deleted")
                        frm.destroy()
                        admin_screen()
                    else:
                        messagebox.showerror("Delete Account","Incorrect OTP")
            
            
             
            Verify_btn=Button(i_frm,command=verify,text="Verify",bd=5,fg='black',bg='#0288d1',font=('Arial',12,'bold'),width=10,height=1)
            Verify_btn.place(relx=.43,rely=.6)
            
        i_frm=Frame(bd=5, relief='ridge')
        i_frm.configure(bg='white',)
        i_frm.place(relx=.25,rely=.22,relwidth=.6,relheight=.65)

        title_lbl=Label(i_frm,text='This is view account Screen',font=('arial',20,'bold'),bg='white',)
        title_lbl.pack()

        acn_lbl=Label(i_frm,text='ACN',bg='white',font=('arial',20,'bold'))
        acn_lbl.place(relx=.3,rely=.18)

        acn_entry=Entry(i_frm,font=('arial',20),bd=5)
        acn_entry.place(relx=.39,rely=.18)
        acn_entry.focus()

        OTP_btn=Button(i_frm,command=send_otp,text="Send OTP",bd=5,fg='black',bg='#0288d1',font=('Arial',15,'bold'),width=10,height=1)
        OTP_btn.place(relx=.42,rely=.32)
         
            
    # view account
    def view_acn():
        def view_details():
            uacn=acn_entry.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            
            tuple=curobj.fetchone()
            conobj.close() 
            if tuple==None:
                messagebox.showerror("View Account","Record not Found")
            else:
                #User Name
                user_name_lbl =Label(i_frm,text=f'User name : = {tuple[1]} ',font=('arial',17,'bold'),bg='white')
                user_name_lbl.place(relx=0.3,rely=0.5)
                # Aval Bal = {tuple[7]}
                Avl_bal_lbl =Label(i_frm,text=f'Available Balance : = {tuple[7]} ',font=('arial',17,'bold'),bg='white')
                Avl_bal_lbl.place(relx=0.3,rely=0.57)
                # ACN Open Date = {tuple[6]}
                acn_opn_date_lbl =Label(i_frm,text=f'Account Open Date : = {tuple[6]} ',font=('arial',17,'bold'),bg='white')
                acn_opn_date_lbl.place(relx=0.3,rely=0.64)
                # Email = {tuple[3]}
                email_lbl =Label(i_frm,text=f'E-mail : = {tuple[3]} ',font=('arial',17,'bold'),bg='white')
                email_lbl.place(relx=0.3,rely=0.71)
                # Mob = {tuple[4]}
                Mob_lbl =Label(i_frm,text=f'Mobile NO : = {tuple[4]} ',font=('arial',17,'bold'),bg='white')
                Mob_lbl.place(relx=0.3,rely=0.78)

                
            
        # /////////////////
        i_frm=Frame(bd=5, relief='ridge')
        i_frm.configure(bg='white',)
        i_frm.place(relx=.25,rely=.22,relwidth=.6,relheight=.65)

        title_lbl=Label(i_frm,text='This is view account Screen',font=('arial',20,'bold'),bg='white',)
        title_lbl.pack()
        
        acn_lbl=Label(i_frm,text='ACN',bg='white',font=('arial',20,'bold'))
        acn_lbl.place(relx=.3,rely=.18)

        acn_entry=Entry(i_frm,font=('arial',20),bd=5)
        acn_entry.place(relx=.39,rely=.18)
        acn_entry.focus()

        View_btn=Button(i_frm,command=view_details,text="View",bd=5,fg='black',bg='#0288d1',font=('Arial',15,'bold'),width=10,height=1)
        View_btn.place(relx=.42,rely=.32)
        
        
      #logout function  
    def logout():
        resp=messagebox.askyesno("logout",'Do you want to logout?')
        if resp:
            frm.destroy()
            main_screen()  
        
    frm = Frame(root)
    frm.configure(bg='#f39c12')
    frm.place(relx=0,rely=.2,relwidth=1,relheight=0.75)

    welcome_lbl=Label(frm,text='Welcome, Admin',bg='#f39c12',font=('arial',17,'bold'))
    welcome_lbl.place(relx=0,rely=0.0)
    #Log-Out Button
    log_out_btn=Button(frm,text='Log out',font=('arial',15,'bold'),command=logout)
    log_out_btn.place(relx=0.9,rely=0.01)
    #Open account Button
    open_btn=Button(frm,width=13,text="open account",bg='green',font=('arial',20,'bold'),command=open_acn)
    open_btn.place(relx=0.05,rely=0.2)
    #Delete button
    delete_btn=Button(frm,width=13,text="Delete account",bg='red',font=('arial',20,'bold'),command=delete_acn)
    delete_btn.place(relx=0.05,rely=.4)
    #view button
    view_btn=Button(frm,width=13,text="View account",fg='black',bg='yellow',font=('arial',20,'bold'),command=view_acn)
    view_btn.place(relx=0.05,rely=0.6)
    #forgot password screen
def forgot_screen():
    def back():
        frm.destroy()
        main_screen()
        #Send OTP at forgot screen to forgot password
    def send_otp():
        uacn=acn_entry.get()
        uemail=email_entry.get()
        ucaptcha = Captcha_entry.get()
        if ucaptcha!=forgot_captcha.replace(' ',''):
            messagebox.showerror('Forgot Password',f'Invalid Captcha')
            return
        
        
        #authenticate acn & email
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=? and accounts_email=?'
        curobj.execute(query,(uacn,uemail))
        
        tuple=curobj.fetchone()
        curobj.close()
        if tuple==None:
            messagebox.showerror("Forgot Password","Record not Found")
        else:
            otp=str(random.randint(1000,9999))
            projects_mail.send_otp(uemail,tuple[1],otp)
            messagebox.showinfo("OTP Sent Successfully",f"OTP sent to given registred mail id ")

            otp_entry=Entry(frm,font=('arial',18),bd = 5,)
            otp_entry.place(relx=.45,rely=.7)
            #to verify OTP at forgot password screen  and to forget password
            def verify():
                uotp=otp_entry.get()
                if otp==uotp:
                    messagebox.showinfo("forgot Password", f"your pass = {tuple[2]}")
                else:
                    messagebox.showerror("forgot Password","Incorrect OTP")
            
            
             
            Verify_btn=Button(frm,command=verify,text="Verify",bd=5,fg='black',bg='#0288d1',font=('Arial',12,'bold'),width=10,height=1)
            Verify_btn.place(relx=.7,rely=.7)
        #send OTP
        #generate entry to enter OTP
        
        
        
        
    frm = Frame(root)
    frm.configure(bg='#f39c12')
    frm.place(relx=0,rely=.2,relwidth=1,relheight=0.75)
    #Back Button
    view_btn=Button(frm,width=8,text="Back",fg='black',bg='#0288d1',font=('arial',15,'bold'),command=back)
    view_btn.place(relx=0.02,rely=0.03)
    #Acn Label
    acn_lbl=Label(frm,text='ACN',bg='#f39c12',font=('arial',18,'bold'))
    acn_lbl.place(relx=0.36,rely=0.2)
    # ACN Entry
    acn_entry=Entry(frm,font=('arial',18),bd = 5,)
    acn_entry.place(relx=.45,rely=.2)
    acn_entry.focus()
    
    email_lbl=Label(frm,text='Email',bg='#f39c12',font=('arial',18,'bold'))
    email_lbl.place(relx=0.36,rely=0.3)
    
    email_entry=Entry(frm,font=('arial',18),bd = 5,)
    email_entry.place(relx=.45,rely=.3)
    #Captcha 
    global captcha_lbl
    forgot_captcha=generate_captcha()
    captcha_lbl=Label(frm,text=forgot_captcha,bg='white',font=('arial',17,'bold'))
    captcha_lbl.place(relx=0.45,rely=0.4)
    #refresh button
    refresh_btn=Button(frm,text="refresh",bd=5,bg='white',fg='black',font=('Arial',12,'bold'),width=8,height=1,command=refresh)
    refresh_btn.place(relx=.55,rely=.4)
    #captcha Text
    inputcap_lbl1=Label(frm,text='Captcha :',font=('arial',18,'bold'),bg='#f39c12')
    inputcap_lbl1.place(relx=.36,rely=.5)
    
    Captcha_entry=Entry(frm,font=('arial',18),bd = 5,)
    Captcha_entry.place(relx=.45,rely=.5)
    
    OTP_btn=Button(frm,text="Send OTP",command=send_otp,bd=5,fg='black',bg='#0288d1',font=('Arial',12,'bold'),width=10,height=1)
    OTP_btn.place(relx=.45,rely=.6)

    Reset_btn=Button(frm,text="Reset",bd=5,fg='black',bg='#0288d1',font=('Arial',12,'bold'),width=10,height=1)
    Reset_btn.place(relx=.54,rely=.6)
#user Screen
def user_screen(uacn=None):
    def logout():
        resp=messagebox.askyesno("logout",'Do you want to logout?')
        if resp:
            frm.destroy()
            main_screen()  
    def get_details():
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=?'
        curobj.execute(query,(uacn,))
            
        tuple=curobj.fetchone()
        conobj.close() 
        return tuple
    
    def update_picture():
        path=filedialog.askopenfilename()
        shutil.copy(path,f'images/{uacn}.png')

        img = Image.open(f"images/{uacn}.png").resize((160,150))
        img_bitmap=ImageTk.PhotoImage(img,master=root)
        logo_lbl.image=img_bitmap 
        logo_lbl.configure(image=img_bitmap)
        
     
                
            
    frm = Frame(root)
    frm.configure(bg='#f39c12')
    frm.place(relx=0,rely=.2,relwidth=1,relheight=0.75)

    
    welcome_lbl=Label(frm,text=f'Welcome,{get_details()[1]}',bg='#f39c12',font=('arial',17,'bold'))
    welcome_lbl.place(relx=0,rely=0.0)
    
    global img_bitmap
    if os.path.exists(f'images/{uacn}.png'):
        path=f"images/{uacn}.png"
    else:
        path="images/profiles.png"
                      
    img = Image.open(path).resize((160,150))
    user_img_bitmap = ImageTk.PhotoImage(img, master=root)
    logo_lbl = Label(frm, image=user_img_bitmap)
    logo_lbl.image = user_img_bitmap

    logo_lbl.place(relx=0.03,rely=0.075)
    
    update_pic_btn=Button(frm,text='Update',command = update_picture,width=13,bg='violet',font=('arial',15,'bold'))
    update_pic_btn.place(relx=.03,rely=.34)
    
    
    
    #Log-Out Button
    log_out_btn=Button(frm,text='Log out',font=('arial',15,'bold'),command=logout)
    log_out_btn.place(relx=0.9,rely=0.01)
    
    #check Button
    chk_btn=Button(frm,text='Check Details',width=13,font=('arial',15,'bold'),command=lambda: check_screen(uacn))
    chk_btn.place(relx=0.03,rely=0.43)
    # Deposit
    deposit_btn=Button(frm,text='Deposit',width=13,bg='green',font=('arial',15,'bold'),command=lambda: deposit_btn_screen(uacn))
    deposit_btn.place(relx=0.03,rely=0.53)
    #withdraw
    withdraw_btn=Button(frm,text='Withdraw',width=13,bg='Red',font=('arial',15,'bold'),command=lambda: withdraw_screen(uacn))
    withdraw_btn.place(relx=0.03,rely=0.63)
    #update
    update_btn=Button(frm,text='update',width=13,bg='violet',font=('arial',15,'bold'),command=lambda: update_screen(uacn))
    update_btn.place(relx=0.03,rely=0.73)
    #Transfer
    Transfer_btn=Button(frm,text='Transfer',width=13,bg='Pink',font=('arial',15,'bold'),command=lambda: transfer_screen(uacn))
    Transfer_btn.place(relx=0.03,rely=0.83)
    #History
    History_btn=Button(frm,text='History',width=13,bg='Pink',font=('arial',15,'bold'),command=lambda: history_screen(uacn))
    History_btn.place(relx=0.03,rely=0.93)
# check button sceen
def check_screen(uacn):
        i_frm=Frame(bd=5, relief='ridge')
        i_frm.configure(bg='white',)
        i_frm.place(relx=.25,rely=.22,relwidth=.6,relheight=.65)

        name_lbl=Label(i_frm,text='This is Details account Screen',font=('arial',20,'bold'),bg='white',)
        name_lbl.pack()
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select * from accounts where accounts_acno=?',(uacn,))
        tup = curobj.fetchone()
        conobj.close()

        details=f'''Account No. = {tup[0]}
        
    opending Date = {tup[6]}
         
    Available Balance = {tup[7]}
        
    Email = {tup[3]}

     Mob = {tup[4]}
        
        '''
        details_lbl=Label(i_frm,text =details,bg='white',fg='purple',font=('arial',20,'bold'))
        details_lbl.place(relx=.2,rely=.2)


        
        
        
def deposit_btn_screen(uacn):
    def Deposit():
        uamt = float(amt_entry.get())
        
        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()

        # ✅ Fixed column name from 'account_bal' to 'accounts_bal'
        query = 'update accounts set accounts_bal = accounts_bal + ? where accounts_acno = ?'
        curobj.execute(query, (uamt, uacn))
        conobj.commit()
        conobj.close()
        
        # Fetch updated balance
        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query  = 'select accounts_bal from accounts where accounts_acno = ?'
        curobj.execute(query, (uacn,))
        ubal = curobj.fetchone()[0]   # ✅ Now ubal is correctly fetched
        conobj.close()
        
        t = str((time.time()))
        utxnid = 'txn' + t[:t.index('.')]
        
        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query = 'insert into stmts values(?,?,?,?,?,?)'
        curobj.execute(query, (uacn, uamt, 'CR', time.strftime("%d-%m-%Y %r"), ubal, utxnid))
        conobj.commit()
        conobj.close()

        messagebox.showinfo("Deposit", f"{uamt} Amount Deposited")
        i_frm.destroy()
        user_screen(uacn)

    i_frm=Frame(bd=5, relief='ridge')
    i_frm.configure(bg='white',)
    i_frm.place(relx=.25,rely=.22,relwidth=.6,relheight=.65)

    name_lbl=Label(i_frm,text='This is deposit account Screen',font=('arial',20,'bold'),bg='white',)
    name_lbl.pack()
    
    amt_lbl=Label(i_frm,text='Amount',bg='white',font=('arial',20,'bold'))
    amt_lbl.place(relx=.2,rely=.18)

    amt_entry=Entry(i_frm,font=('arial',20),bd=5)
    amt_entry.place(relx=.39,rely=.18)
    amt_entry.focus()

    Dep_btn=Button(i_frm,command=Deposit,text="Deposit",bd=5,fg='black',bg='#0288d1',font=('Arial',15,'bold'),width=10,height=1)
    Dep_btn.place(relx=.42,rely=.32)
    
    
    # ////////////////////////////////////////////
    
    
    
    
    
def withdraw_screen(uacn):
    # ///////////////////////////
    def withdraw():
        uamt = float(amt_entry.get())
        # Fetch updated balance
        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query  = 'select accounts_bal from accounts where accounts_acno = ?'
        curobj.execute(query, (uacn,))
        ubal = curobj.fetchone()[0]  
        conobj.close()
        
        if ubal>=uamt:
        
            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            # ✅ Fixed column name from 'account_bal' to 'accounts_bal'
            query = 'update accounts set accounts_bal = accounts_bal - ? where accounts_acno = ?'
            curobj.execute(query, (uamt, uacn))
            conobj.commit()
            conobj.close()
            
            
            
            t = str((time.time()))
            utxnid = 'txn' + t[:t.index('.')]
            
            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            query = 'insert into stmts values(?,?,?,?,?,?)'
            curobj.execute(query, (uacn, uamt, 'DB.', time.strftime("%d-%m-%Y %r"), ubal-uamt, utxnid))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Withdraw", f"{uamt} Amount Withdrawn")
            i_frm.destroy()
            user_screen(uacn)
        else:
            messagebox.showerror("withdraw", f"Insufficient Balance {ubal}")
      
    i_frm=Frame(bd=5, relief='ridge')
    i_frm.configure(bg='white',)
    i_frm.place(relx=.25,rely=.22,relwidth=.6,relheight=.65)

    name_lbl=Label(i_frm,text='This is withdraw account Screen',font=('arial',20,'bold'),bg='white',)
    name_lbl.pack()
    
    amt_lbl=Label(i_frm,text='Amount',bg='white',font=('arial',20,'bold'))
    amt_lbl.place(relx=.2,rely=.18)

    amt_entry=Entry(i_frm,font=('arial',20),bd=5)
    amt_entry.place(relx=.39,rely=.18)
    amt_entry.focus()

    Dep_btn=Button(i_frm,command=withdraw,text="Withdraw",bd=5,fg='black',bg='#0288d1',font=('Arial',15,'bold'),width=10,height=1)
    Dep_btn.place(relx=.42,rely=.32)
    
    
def update_screen(uacn):
    def update_db():
        uname = name_entry.get()
        upass = pass_entry.get()
        uemail = email_entry.get()
        umob = Mobile_entry.get()

        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query = 'update accounts set accounts_name=?, account_pass=?, accounts_email=?, accounts_mob=? WHERE accounts_acno=?'
        curobj.execute(query, (uname, upass, uemail, umob,uacn))
        conobj.commit()
        conobj.close()
        messagebox.showinfo("Update Details","Profile Updated")
        i_frm.destroy()
        user_screen(uacn)




    i_frm=Frame(bd=5, relief='ridge')
    i_frm.configure(bg='white',)
    i_frm.place(relx=.25,rely=.22,relwidth=.6,relheight=.65)

    name_lbl=Label(i_frm,text='This is update account Screen',font=('arial',20,'bold'),bg='white',)
    name_lbl.pack()
    
    conobj=sqlite3.connect(database='bank.sqlite')
    curobj=conobj.cursor()
    curobj.execute('select * from accounts where accounts_acno=?',(uacn,))
    tup = curobj.fetchone()
    conobj.close()
    
    #Name
    acn_lbl=Label(i_frm,text='Name',bg='white',font=('arial',18,'bold'))
    acn_lbl.place(relx=0.1,rely=0.1)
    
    name_entry=Entry(i_frm,font=('arial',18),bd = 5,)
    name_entry.place(relx=.1,rely=.18)
    name_entry.insert(0,tup[1])
    name_entry.focus()
    #E-mail
    email_lbl=Label(i_frm,text='Email',bg='white',font=('arial',20,'bold'))
    email_lbl.place(relx=.1,rely=.4)
        
    email_entry=Entry(i_frm,font=('arial',18),bd = 5,)
    email_entry.place(relx=.1,rely=.48)
    email_entry.insert(0,tup[3])
    #Mobile
    Mobile_lbl=Label(i_frm,text='Mobile',bg='white',font=('arial',18,'bold'))
    Mobile_lbl.place(relx=.55,rely=0.1)
        
    Mobile_entry=Entry(i_frm,font=('arial',18),bd = 5,)
    Mobile_entry.place(relx=.55,rely=.18)
    Mobile_entry.insert(0,tup[4])
    
    password_lbl=Label(i_frm,text='Password',bg='white',font=('arial',18,'bold'))
    password_lbl.place(relx=.55,rely=0.4)
        
    pass_entry=Entry(i_frm,font=('arial',18),bd = 5,)
    pass_entry.place(relx=.55,rely=.48)
    pass_entry.insert(0,tup[2])
    #Update Button / Details Update By user
    update_btn=Button(i_frm,command=update_db,text="Update",bd=5,fg='black',bg='#f39c12',font=('Arial',12,'bold'),width=10,height=1)
    update_btn.place(relx=.38,rely=.6,relheight=.08,relwidth=.17) 

    
    
    
    
def transfer_screen(uacn,):
    # //////////////////////////////
    def Transfer():
        toacn=to_entry.get()
        uamt = float(amt_entry.get())
        
        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query  = 'select accounts_bal from accounts where accounts_acno = ?'
        curobj.execute(query, (toacn,))
        to_tup = curobj.fetchone()   # ✅ Now ubal is correctly fetched
        conobj.close()
        if to_tup==None:
            messagebox.showerror("Transfer",f'To ACN does not exist')
            return

        
        
        # Fetch updated balance
        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query  = 'select accounts_bal from accounts where accounts_acno = ?'
        curobj.execute(query, (uacn,))
        ubal = curobj.fetchone()[0]   # ✅ Now ubal is correctly fetched
        conobj.close()
        
        if ubal>=uamt:
        
            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            # ✅ Fixed column name from 'account_bal' to 'accounts_bal'
            query_deduct = 'update accounts set accounts_bal = accounts_bal - ? where accounts_acno = ?'
            query_credit = 'update accounts set accounts_bal = accounts_bal + ? where accounts_acno = ?'

            curobj.execute(query_deduct, (uamt, uacn))
            curobj.execute(query_credit, (uamt, toacn))
            
             
            conobj.commit()
            conobj.close()
            
            
            
            t = str((time.time()))
            utxnid1 = 'txn_db'+ t[:t.index('.')]
            utxnid2 = 'txn_cr'+ t[:t.index('.')]
            
            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            query1 = 'insert into stmts values(?,?,?,?,?,?)'
            query2 = 'insert into stmts values(?,?,?,?,?,?)'
            curobj.execute(query1, (uacn, uamt, 'DB.', time.strftime("%d-%m-%Y %r"), ubal-uamt, utxnid1))
            curobj.execute(query2, (toacn, uamt, 'CR.', time.strftime("%d-%m-%Y %r"), ubal-uamt, utxnid2))

            conobj.commit()
            conobj.close()

            messagebox.showinfo("Transfer", f"{uamt} Amount Transfer")
            i_frm.destroy()
            user_screen(uacn)
        else:
            messagebox.showerror("Transfer", f"Insufficient Balance {ubal}")
      
    



    # //////////////////////////////
    
    
    i_frm=Frame(bd=5, relief='ridge')
    i_frm.configure(bg='white',)
    i_frm.place(relx=.25,rely=.22,relwidth=.6,relheight=.65)

    name_lbl=Label(i_frm,text='This is transfer account Screen',font=('arial',20,'bold'),bg='white',)
    name_lbl.pack() 
    # ////////////////////////////////////
    to_lbl=Label(i_frm,text='TO ACN',bg='white',font=('arial',20,'bold'))
    to_lbl.place(relx=.2,rely=.18)

    to_entry=Entry(i_frm,font=('arial',20),bd=5)
    to_entry.place(relx=.39,rely=.18)
    to_entry.focus()
    
    
    amt_lbl=Label(i_frm,text='Amount',bg='white',font=('arial',20,'bold'))
    amt_lbl.place(relx=.2,rely=.3)

    amt_entry=Entry(i_frm,font=('arial',20),bd=5)
    amt_entry.place(relx=.39,rely=.3)

    tr_btn=Button(i_frm,command=Transfer,text="Transfer",bd=5,fg='black',bg='#0288d1',font=('Arial',15,'bold'),width=10,height=1)
    tr_btn.place(relx=.42,rely=.42)
    
    
    
    
    
    
    
    # //////////////////////////////
from tkinter.ttk import Treeview

def history_screen(uacn):
    i_frm = Frame(bd=5, relief='ridge', bg='white')
    i_frm.place(relx=.25, rely=.22, relwidth=.6, relheight=.65)

    Label(i_frm, text='Transaction History', font=('arial', 20, 'bold'), bg='white').pack(pady=10)

    columns = ("Txn ID", "Amount", "Txn Type", "Update Bal", "Date")
    tree = Treeview(i_frm, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack(fill='both', expand=True)

    conobj = sqlite3.connect(database='bank.sqlite')
    curobj = conobj.cursor()
    curobj.execute(
        '''SELECT stmts_txnid, stmts_amt, stmts_type, stmts_Update_bal, stmts_date 
           FROM stmts WHERE stmts_acn=?''', (uacn,))
    for row in curobj.fetchall():
        tree.insert("", "end", values=row)

    conobj.close()

# def history_screen(uacn,):
#     i_frm=Frame(bd=5, relief='ridge')
#     i_frm.configure(bg='white',)
#     i_frm.place(relx=.25,rely=.22,relwidth=.6,relheight=.65)

#     name_lbl=Label(i_frm,text='This is history account Screen',font=('arial',20,'bold'),bg='white',)
#     name_lbl.pack()
#     import tktable
#     table_headers = ("Txn ID", "Amount", "Txn Type" ,"Update Bal", "Date")
#     mytable = tktable.Table(i_frm,table_headers,col_width=150,headings_bold=True)
#     mytable.pack(pady = 10)
    
#     conobj=sqlite3.connect(database='bank.sqlite')
#     curobj=conobj.cursor()
#     query='select stmts_txnid,stmts_amt,stmts_type,stmts_Update_bal,stmts_date from stmts where stmts_acn=?'
#     curobj.execute(query,(uacn,))
#     for tup in curobj:
#         mytable.insert_row(tup)
        
#     conobj.close()
    






main_screen()
root.mainloop()                              #Visible the screen







