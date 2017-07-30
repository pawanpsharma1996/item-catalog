# importing framework(flask)
from flask import Flask, render_template
from flask import request, redirect, url_for, jsonify, flash

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Categories, Base, Items, User

# imports for authentication and authorization
from flask import session as login_session
import random
import string

# imports for gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# creating an instance of flask
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

engine = create_engine('sqlite:///itemcatalogwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32))
    login_session['state'] = state

    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # checking if user exists. If not than adding it
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height:"''+" 300px;'
    'border-radius: 150px;-webkit-border-radius: 150px;'
    '-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = "https://accounts.google.com/o/oauth2/"
    "revoke?token=%s" % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# code API endpoints
@app.route('/catalog/json')
def itemCatalogJSON():
    items = session.query(Items).all()
    return jsonify(Items=[i.serialize for i in items])


# code for home page
@app.route('/')
@app.route('/catalog')
def viewCatalog():
    categories = session.query(Categories).all()
    if 'username' not in login_session:
        return render_template('public_home.html', categories=categories)
    else:
        return render_template(
            'home.html', categories=categories, user=login_session)


# code for items display page
@app.route('/catalog/<int:category_id>/items')
def viewItems(category_id):
    category = session.query(Categories).filter_by(id=category_id).first()
    items = session.query(Items).filter_by(category=category.name).all()
    print items
    if 'username' not in login_session:
        return render_template(
            'public_items.html', category=category, items=items)
    else:
        return render_template(
            'items.html', category=category, items=items, user=login_session)


# code for item description page
@app.route('/catalog/items/<int:item_id>')
def viewDescription(item_id):
    item = session.query(Items).filter_by(id=item_id).first()
    if 'username' not in login_session or login_session[
                                                    'user_id'] != item.user_id:
        return render_template('public_description.html', item=item)
    else:
        return render_template(
            'description.html', item=item, user=login_session)


# code for creating new item
@app.route('/catalog/new', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        new_item = Items(
            name=request.form['name'],
            description=request.form['description'],
            category=request.form['category'],
            user_id=login_session['user_id'])
        temp_category = request.form['category']
        session.add(new_item)
        session.commit()
        flash("New Item created!")
        category_temp = session.query(Categories).filter_by(
            name=temp_category).first()
        return redirect(url_for('viewItems', category_id=category_temp.id))
    else:
        categories = session.query(Categories).all()
        return render_template(
            'create.html', categories=categories, user=login_session)


# code for item edit page
@app.route('/catalog/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')
    edited_item = session.query(Items).filter_by(id=item_id).first()
    if edited_item.user_id != login_session['user_id']:
        return "You are not allowed to perform this action"
    if request.method == 'POST':
        if request.form['name']:
            edited_item.name = request.form['name']
        if request.form['description']:
            edited_item.description = request.form['description']
        session.add(edited_item)
        session.commit()
        flash('changes made!')
        return redirect(url_for('viewDescription', item_id=edited_item.id))
    else:
        categories = session.query(Categories).all()
        return render_template(
            'edit.html',
            item_id=item_id,
            categories=categories,
            edited_item=edited_item,
            user=login_session)


# code for delete item page
@app.route('/catalog/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')

    deleted_item = session.query(Items).filter_by(id=item_id).first()
    if deleted_item.user_id != login_session['user_id']:
        return "You are not allowed to perform this action"
    category = session.query(Categories).filter_by(
        name=deleted_item.category).first()
    print deleted_item.category
    print category.name
    if request.method == 'POST':
        session.delete(deleted_item)
        session.commit()
        flash("Item deleted!")
        return redirect(url_for(('viewItems'), category_id=category.id))
    else:
        return render_template(
            'delete.html', item=deleted_item, user=login_session)


# code for local permission system
def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def application(environ, start_response):
    status = '200 OK'

    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return
