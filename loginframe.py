#Login Frame Dated 06-Jan-2023 OOPS Approach
from tkinter import *
from tkinter import messagebox
import mysql.connector as my
from mysql.connector.errors import IntegrityError  #Primary Key
import dbconfig
#Leave 4 lines for future use
#Using Map to store common decoration only ones
decorate={"font": ("Arial", 16), "fg":"brown" , "bg":"pink"}
decorate2={"font": ("courier", 12), "fg":"blue" , "bg":"yellow"}
#Define Class
class LoginFrame(Frame):
    def __init__(self, win):#Initializer( Python), Constructor (C++)
        super().__init__(win) #Passing win to parent Frame 
        self.win=win  #Linking parent with this Frame
        self.config(width=200, height=60)                    
        #Bind Variables
        #Without class
        #userid=StringVar()
        #With class concept, it is must to use self (object variable)
        self.userid=StringVar()
        self.password=StringVar()
        self.initialize() #User-Defined Fn: To design Layout
        
    def initialize(self): #Code to design layout
        lblMessage=Label(self.win, text="Login Frame" , **decorate)
        lblMessage.grid(row=0, column=0,columnspan=2,sticky='news')
        lblUserid=Label(self.win, text="Enter Userid",anchor='w',**decorate2)
        lblUserid.grid(row=1, column=0)
        txtUserid=Entry(self.win, width=20, textvariable=self.userid, **decorate2)
        txtUserid.grid(row=1, column=1)
        lblPassword=Label(self.win, text="Enter Password" ,anchor='w')
        lblPassword.grid(row=2, column=0)
        txtPassword=Entry(self.win, width=20, textvariable=self.password)
        txtPassword["show"]="*"  #Interview - how to display * while entrying password
        txtPassword.grid(row=2, column=1, sticky='w')
        btnLogin=Button(self.win, text="Login", command=self.loginClick)
        btnLogin.grid(row=3, column=0)
        btnRegister=Button(self.win, text="Register", command=self.registerClick)
        btnRegister.grid(row=3, column=1)
    def loginClick(self): 
        #Store data of bind variables into local variables (sime name)
        u=self.userid.get() #obtain userid
        p=self.password.get() #obtain password
        #Validation logic - Check for Empty data
        if len(u)==0 or len(p)==0:
            messagebox.showinfo("Empty", "Userid/Password Cannot be Empty")
            return #Terminate Fn
        #Now design embeded SQL Query using format specifier as in C
        #sql="Select * from candidates where name='%s' and mobile='%s' "%(u,p)
        #Recommonded way
        sql="Select * from candidates where name='{0}' and mobile='{1}' ".format(u,p)
        print(sql)  #Debugging
        #Connect with database by reading credentials from dbconfig        
        mydb = my.connect(**dbconfig.config)
        #Check if not connected with mysql
        if not mydb.is_connected():
            messagebox.showerror('Error' , 'Failed to Connect to Database')
            return #Terminate Fn
        #Step III: Create a temporary memory buffer to store rows known as cursor [Use dictionary internally=>dictionary=True)
        cursor=mydb.cursor(dictionary=False)
        #Step IV: Execute it
        cursor.execute(sql)
        #Step VI: Fetch one rows from Cursor into a variable
        record=cursor.fetchone()  #when only one row exists
        #OR records=cursor.fetchall() #more than one rows exists
        #print(cursor.rowcount)
        #if cursor.rowcount==0:
        #if records==None or len(records)==0:
        if record==None:
            messagebox.showerror('Access Denied' , 'Userid/Password Not Found')
        else:
            self.win.destroy() #Close this window when successful
        #Close database connection to free memory resources    
        if cursor !=None: cursor.close()
        if mydb !=None: mydb.close()
    #So that a new user can register
    def registerClick(self):
        u=self.userid.get() #Obtain userid into local variable
        p=self.password.get()
        #Check if anything is empty
        if len(u)==0 or len(p)==0:
            messagebox.showinfo("Empty", "Userid/Password Cannot be Empty")
            return #Terminate Fn
        #Display dialogbox to reconfirm password
        from tkinter import simpledialog
        response = simpledialog.askstring("Confirm", "Re-Type Password/Mobile", initialvalue=None)
        #If password p and response password doesn't match
        if p!=response:   # != Not equal
            messagebox.showinfo("Not Matched","Password Not Matched")
            return #Terminate Fn now
        #Otherwise, when everything is correct
        #Now design embeded SQL Query
        try: #Unreliable Code that may have errors
            #sql="insert into candidates values('%s' ,'%s')"%(u,p)
            sql="insert into candidates values('{}' ,'{}')".format(u,p)
            print(sql) #Debug
            #Connect with database by reading credentials from dbconfig        
            mydb = my.connect(**dbconfig.config) # ** - passing map
            #Check if not connected with mysql
            if not mydb.is_connected():
                messagebox.showerror('Error' , 'Failed to Connect to Database')
                return #Terminate Fn
            #Step III: Create a temporary memory buffer to store rows known as cursor [Use dictionary internally=>dictionary=True)
            cursor=mydb.cursor(dictionary=False)
            #Step IV: Execute it
            cursor.execute(sql)
            result=cursor.rowcount #It gives number of rows affected
            print(result) #For Debug
            if result==0:
                messagebox.showerror('Sorry' , 'Failed to Create Userid/Password')
                return
                cursor.execute('commit') #Save changes permanently
            if cursor !=None: cursor.close()
            if mydb !=None: mydb.close()
            #pass   #I'll cover it in upcoming lecture
        except IntegrityError as err:
            messagebox.showerror('Duplicate Record' , str(err))
def main():
    #Create Object/Instance
    win=Tk()            #win is object of Tk() class
    obj=LoginFrame(win) #Calling Parameterized Constructor
    obj.grid()
    win.mainloop()
    #win.dispose()
if __name__=="__main__": #This is called when we run this file
    main()                #directly
