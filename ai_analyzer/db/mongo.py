from pymongo import MongoClient

def query_post_id_and_content(profileID):
    # Connect to the MongoDB server
    client = MongoClient('mongodb://localhost:27017/')

    # Select the database and collection to use
    db = client['mydatabase']
    collection = db['mycollection']

    # Set the profileID to query
    profileID = '12345'

    # Query the collection to find all postids and content for the given profileID
    query = {'profileID': profileID}
    results = collection.find(query, {'postid': 1, 'content': 1})

    # Print the results
    for result in results:
        print('postid:', result['postid'])
        print('content:', result['content'])


def insert_post_content_key_words(postid, keywords):
    # Connect to the MongoDB server
    client = MongoClient('mongodb://localhost:27017/')

    # Select the database and collection to use
    db = client['mydatabase']
    collection = db['mycollection']

    # # Set the postid and keywords to insert
    # postid = 'abc123'
    # keywords = ['foo', 'bar', 'baz']

    # Update the document with the given postid to add the keywords field
    result = collection.update_one(
        {'postid': postid},
        {'$set': {'keywords': keywords}}
    )

    # Print the result of the update
    if result.modified_count > 0:
        print('Keywords added successfully')
    else:
        print('Error adding keywords')

def query_post_id_key_words(postid):
    # Connect to the MongoDB server
    # Connect to the MongoDB server
    client = MongoClient('mongodb://localhost:27017/')

    # Select the database and collection to use
    db = client['mydatabase']
    collection = db['mycollection']

    # # Set the postid to query
    # postid = 'abc123'

    # Query the collection for the document with the given postid
    document = collection.find_one({'postid': postid})

    # Print the keywords from the document
    if document:
        print('Keywords:', document['keywords'])
    else:
        print('No document found with postid:', postid)
