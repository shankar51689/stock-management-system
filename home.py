from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
import dbconnect as db
from pymysql import *
import random as ran
import tkinter.simpledialog as sd
from PIL import Image,ImageTk

root=Tk()
bgclr='powder blue'
root.state('zoomed')
root.update()
root.configure(bg=bgclr)
root.resizable(width=False,height=False)
lbl_head=Label(root,bg=bgclr,text='Stock Management',font=('verdna',45,'bold'))
lbl_head.pack(side='top',anchor='c')


def reset(*e):
	l=[e[i].get() for i in range(len(e))]
	for i in range(len(l)):
		e[i].delete(0,len(l[i]))
	if(l[len(l)-1]!=''):
		try:
			e[len(l)-1].current(0)
		except Exception:
			pass
		
def login(frm,e1,e2,cb):
	u=e1.get()
	p=e2.get()
	ut=cb.get()
	if(len(u)==0 or len(p)==0):
		msg.showwarning('Validation Problem','Please fill all fields')
	elif(ut=='--Select--'):
		msg.showwarning('Validation Problem','Please select user type')
	else:
		if(ut=='Admin'):
			if(u=='Admin' and p=='Admin'):
				msg.showinfo('Login','Welcome Admin')
				frm.destroy()
				welcomeAdmin(frm)
			else:
				msg.showerror('Login Failed','Invalid username or password')
		elif(ut=='Salesman'):
			con=db.getCon()
			cur=con.cursor()
			cur.execute("select * from salesman where s_id=%s and s_pass=%s",(u,p))
			row=cur.fetchone()
			con.close()
			if(row==None):
				msg.showerror('Login Failed','Invalid username or password')
			else:
				msg.showinfo('Login',f'Welcome:{row[2]}')
				frm.destroy()
				welcomeSalesman(frm,row)
				    

#*************************************Home page**************************************

def home():
	login_frm=Frame(root,bg=bgclr)
	login_frm.place(x=0,y=100,width=root.winfo_width(),height=root.winfo_height())

	lbl_user=Label(login_frm,bg=bgclr,font=('',20,'bold'),fg='blue',text='User Id:',padx=25)
	lbl_user.place(x=300,y=100)

	lbl_pass=Label(login_frm,bg=bgclr,font=('',20,'bold'),fg='blue',text='Password:')
	lbl_pass.place(x=300,y=150)

	ent_user=Entry(login_frm,bd=5,font=('',15,'bold'))
	ent_user.place(x=490,y=105)
	

	ent_pass=Entry(login_frm,show='*',bd=5,font=('',15,'bold'))
	ent_pass.place(x=490,y=155)

	lbl_usertype=Label(login_frm,bg=bgclr,font=('',20,'bold'),fg='blue',text='User Type:')
	lbl_usertype.place(x=300,y=205)

	cb_usertype=ttk.Combobox(login_frm,font=('',15,'bold'),values=['--Select--','Admin','Salesman'])
	cb_usertype.place(x=490,y=205)
	cb_usertype.current(0)

	lgn_btn=Button(login_frm,text='login',command=lambda:login(login_frm,ent_user,ent_pass,cb_usertype),bd=5,font=('',12,'bold'))
	lgn_btn.place(x=500,y=305)

	rst_btn=Button(login_frm,command=lambda:reset(ent_user,ent_pass,cb_usertype),text='reset',bd=5,font=('',12,'bold'))
	rst_btn.place(x=580,y=305)
	
	load=Image.open("download.jpg")
	render-ImageTk.PhotoImage(load)
	img=Lable(login_frm,image=render)
	img.image=renderimg.place(x=650,y=250)

def logout(frm):
    frm.destroy()
    home()
#*************************************Salesman page*********************************
def new_pass(data):
	conform=msg.askquestion('Conformation','You want to change the password')
	if(conform=='yes'):	
		new=sd.askstring('New password','New Password')
		con=db.getCon()
		cur=con.cursor()
		cur.execute(f"update salesman set s_pass='{new}' where s_id={data[0]}")
		con.commit()
		con.close()
		msg.showinfo('Info','Password successfully Changed')

def billing(frm,data):
	frm.destroy()
	l=[]#for product list
	frm1=Frame(root,bg=bgclr)
	frm1.place(x=0,y=100,width=root.winfo_width(),height=root.winfo_height())

	lbl_user=Label(frm1,bg=bgclr,font=('',20,'bold'),fg='blue',text=f'Welcome:{data[2]}')
	lbl_user.place(x=10,y=100)	

	back_btn=Button(frm1,width=15,command=lambda:welcomeSalesman(frm1,data),font=('',12,'bold'),text='Back',bd=5)
	back_btn.place(x=15,y=445)
	
	con=db.getCon()
	cur=con.cursor()
	cur.execute('select p_name from product')
	d=cur.fetchall()
	
	check_list=['--Select--']
	
	for i in d:
		check_list.append(i[0])
	
	pro_list_lb=Label(frm1,font=('',17,'bold'),text='Product:',bg=bgclr)
	pro_list_lb.place(x=390,y=205)
	
	pro_list=ttk.Combobox(frm1,font=('',15,'bold'),values=check_list)
	pro_list.place(x=490,y=205)
	pro_list.current(0)
	
	qty_lb=Label(frm1,text='Qty:',font=('',15,'bold'),bg=bgclr)
	qty_lb.place(x=440,y=260)
	
	qty_entry=Entry(frm1,bd=5,font=('',15,'bold'))
	qty_entry.place(x=490,y=260)
	con.close()
	
	add_btn=Button(frm1,command=lambda: ready_bill(frm1,pro_list.get(),qty_entry.get(),l),text='Add',bd=5,font=('',15))
	add_btn.place(x=460,y=310)
	
	total_bill_btn=Button(frm1,command=lambda: final_bill(frm1,l),text='Total Bill',bd=5,font=('',15))
	total_bill_btn.place(x=530,y=310)

def final_bill(frm,list):
	bill_field=Text(frm,width=30,height=20)
	bill_field.place(x=900,y=180)
	bill_field.insert(INSERT,'\t   Recipet\n')
	bill_field.insert(INSERT,'------------------------------\n')
	bill_field.insert(INSERT,'Product\t\tQty.\tPrice\n')
	bill_field.insert(INSERT,'------------------------------\n')
	total=0
	for i in list:
		total+=i[2]
		bill_field.insert(INSERT,f'{i[0]}\t\t{i[1]}\t{i[2]}\n')
	bill_field.insert(INSERT,'------------------------------\n')
	bill_field.insert(INSERT,f'Total Amount:-\t\t    Rs.{total}\n')
	
def ready_bill(frm,pro,qty,l):
	if(pro!='--Select--'):
		if(qty!=''):
			con=db.getCon()
			cur=con.cursor()
			cur.execute(f"select p_name,p_qty,p_price from product where p_name='{pro}' and P_qty>={qty}")
			if(cur.rowcount!=0):
				data=cur.fetchall()
				cur.execute(f"update product set p_qty=p_qty-{qty}")
				con.commit()
				con.close()
				amount=int(qty)*float(data[0][2])
				temp=[pro,qty,amount]
				l.append(temp)
				msg.showinfo('Info','Product Successfully added!')
			else:
				msg.showwarning('Warning','The qty you enter is not applicable')
		else:
			msg.showwarning('Warning','Enter any qty.')
	
	else:
		msg.showwarning('Warning','first select a product')
	
	
def welcomeSalesman(frm,user_data):
	frm.destroy()
	login_frm=Frame(root,bg=bgclr)
	login_frm.place(x=0,y=100,width=root.winfo_width(),height=root.winfo_height())

	lbl_user=Label(login_frm,bg=bgclr,font=('',20,'bold'),fg='blue',text=f'Welcome:{user_data[2]}')
	lbl_user.place(x=10,y=100)

	logout_btn=Button(login_frm,width=15,command=lambda:logout(login_frm),font=('',12,'bold'),text='Logout',bd=5)
	logout_btn.place(x=900,y=100)

	new_pass_btn=Button(login_frm,width=15,command=lambda:new_pass(user_data),font=('',12,'bold'),text='Change Password',bd=5)
	new_pass_btn.place(x=500,y=170)

	searchPro_btn=Button(login_frm,width=15,command=lambda:searchPro(login_frm,type='salesman'),font=('',12,'bold'),text='Search Product',bd=5)
	searchPro_btn.place(x=500,y=240)

	Billing_btn=Button(login_frm,width=15,command=lambda:billing(login_frm,user_data),font=('',12,'bold'),text='Billing',bd=5)
	Billing_btn.place(x=500,y=310)
	

	
#*************************************Admin Page*************************************

def delSal(frm):
	sid=sd.askstring('Delete Account','Enter salesmen id:-')
	try:
		sid=int(sid)
	except ValueError:
		msg.showerror('Error','The entry should be in integer')
	else:
		con=db.getCon()
		cur=con.cursor()
		cur.execute(f'delete from salesman where s_id={sid}')
		if(cur.rowcount==1):
			msg.showinfo('Delete Account','Account Deleted')
		else:
			msg.showwarning('Delete Account','Account not found')
		con.commit()
		con.close()
		viewSal(frm)
	
def viewSal(frm):
	con=db.getCon()
	cur=con.cursor()
	cur.execute('select * from salesman')
	s=cur.fetchall()
	cur.close()
	tree=ttk.Treeview(frm,column=('S_Id','S_Pass','S_Name','S_Mob','S_Email'),show='headings')
	
	tree.column('#1',width=70,minwidth=50,stretch=NO)
	tree.column('#2',width=120,minwidth=100,stretch=NO)
	tree.column('#3',width=150,minwidth=150,stretch=NO)
	tree.column('#4',width=70,minwidth=50,stretch=NO)
	tree.column('#5',width=100,minwidth=100,stretch=NO)
	
	tree.heading('#1',text='S_Id')
	tree.heading('#2',text='S_Pass')
	tree.heading('#3',text='S_Name')
	tree.heading('#4',text='S_Mob')
	tree.heading('#5',text='S_Email')
	
	for i in s:	
		tree.insert('',END,values=(i[0],i[1],i[2],i[3],i[4]))	
	
	tree.place(x=750,y=240)
	close=Button(frm,text='Close',command=lambda:welcomeAdmin(frm),font=('',15,'bold'),bd=5)
	close.place(x=800,y=500)

def addPro_db(frm1,*a):

	if(a[0].get()=='' or a[1].get()=='' or a[2].get()==''):
		msg.showwarning('warning','please fill all the entrys!')
	else:
		try:
			a1=a[0].get()
			a2=float(a[1].get())
			a3=int(a[2].get())
		except Exception :
			msg.showwarning('Warning','Qty and price should be integer')
			welcomeAdmin(frm1)
		else:
			con=db.getCon()
			cur=con.cursor()
			cur.execute(f"select p_name from product where p_name='{a[0].get()}'")
			if(cur.rowcount==0):
				cur.execute('select max(p_id)  from product')
				id=cur.fetchall()[0][0]
				id+=1
				cur.execute(f"insert into product values({id},'{a[0].get()}',{a[1].get()},{a[2].get()})")
				con.commit()
				con.close()
				msg.showinfo('Info','Product is successfully added!')
				welcomeAdmin(frm1)
			else:
				cur.execute(f"update product set p_qty=p_qty+{int(a[1].get())} where p_name='{a[0].get()}'")
				con.commit()
				con.close()
				msg.showinfo('Info','Product is successfully added!')
				welcomeAdmin(frm1)
		
def addPro(frm):
	frm.destroy()
	frm1=Frame(root,bg=bgclr)
	frm1.place(x=0,y=100,width=1200,height=root.winfo_height())
	
	lbl_user=Label(frm1,bg=bgclr,font=('',20,'bold'),fg='blue',text='Welcome:Admin')
	lbl_user.place(x=10,y=100)
	
	pro_name=Label(frm1,bg=bgclr,font=('',20,'bold'),fg='blue',text='Product Name:')
	pro_name.place(x=300,y=200)
	
	pro_price=Label(frm1,bg=bgclr,font=('',20,'bold'),fg='blue',text='Price:')
	pro_price.place(x=430,y=250)
	
	pro_qty=Label(frm1,bg=bgclr,font=('',20,'bold'),fg='blue',text='Qty. :')
	pro_qty.place(x=430,y=300)

	name_entry=Entry(frm1,bd=5,font=('',15,'bold'))
	name_entry.place(x=520,y=200)

	price_entry=Entry(frm1,bd=5,font=('',15,'bold'))
	price_entry.place(x=520,y=250)
	
	qty_entry=Entry(frm1,bd=5,font=('',15,'bold'))
	qty_entry.place(x=520,y=300)
	
	add_btn=Button(frm1,command=lambda:addPro_db(frm1,name_entry,qty_entry,price_entry),text='Add',bd=5,font=('',15,'bold'))
	add_btn.place(x=480,y=370)

	reset_btn=Button(frm1,command=lambda:reset(name_entry,price_entry,qty_entry),text='Reset',bd=5,font=('',15,'bold'))
	reset_btn.place(x=580,y=370)
		
	back_btn=Button(frm1,width=15,command=lambda:welcomeAdmin(frm1),font=('',12,'bold'),text='Back',bd=5)
	back_btn.place(x=900,y=445)

def searchPro(frm,type='admin'):
	con=db.getCon()
	cur=con.cursor()
	cur.execute('select * from product')
	s=cur.fetchall()
	cur.close()

	tree=ttk.Treeview(frm,column=('P_Id','P_Name','P_Qty','P_Price'),show='headings')
	
	tree.column('#1',width=55,minwidth=50,stretch=NO)
	tree.column('#2',width=120,minwidth=100,stretch=NO)
	tree.column('#3',width=60,minwidth=150,stretch=NO)
	tree.column('#4',width=80,minwidth=50,stretch=NO)
	
	tree.heading('#1',text='P_Id')
	tree.heading('#2',text='P_Name')
	tree.heading('#3',text='P_Qty')
	tree.heading('#4',text='P_Price')

	
	for i in s:	
		tree.insert('',END,values=(i[0],i[1],i[2],i[3]))	
	
	tree.place(x=750,y=240)
	if(type=='admin'):
		close=Button(frm,text='Close',command=lambda:welcomeAdmin(frm),font=('',15,'bold'),bd=5)
		close.place(x=800,y=500)
	else:
		close=Button(frm,text='Close',command=tree.destroy,font=('',15,'bold'),bd=5)
		close.place(x=800,y=500)	

def welcomeAdmin(frm):
	frm.destroy()
	login_frm=Frame(root,bg=bgclr)
	login_frm.place(x=0,y=100,width=root.winfo_width(),height=root.winfo_height())

	lbl_user=Label(login_frm,bg=bgclr,font=('',20,'bold'),fg='blue',text='Welcome:Admin')
	lbl_user.place(x=10,y=100)

	logout_btn=Button(login_frm,width=15,command=lambda:logout(login_frm),font=('',12,'bold'),text='Logout',bd=5)
	logout_btn.place(x=900,y=100)

	addPro_btn=Button(login_frm,width=15,command=lambda:addPro(login_frm),font=('',12,'bold'),text='Add Product',bd=5)
	addPro_btn.place(x=500,y=170)

	searchPro_btn=Button(login_frm,width=15,command=lambda:searchPro(login_frm),font=('',12,'bold'),text='Search Product',bd=5)
	searchPro_btn.place(x=500,y=240)

	addSal_btn=Button(login_frm,width=15,command=lambda:addSal(login_frm),font=('',12,'bold'),text='Add Salesman',bd=5)
	addSal_btn.place(x=500,y=310)

	viewSal_btn=Button(login_frm,width=15,command=lambda:viewSal(login_frm),font=('',12,'bold'),text='View Salesman',bd=5)
	viewSal_btn.place(x=500,y=380)

	delSal_btn=Button(login_frm,width=15,command=lambda:delSal(login_frm),font=('',12,'bold'),text='Delete Salesman',bd=5)
	delSal_btn.place(x=500,y=450)


def addSal(frm):
	frm.destroy()
	login_frm=Frame(root,bg=bgclr)
	login_frm.place(x=0,y=100,width=root.winfo_width(),height=root.winfo_height())

	lbl_user=Label(login_frm,bg=bgclr,font=('',20,'bold'),fg='blue',text='Welcome:Admin')
	lbl_user.place(x=10,y=100)

	logout_btn=Button(login_frm,width=15,command=lambda:logout(login_frm),font=('',12,'bold'),text='Logout',bd=5)
	logout_btn.place(x=900,y=100)

	back_btn=Button(login_frm,width=15,command=lambda:welcomeAdmin(login_frm),font=('',12,'bold'),text='Back',bd=5)
	back_btn.place(x=900,y=445)

	lbl_name=Label(login_frm,bg=bgclr,font=('',20,'bold'),fg='blue',text='Name:')
	lbl_name.place(x=300,y=200)

	lbl_pass=Label(login_frm,bg=bgclr,font=('',20,'bold'),fg='blue',text='Password:')
	lbl_pass.place(x=300,y=250)

	lbl_email=Label(login_frm,bg=bgclr,font=('',20,'bold'),fg='blue',text='Email:')
	lbl_email.place(x=300,y=300)

	lbl_mob=Label(login_frm,bg=bgclr,font=('',20,'bold'),fg='blue',text='Mob:')
	lbl_mob.place(x=300,y=350)

	ent_name=Entry(login_frm,bd=5,font=('',15,'bold'))
	ent_name.place(x=490,y=205)

	ent_pass=Entry(login_frm,bd=5,show='*',font=('',15,'bold'))
	ent_pass.place(x=490,y=255)

	ent_email=Entry(login_frm,bd=5,font=('',15,'bold'))
	ent_email.place(x=490,y=305)

	ent_mob=Entry(login_frm,bd=5,font=('',15,'bold'))
	ent_mob.place(x=490,y=355)

	sub_btn=Button(login_frm,width=5,text='Add',command=lambda:addSalDb(login_frm,ent_pass,ent_name,ent_mob,ent_email),bd=5,font=('',12,'bold'))
	sub_btn.place(x=520,y=405)

	rst_btn=Button(login_frm,width=5,command=lambda:reset(ent_name,ent_pass,ent_email,ent_mob),text='reset',bd=5,font=('',12,'bold'))
	rst_btn.place(x=600,y=405)

def addSalDb(frm,*e):

	l=[e[i].get() for i in range(len(e))]
	if(l[0]=='' or l[1]=='' or l[2]=='' or l[3]==''):
		msg.showwarning('warning','Please fill all the entrys!')
	elif(l[2]!=int()):
		msg.showwarning('warning','Phone number should be an integer')
	else:
		con=db.getCon()
		cur=con.cursor()
		id=ran.randint(000,999)
		cur.execute(f"insert into salesman values({id},'{l[0]}','{l[1]}','{l[2]}','{l[3]}')")
		con.commit()
		con.close()
		msg.showinfo('Info','New Salesman will be added')
		welcomeAdmin(frm)
	
	
home()
root.mainloop()
