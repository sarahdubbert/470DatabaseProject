from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from creds import usr, pw, hst, db


app = Flask(__name__)
app.secret_key = "SecretKey"


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
        button=request.form['action']

        if button == "getAll":
            def get_petResults_query():
                return "SELECT Pet.PetID, Pet.Name, Owner.FirstName, Owner.LastName, Pet.PetType, Pet.DOB, Pet.Weight, Pet.Height, Pet.Sex FROM Pet JOIN Owner ON Pet.OwnerID = Owner.OwnerID;"
        elif button == "submit":
            def get_petResults_query():
                return "SELECT Pet.PetID, Pet.Name, Owner.FirstName, Owner.LastName, Pet.PetType, Pet.DOB, Pet.Weight, Pet.Height, Pet.Sex FROM Pet JOIN Owner ON Pet.OwnerID = Owner.OwnerID WHERE Name = '" + str(petName) + "' OR PetType = '" + str(petType) + "' OR Weight = '" + str(petWeight) + "' OR Height = '" + str(petHeight) + "' OR Sex = '" + str(petSex) + "' OR Pet.DOB = '" + str(petDOB) + "' OR FirstName = '" + str(ownerFirst) + "' OR LastName = '" +str(ownerLast) + "';"
            
            petName=request.form['petName']
            petType=request.form['petType']
            petWeight=request.form['petWeight']
            petHeight=request.form['petHeight']
            petSex=request.form['petSex']
            petDOB=request.form['petDOB']
            ownerFirst=request.form['ownerFirst']
            ownerLast=request.form['ownerLast']
        
        petResultsQuery = get_petResults_query()
        print("Pet Results Query: " + petResultsQuery)

        cnx.commit()
        ids = []
        pNames = []
        fNames = []
        lNames = []
        types = []
        dobs = []
        weights = []
        heights = []
        sex = []

        try:
            for result in cursor.execute(petResultsQuery, multi = True) :
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(result.statement))
                    results = result.fetchall()
                    for r in results:
                        ids.append(r[0])
                        pNames.append(r[1])
                        fNames.append(r[2])
                        lNames.append(r[3])
                        types.append(r[4])
                        dobs.append(r[5])
                        weights.append(r[6])
                        heights.append(r[7])
                        sex.append(r[8])
                else:
                    print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
        except:
            print("Exception")

        return render_template('petResults.html', ids=ids, pNames=pNames, fNames=fNames, lNames=lNames, types=types, dobs=dobs, weights=weights, heights=heights, sex=sex, len=len(ids))

    cursor.close()
    cnx.close()

    return render_template('pet.html')

@app.route('/petResults', methods=['GET', 'POST'])
def petResults():
    if request.method == "POST":
        print("Made it to results page")
    return render_template('petResults.html', rows=request.args.get('rows'))

@app.route('/newPet', methods=['GET', 'POST'])
def newPet():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        print('owner')
        owner = request.form['owner']
        print(owner)
        # def getOwner():       
            # return(owner)
        #how to get FK for ownerId?
        pet_name=request.form['pet_name']
        owner_id=session['owner_id']
        pet_type=request.form['pet_type']
        pet_dob=request.form['pet_dob']
        weight=request.form['weight']
        height=request.form['height']
        sex=request.form['sex']
        # print(getOwner())
        def get_insertPet_query(): 
            return "INSERT INTO Pet (Name, OwnerID, PetType, DOB, Weight, Height, Sex) VALUES ('" + str(pet_name) + "', '" + owner_id + "', '" + str(pet_type) + "', '" + str(pet_dob) + "', '" + str(weight) + "', '" + str(height) + "', '" + str(sex) + "');"

        newPetQuery = get_insertPet_query()
        cursor.execute(get_insertPet_query())
        cnx.commit()

        return redirect(url_for('pet'))
    
    def getOwners():
        return "SELECT FirstName, LastName FROM Owner;"
    
    ownerResultsQuery = getOwners()
    print("Owner Results Query: " + ownerResultsQuery)

    cnx.commit()
    names = []

    try:
        for result in cursor.execute(ownerResultsQuery, multi = True) :
            if result.with_rows:
                print("Rows produced by statement '{}':".format(result.statement))
                results = result.fetchall()
                for r in results:
                    names.append(r[0] + ' ' + r[1])
            else:
                print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
    except:
        print("Exception")

    return render_template('newPet.html', names=names, len=len(names))

@app.route('/updatePet', methods=['GET', 'POST'])
def updatePet():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        button=request.form['action']

        petID=request.form['petID']
        if button == "load":
            print('load button clicked')

            def get_petInfo_query(petID): 
                return "SELECT Name, DOB, Weight, Height FROM Pet WHERE PetID = '" + str(petID) + "';"

            loadPetInfo = get_petInfo_query(petID)
            print(loadPetInfo)

            cnx.commit()
            rows = []
            try:
                for result in cursor.execute(loadPetInfo, multi = True) :
                    if result.with_rows:
                        print("Rows produced by statement '{}':".format(result.statement))
                        results = result.fetchall()
                        for r in results:
                            print(r)
                    else:
                        print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
            except:
                print("Exception")
            return render_template('updatePet.html', name=results[0][0], dob=results[0][1], weight=results[0][2], height=results[0][3])
        elif button == "submit":
            print('update button clicked')

            def set_petInfo_query():
                return "UPDATE Pet SET Name = '" + str(name) + "', DOB = '" + str(dob) + "', Weight = '" + str(weight) + "', Height = '" + str(height) + "' WHERE PetID = '" + str(petID) + "';"
        
            name=request.form['name']
            dob=request.form['dob']
            weight=request.form['weight']
            height=request.form['height']
            petID=request.form['petID']

            updatePetInfo = set_petInfo_query()
            print(updatePetInfo)

            cursor.execute(set_petInfo_query())
            cnx.commit()
        
    cursor.close()
    cnx.close()
    
    return render_template('updatePet.html')

@app.route('/owner', methods=['GET', 'POST'])
def owner():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        button=request.form['action']

        if button == "getAll":
            def get_ownerResults_query():
                return "SELECT OwnerId, FirstName, LastName, InsuranceNumber, InsuranceCompany, PhoneNumber, Email, PhysicalAddress, SSN, DOB FROM Owner;"
        elif button == "submit":
            def get_ownerResults_query():
                return "SELECT OwnerId, FirstName, LastName, InsuranceNumber, InsuranceCompany, PhoneNumber, Email, PhysicalAddress, SSN, DOB FROM Owner WHERE FirstName = '" + str(ownerFirst) + "' OR LastName = '" + str(ownerLast) + "' OR Owner.DOB = '" + str(ownerDOB) + "' OR InsuranceCompany = '" + str(insComp) + "' OR PhoneNumber = '" + str(phone) + "' OR Email = '" + str(email) + "' OR PhysicalAddress = '" + str(address) + "';"
                
            ownerFirst=request.form['ownerFirst']
            ownerLast=request.form['ownerLast']
            ownerDOB=request.form['ownerDOB']
            insComp=request.form['insComp']
            phone=request.form['phone']
            email=request.form['email']
            address=request.form['address']
        
        ownerResultsQuery = get_ownerResults_query()
        print("Owner Results Query: " + ownerResultsQuery)

        cnx.commit()
        ids = []
        fNames = []
        lNames = []
        insNums = []
        insComps = []
        phones = []
        emails = []
        addresses = []
        ssns = []
        dobs = []

        try:
            for result in cursor.execute(ownerResultsQuery, multi = True) :
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(result.statement))
                    results = result.fetchall()
                    for r in results:
                        ids.append(r[0])
                        fNames.append(r[1])
                        lNames.append(r[2])
                        insNums.append(r[3])
                        insComps.append(r[4])
                        phones.append(r[5])
                        emails.append(r[6])
                        addresses.append(r[7])
                        ssns.append(r[8])
                        dobs.append(r[9])
                else:
                    print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
        except:
            print("Exception")

        return render_template('ownerResults.html', ids=ids, fNames=fNames, lNames=lNames, insNums=insNums, insComps=insComps, phones=phones, emails=emails, addresses=addresses, ssns=ssns, dobs=dobs, len=len(ids))

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

@app.route('/updateOwner', methods=['GET', 'POST'])
def updateOwner():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        button=request.form['action']

        ownerID=request.form['ownerID']
        if button == "load":
            print('load button clicked')

            def get_ownerInfo_query(): 
                return "SELECT FirstName, LastName, InsuranceNumber, InsuranceCompany, PhoneNumber, Email, PhysicalAddress FROM Owner WHERE OwnerID = '" + str(ownerID) + "';"

            loadOwnerInfo = get_ownerInfo_query()
            print(loadOwnerInfo)

            cnx.commit()
            rows = []
            try:
                for result in cursor.execute(loadOwnerInfo, multi = True) :
                    if result.with_rows:
                        print("Rows produced by statement '{}':".format(result.statement))
                        results = result.fetchall()
                        for r in results:
                            print(r)
                    else:
                        print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
            except:
                print("Exception")
            return render_template('updateOwner.html', ownerFirst=results[0][0], ownerLast=results[0][1], insNum=results[0][2], insComp=results[0][3], phone=results[0][4], email=results[0][5], address=results[0][6])
        elif button == "submit":
            print('update button clicked')

            def set_ownerInfo_query():
                return "UPDATE Owner SET FirstName = '" + str(ownerFirst) + "', LastName = '" + str(ownerLast) + "', InsuranceNumber = '" + str(insNum) + "', InsuranceCompany = '" + str(insComp) + "', PhoneNumber = '" + str(phone) + "', Email = '" + str(email) + "', PhysicalAddress = '" + str(address) + "' WHERE OwnerID = '" + str(ownerID) + "';"
        
            ownerFirst=request.form['ownerFirst']
            ownerLast=request.form['ownerLast']
            insNum=request.form['insNum']
            insComp=request.form['insComp']
            phone=request.form['phone']
            email=request.form['email']
            address=request.form['address']

            updateOwnerInfo = set_ownerInfo_query()
            print(updateOwnerInfo)

            cursor.execute(set_ownerInfo_query())
            cnx.commit()
        
    cursor.close()
    cnx.close()
    
    return render_template('updateOwner.html')

@app.route('/illnesses', methods=['GET', 'POST'])
def illnesses():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        button=request.form['action']

        if button == "getAll":
            def get_illnessResults_query():
                return "SELECT IllnessID, IllnessName FROM Illness;"
        elif button == "submit":
            def get_illnessResults_query():
                return "SELECT IllnessID, IllnessName FROM Illness WHERE IllnessID = '" + str(illnessID) + "' OR IllnessName = '" + str(illnessName) + "';"
            illnessID=request.form['illnessID']
            illnessName=request.form['illnessName']
        
        illnessResultsQuery = get_illnessResults_query()
        print("Illness Results Query: " + illnessResultsQuery)

        cnx.commit()
        ids = []
        names = []
        try:
            for result in cursor.execute(illnessResultsQuery, multi = True) :
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(result.statement))
                    results = result.fetchall()
                    for r in results:
                        ids.append(r[0])
                        names.append(r[1])
                else:
                    print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
        except:
            print("Exception")

        return render_template('illnessResults.html', ids=ids, names=names, len=len(ids))

    cursor.close()
    cnx.close()

    return render_template('illnesses.html')

@app.route('/newIllness', methods=['GET', 'POST'])
def newIllness():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        pet_id=request.form['pet_id']
        illness_id=request.form['illness_id']
        illness_date=request.form['illness_date']

        def get_insertIllness_query():
            return "INSERT INTO isDiagnosedWith (IllnessID, PetID, IllnessDate) VALUES ('" + str(illness_id) + "', '" + str(pet_id) + "', '" + str(illness_date) + "');"

        cursor.execute(get_insertIllness_query())
        cnx.commit()

    return render_template('newIllness.html')

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
        button=request.form['action']

        if button == "getAll":
            def get_surgeryResults_query():
                return "SELECT SurgeryID, SurgeryName FROM Surgery;"
        elif button == "submit":
            def get_surgeryResults_query():
                return "SELECT SurgeryID, SurgeryName FROM Surgery WHERE SurgeryID = '" + str(surgeryID) + "' OR SurgeryName = '" + str(surgeryName) + "';"
            surgeryID=request.form['surgeryID']
            surgeryName=request.form['surgeryName']
        
        surgeryResultsQuery = get_surgeryResults_query()
        print("Surgery Results Query: " + surgeryResultsQuery)

        cnx.commit()
        ids = []
        names = []
        try:
            for result in cursor.execute(surgeryResultsQuery, multi = True) :
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(result.statement))
                    results = result.fetchall()
                    for r in results:
                        ids.append(r[0])
                        names.append(r[1])
                else:
                    print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
        except:
            print("Exception")

        return render_template('surgeryResults.html', ids=ids, names=names, len=len(ids))

    cursor.close()
    cnx.close()

    return render_template('surgeries.html')

@app.route('/newSurgery', methods=['GET', 'POST'])
def newSurgery():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        pet_id=request.form['pet_id']
        surgery_id=request.form['surgery_id']
        surgery_date=request.form['surgery_date']

        def get_insertSurgery_query():
            return "INSERT INTO isTreatedWith (SurgeryID, PetID, SurgeryDate) VALUES ('" + str(surgery_id) + "', '" + str(pet_id) + "', '" + str(surgery_date) + "');"

        cursor.execute(get_insertSurgery_query())
        cnx.commit()

    return render_template('newSurgery.html')

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
        button=request.form['action']

        if button == "getAll":
            def get_prescriptionResults_query():
                return "SELECT PrescriptionID, PrescriptionName FROM Prescription;"
        elif button == "submit":
            def get_prescriptionResults_query():
                return "SELECT PrescriptionID, PrescriptionName FROM Prescription WHERE PrescriptionID = '" + str(prescriptionID) + "' OR PrescriptionName = '" + str(prescriptionName) + "';"
            prescriptionID=request.form['prescriptionID']
            prescriptionName=request.form['prescriptionName']
        
        prescriptionResultsQuery = get_prescriptionResults_query()
        print("Prescription Results Query: " + prescriptionResultsQuery)

        cnx.commit()
        ids = []
        names = []
        try:
            for result in cursor.execute(prescriptionResultsQuery, multi = True) :
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(result.statement))
                    results = result.fetchall()
                    for r in results:
                        ids.append(r[0])
                        names.append(r[1])
                else:
                    print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
        except:
            print("Exception")

        return render_template('prescriptionResults.html', ids=ids, names=names, len=len(ids))

    cursor.close()
    cnx.close()

    return render_template('prescriptions.html')

@app.route('/newPrescription', methods=['GET', 'POST'])
def newPrescription():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        pet_id=request.form['pet_id']
        prescription_id=request.form['prescription_id']
        date_prescribed=request.form['date_prescribed']
        description=request.form['description']

        def get_insertPrescription_query():
            return "INSERT INTO isPrescribed (PrescriptionID, PetID, DatePrescribed, Description) VALUES ('" + str(prescription_id) + "', '" + str(pet_id) + "', '" + str(date_prescribed) + "', '" + str(description) + "');"

        cursor.execute(get_insertPrescription_query())
        cnx.commit()

    return render_template('newPrescription.html')


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
        button=request.form['action']

        if button == "getAll":
            def get_vaccinationResults_query():
                return "SELECT VacID, VacName FROM Vaccination;"
        elif button == "submit":
            def get_vaccinationResults_query():
                return "SELECT VacID, VacName FROM Vaccination WHERE VacID = '" + str(vaccinationID) + "' OR VacName = '" + str(vaccinationName) + "';"
            vaccinationID=request.form['vaccinationID']
            vaccinationName=request.form['vaccinationName']
        
        vaccinationResultsQuery = get_vaccinationResults_query()
        print("Vaccination Results Query: " + vaccinationResultsQuery)

        cnx.commit()
        ids = []
        names = []
        try:
            for result in cursor.execute(vaccinationResultsQuery, multi = True) :
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(result.statement))
                    results = result.fetchall()
                    for r in results:
                        ids.append(r[0])
                        names.append(r[1])
                else:
                    print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
        except:
            print("Exception")

        return render_template('vaccinationResults.html', ids=ids, names=names, len=len(ids))
    
    cursor.close()
    cnx.close()

    return render_template('vaccinations.html')

@app.route('/newVaccination', methods=['GET', 'POST'])
def newVaccination():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        pet_id=request.form['pet_id']
        vaccination_id=request.form['vaccination_id']
        vaccination_date=request.form['vaccination_date']

        def get_insertVaccination_query():
            return "INSERT INTO isAdministered (VacID, PetID, VaccinationDate) VALUES ('" + str(vaccination_id) + "', '" + str(pet_id) + "', '" + str(vaccination_date) + "');"

        cursor.execute(get_insertVaccination_query())
        cnx.commit()

    return render_template('newVaccination.html')

@app.route('/vaccinationResults', methods=['GET', 'POST'])
def vaccinationResults():
    if request.method == "POST":
        print("Made it to vaccination results")
    return render_template('vaccinationResults.html', rows=request.args.get('rows'))

@app.route('/deletePet', methods=['GET', 'POST'])
def deletePet():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        remove_pet_id=request.form['remove_pet_id']

        def get_removePet_query():
            return "DELETE FROM Pet WHERE PetID = '" + str(remove_pet_id) + "';"

        cursor.execute(get_removePet_query())
        cnx.commit()
          
    return render_template('deletePet.html')

@app.route('/deleteOwner', methods=['GET', 'POST'])
def deleteOwner():
    cnx = mysql.connector.connect(user=usr, password=pw, host=hst, database=db, use_pure=True)
    cursor = cnx.cursor()
    if request.method == "POST":
        remove_owner_id=request.form['remove_owner_id']
        
        def get_removeOwner_query():
            return "DELETE FROM Owner WHERE OwnerID = '" + str(remove_owner_id) + "';"

        cursor.execute(get_removeOwner_query())
        cnx.commit()
          
    return render_template('deleteOwner.html')