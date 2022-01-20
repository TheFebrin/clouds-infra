#!/usr/local/bin/python
from google.cloud import firestore
from flask import Flask, jsonify
import random
import os

app = Flask(__name__)

# var = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
# print('Key path: ', var)

def create_new_nick(user_dict):
    words = [
        user_dict.get('nick', ''), 
        user_dict.get('name', ''), 
        user_dict.get('surname', ''), 
        user_dict.get('age', ''),
    ]
    print(words)
    random.shuffle(words)
    return ''.join(words)



@app.route("/")
def hello():
    return "Hello Build by CircleCIv3, go to => /read"


@app.route("/read", methods=['GET'])
def read_data():
    db = firestore.Client(credentials=None)

    users_ref = db.collection('clouds-website')
    docs = users_ref.stream()

    stats = {
        'sum_of_ages': 0
    }
    response = []
    for doc in docs:
        user_dict = doc.to_dict()
        user_dict['new_nick'] = create_new_nick(user_dict)
        response.append(user_dict)

        age = user_dict.get('age', False)
        if age is not False and len(age) > 0:
            stats['sum_of_ages'] += int(age)

    final_response = jsonify({
        'users_list': response,
        'stats': stats
    })
    final_response.headers.add('Access-Control-Allow-Origin', '*')  # WARNING DON'T DO THIS IN REAL LIFE
    return final_response


# def main():
#     app.run(host='0.0.0.1', port=4444, debug=True)

# if __name__ == '__main__':
#     print('Start server')
#     main()

