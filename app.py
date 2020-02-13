from flask import *

app = Flask(__name__)

@app.route('/')
def home():
	return render_template("home.html")

@app.route('/', methods =['POST'])
def basic():
	num1 = request.form['n1']
	print(num1)
	num2 = request.form['n2']
	print(num2)
	data = int(num1) + int(num2)
	return render_template("display.html", ans = data)

if __name__ == "__main__":
	app.run(debug=True)