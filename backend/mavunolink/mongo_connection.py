from mongoengine import connect

connect(
    db='mavunolink_db',
    host='mongodb://localhost:27017/mavunolink_db'
)
