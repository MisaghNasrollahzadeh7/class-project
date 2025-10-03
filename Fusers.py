
import sqlite3
import tkinter
import re

cnt=sqlite3.connect("shop.db")

userid=''

def Login(txtPass,txtUser,lblMsg,btnLogin,btnshop,btncart):
    global userid
    user=txtUser.get()
    pas=txtPass.get()
    if user=="" or pas=="":
        lblMsg.configure(text="please fill the Input",fg="red",font="tahoma,bold 14")
        return
    query=f'''
            SELECT * FROM users WHERE username="{user}" AND password="{pas}"
           '''
    result=cnt.execute(query)
    data=result.fetchall()
    if len(data)<1:
        lblMsg.configure(text="Wrong username or password...!!",fg="red",font="tahoma,bold 12")
        return
    lblMsg.configure(text="Welcome",fg="green",font="tahoma,bold 14")
    query=f'''
            SELECT id FROM users WHERE username="{user}"
           '''
    result=cnt.execute(query)
    data=result.fetchall()
    userid=data[0][0]
    txtUser.delete(0,"end")
    txtPass.delete(0,"end")
    btnLogin.configure(state="disabled")
    btnshop.configure(state="active")
    btncart.configure(state="active")


def validate(user,pas,cpas,addr):
    if user=="" or pas=="" or cpas=="" or addr=="":
        return False,"ERROR:please fill the Inputs"
    elif pas!=cpas:
        return False,"ERROR:password and confirm mismatch!"
    query=f'''
            SELECT * FROM users Where username = "{user}"
           '''
    result = cnt.execute(query)
    data=result.fetchall()
    if len(data)>0:
        return False,"ERROR:username already exist"
    regular=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    if not re.match(regular,pas):
        return False,"Invalid Password"

    return True,""
def signup():
    def register():
        user=txtUser.get()
        pas=txtPass.get()
        cpas=txtcPass.get()
        addr=txtAddr.get()
        result,msg=validate(user,pas,cpas,addr)
        if not result:
            lblMsg.configure(text=msg,fg="red",font="tahoma,bold 14")
            return
        query=f'''
                INSERT INTO users (username,password,address,score)
                VALUES("{user}","{pas}","{addr}",0)
               '''
        cnt.execute(query)
        cnt.commit()
        lblMsg.configure(text="Your data registered successfully",font="tahoma,bold 14",fg="green")
        txtUser.delete(0,"end")
        txtPass.delete(0,"end")
        txtcPass.delete(0, "end")
        txtAddr.delete(0,"end")

    winsignup=tkinter.Toplevel()
    winsignup.title("Signup Panel")
    winsignup.geometry('450x450')
    winsignup.configure(bg='light blue')
    lblUser = tkinter.Label(winsignup, text="username:", font="tahoma,bold 14", fg="black", bg="light blue")
    lblUser.pack()
    txtUser = tkinter.Entry(winsignup, width=30, highlightthickness=4, highlightcolor='black')
    txtUser.pack()

    lblPass = tkinter.Label(winsignup, text="password:", font="tahoma,bold 14", fg="black", bg="light blue")
    lblPass.pack()
    txtPass = tkinter.Entry(winsignup, width=30, highlightthickness=4, highlightcolor='black')
    txtPass.pack()

    lblcPass = tkinter.Label(winsignup, text="password confirm:", font="tahoma,bold 14", fg="black", bg="light blue")
    lblcPass.pack()
    txtcPass = tkinter.Entry(winsignup, width=30, highlightthickness=4, highlightcolor='black')
    txtcPass.pack()

    lblAddr = tkinter.Label(winsignup, text="Address:", font="tahoma,bold 14", fg="black", bg="light blue")
    lblAddr.pack()
    txtAddr = tkinter.Entry(winsignup, width=30, highlightthickness=4, highlightcolor='black')
    txtAddr.pack()

    btnRegister = tkinter.Button(winsignup, text="Register", font="tahoma,bold 16",
                                 width=8, bg="black", fg="orange",command=register)
    btnRegister.place(x= 175,y=270)
    # btnRegister.pack()

    lblMsg = tkinter.Label(winsignup, text="", bg="light blue")
    lblMsg.pack()
    winsignup.mainloop()

def shop():
    def add2cart():
        pid=txtid.get()
        pnum=txtnum.get()
        if pid=="" or pnum=="":
            lblmsg3.configure(text='please fill the inputs!',fg='red',font="tahoma,bold 14")
            return
        if (not pid.isdigit()) or (not pnum.isdigit()):
            lblmsg3.configure(text='invalid data!', fg='red', font="tahoma,bold 14")
            return
        query=f'''
                SELECT * FROM products WHERE id={int(pid)}
              '''
        result=cnt.execute(query)
        data=result.fetchall()
        if len(data)<1:
            lblmsg3.configure(text='invalid id',fg='red', font="tahoma,bold 14")
            return
        query = f'''
                    SELECT * FROM products WHERE id={int(pid)} AND numbers>={int(pnum)}
                 '''
        result = cnt.execute(query)
        data = result.fetchall()
        if len(data) < 1:
            lblmsg3.configure(text='Not Enough Products!', fg='red', font="tahoma,bold 14")
            return
        query=f'''
                INSERT INTO cart(uid,pid,numbers)
                VALUES({userid},{int(pid)},{int(pnum)})
               '''
        cnt.execute(query)
        cnt.commit()
        lblmsg3.configure(text='Saved to Cart!',fg='green', font="tahoma,bold 14")
        txtid.delete(0,'end')
        txtnum.delete(0,'end')
        query = f'''
                    UPDATE products SET numbers=numbers - {int(pnum)} WHERE id={int(pid)}
                  '''
        cnt.execute(query)
        cnt.commit()



    winshop=tkinter.Toplevel()
    winshop.title('shop panel')
    winshop.geometry("600x600")
    winshop.configure(bg='light blue')
    lstbox=tkinter.Listbox(winshop,width=60,bg='orange',highlightcolor='black',highlightthickness='4')
    lstbox.pack()
    products=getproducts()
    for item in products:
        text=f'id: {item[0]} ** name: {item[1]} ** price: {item[2]} ** numbers: {item[3]}'
        lstbox.insert(0,text)
    lblid = tkinter.Label(winshop, text="product ID", font="tahoma,bold 14", fg="black", bg="light blue")
    lblid.pack()
    txtid = tkinter.Entry(winshop, width=30, highlightthickness=4, highlightcolor='black')
    txtid.pack()
    lblnum = tkinter.Label(winshop, text="product numbers", font="tahoma,bold 14", fg="black", bg="light blue")
    lblnum.pack()
    txtnum = tkinter.Entry(winshop, width=30, highlightthickness=4, highlightcolor='black')
    txtnum.pack()
    lblmsg3 = tkinter.Label(winshop, text="", font="tahoma,bold 14", fg="black", bg="light blue")
    lblmsg3.pack()
    btnshop = tkinter.Button(winshop, text="Add to Cart", font="tahoma,bold 16",
                                 width=10, bg="black", fg="orange",command=add2cart)
    btnshop.pack()
    winshop.mainloop()

def getproducts():
    query='''
            SELECT * FROM products
          '''
    result=cnt.execute(query)
    data=result.fetchall()
    return data



def showcart():
    wincart = tkinter.Toplevel()
    wincart.title('shopping cart')
    wincart.geometry("500x500")
    wincart.configure(bg='light blue')
    lstbox2 = tkinter.Listbox(wincart, width=60, bg='orange', highlightcolor='black', highlightthickness='4')
    lstbox2.pack()
    query = f'''
           SELECT cart.pid, products.pname, cart.numbers, products.price 
           FROM cart 
           JOIN products ON cart.pid = products.id 
           WHERE cart.uid = {userid}
             '''
    result=cnt.execute(query)
    data=result.fetchall()
    if not data:
        lstbox2.insert(0, "Your cart is empty!!!")
    else:
        for item in data:
            text = f'ID: {item[0]} ** Name: {item[1]} ** Numbers: {item[2]} ** Price: {item[3]}'
            lstbox2.insert(0,text)
    total_price=0
    for item in data:
        t=item[2]*item[3]
        total_price+=t
    lbltotal=tkinter.Label(wincart,text="Total Price", font="tahoma,bold 20", fg="black", bg="light blue")
    lbltotal.pack()
    lblmsg = tkinter.Label(wincart, text="", font="tahoma,bold 20", fg="black", bg="light blue")
    lblmsg.pack()
    lblmsg.configure(text=str(total_price) + " $ ")

    wincart.mainloop()


def admin():
    def validad(txtUser,txtPass,lblMsg,btnlogin,btnremove,btnprod):
        user=txtUser.get()
        pas=txtPass.get()
        if user == "" or pas == "":
            lblMsg.configure(text="Please Fill The Input",font="tahoma,bold 18",fg="blue")
            return
        elif user.isnumeric() or pas.isnumeric():
            lblMsg.configure(text="user or pass can't be numeric", font="tahoma,bold 18", fg="blue")
            txtUser.delete(0, "end")
            txtPass.delete(0, "end")
            return
        if user=="admin" and pas=="ADMIN":
            lblMsg.configure(text="WELCOME", font="tahoma,bold 18",fg="#23fa02")
            btnlogin.configure(state="disabled")
            btnremove.configure(state="active")
            btnprod.configure(state="active")
        else:
            lblMsg.configure(text="Invalid Username or Password",font="tahoma,bold 18",fg="blue")
        txtUser.delete(0, "end")
        txtPass.delete(0, "end")

    def delete():
        def delprod(btndel,txtProductId,lblmsg):
            id=txtProductId.get()
            if id=="":
                lbmsg.configure(text="Please enter a Product ID", fg="blue", font="tahoma,bold 14")
                return
            if not id.isdigit():
                lbmsg.configure(text="Product ID must be a number", fg="blue", font="tahoma,bold 14")
                return
            query = f'''
                        DELETE FROM products WHERE id={int(id)}
                     '''
            cnt.execute(query)
            cnt.commit()
            lbmsg.configure(text="Product deleted successfully!", fg="#23fa02", font="tahoma,bold 14")
            txtProductId.delete(0, 'end')
            lstbox2.delete(0, 'end')

            query = 'SELECT * FROM products'
            result = cnt.execute(query)
            data = result.fetchall()

            for item in data:
                text = f'ID: {item[0]} ** Name: {item[1]} ** Numbers: {item[2]} ** Price: {item[3]}'
                lstbox2.insert(0, text)

        winremove = tkinter.Toplevel()
        winremove.title("Remove Product")
        winremove.geometry("450x450")
        winremove.configure(bg='#f54290')
        lstbox2 = tkinter.Listbox(winremove, width=60, bg='orange', highlightcolor='black', highlightthickness='4')
        lstbox2.pack()
        query = '''
                SELECT * FROM products
                '''
        result = cnt.execute(query)
        data = result.fetchall()
        for item in data:
            text = f'ID: {item[0]} ** Name: {item[1]} ** Numbers: {item[2]} ** Price: {item[3]}'
            lstbox2.insert(0, text)

        lblProductId = tkinter.Label(winremove, text="Product ID", font="tahoma,bold 14", fg="black",
                                             bg="#f54290")
        lblProductId.pack()
        txtProductId = tkinter.Entry(winremove, width=10, highlightthickness=4, highlightcolor='black')
        txtProductId.pack()
        lbmsg = tkinter.Label(winremove, text="", bg="#f54290")
        lbmsg.pack()
        btndel = tkinter.Button(winremove, text="Delete Product", font="tahoma,bold 16",bg="black",fg="white",
                                command=lambda:delprod(btndel,txtProductId,lbmsg))
        btndel.pack()
        winremove.mainloop()

    def edit():
        def change_quantity(btnUpdate,txtNewQuantity,lbmsg,txtProdId):
            product=txtProdId.get()
            quantity = txtNewQuantity.get()
            if product=="" or quantity=="":
                lbmsg.configure(text="Please fill in !!!", fg="blue", font="tahoma,bold 14")
                return
            if not product.isdigit() or not quantity.isdigit():
                lbmsg.configure(text="Product ID and Quantity must be numbers", fg="blue", font="tahoma,bold 14")
                return
            query = f'''
                        UPDATE products
                        SET numbers={int(quantity)}
                        WHERE id={int(product)}
                     '''
            cnt.execute(query)
            cnt.commit()
            lbmsg.configure(text="Product updated successfully!", fg="#23fa02", font="tahoma,bold 14")
            txtProdId.delete(0, 'end')
            txtNewQuantity.delete(0, 'end')
            lstbox2.delete(0, 'end')

            query = 'SELECT * FROM products'
            result = cnt.execute(query)
            data = result.fetchall()

            for item in data:
                text = f'ID: {item[0]} ** Name: {item[1]} ** Numbers: {item[2]} ** Price: {item[3]}'
                lstbox2.insert(0, text)
        winedi = tkinter.Toplevel()
        winedi.title("Edit Product")
        winedi.geometry("450x450")
        winedi.configure(bg='#f54290')
        lstbox2 = tkinter.Listbox(winedi, width=60, bg='orange', highlightcolor='black', highlightthickness='4')
        lstbox2.pack()
        query = '''
                SELECT * FROM products
                '''
        result = cnt.execute(query)
        data = result.fetchall()
        for item in data:
            text = f'ID: {item[0]} ** Name: {item[1]} ** Numbers: {item[2]} ** Price: {item[3]}'
            lstbox2.insert(0, text)
        lblProdId = tkinter.Label(winedi, text="Product ID", font="tahoma,bold 14", fg="black", bg="#f54290")
        lblProdId.pack()
        txtProdId = tkinter.Entry(winedi, width=30, highlightthickness=4, highlightcolor='black')
        txtProdId.pack()
        lblNewQuantity = tkinter.Label(winedi, text="New Product Quantity:", font="tahoma,bold 14", fg="black",
                                       bg="#f54290")
        lblNewQuantity.pack()
        txtNewQuantity = tkinter.Entry(winedi, width=30, highlightthickness=4, highlightcolor='black')
        txtNewQuantity.pack()
        lbmsg = tkinter.Label(winedi, text="", bg="#f54290")
        lbmsg.pack()
        btnUpdate = tkinter.Button(winedi, text="Update Quantity", font="tahoma,bold 16",bg="black",fg="white",
                                   command=lambda:change_quantity(btnUpdate,txtNewQuantity,lbmsg,txtProdId))
        btnUpdate.pack()
        winedi.mainloop()



    winadmin = tkinter.Toplevel()
    winadmin.title('admin panel')
    winadmin.geometry("450x450")
    winadmin.configure(bg='#f54290')
    img = tkinter.PhotoImage(file='ad.png')
    lblUser = tkinter.Label(winadmin, text="USERNAME", font="tahoma,bold 18",
                            fg="black", bg="#f54290",image=img,compound='top')
    lblUser.pack()
    txtUser = tkinter.Entry(winadmin, width=40, highlightthickness=4, highlightcolor='black')
    txtUser.pack()
    lblPass = tkinter.Label(winadmin, text="PASSWORD", font="tahoma,bold 18", fg="black", bg="#f54290")
    lblPass.pack()
    txtPass = tkinter.Entry(winadmin, width=40, highlightthickness=4, highlightcolor='black')
    txtPass.pack()
    lblMsg = tkinter.Label(winadmin, text="", bg="#f54290")
    # lblMsg.place(x=110, y=125)
    lblMsg.pack()
    btnlogin = tkinter.Button(winadmin, text="Login", font="bold 18", width=10,
                              bg="black", fg="white",
                              command=lambda: validad(txtUser,txtPass,lblMsg,btnlogin,btnremove,btnprod))
    btnlogin.place(x=150, y=260)
    btnremove = tkinter.Button(winadmin, text="Remove PROD.", font="bold 14", width=15,
                              bg="black", fg="white",state="disabled",command=delete)
    btnremove.place(x=135, y=310)
    btnprod = tkinter.Button(winadmin, text="Edit PROD.", font="bold 14", width=15,
                               bg="black", fg="white",state="disabled",command=edit)
    btnprod.place(x=135, y=350)

    winadmin.mainloop()




