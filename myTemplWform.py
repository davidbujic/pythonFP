from flask import Flask, render_template, request, flash,redirect, url_for
from forms import ContactForm, DateTimeForm, CommandForm, SubmitForm, PaperMoveForm
import subprocess
from subprocess import call
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
from commands import cmd_Get_Date_Time, cmd_Get_PIB, cmd_Paper_Move, cmd_Get_Status
import datetime
import os
#from app import app
app = Flask(__name__)
app.secret_key = 'development key'

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Ljubisa'}
    posts = [
        {
            'author': {'username': 'Dusan'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Oliver'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',title='Home',  user=user, posts=posts)


@app.route('/g1_cmd')
def g1_cmd():
    cmd_name="getDateTime"
    cmd_xvalue="x67"
    var_status="x80 x85 x80 xBA x80 x8A"
    full_msg="x01 x23 x20 x04 data...x05 BCC x03"
    return render_template('g1CMD.html' , varStatus=var_status, cmdName=cmd_name, cmdXvalue=cmd_xvalue, fullMsg=full_msg)

@app.route('/g11_cmd', methods = ['GET', 'POST'])
def g11_cmd():

    form = SubmitForm()
   
    if request.method == 'POST':
        url = 'https://fp550irvas.localtunnel.me/g11_cmd'
        response = requests.get(url)
        resp_dict = json.loads(response.text)
        if type(resp_dict) is str:
            data_str = resp_dict
        else:
            data_str =  ""
            for m in resp_dict['recv_pck_Data']:
                data_str = data_str + chr(m)
        print data_str
        return render_template('g11success.html', output = data_str)
    elif request.method == 'GET':
        return render_template('g11CMD.html', form = form)

@app.route('/g12_cmd', methods = ['GET', 'POST'])
def g12_cmd():

    form = SubmitForm()
   
    if request.method == 'POST':
        url = 'https://f550irvas.localtunnel.me/g12_cmd'
        response = requests.get(url)
        resp_dict = json.loads(response.text)
        if type(resp_dict) is str:
            data_str = resp_dict
        else:
            data_str = ""
            for m in resp_dict['recv_pck_Data']:
                data_str = data_str + chr(m)
        print data_str
        return render_template('g12success.html', output = data_str)
        
    elif request.method == 'GET':
        return render_template('g12CMD.html', form = form)

@app.route('/g13_cmd', methods = ['GET', 'POST'])
def g13_cmd():

    form = PaperMoveForm()
   
    if request.method == 'POST':
        url = 'https://fp550irvas.localtunnel.me/g13_cmd' + form.lines.data
        response = requests.get(url)
        resp_dict = json.loads(response.text)
        if type(resp_dict) is str:
            data_str = resp_dict
        else:
            data_str = ""
            for m in resp_dict['recv_pck_Data']:
                data_str = data_str + chr(m)
        print data_str
        return render_template('g13success.html', output = data_str)
        
    elif request.method == 'GET':
        return render_template('g13CMD.html', form = form)

@app.route('/g14_cmd', methods = ['GET', 'POST'])
def g14_cmd():

    form = SubmitForm()
   
    if request.method == 'POST':
        output = cmd_Get_Status()
        print output
        bytelist = [bin(int(output[0].encode("hex"),16)),bin(int(output[1].encode("hex"),16)),bin(int(output[2].encode("hex"),16)),bin(int(output[3].encode("hex"),16)),bin(int(output[4].encode("hex"),16)),bin(int(output[5].encode("hex"),16))]
        status_hex = "x"+output[0].encode("hex")+"x"+output[1].encode("hex")+"x"+output[2].encode("hex")+"x"+output[3].encode("hex")+"x"+output[4].encode("hex")+"x"+output[5].encode("hex")
        n=0
        for byte in bytelist:
            bytelist[n] = byte[2:]
            x=8-len(byte)
            for i in range(x-1):
                bytelist[n] = "0"+bytelist[n]
            n+=1
        print bytelist
        bitlist = [[0]*6 for i in range(8)]
        x=0
        y=0
        for byte in bytelist:
            for char in byte:
                #print x,y
                bitlist[x][y]=char
                x+=1
            y+=1
            x=0
        print bitlist
        return render_template('g14success.html', status = bitlist, statusHex = status_hex)

        
    elif request.method == 'GET':
        return render_template('g14CMD.html', form = form)   

@app.route('/g16_cmd', methods['GET','POST'])
def g16_cmd():
    form = SubmitForm()
    
    if request.method == 'POST':
        url = 'https://fp550irvas.localtunnel.me/g16_cmd'
        response = requests.get(url)
        resp_dict = json.loads(response.text)
        if type(resp_dict) is str:
            data_str = resp_dict
        else:
            data_str = ""
            for m in resp_dict['recv_pck_Data']:
                data_str = data_str + chr(m)
        print data_str
        return render_template('g16success.html', output = data_str)
    elif request.method == 'GET':
        return render_template('g16CMD.html', form = form)
    
@app.route('/g17_cmd', methods = ['GET','POST'])
def g17_cmd():
    form = SubmitForm()
    
    if request.method == 'POST':
        url = 'https://f550irvas.localtunnel.me/g17_cmd'
        response = requests.get(url)
        resp_dict = json.loads(response.text)
        if type(resp_dict) is str:
            data_str = resp_dict
        else:
            data_str = ""
            for m in resp_dict['rcv_pck_Data']:
                data_str = data_str + chr(m)
        print data_str
        return render_template('g17success.html', output = data_str)
    elif request.method == 'GET':
        return render_template('g17CMD.html', form = form)

@app.route('/g18_cmd', methods = ['GET','POST'])
def g18_cmd():
    form = SubmitForm()
    
    if request.method == 'POST':
        url = 'https://f550irvas.localtunnel.me/g18_cmd'
        response = requests.get(url)
        resp_dict = json.loads(response.text)
        if type(resp_dict) is str:
            data_str = resp_dict
        else:
            data_str = ""
            for m in resp_dict['recv_pck_Data']:
                data_str = data_str + chr(m)
        print data_str
        return render_template('g18success.html', output = data_str)
    elif request.method == 'GET':
        return render_template('g18CMD.html', form = form)
        
@app.route('/g19_cmd', methods = ['GET', 'POST'])
def g19_cmd():
    global ts1
    form = SubmitForm()
    st= datetime.datetime.now().strftime("%Y-%m-%d--%H-%M") # exmp: 2018-07-01--16-57
    ts= str(st) #.split('.')[0] #eliminise miliseconds
    ts11="/home/pi/Public/WWWpy/static/images/"+ts+".jpg"
    ts1="images/"+ts+".jpg"
    print ts1
    filelist = [] # filelist[1]=

    for root, dirs, files in os.walk("./static/images", topdown=False):
        for name in sorted(files,reverse=True):
            filelist.append(name)
            print name
    
    if request.method == 'POST':
        call(["fswebcam", "-d", "/dev/video0", "-r", "1280x720","--top-banner", ts11])
        return render_template('g19success.html',ts1=ts1,filelist=filelist)

        
    elif request.method == 'GET':
        return render_template('g19CMD.html', form = form)

@app.route('/g19history')
def g19_history():
    filelist = []
    for root, dirs, files in os.walk("./static/images", topdown=False):
        for name in sorted(files,reverse=True):
            filelist.append(name)
    ts1 = "images/"+filelist[0]
    return render_template('g15success.html',ts1=ts1,filelist=filelist)

@app.route('/g19history/<image>')
def g19_history_img(image):
    filelist = []
    for root, dirs, files in os.walk("./static/images", topdown=False):
        for name in sorted(files,reverse=True):
            filelist.append(name)
    ts1 = "images/"+image
    return render_template('g15success.html',ts1=ts1,filelist=filelist)

@app.route('/g2_cmd')
def g2_cmd():

    return render_template('g2CMD.html')

@app.route('/g21_cmd', methods = ['GET', 'POST'])
def g21_cmd():

    form = DateTimeForm()
   
    if request.method == 'POST':
        print form.now
        return render_template('g21success.html', form=form)

        
    elif request.method == 'GET':
        return render_template('g21CMD.html', form = form)

@app.route('/g22_cmd', methods = ['GET', 'POST'])
def g22_cmd():

    form = CommandForm()

    Session = sessionmaker(bind=engine)
    session = Session()
   
    if request.method == 'POST':
        if form.parametar.data.strip()=="":
            proc = subprocess.Popen("lsusb", stdout=subprocess.PIPE)
        else:
            proc = subprocess.Popen(["lsusb",form.parametar.data], stdout=subprocess.PIPE)
        grep = subprocess.Popen(["grep",form.filterfield.data], stdin=proc.stdout, stdout=subprocess.PIPE)
        usb_status = []
        for line in grep.stdout.readlines():
            #print line
            output = Output(line)
            session.add(output)
            usb_status.append(line)
        session.commit()
        #outputs = session.query(Output).order_by(Output.id).total #paginate(1,5,False)
        #dboutputs=Output.query.paginate()
        #print dboutputs.page
        return render_template('g22success.html', usbStatus=usb_status, form=form)

        
    elif request.method == 'GET':
        return render_template('g22CMD.html', form = form)

@app.route('/g23_cmd', methods = ['GET', 'POST'])
def g23_cmd():

    form = CommandForm()
   
    if request.method == 'POST':
        if form.parametar.data.strip()=="":
            proc = subprocess.Popen(["sudo","dmesg"], stdout=subprocess.PIPE)
        else:
            proc = subprocess.Popen(["sudo","dmesg",form.parametar.data], stdout=subprocess.PIPE)
        filter=form.filterfield.data
        print filter
        grep = subprocess.Popen(["grep",form.filterfield.data], stdin=proc.stdout, stdout=subprocess.PIPE)
        serial_status = []
        # pisalo dole <proc.stdout> DV
        for line in grep.stdout.readlines():
            #print line
            serial_status.append(line)
        return render_template('g23success.html', serialStatus=serial_status, filter=filter)

        
    elif request.method == 'GET':
        return render_template('g23CMD.html', form = form)

@app.route('/g3_cmd')
def g3_cmd():

    return render_template('g3CMD.html' )

# rad sa formamam u FLASK-u : contact form

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
   form = ContactForm()
   
   if request.method == 'POST':
      if form.validate() == False:
         print "!! All fields are required!!"
         flash('All fields are required.')

         return render_template('contact.html', form = form)
      else:
         print form.name.data
         print form.language.data
         return render_template('success1.html', form=form)

        
   elif request.method == 'GET':
         return render_template('contact.html', form = form)


app.run(host='0.0.0.0', port= 8090)
engine = create_engine('sqlite:///output.db', echo=True)
