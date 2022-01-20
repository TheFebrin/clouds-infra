from google.cloud import firestore

# Add a new document
db = firestore.Client()
doc_ref = db.collection('berlin52').document('new_doc')
doc_ref.set({
    'first': 'Ada',
    'last': 'Lovelace',
    'born': 1815
})

# Then query for documents
users_ref = db.collection(u'users')

for doc in users_ref.stream():
    print(u'{} => {}'.format(doc.id, doc.to_dict()))