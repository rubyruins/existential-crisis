from flask import *
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
	return render_template("home.html")

@app.route('/', methods =['POST'])
def basic():
	age = request.form['userage']
	sex = request.form['usergender']
	country = request.form['usercountry']

	who_data = pd.read_csv('data.csv')
	#subsetting the dataframe to retain only the useful features
	who_data = who_data[['GHO (DISPLAY)', 'YEAR (CODE)', 'COUNTRY (DISPLAY)', 'SEX (DISPLAY)', 'Numeric']]
	req_data = who_data[who_data['COUNTRY (DISPLAY)'] == country]
	req_data = req_data[who_data['SEX (DISPLAY)'] == sex]
	life_birth = req_data[req_data['GHO (DISPLAY)'] == 'Life expectancy at birth (years)'].sort_values('YEAR (CODE)', ascending = False)
	life_60 = req_data[req_data['GHO (DISPLAY)'] == 'Life expectancy at age 60 (years)'].sort_values('YEAR (CODE)', ascending = False)

	if len(life_birth['Numeric']) > 0 and len(life_60['Numeric']) > 0:
  		rel_ages = [0, 60]
  		rel_life = [life_birth['Numeric'].values[0], life_60['Numeric'].values[0]]

  		slope, intercept, r_value, p_value, std_err = stats.linregress(rel_ages, rel_life)
  		age = int(age)
  		slope = slope.item()
  		intercept = intercept.item()
  		exp_lifespan = int(np.ceil((age*slope) + intercept))
  		pizza_lifespan = int(np.ceil(exp_lifespan/1.04))
  		vice_lifespan = int(np.ceil(exp_lifespan/1.08))
	else:
  		print("Not enough data to conclude.")
	return render_template("display.html", exp=exp_lifespan, pizza=pizza_lifespan, vice=vice_lifespan)

@app.errorhandler(404)
def error(e):
    return render_template("notfound.html")

if __name__ == "__main__":
	app.run(debug=True)