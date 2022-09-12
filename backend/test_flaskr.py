import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from flaskr import create_app
from models import setup_db, Question, Category
from settings import  DB_USER, DB_PASSWORD





class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "answer", "answer":"question", "category": 1, "difficulty": 3}
        self.error_question = {"question": "answer", "answer":"question", "category": "Archeology", "difficulty": 500}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])



    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])      


    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/categories/?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")




    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions/?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")



    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/categories/6/questions/?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")  






    def test_get_question_search_with_results(self):
        res = self.client().post("/questions", json={"search": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
       # self.assertTrue(data["total_questions"])
       # self.assertEqual(len(data["total_questions"]), 19)

    def test_get_question_search_without_results(self):
        res = self.client().post("/questions", json={"search": "applejacks"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
       # self.assertEqual(data["total_questions"], 0)
        #self.assertEqual(len(data["total_questions"]), 0)        

        





    def test_delete_question(self):
        res = self.client().delete("/questions/10")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 10)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")



    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
       # self.assertTrue(data["created"])
        #self.assertTrue(len(data["questions"]))

    def test_create_question_fail(self):
        res = self.client().post('/questions', json=self.error_question)
        data = json.loads(res.data)    

 
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')



    def test_question_by_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['current_category'], 'History')
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])




    def test_play_quizz(self):
        res = self.client().post('/quizzes', json={
            'quiz_category': {'type': 'History', 'id': '4'},
            'previous_questions': []})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['question'])
        self.assertEqual(len(data['previousQuestions']), 0)



    def test_play_quizz_error(self):
        res = self.client().post('/quizzes', json={
            'quiz_category': {'type': 'Anachology', 'id': '10'},
            'previous_questions': []})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad Request')




    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()