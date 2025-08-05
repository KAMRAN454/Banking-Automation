import gmail
email = 'xxxxxxx@gmail.com'     #mention your gmail id
app_pass = 'xxxxxxxxxx'    #mention your app password of same gmail account
def send_mail_for_openacn(to_mail,uacno,uname,upass,udate):
        con=gmail.GMail(email,app _pass)
        sub='Account Opened With GW Bank'
        
        
        body=f"""Dear {uname},
        Your account has been Opened successfully with GW Bank and details are
    ACN={uacno}
    pass={upass}
    open date = {udate}

    Kindly change your password when you login first time
    Thanks
    GW Bank
    Noida
    """
        msg = gmail.Message(to=to_mail,subject=sub,text=body)
        con.send(msg)
        
def send_otp(to_mail,uname,uotp):
    con=gmail.GMail(email,app_pass)
    sub='OTP for password Recovery'
    body=f"""Dear{uname},
        Your OTP to get password = {uotp}
   

    Kindly verify this OTP to application
    Thanks
    GW Bank
    Noida
    """
    msg = gmail.Message(to=to_mail,subject=sub,text=body)
    con.send(msg)
   
    

