# Task
Rest api for getting twitter data
1: Clone the project from given git directory
2: Extract project to any directory
3: Open project using cd Twitter 
4: Now install the requirements by using command 
    pip install -r requirements.txt
5: After installing requirements run
    python manage.py runserver
6: Now local server will be running at
    http://127.0.0.1:8000
7: Use postman or anyother tool to request api's
    1: for specfic user tweets:
         http://127.0.0.1:8000/uesrs/AzharAli?limit=20
         limit is by default an optional parameter by default
         it's value is set to 30
    2: for getting tweets against given hashtag
         http://127.0.0.1:8000/tweets/HASHTAG?limit=10
         limit is by default an optional parameter by default
         it's value is set to 30
8: For testcases kindly use tests.py file inside api app. I wrote 2 tests for these 2 api's and to run test use command
    python manage.py test api.tests
