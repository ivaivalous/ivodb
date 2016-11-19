from flask import Flask

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    """ Get the intex page """
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()
