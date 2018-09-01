# app
import sqlite3
import os
import base64
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog

from PIL import ImageTk, Image

conn = sqlite3.connect("app2.db")
c = conn.cursor()


c.execute("CREATE TABLE IF NOT EXISTS data(f_name text, l_name text, username text, password text, email text)")
conn.commit()
c.execute("CREATE TABLE IF NOT EXISTS pictures(username text, picture BLOB, filename text,extension text )")
conn.commit()
c.execute("CREATE TABLE IF NOT EXISTS profile_picture(username text, profile_pic BLOB)")
# c.execute("INSERT INTO data VALUES())

lgn_name=""
lgn_passwd =""
backup=""


def donothing():
    print("working...")

def quiting1():
    if backup!="":
        os.remove(backup)
    os.remove('shrake.png')
    root.quit()

def about():
    msg = tkinter.messagebox.showinfo('About', '\tShrake\n\nhttps://www.shrake.com\n\nVersion : 1.5.0\n\nBuild : 3176')

              #******  Login account  **************

def login_account(received=None):

    def insert_image():
        global lgn_name
        address = tkinter.filedialog.askopenfilename(filetypes=[("image jpg"),("image png"),("text txt"),("AllFiles .*")])
        with open(address,'rb') as txt:
            ablob = txt.read()
            base_name = os.path.basename(address)
            file_name, file_ext = os.path.splitext(base_name)
            c.execute("INSERT INTO pictures VALUES(?, ?, ?, ?)",(lgn_name, sqlite3.Binary(ablob), file_name, file_ext))
            conn.commit()
        labl = Label(lgn_frame1, text="Image Added Successfully.",bg='light green').place(x=220, y=200)

    def list_image():

        def item_select(event):
            global lgn_name,backup
            def viewer():
                vr = Toplevel()
                img = Image.open(filenm)
                img.thumbnail((1100, 850))
                vr.geometry("1200x900")
                vr.title("Image Viewer")
                fr = Frame(vr, width=1200, height=900)
                fr.place(x=0, y=0)
                img = ImageTk.PhotoImage(img)
                can = Canvas(fr)
                lb = Label(fr, image=img)
                lb.place(x=0,y=0)
                Canvas.create_image(can, image=img).pack()

            lgn_frame_2 = Frame(lgn_frame1, width=500, height=500)
            view = Button(lgn_frame1,command=viewer, text="view", bg="light blue")
            view.place(x=640,y=70)

            lgn_frame_2.place(x=400, y=100)
            filenm = str(img_list.get(ACTIVE))
            if backup!=filenm:
                if backup!="":
                    os.remove(backup)
            backup = filenm
            file_nm, file_ext = filenm[:len(filenm)-4], filenm[len(filenm)-4:]

            c.execute("SELECT picture FROM pictures WHERE username=? AND filename=? AND extension=?",(lgn_name, file_nm, file_ext))
            conn.commit()
            ablob = c.fetchone()
            ab = ablob[0]
            with open(filenm,'wb') as output:
                output.write(ab)
            if file_ext=='.jpg' or file_ext=='.png':
                cann = Canvas(lgn_frame1,width=500, height=500)
                cann.pack()
                img = Image.open(filenm)
                img.thumbnail((500,500))
                img = ImageTk.PhotoImage(img)
                lbl5 = Label(lgn_frame_2, image=img).place(x=0, y=0)

                ca = cann.create_image(image=img).pack()

            elif file_ext=='.txt':
                lgn_frame_2 = Frame(lgn_frame1, width=450, height=500)
                lgn_frame_2.place(x=400, y=100)
                with open(filenm,'r') as txt:
                    text = txt.read()
                msg = Message(lgn_frame_2, text=text)
                msg.config(bg='light blue', font=('material',10,))
                msg.pack()

        global lgn_name
        lgn_frame_2 = Frame(lgn_frame1, width=200, height=200)
        lgn_frame_2.place(x=180, y=200)
        scrollbar = Scrollbar(lgn_frame_2)
        scrollbar.pack(side=RIGHT, fill=Y)
        img_list = Listbox(lgn_frame_2,width=30, height=10, yscrollcommand = scrollbar.set )
        c.execute("SELECT filename, extension FROM pictures WHERE username=?",(lgn_name,))
        conn.commit()
        images = c.fetchall()
        for img in images:
            img_list.insert(END, img[0]+img[1])

        img_list.bind("<<ListboxSelect>>", item_select)
        img_list.pack( side = LEFT, fill = BOTH )
        scrollbar.config( command = img_list.yview )


    def delete_file():

        # profile()
        global lgn_name
        lgn_frame3 = Frame(lgn_frame1, width=200, height=200)
        lgn_frame3.place(x=180, y=200)

        def item_sel(event):
            def delete_select():
                msg = tkinter.messagebox.askquestion("Delete File","Are you sure you want to delete this file?")
                if msg=='yes':

                    c.execute("DELETE FROM pictures WHERE username=? AND filename=? AND extension=?",(lgn_name, file_nm1, file_ext1))
                    conn.commit()
                    delete_file()


            filenme = str(imglist.get(ACTIVE))
            file_nm1, file_ext1 = filenme[:len(filenme)-4], filenme[len(filenme)-4:]
            dele = Button(lgn_frame1, text="  Delete  ", bg='light blue', command=delete_select).place(x=255, y=170)


        scr = Scrollbar(lgn_frame3)
        scr.pack(side=RIGHT, fill=Y)
        imglist = Listbox(lgn_frame3,width=30, height=10, yscrollcommand = scr.set )
        c.execute("SELECT filename, extension FROM pictures WHERE username=?",(lgn_name,))
        conn.commit()
        images = c.fetchall()
        for img in images:
            imglist.insert(END, img[0]+img[1])
        imglist.bind("<<ListboxSelect>>", item_sel)
        imglist.pack( side = LEFT, fill = BOTH )
        scr.config( command = imglist.yview )


    def profile():
        lgn_frame2 = Frame(lgn_frame1,width=950,height=500)
        lgn_frame2.place(x=0,y=55)
        cann = Canvas(lgn_frame2,width=950,height=500)
        cann.pack()
        for i in range(0,700,1):
            can1 = cann.create_line(0+i,0,900+i,400+i,fill='grey')
            can4 = cann.create_line(50-i*i//9,300+i,i+700,600,fil='light blue')
            can2 = cann.create_line(600-i*i,900+i,i,400-i,fill='red')
            can3 = cann.create_line(1000,i,200+i,100+i, fill='light green')
            can5 = cann.create_oval(15,40,120,145,fill='grey97')

        profile_btn = Button(lgn_frame1, text="   Profile   ", border=0,bg='light green',command=profile).place(x=35, y=280)
        img_btn = Button(lgn_frame1, text='  Add File  ', border=0, bg='light blue',command=insert_image).place(x=250, y=70)
        list_img_btn = Button(lgn_frame1, text="   List File  ", border=0, bg='light blue',command=list_image).place(x=250, y=100)
        delete_btn = Button(lgn_frame1, command=delete_file, text="Delete File", border=0, bg='light blue').place(x=250, y=130)
        search_btn = Button(lgn_frame1, text="search user", border=0, bg='light green', command=search_bar).place(x=433, y=100)
        changeprofile = Button(lgn_frame1, text="Change profile", border=0, bg="light green", command=change_profile).place(x=22, y=220)

        profile_frame = Frame(lgn_frame1, width=140, height=140)
        profile_frame.place(x=5, y=65)
        c1 = Canvas(lgn_frame1,width=140, height=140)
        c1.pack()

        c.execute("SELECT profile_pic FROM profile_picture WHERE username=?",(lgn_name,))
        conn.commit()
        pic_tuple = c.fetchone()
        if pic_tuple!=None:

            pic = pic_tuple[0]
            with open("profile.png",'wb') as txt:
                txt.write(pic)

            img_1 = PhotoImage(file="profile.png")
            pic_lbl = Label(profile_frame, image=img_1).place(x=0, y=0)
            c1.create_image(image=img_1)
        else:

#************default profile   ***************

            default_pro = """iVBORw0KGgoAAAANSUhEUgAAAIwAAACMBAMAAABc7lwNAAAAMFBMVEXR1dr////O0tf8/PzY29/09PX5+frt8PHl6evR09rU2Nzi5ujr7e/f4eXo6ezk5egQ1QesAAACuUlEQVR4nO3ZTY8MQRgH8N62SA9iH7MzO2TR4y3iLQYXCUmv5SjZ9g0mXDjxDUicnNrG0TLExUXWNzCOTrM2Dm7CJ0Ai4WTX2J2qenqrq/9Vtiax/w/wS1X3U9Vd9QTBRjYyzIlfXH4+NMzV62erFzqWyOwVWk7DkvlB/dgpT/8q9NlGGU1XmPHMP9NcUah2IIaV8PUqQ/X7MHOSxMDDmZaYGZRpS0zNLxOSnDcYU1GYMYw5pTC7MeagwoxjzJTCTMSIEnYVpuqTCVKFwfau0ZbK9BBmh6rQN4RRywbcSU8w5q1H5rAbRl0LRLc9Ms3/g4HelCPmCGOgxcAZaGnyKn6PMHxN9Twy2xiTIMwhVcG29A9sNA8QhilUBRT1f2I5896YKIe5643Jm5QjZr48k/PCodXw75gEYNpMQao4SBlTiwHmK2P2I8wIY24BSnCUMdBe7IgJv7h4NOrhjmgXpLACnMEUdXF+csMkXhnl2dQ7INOSGPjk25WYRgwyCxKzBx3NZom5hjKPnLwoV4x82sxQRtq56rASbBKYGzhTaQ+YSzgTDioHPIQ7Ze4NJjUEzB3nTMeCSR2sBXeMUH49nBGr2OLGWLzCgQ6a/YhXOPDmFwQ7BeYmzmwXmHPemRGBsWg1NAXGotUwJTIxqhxriQxcOIuiQhN+mYzknMaU7wpTQ74xoaosOUlpJTrOlKVfnKwsM9fOYeidHyZcyFOIwlJKxK9L+mkkZRh2d7OaMyWUQbON55exEj5bW6F6bMq80ihEF00dN8xsS8sYfmqiRb1Cky9NmK0Fitm0xGamxbQeFyu0N1snppIaMPSziNliotC+IuahEVN0nImM5kT0Uc/wplR+zq8LM10s/MlkrGW6hkw10TKGSkE/Ju8iND9jbkajZdQW+NrR3lA5YuaMGW2P/YkxI/fYfwNvdQRLDJTwtwAAAABJRU5ErkJggg=="""

            with open("profile.png",'wb') as txt:
                txt.write(base64.b64decode(default_pro))
            with open("profile.png","rb") as txt:
                ablo = txt.read()
            c.execute("INSERT INTO profile_picture VALUES(?, ?)",(lgn_name, sqlite3.Binary(ablo)))
            img_1 = PhotoImage(file="profile.png")
            pic_lbl = Label(profile_frame, image=img_1).place(x=0, y=0)
            c1.create_image(image=img_1)


    def general_setting():
        lgn_frame2 = Frame(lgn_frame1,width=500, height=500)
        lgn_frame2.place(x=400,y=90)

        notification = Label(lgn_frame2, text='Notification : ON').place(x=80, y=50)
        def noti_off():
            def noti_on():
                notification = Label(lgn_frame2, text='Notification : ON').place(x=80, y=50)
                notification_btn = Button(lgn_frame2,border=0, text='    OFF    ', command=noti_off, bg='light blue').place(x=210, y=50)
            notification = Label(lgn_frame2, text='Notification : OFF').place(x=80, y=50)
            notification_btn = Button(lgn_frame2,border=0, text='    ON     ', command=noti_on, bg='light blue').place(x=210, y=50)
        notification_btn = Button(lgn_frame2,border=0, text='    OFF    ', command=noti_off, bg='light blue').place(x=210, y=50)

        sound = Label(lgn_frame2, text='Sound : ON').place(x=80, y=80)
        def sound_off():
            def sound_on():
                sound = Label(lgn_frame2, text='Sound : ON').place(x=80, y=80)
                sound_btn = Button(lgn_frame2,border=0, text='    OFF    ', command=sound_off, bg='light blue').place(x=210, y=80)
            sound = Label(lgn_frame2, text='Sound : OFF').place(x=80, y=80)
            sound_btn = Button(lgn_frame2,border=0, text='    ON     ', command=sound_on, bg='light blue').place(x=210, y=80)
        sound_btn = Button(lgn_frame2,border=0, text='    OFF    ', command=sound_off, bg='light blue').place(x=210, y=80)

        theme = Label(lgn_frame2, text='Theme : material').place(x=80, y=110)
        def theme_off():
            say = Label(lgn_frame2, text="No theme availabe right now...",fg="purple").place(x=80, y=150)
        theme_btn = Button(lgn_frame2,border=0, text=' change ',command=theme_off, bg='light blue').place(x=210, y=110)

    def privacy_setting():
        def see_set():
            def every_set():
                who_can_see = Label(lgn_frame2, text='Who can see your Profile :  Everyone').place(x=20, y=20)
            def friend_set():
                who_can_see = Label(lgn_frame2, text='Who can see your Profile :  Friends   ').place(x=20, y=20)
            def only_set():
                who_can_see = Label(lgn_frame2, text='Who can see your Profile :  Only me ').place(x=20, y=20)
            everyone_btn = Button(lgn_frame2, border=0, command=every_set, text=' Everyone ', bg='light green').place(x=30, y=55)
            friend_btn = Button(lgn_frame2, border=0, command=friend_set, text='  Friends ', bg='light green').place(x=120, y=55)
            onlyme_btn = Button(lgn_frame2, border=0, command=only_set, text='  Only me ', bg='light green').place(x=200, y=55)

        def send_set():
            def any_set():
                who_can_send = Label(lgn_frame2, text="Who can send you message :  Anyone  ").place(x=20, y=100)
            def fr_set():
                who_can_send = Label(lgn_frame2, text="Who can send you message :  Friends ").place(x=20, y=100)
            def me_set():
                who_can_send = Label(lgn_frame2, text="Who can send you message :  Only me ").place(x=20, y=100)
            anyone_btn = Button(lgn_frame2, border=0, command=any_set, text='  Anyone  ', bg='light green').place(x=30, y=135)
            friend_btn = Button(lgn_frame2, border=0, command=fr_set, text='  Friends ', bg='light green').place(x=120, y=135)
            onlyme_btn = Button(lgn_frame2, border=0, command=me_set, text='  Only me ', bg='light green').place(x=200, y=135)

        def encrypt_set():
            def yes_set():
                encrypt_data = Label(lgn_frame2, text="encrypt your data :  Yes ").place(x=20, y=180)
            def no_set():
                encrypt_data = Label(lgn_frame2, text="encrypt your data :  No  ").place(x=20, y=180)
            encrypt_data_btn = Button(lgn_frame2, border=0, command=yes_set, text='  Yes  ', bg='light blue').place(x=80, y=210)
            encrypt_data_btn = Button(lgn_frame2, border=0, command=no_set, text='   No  ', bg='light blue').place(x=160, y=210)

        lgn_frame2 = Frame(lgn_frame1,width=500, height=500)
        lgn_frame2.place(x=400,y=90)
        who_can_see = Label(lgn_frame2, text='Who can see your Profile :  Everyone').place(x=20, y=20)
        who_can_see_btn = Button(lgn_frame2, border=0, command=see_set, text=' change ', bg='light blue').place(x=230, y=20)

        who_can_send = Label(lgn_frame2, text="Who can send you message :  Anyone").place(x=20, y=100)
        who_can_send_btn = Button(lgn_frame2, border=0, command=send_set, text=' change ', bg='light blue').place(x=230, y=100)

        encrypt_data = Label(lgn_frame2, text="encrypt your data :  Yes").place(x=20, y=180)
        encrypt_data_btn = Button(lgn_frame2, border=0, command=encrypt_set, text=' change ', bg='light blue').place(x=230, y=180)

    def account_setting(statement = None):

        def change_name():

            def save_change_name():
                global lgn_name
                new_name = _name.get()
                first, last =new_name.split(" ")
                c.execute("UPDATE data SET f_name=? WHERE username=?",(first,lgn_name))
                conn.commit()
                c.execute("UPDATE data SET l_name=? WHERE username=?",(last,lgn_name))
                conn.commit()
                user_fullname[0], user_fullname[1] = first, last
                account_setting("Name Changed Successfully")


            save_btn = Button(lgn_frame2, border=0, text='    save    ', bg='light green',command=save_change_name).place(x=230, y=10)
            lbl = Label(lgn_frame2,text='New Name : ').place(x=35, y=40)
            _name = Entry(lgn_frame2)
            _name.place(x=125, y=40)

        def change_email():

            def save_change_email():
                global lgn_name
                email = n_email.get()
                c.execute("UPDATE data SET email=? WHERE username=?",(email,lgn_name))
                conn.commit()
                user_fullname[2] = email
                account_setting('Email Changed Successfully')

            save_btn = Button(lgn_frame2, border=0, text='    save    ', bg='light green',command=save_change_email).place(x=230, y=70)
            lbl = Label(lgn_frame2,text='New Email : ').place(x=35, y=100)
            n_email = Entry(lgn_frame2)
            n_email.place(x=125, y=100)

        def change_password():

            def save_change_password():
                old_pass = old_1.get()
                new_pass = new_1.get()
                new_pass_c = new_2.get()
                global lgn_passwd,lgn_name
                if lgn_passwd==old_pass:
                    if new_pass==new_pass_c:
                        c.execute("UPDATE data SET password=? WHERE username=?",(new_pass,lgn_name))
                        conn.commit()

                        lgn_passwd = new_pass # to store new pass in variable

                        account_setting('Password Changed Successfully')


                    else:
                        msg = tkinter.messagebox.showwarning("Info","Password Does not match")

                else:
                    msg1 = tkinter.messagebox.showwarning("Info","Incorrect Password")

            save_btn = Button(lgn_frame2, border=0, text='    save    ', bg='light green',command=save_change_password).place(x=230, y=140)
            lbl = Label(lgn_frame2,text='Old password : ').place(x=35, y=180)
            lbl = Label(lgn_frame2,text='New password : ').place(x=35, y=210)
            lbl = Label(lgn_frame2,text='New password : ').place(x=35, y=240)
            old_1 = Entry(lgn_frame2, show="\u2022")
            old_1.place(x=125, y=180)
            new_1 = Entry(lgn_frame2, show="\u2022")
            new_1.place(x=125, y=210)
            new_2 = Entry(lgn_frame2, show="\u2022")
            new_2.place(x=125, y=240)


        lgn_frame2 = Frame(lgn_frame1,width=500, height=500)
        lgn_frame2.place(x=400,y=90)

        name = Label(lgn_frame2,text='Name :  ' +user_fullname[0]+' '+user_fullname[1]).place(x=35, y=10)
        name_btn = Button(lgn_frame2, border=0, text=' change ', bg='light blue',command=change_name).place(x=230, y=10)

        email = Label(lgn_frame2,text='Email :  '+user_fullname[2]).place(x=35, y=70)
        email_btn = Button(lgn_frame2, border=0, text=' change ', bg='light blue',command=change_email).place(x=230, y=70)

        password = Label(lgn_frame2, text="Password :  *******").place(x=35, y=140)
        password_btn = Button(lgn_frame2, border=0, text=' change ', bg='light blue',command=change_password).place(x=230, y=140)
        if statement !=None:
            lbl2 = Label(lgn_frame2,text=statement, fg='green').place(x=120, y=270)



    global lgn_name, lgn_passwd
    if received == None:
        lgn_name = uname.get()
        lgn_passwd = passwd.get()


    c.execute("SELECT username,password FROM data WHERE username=? AND password=?",(lgn_name, lgn_passwd))
    conn.commit()
    lgn_data = c.fetchone()


    if lgn_data==None:
        tkinter.messagebox.showerror('Info',"Incorrect Credential...\n\nTry Again...")
    else:


        frame2.destroy()
        lgn = root
        lgn.title('shrake')
        lgn.geometry('950x500+200+100')
        lgn.overrideredirect(False)
        lgn_frame1 = Frame(lgn, width=950, height=200)
        lgn_frame1.pack(fill=BOTH)
        chck = Label(lgn_frame1, text="",bg="light blue").pack(fill=X)


        c.execute("SELECT f_name, l_name,email FROM data WHERE username=?",(lgn_name,))
        conn.commit()
        user_fullname_tuple = c.fetchone()
        user_fullname = list(user_fullname_tuple)
        use = Label(lgn_frame1, text=user_fullname[0]+' '+user_fullname[1],font=('material',18,'bold'), bg='light blue').pack(fill=X)


        def quiting():
            global backup
            if backup!="":
                os.remove(backup)

            os.remove('profile.png')
            os.remove('shrake.png')
            root.quit()

        logout_btn = Button(lgn_frame1, text="   Logout   ",command=quiting,bg="light green").place(x=850, y=15)

        can = Canvas(lgn_frame1,width=950,height=500)
        can.pack()
        for i in range(0,700,1):
            can1 = can.create_line(0+i,0,900+i,400+i,fill='grey')
            can4 = can.create_line(50-i*i//9,300+i,i+700,600,fil='light blue')
            can2 = can.create_line(600-i*i,900+i,i,400-i,fill='red')
            can3 = can.create_line(1000,i,200+i,100+i, fill='light green')
            can5 = can.create_oval(15,40,120,145,fill='grey97')


        profile_btn = Button(lgn_frame1, text="   Profile   ", border=0, bg='light green',command=profile).place(x=35, y=280)

        menu = Menubutton(lgn_frame1, text="       setting       ", bg="light green")
        menu.place(x=750, y=15)
        sub_menu = Menu(menu)
        menu.config(menu=sub_menu)
        sub_menu.add_command(label="General",command=general_setting)
        sub_menu.add_command(label="Privacy",command=privacy_setting)
        sub_menu.add_command(label="Account",command=account_setting)

        img_btn = Button(lgn_frame1, text="  Add File  ", border=0, bg='light blue',command=insert_image).place(x=250, y=70)

        list_img_btn = Button(lgn_frame1, text="   List File  ", border=0, bg='light blue',command=list_image).place(x=250, y=100)

        delete_btn = Button(lgn_frame1, command=delete_file, border=0, text="Delete File", bg='light blue').place(x=250, y=130)
        def search_bar():

            def search_user():
                lgn_frame4 = Frame(lgn_frame1,width=250, height=300)
                lgn_frame4.place(x=345, y=130)
                ca = Canvas(lgn_frame4, width=250, height=300)
                ca.pack()
                for i in range(0,300):
                    clr = ca.create_line(0+i,0,0+i,300,fill='light blue')
                search_name = search.get()
                search_name = search_name.strip()
                search_list = search_name.split(" ")
                # print(search_list)
                i=10
                if len(search_list)==2:
                    c.execute("SELECT f_name, l_name FROM data WHERE f_name=? AND l_name=?",(search_list[0], search_list[1]))
                    conn.commit()
                    search_res = c.fetchall()

                    if search_res!=None:
                        for ser in search_res:
                            lb = Label(lgn_frame4, text=ser[0]+' '+ser[1]).place(x=10, y=i)
                            lb1 = Label(lgn_frame4, text="matched ", bg="light blue", fg='purple').place(x=180, y=i)
                            i += 30
                for ser in search_list:
                    c.execute("SELECT username FROM data WHERE username=?",(ser,))
                    conn.commit()
                    search_res = c.fetchone()
                    if search_res!=None:
                        lb = Label(lgn_frame4, text=search_res).place(x=10, y=i)
                        lb1 = Label(lgn_frame4, text="username", bg="light blue", fg='purple').place(x=180, y=i)
                        i += 30
                        # print(search_res)
                for ser in search_list:
                    c.execute("SELECT f_name FROM data WHERE f_name=?",(ser,))
                    conn.commit()
                    ser_lst = c.fetchall()
                    for ser in ser_lst:
                        lb = Label(lgn_frame4, text=ser[0]).place(x=10, y=i)
                        lb1 = Label(lgn_frame4, text="name", bg="light blue", fg='purple').place(x=180, y=i)
                        i += 30

            search = Entry(lgn_frame1,width=40)
            search.place(x=350, y=70)
            search_btn = Button(lgn_frame1, text="    search    ", border=0, bg='light green', command=search_user).place(x=433, y=100)


        def change_profile():

            address_1 = tkinter.filedialog.askopenfilename(filetypes=[("image jpg"),("image png")])
            if address_1!="":
                profile_frame = Frame(lgn_frame1, width=140, height=140)
                profile_frame.place(x=5, y=65)
                c1 = Canvas(lgn_frame1,width=140, height=140)
                c1.pack()
                img_1 = Image.open(address_1)
                img_resize = img_1.resize((140,140))
                img_resize.save('profile.png')

                with open('profile.png',"rb") as txt:
                    ablob_1 = txt.read()
                    c.execute("UPDATE profile_picture SET profile_pic=? WHERE username=?",(sqlite3.Binary(ablob_1), lgn_name))
                    conn.commit()

                img_1 = PhotoImage(file="profile.png")
                pic_lbl = Label(profile_frame, image=img_1).place(x=0, y=0)
                c1.create_image(image=img_1)


        search_btn = Button(lgn_frame1, border=0, text="search user",bg='light green', command=search_bar).place(x=433, y=100)

        changeprofile = Button(lgn_frame1, text="Change profile", border=0, bg="light green", command=change_profile).place(x=22, y=220)

#***********  pic from DB *******

        profile_frame = Frame(lgn_frame1, width=140, height=140)
        profile_frame.place(x=5, y=65)
        c1 = Canvas(lgn_frame1,width=140, height=140)
        c1.pack()

        c.execute("SELECT profile_pic FROM profile_picture WHERE username=?",(lgn_name,))
        conn.commit()
        pic_tuple = c.fetchone()
        if pic_tuple!=None:

            pic = pic_tuple[0]
            with open("profile.png",'wb') as txt:
                txt.write(pic)

            img_1 = PhotoImage(file="profile.png")
            pic_lbl = Label(profile_frame, image=img_1).place(x=0, y=0)
            c1.create_image(image=img_1)
        else:

#************default profile   ***************

            default_pro = """iVBORw0KGgoAAAANSUhEUgAAAIwAAACMBAMAAABc7lwNAAAAMFBMVEXR1dr////O0tf8/PzY29/09PX5+frt8PHl6evR09rU2Nzi5ujr7e/f4eXo6ezk5egQ1QesAAACuUlEQVR4nO3ZTY8MQRgH8N62SA9iH7MzO2TR4y3iLQYXCUmv5SjZ9g0mXDjxDUicnNrG0TLExUXWNzCOTrM2Dm7CJ0Ai4WTX2J2qenqrq/9Vtiax/w/wS1X3U9Vd9QTBRjYyzIlfXH4+NMzV62erFzqWyOwVWk7DkvlB/dgpT/8q9NlGGU1XmPHMP9NcUah2IIaV8PUqQ/X7MHOSxMDDmZaYGZRpS0zNLxOSnDcYU1GYMYw5pTC7MeagwoxjzJTCTMSIEnYVpuqTCVKFwfau0ZbK9BBmh6rQN4RRywbcSU8w5q1H5rAbRl0LRLc9Ms3/g4HelCPmCGOgxcAZaGnyKn6PMHxN9Twy2xiTIMwhVcG29A9sNA8QhilUBRT1f2I5896YKIe5643Jm5QjZr48k/PCodXw75gEYNpMQao4SBlTiwHmK2P2I8wIY24BSnCUMdBe7IgJv7h4NOrhjmgXpLACnMEUdXF+csMkXhnl2dQ7INOSGPjk25WYRgwyCxKzBx3NZom5hjKPnLwoV4x82sxQRtq56rASbBKYGzhTaQ+YSzgTDioHPIQ7Ze4NJjUEzB3nTMeCSR2sBXeMUH49nBGr2OLGWLzCgQ6a/YhXOPDmFwQ7BeYmzmwXmHPemRGBsWg1NAXGotUwJTIxqhxriQxcOIuiQhN+mYzknMaU7wpTQ74xoaosOUlpJTrOlKVfnKwsM9fOYeidHyZcyFOIwlJKxK9L+mkkZRh2d7OaMyWUQbON55exEj5bW6F6bMq80ihEF00dN8xsS8sYfmqiRb1Cky9NmK0Fitm0xGamxbQeFyu0N1snppIaMPSziNliotC+IuahEVN0nImM5kT0Uc/wplR+zq8LM10s/MlkrGW6hkw10TKGSkE/Ju8iND9jbkajZdQW+NrR3lA5YuaMGW2P/YkxI/fYfwNvdQRLDJTwtwAAAABJRU5ErkJggg=="""
            with open("profile.png",'wb') as txt:
                txt.write(base64.b64decode(default_pro))
            with open("profile.png","rb") as txt:
                ablo = txt.read()
            c.execute("INSERT INTO profile_picture VALUES(?, ?)",(lgn_name, sqlite3.Binary(ablo)))
            img_1 = PhotoImage(file="profile.png")
            pic_lbl = Label(profile_frame, image=img_1).place(x=0, y=0)
            c1.create_image(image=img_1)


              #*******  create account  *************

def create_account():

    def info_saving():

        p1 = entry_4.get()
        p2 = entry_5.get()
        u1 = entry_3.get()
        c.execute("SELECT username FROM data WHERE username=?",(u1,))
        conn.commit()
        l = c.fetchall()
        if l==[]:

            if p1 == p2:

                if entry_1.get() is not "" and entry_2.get() is not '' and entry_3.get() is not "" and entry_4.get() is not '' and entry_6.get() is not "":
                    fname = entry_1.get()
                    lname = entry_2.get()
                    uname = entry_3.get()
                    passwd = entry_4.get()
                    email = entry_6.get()
                    c.execute("INSERT INTO data VALUES(?,?,?,?,?)", (fname, lname, uname, passwd, email))
                    conn.commit()
                    text = Label(cr, text='  ', padx=350, pady=5, bg="grey40").place(x=30, y=290)
                    review = tkinter.messagebox.showinfo('Information', "Account Successfully Created.")
                    if review=='ok':
                        frame3.destroy()
                        frame4.destroy()
                        global lgn_name, lgn_passwd
                        lgn_name = uname
                        lgn_passwd = passwd
                        login_account("called")


                else:
                    text1 = Label(cr, text="    * required fields are empty       ",bg="grey50", fg='cyan', font=("",10,"bold")).place(x=90, y=290)

            else:
                text = Label(cr, text='      * password does not match         ',bg="grey50", fg='cyan', font=("",10,"bold")).place(x=90, y=290)

        else:
            text = Label(cr, text="     * This username is not available...      ", bg="grey50", fg='cyan', font=("",10,"bold")).place(x=70, y=290)


    frame2.destroy()
    cr = root
    cr.title("Create Account")
    cr.geometry("400x330+450+200")
    cr.overrideredirect(False)
    frame3 = Frame(cr, bg="grey40")
    frame3.pack()
    frame4 = Frame(cr, width=400, height=310, bg="grey40")
    frame4.pack()
    label_1 = Label(frame3, text='Creating Account', bg="grey50", fg="light green", font=("consolas",15,"bold"), padx=400).pack(fill=X)
    logo_img = Label(frame4, image=img, bg="grey40").place(x=280, y=16)

    label_2 = Label(frame4, text="First Name ",bg="grey40", fg="white").place(x=30, y=10)
    label_3 = Label(frame4, text='Last Name ',bg="grey40", fg="white").place(x=30, y=40)
    label_4 = Label(frame4, text='Username',bg="grey40", fg="white").place(x=30, y=70)
    label_5 = Label(frame4, text='Password ',bg="grey40", fg="white").place(x=30, y=100)
    label_6 = Label(frame4, text='Confirm ',bg="grey40", fg="white").place(x=30, y=130)
    label_7 = Label(frame4, text='Email ',bg="grey40", fg="white").place(x=30, y=160)

    entry_1 = Entry(frame4, bg="grey90", width=23, font=("consolas",10))
    entry_1.place(x=100, y=10)

    entry_2 = Entry(frame4, bg="grey90", width=23, font=("consolas",10))
    entry_2.place(x=100, y=40)

    entry_3 = Entry(frame4, bg="grey90", width=23, font=("consolas",10))
    entry_3.place(x=100, y=70)

    entry_4 = Entry(frame4, bg="grey90", show="\u2022", width=23, font=("consolas",10))
    entry_4.place(x=100, y=100)

    entry_5 = Entry(frame4, bg="grey90", show="\u2022", width=23, font=("consolas",10))
    entry_5.place(x=100, y=130)

    entry_6 = Entry(frame4, bg="grey90", width=23, font=("consolas",10))
    entry_6.place(x=100, y=160)
    chk_btn = Checkbutton(frame4, text="I Agree to \' Term and Condition \'", bg="grey40", fg="cyan")
    chk_btn.place(x=65, y=190)

    des = Canvas(frame4, width=51, height=24).place(x=134, y=219)
    des = Canvas(frame4, width=51, height=24).place(x=249, y=219)

    sign_up_btn = Button(frame4, text=" sign up", border=0, padx=3, pady=3, command=info_saving, bg='grey40', fg="white")
    sign_up_btn.place(x=135, y=220)
    close_btn = Button(frame4, text='  Close ', border=0, padx=5, pady=3, command=frame4.quit, bg='grey40', fg="white")
    close_btn.place(x=250, y=220)

#*************  root  ***********


root = Tk()

raw = """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"""

"""
raw are encoded by base64
    raw = base64.b64encode(file)
decoded = base64.b64decode(raw)

"""

with open('shrake.png','wb') as txt:
    txt.write(base64.b64decode(raw))

img = PhotoImage(file='shrake.png')
root.title("Shrake Authentication")
root.geometry("400x200+450+200")
root.overrideredirect(True)
root.tk.call('wm','iconphoto',root._w, img)

frame1 = Frame(root, width=400, height=30, bg="grey90")
frame2 = Frame(root, width=400, height=200, bg="grey40")

def toolbar():
    mainMenu = Menu(frame1)
    root.config(menu=mainMenu, bg="grey40")

    fileSubMenu = Menu(mainMenu,border=0, bg="grey40", fg="white")
    mainMenu.add_cascade(label="File", menu=fileSubMenu)
    fileSubMenu.add_command(label="New      Ctrl+N", command=donothing)
    fileSubMenu.add_command(label="open     Ctrl+O", command=donothing)
    fileSubMenu.add_command(label="Save      Ctrl+S", command=donothing)
    fileSubMenu.add_command(label="save as", command=donothing)
    fileSubMenu.add_separator()
    fileSubMenu.add_command(label="Exit", command=quiting1)

    editSubMenu = Menu(mainMenu, bg="grey40", fg="white")
    mainMenu.add_cascade(label="Edit", menu=editSubMenu)
    editSubMenu.add_command(label="Undo      Ctrl+Z", command=donothing)
    editSubMenu.add_command(label="Redo       Ctrl+Y", command=donothing)
    editSubMenu.add_command(label="Cut          Ctrl+X", command=donothing)
    editSubMenu.add_command(label="Copy       Ctrl+C", command=donothing)
    editSubMenu.add_command(label="Paste       Ctrl+V", command=donothing)

    helpMenu = Menu(mainMenu, bg="grey40", fg="white")
    mainMenu.add_cascade(label="Help", menu=helpMenu)
    helpMenu.add_command(label="Documentation", command=donothing)
    helpMenu.add_command(label="twitter", command=donothing)
    helpMenu.add_command(label="Update License", command=donothing)
    helpMenu.add_command(label="Check for Update..", command=donothing)
    helpMenu.add_command(label="About", command=about)
    frame1.pack()


heading = Label(frame2, text="Shrake Authentication", font=("consolas",18,"bold","italic"), bg="grey40", fg="black").place(x=60, y=10)

logo_img = Label(frame2, image=img, bg="grey40").place(x=290, y=50)

text1 = Label(frame2, text="Username : ", bg="grey40", fg="white").place(x=30, y=70)
text2 = Label(frame2, text="Password  : ", bg="grey40", fg="white").place(x=30, y=100)
uname = Entry(frame2, bg='grey90', width=25, font=("consolas",10,"bold"))
uname.place(x=95, y=70)
passwd = Entry(frame2, bg="grey90",show="\u2022", width=25, font=("consolas",10,"bold"))
passwd.place(x=95, y=100)

btn_design = Canvas(frame2, width=51, height=24).place(x=59, y=149)
btn_design = Canvas(frame2, width=51, height=24).place(x=173, y=149)
btn_design = Canvas(frame2, width=51, height=24).place(x=288, y=149)


signup_btn = Button(frame2, text="Sign up", border=0, padx=4, pady=3, bg="grey40", fg="white", command=create_account).place(x=60, y=150)
login_btn = Button(frame2, text="  Login ", border=0, padx=4, pady=3, command=login_account, bg="grey40", fg="white", font=("",9,"bold")).place(x=174, y=150)
cancel_btn = Button(frame2, text=" Cancel ", border=0, padx=3, pady=3, command=quiting1, bg="grey40", fg="white").place(x=289, y=150)


frame2.pack()

root.mainloop()

conn.close()


