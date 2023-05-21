from flask import Flask,request,jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
CORS(app)
uri = "mongodb+srv://archiaa1008:yIl1Ee7UjOvMx3S7@cluster0.c3i9bn9.mongodb.net/?retryWrites=true&w=majority"
app.config['MONGO_URI'] = uri
client = MongoClient(app.config['MONGO_URI'])
db = client['cluster0']['crudapp']
mongo = PyMongo(app)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# app.config['MONGO_URI'] = "mongodb+srv://archiaa1008:yIl1Ee7UjOvMx3S7@cluster0.c3i9bn9.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(app.config['MONGO_URI'])

# app.config['MONGO_URI']= 'mongodb://127.0.0.1/crudapp'

# db = mongo.db['cluster0']

#Route to create a new user
@app.route('/users',methods = ['POST'])
def createUser():
    id = db.insert_one({
        'title': request.json['title'],
        'time': request.json['time'],
        'priority': request.json['priority'],
        'status': 'pending'
    })
    return jsonify({'id': str(id.inserted_id),'msg': f"Task with {id} Added Successfully"})

#route to get all users
@app.route("/users", methods= ['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str((doc['_id'])),
            'title': doc['title'],
            'time': doc['time'],
            'priority': doc['priority'],
            'status': doc['status'],
        })
    return jsonify(users)    

#get single user
@app.route("/users/<id>",methods = ['GET'])
def getUser(id):
    user = db.find_one({'_id':ObjectId(id)})
    if user:
        return jsonify({
            '_id': str(user['_id']),
            'title': user['title'],
            'time': user['time'],
            'priority': user['priority'],
            'status': user['status'],
        })
    else:
        return jsonify({'error':'Task not found'})
    
#Route to update
@app.route("/users/<id>",methods=['PUT'])
def updateUser(id):
    task = db.find_one({'_id': ObjectId(id)})
    if task:
        task['title'] = request.json.get('title', task['title'])
        task['time'] = request.json.get('time', task['time'])
        task['priority'] = request.json.get('priority', task['priority'])
        task['status'] = request.json.get('status', task['status'])
        
        db.update_one({'_id': ObjectId(id)}, {'$set': task})
        
        return jsonify({'msg': 'Task Updated Successfully'})
    else:
        return jsonify({'error': 'Task not found'})
    
#route to update status    
@app.route("/users/status/<id>",methods=['PUT'])
def updateUserStatus(id):
    print('my id',id)
    task = db.find_one({'_id': ObjectId(id)})
    if task:
        task['status'] = 'completed'
        
        db.update_one({'_id': ObjectId(id)}, {'$set': task})
        
        return jsonify({'msg': 'Task Updated Successfully'})
    else:
        return jsonify({'error': 'Task not found'})    

#Route to delete task    
@app.route('/users/<id>',methods=['DELETE'])
def deleteUser(id):
        print(str(id))
        db.delete_one({'_id':  ObjectId(id)})  
        return jsonify({'msg':f'Task with {id} Deleted Successfully'})  
    
if __name__ == '__main__':
    app.run(debug=True,port=5000,use_reloader=False)
