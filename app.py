from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to my watchlist!'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='qiangli'))
    return url_for('test_url_for', name='qiangli')

#
#
# if __name__ == '__main__':
#     app.run(debug = True)
