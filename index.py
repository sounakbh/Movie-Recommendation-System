from flask import Flask, render_template, request
import cosine_sim
app = Flask(__name__)

@app.route('/')
def formPage():
    return render_template('test.html')



@app.route('/',methods=['POST'])
def displayResults():
	text = request.form['text']
	li = cosine_sim.recommendations(text)
	return render_template('test.html', options=li)

@app.errorhandler(500)
def internal_error(error):
    return render_template('test.html', task='fail')


if __name__ == '__main__':
   app.run()