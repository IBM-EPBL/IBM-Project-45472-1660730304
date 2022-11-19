from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
import os

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator #Authenticate our Model 
from playsound import playsound

# Creds Text to Speech
apikey = 'qoaM1vFcc9Vj7lbKKsZr97SnsPcYfb9ukR41BuEh90OZ'
url = 'https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/8f6bfb66-68b2-4194-bb43-f8567c8b81d3'


#setup service
authenticator = IAMAuthenticator(apikey)
#Create our service
tts = TextToSpeechV1(authenticator=authenticator)
#set the IBM service url
tts.set_service_url(url) 

import ibm_db
try:
  conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cnw63680;PWD=xjQe006RR0Btl5RL",'','')
  print("Successfully connected with db2")
except:
  print("Sorry.. Unable to connect : ", ibm_db.conn_errormsg())

app = Flask(__name__)


# Home page open aagum
@app.route('/')
def home():
  return render_template('home.html')


  
# register oda submit action
@app.route('/register',methods = ['POST', 'GET'])
def register():
  if request.method == 'POST':
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']
    
    
    sql = "SELECT * FROM user WHERE email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
      return render_template('home.html', msg="You are already a member, please login using your details")
    else:
      if(len(password) < 6):
        return render_template('home.html', msg="Password should have more than 6 characters!!")
      else:
        insert_sql = "INSERT INTO user VALUES (?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, fname)
        ibm_db.bind_param(prep_stmt, 2, lname)
        ibm_db.bind_param(prep_stmt, 3, email)
        ibm_db.bind_param(prep_stmt, 4, password)
        ibm_db.execute(prep_stmt)
        return render_template('home.html', msg="Student Data saved successfuly..")

  
 

@app.route("/login", methods=["POST"])
def login():
  print("--------------------------")
  print("Inside login entrance")
  email = request.form.get("email")
  password = request.form.get("password")
  sql = "SELECT * FROM user WHERE email = ?" 
  stmt = ibm_db.prepare(conn, sql)
  ibm_db.bind_param(stmt, 1, email)
  ibm_db.execute(stmt)
  account = ibm_db.fetch_assoc(stmt)
  if not account:
    return render_template('home.html', msg="You are not yet registered, please sign up using your details")
  else:
    print("+====================================+")
    print(account)
    print("+====================================+")
    print("Inside login")
    if(password == account['PASSWORD']):
      email = account['EMAIL']
      name = account['FNAME']
      lname = account['LNAME']
      output = " "+str(name)+" "+str(lname)
      print("Going to redirect to dashboard")
      return render_template('input.html',text=output)
    else:
     return render_template('home.html', msg="Please enter the correct password")
     
@app.route('/dashboard')
def dashboard():
  return render_template('asl.html')


@app.route('/getdata',methods=['post'])
def data():
    os.system('python asl.py')
    return render_template('input.html')
@app.route('/getdata2',methods=['post'])
def data2():
    os.system('python object.py')
    return render_template('input.html')
@app.route('/getdata3',methods=['post'])
def data3():
    os.system('python s2txt.py')
    h = open('mod.txt','r')
    text = h.readlines()
    text = ''.join(str(line) for line in text)
    return render_template('stxt.html',result=text)
@app.route('/getdata4',methods=['post'])
def data4():
  text = request.form['speech']
  if request.method == 'POST':
    f = open("mode.txt", 'w')
    f.write(str(text))
    f.close
    with open('mode.txt', 'r') as f:
        text = f.readlines()
        text = ''.join(str(line) for line in text)
    with open('./winston.mp3', 'wb') as audio_file:
        res = tts.synthesize(text, accept='audio/mp3', voice='en-US_EmmaExpressive').get_result() #selecting the audio format and voice
        audio_file.write(res.content) #writing the contents from text file to a audio file
            
    playsound('winston.mp3')
    return render_template('txts.html')
  
@app.route('/asl',methods=['post'])
def asl():
    return render_template('asl.html')
@app.route('/object',methods=['post'])
def object():
    return render_template('object.html')
@app.route('/speech',methods=['post'])
def speech():
    return render_template('stxt.html')
@app.route('/aloud',methods=['post'])
def aloud():
    return render_template('txts.html')
@app.route('/about',methods=['post'])
def about():
    return render_template('about.html')
  
@app.route('/svr',methods=['post'])
def svr():
    return redirect("https://www.linkedin.com/in/siva-vimel-rajhen-05ab80194/")
@app.route('/ss',methods=['post'])
def ss():
    return redirect("https://www.linkedin.com/in/subiksha-sathiasai-9b3600195/")
@app.route('/ps',methods=['post'])
def ps():
    return redirect("https://www.linkedin.com/in/priyasha-s-23ba6121b/")
@app.route('/pks',methods=['post'])
def pks():
    return redirect("https://www.linkedin.com/in/praveen-kumar-2a8021218/")
@app.route('/github',methods=['post'])
def github():
    return redirect("https://github.com/IBM-EPBL/IBM-Project-45472-1660730304")


if __name__ == '__main__':
    app.run()

