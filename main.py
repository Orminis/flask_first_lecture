# from flask import Flask, render_template
#
# app = Flask(__name__)       # syzdawame Flask app :)
#
#
# @app.route('/')   # direktno na domaina
# def initial():
#     my_name = "imenceee"
#     return render_template("index.html", name=my_name)
#
#
# @app.route("/contact")
# def display_contact():
#     return "<h1 style='color: #62131a'>Our contacts are!</h1>"
#
#
# if __name__ == '__main__':
#     app.run()


from flask import Flask, request
from flask_restful import Resource, Api
'''В фласк не закачаме декоратори  а използваме апи обект '''
app = Flask(__name__)
api = Api(app)     # вдигаме обект от клас Api който приема Flask обекта app


class BookModel:
    _pk = 1

    def __init__(self, title, author):
        self.pk = BookModel._pk
        self.title = title
        self.author = author
        BookModel._pk += 1

    def serialize(self):    # превръща стринговата репрезентанрия към речник който фласк да подаде като json
        return self.__dict__

    def __str__(self):
        return f"{self.pk} Title: {self.title} from {self.author}"


books = [BookModel(f"Title {i}", f"Author {i}") for i in range(1, 11)]


class Books(Resource):  # наследява class Resource ot flask restful
    def get(self):      # predefinirame metod get ot flaskrestful
        return {"books": [book.__dict__ for book in books]}  # сирилизира от речник към JSON

    def post(self):     # добавяне на книга
        data = request.get_json()   # request получава заявка от сървъра с json информация и я предава за обработка
        book = BookModel(title=data.get("title"), author=data.get("author"))
        books.append(book)
        return {"books": [book.__dict__ for book in books]}


class Book(Resource):
    def _get_book(self, pk):
        try:
            return [b for b in books if b.pk == pk][0]
        except IndexError:
            return None

    def get(self, pk):
        book = [b for b in books if b.pk == pk][0]
        return book.__dict__


api.add_resource(Books, "/books/")   # Zakachame na endpoint /books  class Books chrez api.
api.add_resource(Book, "/books/<int:pk>")

if __name__ == '__main__':    # za da startirame flask syrwyrcheto

    app.run(debug=True)         # app.run() за да се стартира / debug=True: za da izpishe wsichki greshki
