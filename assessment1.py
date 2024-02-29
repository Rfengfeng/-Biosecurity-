from flask import Flask,render_template,redirect,url_for
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/FreshwaterGuide')
def FreshwaterGuide():
    return render_template('FreshwaterGuide.html')

@app.route('/redirect_to_FreshwaterGuide')
def redirect_to_FreshwaterGuide():
    return redirect(url_for('FreshwaterGuide'))



if __name__ == '__main__':
    app.run(debug=True)