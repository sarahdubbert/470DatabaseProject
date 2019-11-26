from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "SecretKey"


#Set db connection variables
usr = "root"
pw = "MySQLPassword"
hst = "127.0.0.1"
db = "VetClinic"

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
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":

        def get_petResults_query(ownerLast, ownerFirst, petID, petName, petDOB):
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
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":

        def get_ownerResults_query(petID, petName):
            return "SELECT Pet.PetID, Pet.Name, Owner.OwnerId, Owner.FirstName, Owner.LastName, Owner.InsuranceNumber, Owner.InsuranceCompany, Owner.PhoneNumber, Owner.Email, Owner.PhysicalAddress, Owner.SSN, Owner.DOB FROM Pet JOIN Owner ON Pet.OwnerID = Owner.OwnerID WHERE PetID = '" + str(petID) + "' OR Name = '" + str(petName) + "';"

        petID=request.form['petID']
        petName=request.form['petName']
        ownerResultsQuery = get_ownerResults_query(petID, petName)
        print("Owner Results Query: " + ownerResultsQuery)

        cnx.commit()
        rows = []
        try:
            for result in cursor.execute(ownerResultsQuery, multi = True) :
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(result.statement))
                    results = result.fetchall()
                    for r in results:
                        print(r)
                else:
                    print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
        except:
            print("Exception")

        return redirect(url_for('ownerResults', rows=results))

    cursor.close()
    cnx.close()

    return render_template('owner.html')

@app.route('/ownerResults', methods=['GET', 'POST'])
def ownerResults():
    if request.method == "POST":
        print("Made it to owner results")
    return render_template('ownerResults.html', rows=request.args.get('rows'))

@app.route('/newOwner', methods=['GET', 'POST'])
def newOwner():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        insurance_number=request.form['insurance_number']
        insurance_company=request.form['insurance_company']
        phone_number=request.form['phone_number']
        email=request.form['email']
        physical_address=request.form['physical_address']
        ssn=request.form['ssn']
        owner_dob=request.form['owner_dob']



        def get_insertOwner_query():
            return "INSERT INTO Owner (FirstName, LastName, InsuranceNumber, InsuranceCompany, PhoneNumber, Email, PhysicalAddress, SSN, DOB) VALUES ('" + str(first_name) + "', '" + str(last_name) + "', '" + str(insurance_number) + "', '" + str(insurance_company) + "', '" + str(phone_number) + "', '" + str(email) + "', '" + str(physical_address) + "', '" + str(ssn) + "', '" + str(owner_dob) + "');"

        newOwnerQuery = get_insertOwner_query()
        cursor.execute(get_insertOwner_query())
        cnx.commit()
        ownerID = cursor.lastrowid
        print("last row: " + str(ownerID))

        session['owner_id'] = str(ownerID)
        print("session: " + session['owner_id'])

        return redirect(url_for('newPet'))

    return render_template('newOwner.html')

@app.route('/newPet', methods=['GET', 'POST'])
def newPet():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        #how to get FK for ownerId?
        pet_name=request.form['pet_name']
        owner_id=session['owner_id']
        pet_type=request.form['pet_type']
        pet_dob=request.form['pet_dob']
        weight=request.form['weight']
        height=request.form['height']
        sex=request.form['sex']

        def get_insertPet_query(): 
            return "INSERT INTO Pet (Name, OwnerID, PetType, DOB, Weight, Height, Sex) VALUES ('" + str(pet_name) + "', '" + owner_id + "', '" + str(pet_type) + "', '" + str(pet_dob) + "', '" + str(weight) + "', '" + str(height) + "', '" + str(sex) + "');"

        newPetQuery = get_insertPet_query()
        cursor.execute(get_insertPet_query())
        cnx.commit()

        return redirect(url_for('pet'))
    
    return render_template('newPet.html')

@app.route('/illnesses', methods=['GET', 'POST'])
def illnesses():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":

        def get_illnessResults_query(illnessID, illnessName):
            return "SELECT IllnessID, IllnessName FROM Illness WHERE IllnessID = '" + str(illnessID) + "' OR IllnessName = '" + str(illnessName) + "';"

        illnessID=request.form['illnessID']
        illnessName=request.form['illnessName']
        illnessResultsQuery = get_illnessResults_query(illnessID, illnessName)
        print("Illness Results Query: " + illnessResultsQuery)

        cnx.commit()
        rows = []
        try:
            for result in cursor.execute(illnessResultsQuery, multi = True) :
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(result.statement))
                    results = result.fetchall()
                    for r in results:
                        print(r)
                else:
                    print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
        except:
            print("Exception")

        return redirect(url_for('illnessResults', rows=results))

    cursor.close()
    cnx.close()

    return render_template('illnesses.html')

@app.route('/illnessResults', methods=['GET', 'POST'])
def illnessResults():
    if request.method == "POST":
        print("Made it to illness results")
    return render_template('illnessResults.html', rows=request.args.get('rows'))

@app.route('/surgeries', methods=['GET', 'POST'])
def surgeries():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":

        def get_surgeryResults_query(surgeryID, surgeryName):
            return "SELECT SurgeryID, SurgeryName FROM Surgery WHERE SurgeryID = '" + str(surgeryID) + "' OR SurgeryName = '" + str(surgeryName) + "';"

        surgeryID=request.form['surgeryID']
        surgeryName=request.form['surgeryName']
        surgeryResultsQuery = get_surgeryResults_query(surgeryID, surgeryName)
        print("Surgery Results Query: " + surgeryResultsQuery)

        cnx.commit()
        rows = []
        try:
            for result in cursor.execute(surgeryResultsQuery, multi = True) :
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(result.statement))
                    results = result.fetchall()
                    for r in results:
                        print(r)
                else:
                    print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
        except:
            print("Exception")

        return redirect(url_for('surgeryResults', rows=results))

    cursor.close()
    cnx.close()

    return render_template('surgeries.html')

@app.route('/surgeryResults', methods=['GET', 'POST'])
def surgeryResults():
    if request.method == "POST":
        print("Made it to surgery results")
    return render_template('surgeryResults.html', rows=request.args.get('rows'))

@app.route('/prescriptions', methods=['GET', 'POST'])
def prescriptions():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":

        def get_prescriptionResults_query(prescriptionID, prescriptionName):
            return "SELECT PrescriptionID, PrescriptionName FROM Prescription WHERE PrescriptionID = '" + str(prescriptionID) + "' OR PrescriptionName = '" + str(prescriptionName) + "';"

        prescriptionID=request.form['prescriptionID']
        prescriptionName=request.form['prescriptionName']
        prescriptionResultsQuery = get_prescriptionResults_query(prescriptionID, prescriptionName)
        print("Prescription Results Query: " + prescriptionResultsQuery)

        cnx.commit()
        rows = []
        try:
            for result in cursor.execute(prescriptionResultsQuery, multi = True) :
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(result.statement))
                    results = result.fetchall()
                    for r in results:
                        print(r)
                else:
                    print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
        except:
            print("Exception")

        return redirect(url_for('prescriptionResults', rows=results))

    cursor.close()
    cnx.close()

    return render_template('prescriptions.html')

@app.route('/prescriptionResults', methods=['GET', 'POST'])
def prescriptionResults():
    if request.method == "POST":
        print("Made it to prescription results")
    return render_template('prescriptionResults.html', rows=request.args.get('rows'))

@app.route('/vaccinations', methods=['GET', 'POST'])
def vaccinations():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":

        def get_vaccinationResults_query(vaccinationID, vaccinationName):
            return "SELECT VacID, VacName FROM Vaccination WHERE VacID = '" + str(vaccinationID) + "' OR VacName = '" + str(vaccinationName) + "';"

        vaccinationID=request.form['vaccinationID']
        vaccinationName=request.form['vaccinationName']
        vaccinationResultsQuery = get_vaccinationResults_query(vaccinationID, vaccinationName)
        print("Vaccination Results Query: " + vaccinationResultsQuery)

        cnx.commit()
        rows = []
        try:
            for result in cursor.execute(vaccinationResultsQuery, multi = True) :
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(result.statement))
                    results = result.fetchall()
                    for r in results:
                        print(r)
                else:
                    print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
        except:
            print("Exception")

        return redirect(url_for('vaccinationResults', rows=results))

    cursor.close()
    cnx.close()

    return render_template('vaccinations.html')

@app.route('/vaccinationResults', methods=['GET', 'POST'])
def vaccinationResults():
    if request.method == "POST":
        print("Made it to vaccination results")
    return render_template('vaccinationResults.html', rows=request.args.get('rows'))