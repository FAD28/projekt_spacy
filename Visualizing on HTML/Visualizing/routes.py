import os, time
from flask import Flask
from flask import render_template
import pandas as pd
app = Flask(__name__)


file = pd.read_csv('NRC-Emotionen_Deutsch_03022020.csv', sep=";")
liste = [str(i) for i in file['German (de)']]









######### SERVER ############

@app.route("/")
@app.route("/main")
def home():
	# page = request.args.get('page', 1, type=int)
	# posts= Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('main.html', title = 'Meine Website', login_name= None)

@app.route("/results")
def about():
	return render_template('results.html', liste = liste)

@app.route("/analysis")
def analysis():
	return render_template('analysis.html')

@app.route("/login")
def login():
	return render_template('login.html')


if __name__=='__main__':
	app.run(debug=True)


