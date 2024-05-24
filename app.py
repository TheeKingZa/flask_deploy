from flask import Flask, render_template

Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/app')
def app_page():
    return render_template('app.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

if __name__ == '__main__':
    app.run(debug=True)