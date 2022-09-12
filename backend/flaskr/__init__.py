import os
from re import search
from unicodedata import category
from flask import Flask, app, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
#from flask_migrate import Migrate
from models import setup_db, db, Question, Category

#app = Flask(__name__)
#db.init_app(app)
#migrate = Migrate(app, db)
#app.config.from_object('config')

#def loop(incr):
 #   i= len(incr)
   # j=0
  #  for j in range(i) :
   #   return incr[j]
   # j +=1

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
  

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    
    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    
    

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response





    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """




    @app.route('/categories')
    #@cross_origin()
    def get_category():

        categories = Category.query.order_by(Category.id).all()
        #current_categories = paginate_questions(request, categories)
        formatted_category = [category.format() for category in categories]
        dictionary = {}
        for k in categories :
            dictionary[k.id] = k.type

        if len (formatted_category) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": dictionary, 
                
            }
        )






    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """




    
    @app.route("/questions", methods= ['GET'])
   # @cross_origin()
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.order_by(Category.id).all()
        #formatted_category = [category.format() for category in categories]
        dictionary = {}
        for k in categories :
            dictionary[k.id] = k.type


        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": dictionary,
                #"categories":len(Category.query.all())
            }
        )






    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """





    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(422)




    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """







    @app.route("/questions", methods=["POST"])
    def create_question():
        try: 
            body = request.get_json()
            new_question = body.get("question", None)
            search = body.get('searchTerm', None)
            new_answer = body.get("answer", None)
            new_category = body.get("category", None)
            new_difficulty= body.get("difficulty", None)
               
            if search is not None:

                selection = Question.query.order_by(Question.id).\
                filter(Question.title.ilike("%{}%".format(search)))

                if len(selection) == 0:
                    abort(404)
                current_questions = paginate_questions(request, selection)

                return jsonify({
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(selection.all()),
                })

            else:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                "success": True,
                "created": question.id,
                "questions": current_questions,
                })
        except:
            abort(422)







    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """


    @app.route("/categories/<int:category_id>/questions", methods= ['GET'])
    @cross_origin()
    def retrieve_questionsbasedoncategory(category_id):
        #selection = Question.query.all()
        #current_questions = paginate_questions(request, selection)
        sels = Question.query.all()
        asel = []
        #categor = Category.query.get(category_id)

        cater = Category.query.get(category_id)
        
        #try:

        for sel in sels:
            
        
          if category_id == sel.category :
             
            asel.append(sel)

        formatted_questions = [asell.format() for asell in asel]
     

        return jsonify(
            {
            "success": True,
            "questions": formatted_questions,
            #"list of questions2": asel[j+1].format(),
            "total_questions": len(Question.query.all()),
            "current_category": cater.type
            #"categories":len(Category.query.all())
             }
             )
    
 




    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """


    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
     try:
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category', None).get('id')
        category = Category.query.filter(Category.id == quiz_category).one_or_none()
        q1 = None
        qn = None
        
        if category is None:
            qn = Question.query.filter(Question.id.not_in(previous_questions)).all()
        
        else:
            A = Question.query.filter(Question.category == quiz_category)
            B = Question.id.not_in(previous_questions)
            qn = A.filter(B).all()

        if len(qn) != 0:
                random_question = random.choice(qn)
                q1 = random_question.format()

        return jsonify({
                #'success': True,
                'previousQuestions': previous_questions,
                'question': q1
            })
     except:
            abort(400)       








    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """


    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({

                "success": False, 
                "error": 404, 
                "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                
                "success": False, 
                "error": 422, 
                "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return ( jsonify({

               "success": False, 
               "error": 400, 
               "message": "bad request"}),
                400,
          )
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({
                'success': False,
                'error': 500,
                'message': 'Internal Server Error'
            }),
            500
        )

    return app
  
       

