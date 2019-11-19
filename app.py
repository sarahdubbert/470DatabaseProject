from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import yaml

app = Flask(__name__)

#configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', method=['GET', 'POST'])
def index():
	if request.method == 'POST':
		#fetch form data
		userDetails = request.form
		PetID = userDetails['petid']
		Name = userDetails['petname']
		OwnerID = userDetails['ownerid']
		PetType = userDetails['type']
		DOB = userDetails['dob']
		Weight = userDetails['weight']
		Height = userDetails['height']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO Pet(PetID, Name, OwnerID, PetType, DOB, Weight, Height) VALUES(%s, %s, %s, %s, %s, %s, %s,)",(PetID, Name, OwnerID, PetType, DOB, Weight, Height))
		mysql.connection.commit()
		cur.close()
		return 'success'
		
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)
