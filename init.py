from flask import Flask

def create_web():
    web = Flask(__name__)
    web.config['SECRET_KEY'] = 'chickenstuffe'
    return web

web=create_web()
if __name__ == "__main__":
    web.run(debug=True)
