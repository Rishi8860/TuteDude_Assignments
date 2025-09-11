from flask import Flask, jsonify, request, render_template, redirect, url_for
import json
import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

# MongoDB Atlas connection string (temporary placeholder)
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')

client = MongoClient(MONGO_URI)
db = client['assignment']
collection = db['form_data']

@app.route('/api', methods=['GET'])
def api():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/form', methods=['GET', 'POST'])
def form():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        value = request.form.get('value')
        if not name or not value:
            error = "Both name and value are required."
            return render_template('form.html', error=error)
        try:
            value_int = int(value)
        except ValueError:
            error = "Value must be an integer."
            return render_template('form.html', error=error)
        try:
            collection.insert_one({'name': name, 'value': value_int})
            return redirect(url_for('success'))
        except PyMongoError as e:
            error = f"Database error: {str(e)}"
            return render_template('form.html', error=error)
    return render_template('form.html', error=error)

@app.route('/success')
def success():
    return render_template('success.html')

todos_collection = db['todos']

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')
    if not item_name or not item_description:
        return jsonify({'error': 'Both itemName and itemDescription are required.'}), 400
    try:
        todos_collection.insert_one({
            'itemName': item_name,
            'itemDescription': item_description
        })
        return jsonify({'message': 'To-Do item submitted successfully.'}), 201
    except PyMongoError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/todo', methods=['GET'])
def todo():
    return render_template('todo.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
