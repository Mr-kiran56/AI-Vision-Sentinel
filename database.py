# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://facereco-f00ec-default-rtdb.firebaseio.com/",
#     'storageBucket': "facereco-f00ec.appspot.com"  # <-- Add this line
# })


# ref=db.reference('Persons')
# data={
#     "Virat_Kohli":{
#         "name":"Virat_Kohli",
#         "Category":"Cricketr",
#         "Age":38
#     },
#     "Narendra_Modi":{
#         "name":"Narendra_Modi",
#         "Category":"Politician",
#         "Age":78},

#         "Kajal_Aggarwal":{
#         "name":"Kajal_Aggarwal",
#         "Category":"Acteress",
#         "Age":39}
    
# }
# for key,value in data.items():
#     ref.child(key).set(value)


