from flask import Flask,render_template,request,redirect,session,flash,redirect
import mysql.connector
import os
import tweepy
import api
import ml
app= Flask(__name__)
app.secret_key=os.urandom(24)
 
conn=mysql.connector.connect(host="remotemysql.com",user="9YwiYaINDg",password="WB2u9rVHb5",database="9YwiYaINDg")
cursor=conn.cursor()



@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('home.html')



@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')
   

@app.route("/loginvalidation", methods=['POST'])
def loginval():
    global email
    global password
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users=cursor.fetchall()
  
    if len(users)>0:
        session['user_id']=users[0][0]
        flash('account logged in')
        return render_template('home.html',displayname=displayname)
        
    else:
        return redirect('/login')


    


@app.route('/add_user',methods=['POST'])
def add_user():
    global name    
    global phone_number
    global gender
    global twitter_id
    name=request.form.get('username')
    email=request.form.get('useremail')
    password=request.form.get('userpassword')
    phone_number=request.form.get('userphone')
    gender=request.form.get('gender')
    twitter_id=request.form.get('twitter_id')
    cursor.execute("""INSERT INTO `users` (`user_id`,`name`,`email`,`password`,`phone_number`,`gender`,`twitter_id`) VALUES (NULL,'{}','{}','{}','{}','{}','{}')""".format(name,email,password,phone_number,gender,twitter_id))
    conn.commit()

    cursor.execute("""SELECT * FROM `users`  WHERE `email` LIKE '{}' AND `password` LIKE '{}' """.format(email,password))
    user=cursor.fetchone()
    twitter_id = user[6]
    a=api.twitter_api(twitter_id)
    #print(a)
    res=ml.predict(a)
    per_map={0:'ENFJ', 1:'ENFP', 2:'ENTJ', 3:'ENTP', 4:'ESFJ', 5:'ESFP', 6:'ESTJ', 7:'ESTP', 8:'INFJ', 9:'INFP', 10:'INTJ', 11:'INTP', 12:'ISFJ', 13:'ISFP', 14:'ISTJ', 15:'ISTP'}

    personality_index =per_map[res]
    print(personality_index)
    cursor.execute("""SELECT * FROM `users`  WHERE `email` LIKE '{}' AND `password` LIKE '{}' """.format(email,password))
    user=cursor.fetchone()
    cursor.execute("""UPDATE `users` set personality_index='{}' WHERE email='{}' """.format(personality_index,email))
    conn.commit()
    #flash('account created')
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/home', methods=['POST'])
def form_data():
    global result
    if request.method=="POST":
        req=request.form
        movie=req['movie']
        music=req['music']
        sport=req['sport']
        choice=req['choice']
        result=movie+music+sport+choice
        cursor.execute("""SELECT * FROM `users`  WHERE `email` LIKE '{}' AND `password` LIKE '{}' """.format(email,password))
        user=cursor.fetchone()
        cursor.execute("""UPDATE `users` set results='{}' WHERE email='{}' """.format(result,email))
        conn.commit()
        conn.commit()
        return render_template('home.html')


@app.route('/map1')
def map1():
    
    # #latitude and longitude stuff

    # #matching personality
    
    cursor.execute("""SELECT * FROM `users` """)
    records = cursor.fetchall()
    d1= {record[0]: record[7] for record in records}
    print(d)

    # p1="INFP" # personality of user

    # compatibility1={'INTP':'INTJ','ENFP':'INFJ',
    # 'ENFJ':'INFP','ISTJ':'ESFP','ESTP':'ISFJ','ESFJ':'ISFP','ISTP':'ESTJ','INFJ':'ENTP',
    # 'ENTJ':'INTP'
    # }
    
    # compatibility2={'INTJ':'INTP',
    # 'INFJ':'ENFP','INFP':'ENFJ',
    # 'ESFP':'ISTJ','ISFJ':'ESTP',
    # 'ISFP':'ESFJ',"ESTJ":"ISTP",
    # 'ENTP':'INFJ','INTP':'ENTJ'
    # }


    # # matching answers
    cursor.execute("""SELECT * FROM `users` """)
    records = cursor.fetchall()
    d2= {record[0]: record[8] for record in records}
    print(d)


    # st1="abcd"








    return render_template('map1.html')

@app.route('/map2')
def map2():
    return render_template('map2.html')






if __name__ == '__main__':
    app.run(debug=True)
