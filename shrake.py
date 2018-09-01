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
    os.remove('shrake1.png')
    os.remove('shrake2.png')
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

        profile_btn = Button(lgn_frame1, text="   Profile   ",bg='light green',command=profile).place(x=35, y=280)
        img_btn = Button(lgn_frame1, text='  Add File  ',bg='light blue',command=insert_image).place(x=250, y=70)
        list_img_btn = Button(lgn_frame1, text="   List File  ",bg='light blue',command=list_image).place(x=250, y=100)
        delete_btn = Button(lgn_frame1, command=delete_file, text="Delete File", bg='light blue').place(x=250, y=130)
        search_btn = Button(lgn_frame1, text="search user",bg='light green', command=search_bar).place(x=433, y=100)
        changeprofile = Button(lgn_frame1, text="Change profile",bg="light green", command=change_profile).place(x=22, y=220)

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
                notification_btn = Button(lgn_frame2, text='    OFF    ', command=noti_off, bg='light blue').place(x=210, y=50)
            notification = Label(lgn_frame2, text='Notification : OFF').place(x=80, y=50)
            notification_btn = Button(lgn_frame2, text='    ON     ', command=noti_on, bg='light blue').place(x=210, y=50)
        notification_btn = Button(lgn_frame2, text='    OFF    ', command=noti_off, bg='light blue').place(x=210, y=50)

        sound = Label(lgn_frame2, text='Sound : ON').place(x=80, y=80)
        def sound_off():
            def sound_on():
                sound = Label(lgn_frame2, text='Sound : ON').place(x=80, y=80)
                sound_btn = Button(lgn_frame2, text='    OFF    ', command=sound_off, bg='light blue').place(x=210, y=80)
            sound = Label(lgn_frame2, text='Sound : OFF').place(x=80, y=80)
            sound_btn = Button(lgn_frame2, text='    ON     ', command=sound_on, bg='light blue').place(x=210, y=80)
        sound_btn = Button(lgn_frame2, text='    OFF    ', command=sound_off, bg='light blue').place(x=210, y=80)

        theme = Label(lgn_frame2, text='Theme : material').place(x=80, y=110)
        def theme_off():
            say = Label(lgn_frame2, text="No theme availabe right now...",fg="purple").place(x=80, y=150)
        theme_btn = Button(lgn_frame2, text=' change ',command=theme_off, bg='light blue').place(x=210, y=110)

    def privacy_setting():
        def see_set():
            def every_set():
                who_can_see = Label(lgn_frame2, text='Who can see your Profile :  Everyone').place(x=20, y=20)
            def friend_set():
                who_can_see = Label(lgn_frame2, text='Who can see your Profile :  Friends   ').place(x=20, y=20)
            def only_set():
                who_can_see = Label(lgn_frame2, text='Who can see your Profile :  Only me ').place(x=20, y=20)
            everyone_btn = Button(lgn_frame2,command=every_set, text=' Everyone ', bg='light green').place(x=30, y=55)
            friend_btn = Button(lgn_frame2,command=friend_set, text='  Friends ', bg='light green').place(x=120, y=55)
            onlyme_btn = Button(lgn_frame2,command=only_set, text='  Only me ', bg='light green').place(x=200, y=55)

        def send_set():
            def any_set():
                who_can_send = Label(lgn_frame2, text="Who can send you message :  Anyone  ").place(x=20, y=100)
            def fr_set():
                who_can_send = Label(lgn_frame2, text="Who can send you message :  Friends ").place(x=20, y=100)
            def me_set():
                who_can_send = Label(lgn_frame2, text="Who can send you message :  Only me ").place(x=20, y=100)
            anyone_btn = Button(lgn_frame2,command=any_set, text='  Anyone  ', bg='light green').place(x=30, y=135)
            friend_btn = Button(lgn_frame2,command=fr_set, text='  Friends ', bg='light green').place(x=120, y=135)
            onlyme_btn = Button(lgn_frame2,command=me_set, text='  Only me ', bg='light green').place(x=200, y=135)

        def encrypt_set():
            def yes_set():
                encrypt_data = Label(lgn_frame2, text="encrypt your data :  Yes ").place(x=20, y=180)
            def no_set():
                encrypt_data = Label(lgn_frame2, text="encrypt your data :  No  ").place(x=20, y=180)
            encrypt_data_btn = Button(lgn_frame2,command=yes_set, text='  Yes  ', bg='light blue').place(x=80, y=210)
            encrypt_data_btn = Button(lgn_frame2,command=no_set, text='   No  ', bg='light blue').place(x=160, y=210)

        lgn_frame2 = Frame(lgn_frame1,width=500, height=500)
        lgn_frame2.place(x=400,y=90)
        who_can_see = Label(lgn_frame2, text='Who can see your Profile :  Everyone').place(x=20, y=20)
        who_can_see_btn = Button(lgn_frame2,command=see_set, text=' change ', bg='light blue').place(x=230, y=20)

        who_can_send = Label(lgn_frame2, text="Who can send you message :  Anyone").place(x=20, y=100)
        who_can_send_btn = Button(lgn_frame2, command=send_set, text=' change ', bg='light blue').place(x=230, y=100)

        encrypt_data = Label(lgn_frame2, text="encrypt your data :  Yes").place(x=20, y=180)
        encrypt_data_btn = Button(lgn_frame2,command=encrypt_set, text=' change ', bg='light blue').place(x=230, y=180)

    def account_setting(statement = None):

        def change_name():

            def save_change_name():
                global lgn_name
                new_name = _name.get()
                first, last =new_name.split(" ")
                # print(new_name,first,last)
                c.execute("UPDATE data SET f_name=? WHERE username=?",(first,lgn_name))
                conn.commit()
                c.execute("UPDATE data SET l_name=? WHERE username=?",(last,lgn_name))
                conn.commit()
                user_fullname[0], user_fullname[1] = first, last
                account_setting("Name Changed Successfully")


            save_btn = Button(lgn_frame2, text='    save    ', bg='light green',command=save_change_name).place(x=230, y=10)
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

            save_btn = Button(lgn_frame2, text='    save    ', bg='light green',command=save_change_email).place(x=230, y=70)
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

            save_btn = Button(lgn_frame2, text='    save    ', bg='light green',command=save_change_password).place(x=230, y=140)
            lbl = Label(lgn_frame2,text='Old password : ').place(x=35, y=180)
            lbl = Label(lgn_frame2,text='New password : ').place(x=35, y=210)
            lbl = Label(lgn_frame2,text='New password : ').place(x=35, y=240)
            old_1 = Entry(lgn_frame2)
            old_1.place(x=125, y=180)
            new_1 = Entry(lgn_frame2)
            new_1.place(x=125, y=210)
            new_2 = Entry(lgn_frame2)
            new_2.place(x=125, y=240)


        lgn_frame2 = Frame(lgn_frame1,width=500, height=500)
        lgn_frame2.place(x=400,y=90)

        name = Label(lgn_frame2,text='Name :  ' +user_fullname[0]+' '+user_fullname[1]).place(x=35, y=10)
        name_btn = Button(lgn_frame2, text=' change ', bg='light blue',command=change_name).place(x=230, y=10)

        email = Label(lgn_frame2,text='Email :  '+user_fullname[2]).place(x=35, y=70)
        email_btn = Button(lgn_frame2, text=' change ', bg='light blue',command=change_email).place(x=230, y=70)

        password = Label(lgn_frame2,text="Password :  *******").place(x=35, y=140)
        password_btn = Button(lgn_frame2, text=' change ', bg='light blue',command=change_password).place(x=230, y=140)
        if statement !=None:
            lbl2 = Label(lgn_frame2,text=statement, fg='green').place(x=120, y=270)



    global lgn_name, lgn_passwd
    if received == None:
        lgn_name = uname.get()
        lgn_passwd = passwd.get()
  #  c.execute("SELECT username,password FROM data WHERE username=:user AND password=:passwd",{'user':lgn_name, 'passwd':lgn_passwd})

    c.execute("SELECT username,password FROM data WHERE username=? AND password=?",(lgn_name, lgn_passwd))
    conn.commit()
    lgn_data = c.fetchone()


    if lgn_data==None:
        tkinter.messagebox.showerror('Info',"Incorrect Credential...\n\nTry Again...")
    else:

        # lgn = Toplevel()
        frame2.destroy()
        lgn = root
        lgn.title('shrake')
        lgn.geometry('950x500+200+100')
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
            os.remove('shrake1.png')
            os.remove('shrake2.png')
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


        profile_btn = Button(lgn_frame1, text="   Profile   ",bg='light green',command=profile).place(x=35, y=280)

        menu = Menubutton(lgn_frame1, text="       setting       ", bg="light green")
        menu.place(x=750, y=15)
        sub_menu = Menu(menu)
        menu.config(menu=sub_menu)
        sub_menu.add_command(label="General",command=general_setting)
        sub_menu.add_command(label="Privacy",command=privacy_setting)
        sub_menu.add_command(label="Account",command=account_setting)

        img_btn = Button(lgn_frame1, text="  Add File  ",bg='light blue',command=insert_image).place(x=250, y=70)

        list_img_btn = Button(lgn_frame1, text="   List File  ",bg='light blue',command=list_image).place(x=250, y=100)

        delete_btn = Button(lgn_frame1, command=delete_file, text="Delete File", bg='light blue').place(x=250, y=130)
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
            search_btn = Button(lgn_frame1, text="    search    ",bg='light green', command=search_user).place(x=433, y=100)


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


        search_btn = Button(lgn_frame1, text="search user",bg='light green', command=search_bar).place(x=433, y=100)

        changeprofile = Button(lgn_frame1, text="Change profile",bg="light green", command=change_profile).place(x=22, y=220)

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
                    text = Label(cr, text='                                                      ').place(x=90, y=270)
                    review = tkinter.messagebox.showinfo('Information', "Account Successfully Created.")
                    if review=='ok':
                        frame3.destroy()
                        frame4.destroy()
                        global lgn_name, lgn_passwd
                        lgn_name = uname
                        lgn_passwd = passwd
                        login_account("called")


                else:
                    text1 = Label(cr, text="      required fields are empty       ", fg='red').place(x=90, y=270)

            else:
                text = Label(cr, text='        password does not match         ', fg='red').place(x=90, y=270)

        else:
            text = Label(cr, text="       This username is not available...      ", fg='red').place(x=70, y=270)


    frame2.destroy()
    cr = root
    cr.title("Create Account")
    cr.geometry("350x300+450+200")
    frame3 = Frame(cr)
    frame3.pack()
    frame4 = Frame(cr, width=350, height=250)
    frame4.pack()
    label_1 = Label(frame3, text='Creating Account', bg='light blue').pack(fill=X)
    logo_img = Label(frame4, image=img2).place(x=270, y=6)
    shrake_img = Label(frame4, image=img1).place(x=265, y=65)

    label_2 = Label(frame4, text="First Name ").place(x=30, y=10)
    label_3 = Label(frame4, text='Last Name ').place(x=30, y=40)
    label_4 = Label(frame4, text='Username').place(x=30, y=70)
    label_5 = Label(frame4, text='Password ').place(x=30, y=100)
    label_6 = Label(frame4, text='Confirm ').place(x=30, y=130)
    label_7 = Label(frame4, text='Email ').place(x=30, y=160)

    entry_1 = Entry(frame4)
    entry_1.place(x=100, y=10)

    entry_2 = Entry(frame4)
    entry_2.place(x=100, y=40)

    entry_3 = Entry(frame4)
    entry_3.place(x=100, y=70)

    entry_4 = Entry(frame4)
    entry_4.place(x=100, y=100)

    entry_5 = Entry(frame4)
    entry_5.place(x=100, y=130)

    entry_6 = Entry(frame4)
    entry_6.place(x=100, y=160)
    chk_btn = Checkbutton(frame4, text="I Agree to \' Term and Condition \'")
    chk_btn.place(x=65, y=190)
    sign_up_btn = Button(frame4, text="sign up", command=info_saving, bg='light green')
    sign_up_btn.place(x=135, y=220)
    close_btn = Button(frame4, text=' Close ', command=frame4.quit, bg='red')
    close_btn.place(x=250, y=220)

#*************  root  ***********


root = Tk()

raw1 = """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"""

raw2 = """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"""

"""
raw1 and raw2 are encoded by base64
    raw = base64.b64encode(file)
decoded = base64.b64decode(raw)

"""


with open('shrake1.png','wb') as txt:
    txt.write(base64.b64decode(raw1))

with open('shrake2.png','wb') as txt:
    txt.write(base64.b64decode(raw2))

img1 = PhotoImage(file='shrake1.png')
img2 = PhotoImage(file='shrake2.png')
root.title("Shrake Authentication")
root.geometry("350x150+450+200")
root.tk.call('wm','iconphoto',root._w, img2)

frame1 = Frame(root)
frame2 = Frame(root, width=350, height=150)

mainMenu = Menu(frame1)
root.config(menu=mainMenu)

fileSubMenu = Menu(mainMenu)
mainMenu.add_cascade(label="File", menu=fileSubMenu)
fileSubMenu.add_command(label="New      Ctrl+N", command=donothing)
fileSubMenu.add_command(label="open     Ctrl+O", command=donothing)
fileSubMenu.add_command(label="Save      Ctrl+S", command=donothing)
fileSubMenu.add_command(label="save as", command=donothing)
fileSubMenu.add_separator()
fileSubMenu.add_command(label="Exit", command=quiting1)

editSubMenu = Menu(mainMenu)
mainMenu.add_cascade(label="Edit", menu=editSubMenu)
editSubMenu.add_command(label="Undo      Ctrl+Z", command=donothing)
editSubMenu.add_command(label="Redo       Ctrl+Y", command=donothing)
editSubMenu.add_command(label="Cut          Ctrl+X", command=donothing)
editSubMenu.add_command(label="Copy       Ctrl+C", command=donothing)
editSubMenu.add_command(label="Paste       Ctrl+V", command=donothing)

helpMenu = Menu(mainMenu)
mainMenu.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(label="Documentation", command=donothing)
helpMenu.add_command(label="twitter", command=donothing)
helpMenu.add_command(label="Update License", command=donothing)
helpMenu.add_command(label="Check for Update..", command=donothing)
helpMenu.add_command(label="About", command=about)
frame1.pack()

logo_img = Label(frame2, image=img2).place(x=270, y=6)
shrake_img = Label(frame2, image=img1).place(x=265, y=65)

text1 = Label(frame2, text="Username : ").place(x=30, y=10)
text2 = Label(frame2, text="Password  : ").place(x=30, y=40)
uname = Entry(frame2)
uname.place(x=95, y=10)
passwd = Entry(frame2)
passwd.place(x=95, y=40)


check_btn = Checkbutton(frame2, text="Keep me logged in.").place(x=60, y=70)
login_btn = Button(frame2, text=" Login ", command=login_account, bg="light green").place(x=80, y=100)
cancel_btn = Button(frame2, text=" Cancel", command=quiting1, bg="red").place(x=180, y=100)
signup_btn = Button(frame2, text="Sign up", command=create_account, bg='light blue')
signup_btn.place(x=280, y=100)
frame2.pack()

root.mainloop()

conn.close()


