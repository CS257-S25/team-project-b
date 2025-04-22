'''
The eventual location for the Flask app interface for the project.
'''

from flask import Flask

app = Flask(__name__)


@app.route('/about')
def aboutpage():
    return "Hello, this is the about page."


@app.route('/<favorite_number>', strict_slashes=False)
def favorite_number(favorite_number):
    return f"Your favorite number is {favorite_number}."



if __name__ == "__main__":
    app.run(debug=True)