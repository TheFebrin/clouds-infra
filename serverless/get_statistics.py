from google.cloud import firestore
import datetime

WRONG_REQUEST_MESSAGE = """
Wrong request.
Use: curl <address> -H "Content-Type:application/json"\
--data {"request":"<request>", "begin": "<%y-%m-%d-%H-%M-%S>", "end": "<%y-%m-%d-%H-%M-%S>"}')
"""
def response_to_request(request_json):
    if request_type == 'TODO':
        pass
    get_data_from_db()
     

def is_valid_request_json(request_json):
    return request_json \
        and 'request' in request_json \
        and 'begin' in request_json \
        and 'end' in request_json \

def main(_request):
    if _request is not None:
        request_json = _request.get_json()
        print('Got request: ', _request.get_json(), _request.args)
        if is_valid_request_json(request_json):
            return response_to_request(request_json)
    return WRONG_REQUEST_MESSAGE


def get_data_from_db():
    db = firestore.Client()
    data_ref = db.collection(u'covid-data')

    records = []
    for doc in data_ref.stream():
        date_time = datetime.datetime.strptime(doc.id, "%y-%m-%d-%H-%M-%S")
        records.append((date_time, doc.to_dict()))

    records.sort(key=lambda x: x[0])

if __name__ == '__main__':
    # display_data_from_db()
    print(main(None))