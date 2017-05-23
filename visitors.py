from flask import Flask,jsonify,abort,request,make_response
from flask_httpauth import HTTPBasicAuth
import time
auth = HTTPBasicAuth()

app = Flask(__name__)


app.config.update({
   "DEBUG": True
})

users = [
    {
        'username': 'dhannu',
        'password': 'p',
        'Age': '24',
        'City': 'delhi',
        'Bio': 'married'
    }
]

places = [
    {
        'placename': 'sarita vihar',
        'username': 'dhannu',
        'Details': "it is good place",
        'added_on': time.strftime("%d/%m/%Y"),
        "likes": 20,
        "id": 1
    },
    {
        'placename': 'sanjay colony',
        'username': 'dhannu',
        'Details': "it is good place",
        'added_on': time.strftime("%d/%m/%Y"),
        "likes": 20,
        "id": 2
    }
]
comment = [
    {
        'username': 'dhannu',
        'comment': 'this is not good place',
        'added_on': time.strftime("%d/%m/%Y"),
        'id': 1
    },
    {
        'username': 'dhannu',
        'comment': 'this is good place',
        'added_on': time.strftime("%d/%m/%Y"),
        'id': 2
    }
]


@auth.get_password
def get_passwords(username):
    new = [user for user in users if username == user['username']]
    if len(new) == 0:
        abort(404)
    return new[0]['password']

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)



@app.route('/info', methods = ['POST'])
def adding():
    if not request.json or not 'username' in request.json:
        abort(400)
    add = {
        'username': request.json['username'],
        'password': request.json['password'],
        'Age': request.json['Age'],
        'City': request.json['City'],
        'Bio': request.json['Bio']
    }
    users.append(add)
    return jsonify({'userss': add}), 201

@app.route('/info/places/get', methods=['GET'])
@auth.login_required
def get_new():
    kaam = [place for place in users if auth.username() == place['username']]
    return jsonify({'places': kaam})



@app.route('/info/places', methods = ['POST'])
def change_place():
    if not request.json or not 'username' in request.json:
        abort(400)
    place_add = {
        'placename': request.json['placename'],
        'username': auth.username(),
        'Details': request.json['Details'],
        'added_on': time.strftime("%d/%m/%Y"),
        'likes':places[-1]['likes'] + 1,
        'id': places[-1]['id'] + 1
    }
    places.append(place_add)
    return jsonify({'userss': place_add}), 201



@app.route('/get/info/places', methods=['GET'])
@auth.login_required
def get_task():
    place = [place for place in places if auth.username() == place['username']]
    return jsonify({'users': place})



@app.route('/current_user_one_place/<int:place_id>', methods = ['GET'])
@auth.login_required
def current_place(place_id):
    place = [place for place in places if auth.username() == place['username']]
    one_place = [one_place for one_place in place if place_id == one_place['id']]
    return jsonify({'users': one_place})



@app.route('/user_comment/<int:comment_id>', methods = ['GET'])
@auth.login_required
def user_comment(comment_id):
    user_comment = [user_comment for user_comment in comment if auth.username() == user_comment['username']]
    one_comment = [one_comment for one_comment in user_comment if comment_id == one_comment['id']]
    return jsonify({'users': one_comment})


@app.route('/extra/add_comment/<int:comment_id>', methods = ['POST'])
@auth.login_required
def user_comm(comment_id):
   comments = [comments for comments in comment if comment_id==comments['id']]
   particular_comment = [particular_comment for particular_comment in comments if auth.username()==particular_comment['username']]
   if not request.json or not 'comment' in request.json:
       abort(400)
   add = {
       'username': auth.username(),
       'added_on': time.strftime('%d/%m/%Y'),
       'comment':request.json['comment']
   }
   comment.append(add)
   return jsonify({'comment':add})


@app.route('/updete_place/<int:update_id>', methods=['PUT'])
@auth.login_required
def update_place(update_id):
    updte_value = [updte_value for updte_value in places if auth.username() == updte_value['username']]
    update = [update for update in updte_value if update_id == update['id']]
    if len(update) == 0:
        abort(404)
    if not request.json:
        abort(404)
    if 'Details' in request.json and type(request.json['Details']) is not unicode:
        abort(400)
    update[0]['Details'] = request.json.get('Details', update[0]['Details'])
    return jsonify({'update': update[0]})







if __name__ == '__main__':
   app.run()
