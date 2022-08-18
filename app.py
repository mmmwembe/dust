from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from functools import wraps
from flask_pymongo import PyMongo


app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
app.config['MONGO_URI']='mongodb+srv://mmm111:Password123@3megacluster.cnmlv.mongodb.net/db?retryWrites=true&w=majority'
mongo = PyMongo(app) 
db = mongo.db

users_collection = db["users"]
projects_collection = db["projects"]
expenses_collection = db["expenses"]
authorized_users_collection = db["authorized_users_collection"]

from project.models import Project
from expense.models import Expense
# Bootstrap
bootstrap = Bootstrap(app)

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap


# General utility functions

def getKeysTuple(dict):
    list = []
    for key in dict.keys():
        list.append(key)      
    return tuple(list)


def getValuesTuple(dict):
    list = []
    for value in dict.values():
        list.append(value)      
    return tuple(list)

def getValuesTuplefromMongoDbResults(results):

  data =[]
  for result in results:
    values = getValuesTuple(result)
    data.append(values)

  data = tuple(data)

  return data

# Routes
from user import routes
from project import routes

@app.route('/')
def home():
  # return render_template('home.html')
  return render_template('home-user-login.html')

@app.route('/create-user-account/')
def create_user_account():
  # return render_template('home.html')
  return render_template('create-user-account.html')



@app.route('/dashboard/')
@login_required
def dashboard():
  # return render_template('dashboard.html')
  return redirect(url_for("view_dynamic_dashboard"))
  # return render_template('dashboard-v3.html')

@app.route('/add_project_photo/')
@login_required
def add_project_photo():
  return render_template('add-project-photo.html')

@app.route('/dust/')
@login_required
def dust():
    return "DUST MONITORING PROJECT"

@app.route('/smokestack/')
@login_required
def smokestack():
    return "SMOKE STACK PROJECT"

@app.route('/algae/')
@login_required
def algae():
    return "ALGAE"

@app.route('/concentrator/')
@login_required
def concentrator():
    return "CONCENTRATOR PROJECT"

@app.route('/registered-users/')
@login_required
def registered_users():
    return "REGISTERED USERS"

@app.route('/user-profile/')
@login_required
def user_profile():
    return render_template('user-profile.html')


@app.route('/add-project-ignore/')
@login_required
def add_project_ignore():
    # return render_template('add-project.html')
    return render_template('add-project-v2.html')

@app.route('/create-project-ignore', methods=['POST'])
@login_required
def submit_new_project():

  # write project object to  mongodb
  project = Project().createProject()

 
  # project = jsonify(project)
  return redirect(url_for("view_dynamic_dashboard"))
  # return render_template('dashboard-v2.html')
  #return render_template('project-page.html', project = project)

  # return jsonify({ "error": "Project creation failed" }), 400

    # save image to mongodb
@app.route('/view-project/', methods=['POST','GET'])
@login_required
def view_project_page():

  return render_template('dynamic-dashboard-v3.html')


# view dynamic table of data from mongodb
@app.route('/get-table/')
@login_required
def view_dynamic_table():
  query ={}
  # filters ={"_id":1, "name": 1, "email": 1, "password": 1}
  filters ={"_id":0,"name": 1, "email": 1}
  results = users_collection.find(query, filters)

  # subject ="Dummy Test Data for Registered Users"
  # headings = ("_id","Name","Email","Password")
  # data = ((1,"Rolf Reindeer", "rolf@gmail.com","mysimplepassword"),(2,"Chilufya Zulu", "chilufya@gmail.com","mysimplepassword"),(3,"Andrew Kondwani", "andrew@gmail.com","mysimplepassword23"))
  
  subject ="Users Registered on 3 MegaLabs"
  filters ={"name": 1, "email": 1}
  headings = getKeysTuple(filters)
  data = getValuesTuplefromMongoDbResults(results)

  return render_template('table.html', subject = subject, headings = headings, data = data)


# an endpoint that allows us to retrieve an image file
@app.route('/file/<filename>')
def file(filename):
  return mongo.send_file(filename)


# view dynamic table of data from mongodb
@app.route('/get-dynamic-dashboard/')
@login_required
def view_dynamic_dashboard():
  query ={}
  # filters ={"_id":1, "name": 1, "email": 1, "password": 1}
  filters ={"_id":1,"project_title": 1, "project_summary":1, "project_description": 1, "project_profile_image":1 ,"project_profile_image_file_path": 1}
  # filters ={"_id":0,"name": 1, "email": 1}
  results = projects_collection.find(query, filters)

  subject ="Dynamically Populated Projects Dashboard"
  # filters ={"name": 1, "email": 1}
  # headings = getKeysTuple(filters)
  # data = getValuesTuplefromMongoDbResults(results)
  
  return render_template('dynamic-dashboard-v3.html', subject = subject, results = results)



# Show project details
@app.route('/show_project_information/', methods=['POST', 'GET'])
#@app.route('/project-info/', methods=['POST'])
@login_required
def show_project_information():

  if request.method == 'POST':

    project_id = request.form.get('project_id') 

    query ={ "_id": str.format(project_id) }

    filters ={"_id":1,"project_title": 1, "project_summary":1, "project_description": 1, "project_profile_image":1 ,"project_profile_image_file_path": 1}
    
    results = projects_collection.find(query, filters)
    
  return render_template('project_dashboard.html', project_id = project_id, results = results)


# Show project details
@app.route('/project/show/', methods=['GET'])
@login_required
def get_project_information():

  if request.method == 'GET':

    project_id = request.args.get('id')
     
    query ={ "_id": str.format(project_id) }

    filters ={"_id":1,"project_title": 1, "project_summary":1, "project_description": 1, "project_profile_image":1 ,"project_profile_image_file_path": 1}
    
    results = projects_collection.find(query, filters)
    
  return render_template('project_dashboard.html', project_id = project_id, results = results)


@app.route('/project-page-options/', methods =['POST', 'GET'])

@login_required

def evaluate_project_page_nav_options():

   if request.method == 'POST':
     
     return render_template('ai-platform-v2.html')

@app.route('/platform/', methods =['GET'])

@login_required

def get_platform():

   if request.method == 'GET':

      id = request.args.get('id')

      project_id = request.args.get('proj')

      query ={ "_id": str.format(project_id) }

      filters ={"_id":1,"project_title": 1, "project_summary":1, "project_description": 1, "project_profile_image":1 ,"project_profile_image_file_path": 1}
    
      results = projects_collection.find(query, filters)


      if (id == str(1)):
        return render_template('ai-platform-v2.html', project_id = project_id, results = results)


@app.route('/platform-option/', methods =['GET'])

@login_required

def get_platform_option():

   if request.method == 'GET':

      option = request.args.get('opt')
      # project_id = request.args.get('_id')

      if (option =="btn_classify_images"):
        return render_template('ai-platform-classify-images.html')

      elif (option =="btn_classify_webcam_stream"):
        return render_template('ai-platform-classify-webcam-images.html') 

      elif (option =="btn_classify_video_stream"):
        return render_template('ai-platform-classify-video.html')
        
      else:
        return render_template('ai-platform-v2.html')



@app.route('/project/', methods =[ 'GET'])

@login_required

def get_project():

  if request.method == 'GET':

    project_id = request.args.get('id')
     
    query ={ "_id": str.format(project_id) }

    filters ={"_id":1,"project_title": 1, "project_summary":1, "project_description": 1, "project_profile_image":1 ,"project_profile_image_file_path": 1}
    
    results = projects_collection.find(query, filters)
    
    return render_template('project_dashboard.html', project_id = project_id, results = results)

  # if request.method == 'GET':
  #  project_id = request.args.get('id')
  #  return '''<h1>The project id is: {}</h1>'''.format(project_id)

  #################### Expense Tracker ###########################################################
@app.route('/add_member_expense/')
@login_required
def add_member_expense():
  return render_template('add-expense-v2.html')


@app.route('/create-expense', methods=['POST'])
@login_required
def submit_new_expense():
  expense = Expense().createExpense()
  return redirect(url_for("view_dynamic_expense_table"))


# view dynamic table of data from mongodb
@app.route('/get-expense-table/')
@login_required
def view_dynamic_expense_table():
  query ={}
  results = expenses_collection.find(query)
  subject ="Expenses Tracker"
  return render_template('expenses-table.html', subject = subject, results = results)

 


