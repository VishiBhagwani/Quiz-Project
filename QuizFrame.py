#Step I: required imports
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno
import pandas
from datetime import datetime #11-Aug-2023
import string
#12-aug-2023 - we are importing loginframe.py as lf
import loginframe as lf
#Step II: Connect with Database (Sql-Alchemy)
import dbconfig   #as created on 8-Aug
import sys  #To terminate program using exit(0)
from sqlalchemy import create_engine, text
#Step III: Create object of Tkinter and set title and geometry
width,height,X,Y=800,500,150,100 #Concept of Tuple #8-Aug
totalQuestions=2 #8-Aug
#9-Aug 
index,rows,cols,previousIndex=0,0,0,-1 #By Default show first question from Shuffled DataFrame

#Additional logic added on 9-Aug
#Creating two list for storing answers of user, buttons for each Question
answerList=[None]*totalQuestions
btn=[None]*totalQuestions


win=Tk()
win.title('Quiz Frame - Ajay')
win.geometry('{}x{}+{}+{}'.format(width,height,X,Y))
#12-Aug-2023 For QR Code
def generateQRCode(data):
        import pyqrcode,png
        #import png 
        from pyqrcode import QRCode   #QRCode is a class
        from PIL import Image         #Python Image Library
        # String which represents the QR code       
        print("Verification Code is " , data) #Debugging
        # Generate QR code 
        url = pyqrcode.create(data) 
        # Now save the image as .png file
        url.png(data, scale = 6)
    
#12-Aug-2023 - Login Frame
def topWindow(title,w, h):
        top=Toplevel(win)
        top.title(title)
        top.minsize(width=w,height=h)
        top.maxsize(width=w,height=h)
        #top.minsize(width=self.width,height=self.height)
        #top.maxsize(width=self.width,height=self.height)
        top.geometry(("+%d+%d")%(w,h)) #Tuple  + means position
        top.transient(win)
        #module = __import__(moduleName,fromlist=[None])
        #class_ = getattr(module, className)
        return top
#12-Aug-2023 - Display Popup or Modal Window before showing question
top=topWindow("Login Frame",300,150) #12-Aug
frame=lf.LoginFrame(top) #object of LoginFrame
top.wait_window(frame) #Imp: parent should wait till popup window closed

#Step IV: Bind variables to link with UI
qno=IntVar(value=1)
question=StringVar()
option1=IntVar()  # To support 0/1
option2=IntVar() 
option3=IntVar() 
option4=IntVar() 
answer=StringVar()  #To support concat/joining of digits
#Step V: Define some global variables that may be required in multiple 
try:
    engine = create_engine(dbconfig.config2)   
except Exception as e:
    messagebox.showerror('Database Failed', 'Failed to Connect with Database')
    sys.exit(0)
df=None #None - means not Initialized
#Functions as we've used variable operation in QuestionsFrame
#Dictionary for decoration
decoration1={'background':'blue', 'font':'arial,10', 'width': '10'}
#Step VI: User-Defined Functions
#10-Aug-2023 Fn to save answer before moving to next question
def saveAnswer(index):
    opted='' #Empty String (1: Checked 0: Unchecked)
    if option1.get()==1: opted+='1'   #Means Checked
    if option2.get()==1: opted+='2'
    if option3.get()==1: opted+='3'
    if option4.get()==1: opted+='4'      
    print('save Answer, opted=', opted)    
    answerList[index]=opted    
    
    
#9-Aug-2023 - Fn to change color of Button
def changeButtonState(previousIndex2, index):
    global previousIndex
    #Section A: Enabling Disabling Navigation Buttons
    #By default make prev, next as normal and finish as disabled
    btnPrevious.config(state='normal')
    btnNext.config(state='normal')
    btnFinish.config(state='disabled')
    #Activate or Deactivate Finish Button
    if index==0:  #We are at First Question
        btnPrevious.config(state='disabled')
    #if index<totalQuestions-1:
    #    btnFinish.config(state='disabled')
        #btnFinish['config']='disabled'
    elif index==totalQuestions -1: #At Last Question
        btnNext.config(state='disabled')
        btnFinish.config(state='normal')
    #Section B: Changing Button Color        
    #Changing Color of previously answered Buttons based on answered or not
    print('Previous Index={}  Index={}'.format(previousIndex, index))
    
        
    #(Point IV) - Disable Current index Question Button, make it yellow
    btn[index].config(state='disabled')
    btn[index].config(bg='yellow')
    #Means if index and previousIndex are different Buttons
    if previousIndex!=-1: #Activate previously pressed button
        btn[previousIndex].config(state='normal')
        print('Previous Ans=', answerList[previousIndex])
        if answerList[previousIndex]!=None:
            print('Length=' , len(answerList[previousIndex]))
    #Not Answered=>Red, Answered=>Green    
    #By default answer list contains None
    
    if answerList[previousIndex]==None:
        #print('Previous Index Value is None' )
        return #Do Nothing
    elif len(answerList[previousIndex])==0:
        btn[previousIndex].config(bg='red')  #Red - If Not Answered
    elif  len(answerList[previousIndex])>0:
        btn[previousIndex].config(bg='green') #Green - if Answered
    if previousIndex!=-1: #Activate previously pressed button
        print('Previous Ans=', answerList[previousIndex])
        print('Length=' , len(answerList[previousIndex]))
    
#8-Aug-2023 - Fn to Load Questions into DataFrame
def showQuestion(index):
    #Imp: index must match with the sequence of column in table
    question.set(df.loc[index][1])#current indexed row, col=>1 (question)
    #Change text of Checkboxes at runtime (config)
    chkOption1.config(text=df.loc[index][3])
    chkOption2.config(text=df.loc[index][4])
    chkOption3.config(text=df.loc[index][5])
    chkOption4.config(text=df.loc[index][6])
    lblQuestion.config(text='Q' + str(index+1) +":")
    #9-Aug-2023: Check/Uncheck buttons based on user opted
    
    #Uncheck all buttons
    option1.set(0)
    option2.set(0)
    option3.set(0)
    option4.set(0)
    opted=answerList[index]
    print('ShowQuestions, opted=', opted)
    if opted !=None and len(opted)>0:
        option1.set( 1 if opted.find('1')>-1 else 0)    
        option2.set( 1 if opted.find('2')>-1 else 0)    
        option3.set( 1 if opted.find('3')>-1 else 0)    
        option4.set( 1 if opted.find('4')>-1 else 0)    
#8-Aug-2023: It fetch questions from database and load into DataFrame
def loadQuestions():
    global df  #To inform that it's a global variable
    sql='Select * from questions' #Any Query
    #execute the query and load data into dataframe
    df=pandas.read_sql(sql, engine) 
    global index,rows, cols
    rows,cols=df.shape  #Interview - To count no of rows and columns
    #In case sufficient questions are not available
    if rows< totalQuestions:
        messagebox.showerror('Insufficient Questions', 'Sorry. Database do Not have enough questions to ask')
        sys.exit(0)
    #Otherwise, Shuffle set of Questions in dataframe [Interview]
    df = df.sample(frac=1).reset_index(drop=True)
    #print('Data Frame is' , df)  #Debugging
    index=0 #To display First Question
    showQuestion(index) #Display the Question
    #Display data frame
    #print('Data Frame=',df)  #For debugging
#11-Aug-2023 Fn to compute result when exam ends
def saveToFile(html ,filename): #It takes html code
    #utf-8 Unicode text format - Supports multi-lingual data
    #with keyword opens file and close automatically at the end
    #of with block
    with open(filename , "w" , encoding='utf-8') as f:
        f.write(html)
    #14-Aug-2023 Extra logic for html to pdf
    import weasyprint
    pdfname=filename.replace('.html', '.pdf')
    pdf = weasyprint.HTML(filename).write_pdf()
    if len(pdf)>0:
        open('pdfname', 'wb').write(pdf)
    messagebox.showinfo('Congrats', 'Certificate Generate. Filename:' + filename + 'PDF Name is '+ pdfname)
    confirmation = askyesno(title='confirmation',
                    message='Are you sure to Close App?')
    #Automatically opening certificate page in a web-browser
    import webbrowser  #12-Aug-2023 (Built-in module)
    webbrowser.open(filename)
    if confirmation:         
        sys.exit(0) #To terminate program
#11-Aug-2023
def generateCertificate(name,correct,wrong,total,percent,grade):
    category=string.capwords(df.loc[index][2]) #Like Java, Python, C++
    today=datetime.now()
    #date=today.strftime("%d-%b-%Y %H:%M:%S"))
    date=today.strftime("%d-%b-%Y")
    #Multi-Line String: html code to design certificate
    #filename=name +"-" + date + ".html"
    imagename='{}-{}.png'.format(name,date) #12-Aug-2023
    filename='{}-{}.html'.format(name,date) #11-Aug-2023
    generateQRCode(imagename) #Calling fn
    #11-Aug-2023
    html='''
    <html>
        <head><h1><center><u>TecDev Certificate</u></center></h1>
        <hr/>
        <style>
  .mystyle
  {{
     border: double gold 2px;
     margin: auto;
     width: 100%;
     padding: 10px;
     text-align: center;
   }}
</style> 
<img src='{8}' align='right' width='100px' height='100px' />
</head>
        <body>
        <div class="mystyle">
        <h2>
        <pre>
        This certificate is awarded to <u>{0}</u> 
        in recognition of their successful completion of {1} on {2}. 
        Your hard work, dedication, and commitment to learning have 
        enabled you to achieve this milestone, and we are proud to 
        recognize your accomplishment.
        </pre>
        </h2>
        </div>
        <hr/>
        <h2>Your Performance</h2> 
        <h3>Correct={3}, Wrong={4}, Total Marks={5}, percent={6}, Grade={7} </h3>
        <hr/>
        </body>
    </html>
    '''.format(name,category,date,correct,wrong,total,percent,grade,imagename)
    saveToFile(html,filename) #11-Aug-2023
#14-Aug-2023 Step II UDF saveResultToDB
def saveResultToDB(name,mobile,correct,wrong,total):
    today=datetime.now()
    dated=today.strftime("%d-%b-%Y")  #mysql dated varchar
    #mysql dated date  =>  dated=today.strftime('%Y-%m-%d')
    sql='''
    insert into result(dated, correct, wrong, total, name, mobile)
    values('{}','{}','{}','{}','{}','{}')
    '''.format(dated, correct, wrong,total,'ram','345')
    print('SQL = ', sql)
    #Connect as SQLAlchemy
    with engine.begin() as con:
        result=con.execute(text(sql))
        #insert, update, delete gives rowcount - rows affected by sql
        if result.rowcount>0:
            con.execute(text('commit')) #save permanently
            messagebox.showinfo('Success', 'Result Saved to DB')
        else:
            messagebox.showerro('Failure', 'Failed to Save to DB')
def calculateResult():
    total,wrong,correct,percent=0,0,0,0
    name=string.capwords('ajay kumar verma') #Later we take it at runtime
    #Perform Loop to compare answer stored in dataframe vs answered
    #by user - stored in list with name answerList
    #Perform loop to travese each answer
    for i in range(0, totalQuestions): #0 to totalQuestions-1
        answer=str(df.loc[i][7]) #Actual Answer - convert to string
        opted=answerList[i] #What user Answered
        if opted==answer: #both answer and opted match
            correct+=1    #increase correct by 1
        elif len(opted)>0:  #means answer does not match
            wrong+=1      #increate wrong by 1
    #Unanswered answered question are not considered
    total=4*correct -wrong #Business Logic - May change as per specification
    percent=total*100/(4*totalQuestions)
    #Single line if statement
    grade='Pass' if percent>=60 else 'Fail'
    #Calling fn by passing some values
    #14-Aug-2023 Saving to database -Step I
    mobile='123'
    saveResultToDB(name,mobile,correct,wrong,total)
    generateCertificate(name,correct,wrong,total,percent,grade) #UDF
    
    
#Step VII: Event Handler Functions
'This function handles event for previous next finish button'
def navigationClick(value): #08-Aug
    global index, totalQuestions, previousIndex
    #Without writing variable as global, a new local variable created
    previousIndex=index #Store previous index value
    saveAnswer(previousIndex) #OR saveAnswer(index) 10-Aug
    #changeButtonState(previousIndex)
    #Update value of index
    if value=='F': #Finish Button
        index=totalQuestions  #Finish
        calculateResult() #09-Aug
        return #Terminate Fn
    elif value=='P':  #Previous Record
        if index>0:  #If not on first record
            index-=1   #index=index-1 #Decrease value by 1
        #else:
        #    index=totalQuestions-1 #Move to the Last row (cycle)
    elif value=='N':  #Next Record
        if index<totalQuestions-1:  #If not on last record
            index+=1  #Move to next record
        #else:
        #    index=0 #Move back to the first row    (cycle)
    showQuestion(index) #To display data
    changeButtonState(previousIndex, index) #10-Aug
    
'This function handles event when checkbox are selected or unselected'
def optionChanged(value): #9-Aug
    print('Option Changed  - ' , value)
    #opted='' #Means What user answer
    
#8-Aug-2023 Event Handler for Questions Buttons
def questionClick(value):
    global index, previousIndex
    previousIndex=index
    saveAnswer(previousIndex) # or index - 10-Aug-2023
    index=value #Means value of index is same as Button No pressed
    showQuestion(index)
    changeButtonState(previousIndex, index) #10-Aug
    
#Step VIII: Design UI (as per specification)
img= PhotoImage(file='quiz_background.png')
#8-Aug-2023 Using Lable to display image inplace of Canvas
Label(win,image=img).place(x=width/2,y=height/2, anchor='center')

#Create UI Elements as child of win
lblQuestion=Label(win, text='Question ' + str(qno.get()) +':')
lblQuestion.grid(row=0, column=0)
#on 7-Aug we use Text widget for Question but it is not working
#when state='disabled' on 8-Aug, we replaced it with Label (Readonly)
#txtQuestion=Text(win,width='70' ,height='8' )
txtQuestion=Label(win, width='70', height='8' ,textvariable=question, anchor='w')
txtQuestion.grid(row=0, column=1)
#Anonymous - Without variable name - created and immediately destroyed
Label(win, text='Choose one or Options that you feel correct').grid(row=1,column=0, columnspan=2)
chkOption1 = Checkbutton(win, text = "Option1", variable = option1,  \
                 onvalue = 1, offvalue = 0, height=5,   width = 20, \
                     command=lambda: optionChanged(1))
chkOption1.grid(row=2, column=0)

chkOption2 = Checkbutton(win, text = "Option2", variable = option2,  \
                 onvalue = 1, offvalue = 0, height=5,   width = 20, \
                     command=lambda: optionChanged(2))
chkOption2.grid(row=2, column=1)

chkOption3 = Checkbutton(win, text = "Option3", variable = option3,  \
                 onvalue = 1, offvalue = 0, height=5,   width = 20, \
                     command=lambda: optionChanged(3))
chkOption3.grid(row=3, column=0)

chkOption4 = Checkbutton(win, text = "Option4", variable = option4,  \
                 onvalue = 1, offvalue = 0, height=5,   width = 20, \
                     command=lambda: optionChanged(4))
chkOption4.grid(row=3, column=1 )
#Concept of Frame - Which consist one or more child components
frame1=LabelFrame(win, text='Navigation')
#Making buttons with frame1 as parent
btnPrevious=Button(frame1,text='Previous', width='10', state='disabled', command=lambda: navigationClick('P'))
btnPrevious.grid(row=0, column=0 ,padx=10 ,pady=10)
btnNext=Button(frame1,text='Next', width='10', command=lambda: navigationClick('N'))
btnNext.grid(row=0, column=1,padx=10)

btnFinish=Button(frame1,text='Finish', width='10', state='disabled', command=lambda: navigationClick('F'))
btnFinish.grid(row=0, column=2,padx=10)

frame1.grid(row=4, column=0, columnspan=3)
frame2=LabelFrame(win, text='Jump To Question No')
#9-aug-2023 Dynamically adding Buttons in frame2 and assign to List
for i in range(0, totalQuestions):
    #8-Aug  - Button without variable
    #Button(frame2,text='Q' + str(i+1) , command=lambda x=i: questionClick(x))
    #9-Aug - Assigning Button to List of Buttons
    btn[i]=Button(frame2,text='Q' + str(i+1) , command=lambda x=i: questionClick(x))
    btn[i].pack(side='left')
frame2.grid(row=5, column=0, columnspan=3)
#8-aug-2023 After UI Completes Load Questions into Memory
loadQuestions() 
#Step IX: start mainloop

win.mainloop()