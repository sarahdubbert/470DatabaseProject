from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)




@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        HomePage=request.form['home']
        PetPage=request.form['pet']
        OwnerPage=request.form['owner']
        IllnessesPage=request.form['illnesses']
        SurgeriesPage=request.form['surgeries']
        PrescriptionsPage=request.form['prescriptions']
        VaccinationsPage=request.form['vaccinations']


    return render_template('home.html')

@app.route('/pet', methods=['GET', 'POST'])
def pet():
    cnx = mysql.connector.connect(user='root', password='MySQLPassword', host='127.0.0.1', database='VetClinic', use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        #HomePage=request.form['home']
        #PetPage=request.form['pet']
        #OwnerPage=request.form['owner']
        #IllnessesPage=request.form['illnesses']
        #SurgeriesPage=request.form['surgeries']
        #PrescriptionsPage=request.form['prescriptions']
        #VaccinationsPage=request.form['vaccinations']

        def get_petResults_query(ownerLast, ownerFirst, petID, petName, petDOB):
            print("petID" + petID)
            return "SELECT Pet.PetID, Pet.Name, Owner.FirstName, Owner.LastName, Pet.PetType, Pet.DOB, Pet.Weight, Pet.Height, Pet.Sex FROM Pet JOIN Owner ON Pet.OwnerID = Owner.OwnerID WHERE LastName = '" + str(ownerLast) + "' OR FirstName = '" + str(ownerFirst) + "' OR PetID = '" + str(petID) + "' OR Name = '" + str(petName) + "' OR Pet.DOB = '" + str(petDOB) + "';"


        ownerLast=request.form['ownerLast']
        ownerFirst=request.form['ownerFirst']
        petID=request.form['petID']
        petName=request.form['petName']
        petDOB=request.form['petDOB']
        petResultsQuery = get_petResults_query(ownerLast, ownerFirst, petID, petName, petDOB)
        print("pet Results Query: " + petResultsQuery)

        cnx.commit()
        rows = []
        try:
            for result in cursor.execute(petResultsQuery, multi = True) :
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(result.statement))
                    results = result.fetchall()
                    for r in results:
                        print(r)
                else:
                    print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
        except:
            print("Exception")

        return redirect(url_for('petResults', rows=results))

    cursor.close()
    cnx.close()

    return render_template('pet.html')

@app.route('/petResults', methods=['GET', 'POST'])
def petResults():
    if request.method == "POST":
        print("Made it to pet results")
    return render_template('petResults.html', rows=request.args.get('rows'))


@app.route('/owner', methods=['GET', 'POST'])
def owner():
    if request.method == "POST":
        HomePage=request.form['home']
        PetPage=request.form['pet']
        OwnerPage=request.form['owner']
        IllnessesPage=request.form['illnesses']
        SurgeriesPage=request.form['surgeries']
        PrescriptionsPage=request.form['prescriptions']
        VaccinationsPage=request.form['vaccinations']
    return render_template('owner.html')

@app.route('/illnesses', methods=['GET', 'POST'])
def illnesses():
    if request.method == "POST":
        HomePage=request.form['home']
        PetPage=request.form['pet']
        OwnerPage=request.form['owner']
        IllnessesPage=request.form['illnesses']
        SurgeriesPage=request.form['surgeries']
        PrescriptionsPage=request.form['prescriptions']
        VaccinationsPage=request.form['vaccinations']
    return render_template('illnesses.html')

@app.route('/surgeries', methods=['GET', 'POST'])
def surgeries():
    if request.method == "POST":
        HomePage=request.form['home']
        PetPage=request.form['pet']
        OwnerPage=request.form['owner']
        IllnessesPage=request.form['illnesses']
        SurgeriesPage=request.form['surgeries']
        PrescriptionsPage=request.form['prescriptions']
        VaccinationsPage=request.form['vaccinations']
    return render_template('surgeries.html')

@app.route('/prescriptions', methods=['GET', 'POST'])
def prescriptions():
    if request.method == "POST":
        HomePage=request.form['home']
        PetPage=request.form['pet']
        OwnerPage=request.form['owner']
        IllnessesPage=request.form['illnesses']
        SurgeriesPage=request.form['surgeries']
        PrescriptionsPage=request.form['prescriptions']
        VaccinationsPage=request.form['vaccinations']
    return render_template('prescriptions.html')

@app.route('/vaccinations', methods=['GET', 'POST'])
def vaccinations():
    if request.method == "POST":
        HomePage=request.form['home']
        PetPage=request.form['pet']
        OwnerPage=request.form['owner']
        IllnessesPage=request.form['illnesses']
        SurgeriesPage=request.form['surgeries']
        PrescriptionsPage=request.form['prescriptions']
        VaccinationsPage=request.form['vaccinations']
    return render_template('vaccinations.html')

