# =============================================================================
# importing the necessary libraries
# =============================================================================
from flask import Flask, render_template, url_for, redirect, request,Request, Response, session
from flask_login import login_user, LoginManager, login_required,logout_user, current_user
from flask_bcrypt import Bcrypt
from database import db, db_init
from tables import User, StatusUpload, activityStack
from forms import LoginForm, RegisterForm, updateStatus, userActivity
from werkzeug.utils import secure_filename
from flask_session import Session
# =============================================================================


# =============================================================================
# initalising the app, session and database
# =============================================================================
app = Flask(__name__)
bcrypt=Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "NobodyCanReadThis"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # max-limit 4MB
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
sess = Session()
sess.init_app(app)
db_init(app)
# =============================================================================


# =============================================================================
# initalising login Manager
# =============================================================================
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# =============================================================================

# =============================================================================
# function for creating the five user to display
# =============================================================================
def fishingFive(userAct, fiveUserList ):
         userAct.reverse()
         temp=userAct[:5]
         for i in temp:
                  user = User.query.filter_by(id=i.userid).first()
                  fiveUserList.append(user.username)
         del userAct[:5]
         session['userAct']=userAct
         session['flag']=1
# =============================================================================




# =============================================================================
# home page
# =============================================================================
@app.route('/')
def home():
    return render_template('index.html')

# =============================================================================
# login
# =============================================================================
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data ):
                login_user(user) 
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

# =============================================================================
# sign up
# =============================================================================
@app.route('/signUp', methods=['GET','POST'])
def signUp():
    form = RegisterForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data)
        newUser = User(username=form.username.data, password=hashedPassword)
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signUp.html', form=form)

# =============================================================================
# logout
# =============================================================================
@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    session['value']=None
    session['userAct']=None
    session['flag']=None
    logout_user()
    return redirect(url_for('login'))

# =============================================================================
# user dashboard
# =============================================================================
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    currUser = str(current_user)
    id=int(currUser[currUser.index(" "):len(currUser)-1])
    formStatusUpload = updateStatus()
    formUserActivity = userActivity()
    if session.get('value')==None:
             session['value'] = id
             newAct = activityStack(userid=session.get('value'))
             db.session.add(newAct)
             db.session.commit()
    # print("flag: ", session.get("flag"))
    
    if session.get('flag')==None:  
        #  print("flag: ", session.get("flag"))
         fiveUserList=[]
         if session.get('userAct')==None: 
             userAct= activityStack.query.all()
         else:
              userAct = session.get('userAct')
         fishingFive(userAct, fiveUserList)
    
    if request.method=="POST":
         if formStatusUpload.validate_on_submit():
             pic = formStatusUpload.img.data
             desc = formStatusUpload.desc.data
             mimetype=pic.mimetype
             update= StatusUpload(desc=desc, img=pic.read(), mimetype=mimetype, userid=id)
             db.session.add(update)
             db.session.commit()
             return redirect(url_for('viewStatus'))
         else:
             fiveUserList=[]
             userAct = session.get('userAct')
             fishingFive(userAct,fiveUserList)
             return render_template('dashboard.html', form=formStatusUpload, formUserActivity=formUserActivity, fiveUserList=fiveUserList)
             
    try:
        testTheExistense = fiveUserList
    except:
        fiveUserList=[]
    return render_template('dashboard.html', form=formStatusUpload, formUserActivity=formUserActivity, fiveUserList=fiveUserList)

# =============================================================================
# user status view
# =============================================================================
@app.route('/viewStatus', methods=['GET'])
@login_required
def viewStatus():
    status = StatusUpload.query.filter_by(userid=session.get('value')).all()
    if status==[]:
        return render_template('statusView.html',flag=0)
    else:
        status=status[-1]
        return render_template('statusView.html', desc=status.desc,flag=1)

# =============================================================================
# status image
# =============================================================================
@app.route("/statusImg")
@login_required
def statusImg():
    status = StatusUpload.query.filter_by(userid=session.get('value'))[-1]
    return Response(status.img, mimetype=status.mimetype)




if __name__ == "__main__":
    app.run(debug=True, port=5000)

