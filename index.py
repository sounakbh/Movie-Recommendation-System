from flask import Flask, render_template, request
import mainRecommender
app = Flask(__name__)

@app.route('/')
def formPage():
    return render_template('test.html')

@app.route('/',methods=['POST'])
def displayResults():
	userInput = request.form['text']
	recommendedMovies = mainRecommender.getMovies(userInput)
	return render_template('test.html', options=recommendedMovies)

@app.errorhandler(500)
def internal_error(error):
    return render_template('test.html', task='fail')

if __name__ == '__main__':
   app.run()