import os
from dbconn import connection
from wtforms import Form, TextField, validators, FileField
from flask import Flask, render_template, request, url_for, flash, redirect, session, send_file
from MySQLdb import escape_string as thwart
import gc
from werkzeug import secure_filename
UPLOAD_FOLDER = 'mysite/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug=True

app.secret_key = 'ENTER SECURITY KEY HERE'
srcho = False
sin = ""
sis = ""
lt="None"

cbool = False
class EditForm(Form):
    title = TextField('Title',[validators.Length(min=1,max=50),validators.Required()])
    ptext = TextField('Post',[validators.Length(min=1,max=10000),validators.Required()])
@app.route('/editpost/', methods=["GET","POST"])
def editpost():
    try:
        postc="2"
        sin="None"
        sis="None"
        formp= PostForm(request.form)
        forme= EditForm(request.form)
        formr= RegForm(request.form)
        c, conn = connection()
        c.execute("SELECT * FROM RegLog WHERE admno=%s",(session['admno'],))
        temp1 = [item9[6] for item9 in c.fetchall()]
        postc = str(temp1[0])
        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        c, conn= connection()
        c.execute("SELECT * FROM RegLog WHERE admno=%s",(session['admno'],))
        picc = [item1[5] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        if request.method=="POST" and forme.validate():
            title= forme.title.data
            ptext= forme.ptext.data
            c, conn = connection()
            c.execute("UPDATE Posts SET ptitle=%s,ptext=%s WHERE admno=%s",(thwart(title),thwart(ptext),session['admno']))
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
            return redirect(url_for('posts'))
        else:

            if session['logged_in']==True:
                c, conn = connection()
                c.execute("SELECT * FROM RegLog WHERE admno=%s",(session['admno'],))
                temp1 = [item1[6] for item1 in c.fetchall()]
                postc = str(temp1[0])
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
            if session['logged_in']==True:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE admno=%s",(session['admno'],))
                temp1 = [item2[0] for item2 in c.fetchall()]
                ptitlee = str(temp1[0])
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
            if session['logged_in']==True:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE admno=%s",(session['admno'],))
                temp2 = [item3[4] for item3 in c.fetchall()]
                ptexte = str(temp2[0])
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
            return render_template("editpost.html",sin=sin,sis=sis,formr=formr,picc=picc[0],formp=formp,postc=postc,forme=forme,ptexte=ptexte,ptitlee=ptitlee)
    except Exception as e:
        return (str(e))

@app.route('/getimg')
def getimg():
    filename = request.args.get('admno')+'.jpg'
    return send_file(filename)

logerr = False
@app.route('/', methods=["GET","POST"])
@app.route('/home/', methods=["GET","POST"])
def index():
    try:
        formr= RegForm(request.form)
        if session['logged_in']==True and request.method!="POST":

            c, conn= connection()
            c.execute("SELECT * FROM RegLog WHERE admno=%s",(session['admno'],))
            picc = [item1[5] for item1 in c.fetchall()]
            return render_template("index.html",picc=picc[0],formr=formr,logerr=logerr)
        if request.method=="POST" and session['logged_in']==True:
            file = request.files['file']
            filename = secure_filename(session['admno'])+'.jpg'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            c, conn = connection()
            c.execute("UPDATE RegLog SET picc=1 WHERE admno=%s",(session['admno'],))
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
            return redirect(url_for('index'))
        if session['logged_in']!=True and request.method!="POST":
            return render_template("index.html",formr=formr,logerr=logerr)
    except Exception as e:
        return render_template("index.html",formr=formr,logerr=logerr)

@app.route('/checkdb/')
def dbconn():
    try:
        c, conn = connection()
        return "connection ok!"

    except Exception as e:
        return (str(e))

class PostForm(Form):
    title = TextField('Title',[validators.Length(min=1,max=50),validators.Required()])
    ptext = TextField('Post',[validators.Length(min=1,max=10000),validators.Required()])

class RegForm(Form):
    name = TextField('Name',[validators.Length(min=1,max=50), validators.Required()])
    classs = TextField('Class',[validators.Length(min=1,max=10), validators.Required()])
    sec = TextField('Section',[validators.Length(min=1,max=10), validators.Required()])
    admno = TextField('Admission Number',[validators.Length(min=1,max=10), validators.Required()])

@app.route('/register/', methods=["GET","POST"])
def register():
    try:
        err = False
        formp= PostForm(request.form)
        formr= RegForm(request.form)
        if request.method=="POST" and formr.validate()!=True:
            err = True
            return render_template("index.html",err=err,formr=formr)
        if request.method=="POST" and formr.validate():
            name= formr.name.data
            classs= formr.classs.data
            sec= formr.sec.data
            admno= formr.admno.data
            name = name.lower()
            name = name.title()
            sec = sec.lower()
            sec = sec.title()
            c, conn = connection()
            x = c.execute("SELECT * FROM RegLog WHERE name = (%s) AND classs = (%s) AND sec = (%s) AND admno = (%s) ",
                          (thwart(name),thwart(classs),thwart(sec),thwart(admno)))
            if int(x) > 0:
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['name'] = name
                session['admno'] = admno
                session['sec'] = sec
                session['classs'] = classs
                return redirect(url_for('index'))
            else:
                return redirect(url_for('index',logerr=True))
        else:
            return render_template("index.html", formr=formr,err=err)

    except Exception as e:
        return (str(e))

@app.route('/posts/' , methods=["GET","POST"])
def posts():
    try:
        global sin
        global sis
        global srcho
        global lt
        global cbool
        global ts
        global te
        postc="2"
        formp= PostForm(request.form)
        formr= RegForm(request.form)
        c, conn= connection()
        c.execute("SELECT * FROM RegLog WHERE admno=%s",(session['admno'],))
        picc = [item1[5] for item1 in c.fetchall()]
        factor = request.args.get('page',default=1,type=int)
        l = factor * 5
        udcs = "None"
        if lt!="sec":
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY upvotes DESC")
            ptitles = [item1[0] for item1 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY upvotes DESC")
            postids= [item2[2] for item2 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY upvotes DESC")
            upvotess = [item3[3] for item3 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY upvotes DESC")
            ptexts = [item4[4] for item4 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY upvotes DESC")
            names = [item5[5] for item5 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY upvotes DESC")
            classss = [item6[6] for item6 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY upvotes DESC")
            secs = [item7[7] for item7 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY upvotes DESC")
            admnos = [item8[8] for item8 in c.fetchall()]
        if lt=="sec":
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY sec ASC")
            ptitles = [item1[0] for item1 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY sec ASC")
            postids= [item2[2] for item2 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY sec ASC")
            upvotess = [item3[3] for item3 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY sec ASC")
            ptexts = [item4[4] for item4 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY sec ASC")
            names = [item5[5] for item5 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY sec ASC")
            classss = [item6[6] for item6 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY sec ASC")
            secs = [item7[7] for item7 in c.fetchall()]
            c, conn = connection()
            c.execute("SELECT * FROM Posts ORDER BY sec ASC")
            admnos = [item8[8] for item8 in c.fetchall()]
        if srcho==True:
            srcho=False
            if sin!="None" and sis=="None" and lt=="sec" and cbool==True:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY sec ASC",("%"+sin+"%",))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY sec ASC",("%"+sin+"%",))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY sec ASC",("%"+sin+"%",))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY sec ASC",("%"+sin+"%",))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY sec ASC",("%"+sin+"%",))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY sec ASC",("%"+sin+"%",))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY sec ASC",("%"+sin+"%",))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY sec ASC",("%"+sin+"%",))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin!="None" and sis=="None" and lt=="up" and cbool==True:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY upvotes DESC",("%"+sin+"%",))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY upvotes DESC",("%"+sin+"%",))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY upvotes DESC",("%"+sin+"%",))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY upvotes DESC",("%"+sin+"%",))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY upvotes DESC",("%"+sin+"%",))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY upvotes DESC",("%"+sin+"%",))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY upvotes DESC",("%"+sin+"%",))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s ORDER BY upvotes DESC",("%"+sin+"%",))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin!="None" and sis=="None" and lt=="None" and cbool==True:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s",("%"+sin+"%",))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s",("%"+sin+"%",))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s",("%"+sin+"%",))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s",("%"+sin+"%",))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s",("%"+sin+"%",))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s",("%"+sin+"%",))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s",("%"+sin+"%",))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s",("%"+sin+"%",))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin!="None" and sis=="None" and lt=="up" and cbool==False:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY upvotes DESC",(sin,))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY upvotes DESC",(sin,))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY upvotes DESC",(sin,))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY upvotes DESC",(sin,))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY upvotes DESC",(sin,))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY upvotes DESC",(sin,))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY upvotes DESC",(sin,))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY upvotes DESC",(sin,))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin!="None" and sis=="None" and lt=="sec" and cbool==False:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY sec ASC",(sin,))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY sec ASC",(sin,))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY sec ASC",(sin,))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY sec ASC",(sin,))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY sec ASC",(sin,))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY sec ASC",(sin,))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY sec ASC",(sin,))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s ORDER BY sec ASC",(sin,))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin!="None" and sis=="None" and lt=="None" and cbool==False:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s",(sin,))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s",(sin,))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s",(sin,))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s",(sin,))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s",(sin,))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s",(sin,))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s",(sin,))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s",(sin,))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin!="None" and sis!="None" and lt=="None" and cbool==True:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s",("%"+sin+"%",sis,))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s",("%"+sin+"%",sis,))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s",("%"+sin+"%",sis,))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s",("%"+sin+"%",sis,))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s",("%"+sin+"%",sis,))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s",("%"+sin+"%",sis,))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s",("%"+sin+"%",sis,))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s",("%"+sin+"%",sis,))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin!="None" and sis!="None" and lt=="sec" and cbool==True:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY sec ASC",("%"+sin+"%",sis,))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY sec ASC",("%"+sin+"%",sis,))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY sec ASC",("%"+sin+"%",sis,))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY sec ASC",("%"+sin+"%",sis,))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY sec ASC",("%"+sin+"%",sis,))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY sec ASC",("%"+sin+"%",sis,))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY sec ASC",("%"+sin+"%",sis,))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY sec ASC",("%"+sin+"%",sis,))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin!="None" and sis!="None" and lt=="up" and cbool==True:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY upvotes DESC",("%"+sin+"%",sis,))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY upvotes DESC",("%"+sin+"%",sis,))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY upvotes DESC",("%"+sin+"%",sis,))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY upvotes DESC",("%"+sin+"%",sis,))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY upvotes DESC",("%"+sin+"%",sis,))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY upvotes DESC",("%"+sin+"%",sis,))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY upvotes DESC",("%"+sin+"%",sis,))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name LIKE %s AND sec=%s ORDER BY upvotes DESC",("%"+sin+"%",sis,))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin!="None" and sis!="None" and lt=="up" and cbool==False:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY upvotes DESC",(sin,sis,))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY upvotes DESC",(sin,sis,))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY upvotes DESC",(sin,sis,))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY upvotes DESC",(sin,sis,))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY upvotes DESC",(sin,sis,))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY upvotes DESC",(sin,sis,))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY upvotes DESC",(sin,sis,))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY upvotes DESC",(sin,sis,))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin!="None" and sis!="None" and lt=="sec" and cbool==False:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY sec ASC",(sin,sis,))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY sec ASC",(sin,sis,))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY sec ASC",(sin,sis,))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY sec ASC",(sin,sis,))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY sec ASC",(sin,sis,))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY sec ASC",(sin,sis,))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY sec ASC",(sin,sis,))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s ORDER BY sec ASC",(sin,sis,))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin!="None" and sis!="None" and lt=="None" and cbool==False:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s",(sin,sis,))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s",(sin,sis,))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s",(sin,sis,))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s",(sin,sis,))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s",(sin,sis,))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s",(sin,sis,))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s",(sin,sis,))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE name=%s AND sec=%s",(sin,sis,))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin=="None" and sis!="None" and lt=="up" and cbool==False:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY upvotes DESC",(sis,))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY upvotes DESC",(sis,))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY upvotes DESC",(sis,))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY upvotes DESC",(sis,))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY upvotes DESC",(sis,))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY upvotes DESC",(sis,))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY upvotes DESC",(sis,))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY upvotes DESC",(sis,))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin=="None" and sis!="None" and lt=="sec" and cbool==False:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY sec ASC",(sis,))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY sec ASC",(sis,))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY sec ASC",(sis,))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY sec ASC",(sis,))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY sec ASC",(sis,))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY sec ASC",(sis,))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY sec ASC",(sis,))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s ORDER BY sec ASC",(sis,))
                admnos = [item8[8] for item8 in c.fetchall()]
            if sin=="None" and sis!="None" and lt=="None" and cbool==False:
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s",(sis,))
                ptitles = [item1[0] for item1 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s",(sis,))
                postids= [item2[2] for item2 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s",(sis,))
                upvotess = [item3[3] for item3 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s",(sis,))
                ptexts = [item4[4] for item4 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s",(sis,))
                names = [item5[5] for item5 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s",(sis,))
                classss = [item6[6] for item6 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s",(sis,))
                secs = [item7[7] for item7 in c.fetchall()]
                c, conn = connection()
                c.execute("SELECT * FROM Posts WHERE sec=%s",(sis,))
                admnos = [item8[8] for item8 in c.fetchall()]
        if session['logged_in']==True:
            c, conn = connection()
            c.execute("SELECT * FROM RegLog WHERE admno=%s",(session['admno'],))
            temp1 = [item9[6] for item9 in c.fetchall()]
            postc = str(temp1[0])
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
            c, conn = connection()
            c.execute("SELECT * FROM RegLog WHERE admno=%s",(session['admno'],))
            udcs = [item10[7] for item10 in c.fetchall()]
            udcs = udcs[0]
            udcs = udcs.split(',')
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
        if request.method=="POST" and formp.validate():
            title=formp.title.data
            ptext=formp.ptext.data
            l = str("startingvalue,secondstartingvalue")
            if session['logged_in']==True:
                c, conn = connection()
                c.execute("INSERT INTO Posts (ptitle, ptext, name, sec, classs, admno, upvotesid) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                          (title, ptext, session['name'], session['sec'],session['classs'],session['admno'],l))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                c, conn = connection()
                c.execute("UPDATE RegLog SET postc='1' WHERE admno=%s",(session['admno'],))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                return redirect(url_for('posts'))
        else:
            return render_template("posts.html",picc=picc[0],sin=sin,sis=sis,udcs=udcs,formr=formr,formp=formp,ptitles=ptitles,upvotess=upvotess,l=l,factor=factor,postc=postc,ptexts=ptexts,names=names,classss=classss,secs=secs,postids=postids,admnos=admnos)
    except Exception as e:
        return render_template("posts.html",picc=picc[0],sin=sin,sis=sis,udcs=udcs,formr=formr,formp=formp,ptitles=ptitles,upvotess=upvotess,l=l,factor=factor,postc=postc,ptexts=ptexts,names=names,classss=classss,secs=secs,postids=postids,admnos=admnos)

@app.route('/logout/')
def logout():
    session['logged_in'] = False
    session['name']= None
    session['admno']=None
    return redirect(url_for('index'))
@app.route('/error/')
def error():
    return render_template("error.html")
@app.route('/loginopr/')
def loginopr():
    formr= RegForm(request.form)
    return render_template("loginopr.html",formr=formr)
@app.route('/search/', methods=["GET","POST"])
def search():
    try:
        global sin
        global sis
        global srcho
        global lt
        global cbool
        srcho = True
        sin = request.args.get('sin',type=str)
        sis = request.args.get('sis',type=str)
        lt = request.args.get('lt',type=str)
        sin = sin.strip()
        sis = sis.strip()
        lt = lt.strip()
        sin = sin.lower()
        sin = sin.title()
        sis = sis.lower()
        sis = sis.title()
        temp = len(sin.split())
        if temp==1 and sin!="None":
            cbool=True
        else:
            cbool=False
        return redirect(url_for('posts'))
    except Exception as e:
        return str(e)

@app.route('/upvote/')
def upvote():
    try:
        if session['logged_in']==True:
            tbu =request.args.get('postid',None,type=str)
            pagen = request.args.get('pagen',type=str)
            backl = "/posts?page="+pagen
            c, conn = connection()
            c.execute("SELECT * FROM Posts WHERE postid=%s",(tbu,))
            upvotesid = [item1[9] for item1 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
            c, conn = connection()
            c.execute("SELECT * FROM RegLog WHERE admno=%s",(session['admno'],))
            udc = [item2[7] for item2 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
            temp = str(upvotesid[0])
            temp2 = str(udc[0])
            ul = temp.split(',')
            if session['admno'] in ul:
                sl = temp.replace((","+session['admno']),"")
                c, conn = connection()
                c.execute("UPDATE Posts SET upvotes=upvotes-1,upvotesid=%s WHERE postid=%s",(sl,tbu,))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                sl2 = temp2.replace((","+tbu),"")
                c, conn = connection()
                c.execute("UPDATE RegLog SET udc=%s WHERE admno=%s",(sl2,session['admno'],))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                return redirect(backl)
            else:
                sl  = temp+","+session['admno']
                c, conn = connection()
                c.execute("UPDATE Posts SET upvotes=upvotes+1,upvotesid=%s WHERE postid=%s",(sl,tbu,))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                sl2  = temp2+","+tbu
                c, conn = connection()
                c.execute("UPDATE RegLog SET udc=%s WHERE admno=%s",(sl2,session['admno'],))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                return redirect(backl)
        else:
            return redirect(url_for('index'))
    except Exception as e:
        return (str(e))
