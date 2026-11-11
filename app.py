import os

from flask import Flask, jsonify

from books import book_routes
from db import init_db
from errors import LibraryError
from loans import loan_routes
from members import member_routes
from reports import report_routes

app = Flask(__name__)
app.register_blueprint(book_routes.bp)
app.register_blueprint(member_routes.bp)
app.register_blueprint(loan_routes.bp)
app.register_blueprint(report_routes.bp)


@app.errorhandler(LibraryError)
def handle_library_error(error):
    return jsonify({"error": error.message}), error.status


if not os.path.exists("library.db"):
    init_db()
