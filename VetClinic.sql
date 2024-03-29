CREATE SCHEMA VetClinic;
USE VetClinic;

CREATE TABLE Pet (
PetID INT NOT NULL,
Name VARCHAR(25) NOT NULL,
OwnerID INT NOT NULL,
PetType VARCHAR(25) NOT NULL,
DOB CHAR(8) NULL,
Weight INT NOT NULL,
Height INT NULL,
Sex CHAR(1) NULL,
PRIMARY KEY(PetID));

CREATE TABLE Breed (
PetID INT NOT NULL,
PetType VARCHAR(25) NOT NULL,
Main VARCHAR(30) NOT NULL,
Secondary VARCHAR(30) NULL,
PRIMARY KEY(PetID));

CREATE TABLE Illness (
IllnessID INT NOT NULL,
IllnessName VARCHAR(40) NOT NULL,
PRIMARY KEY(IllnessID));

CREATE TABLE Vaccination (
VacID INT NOT NULL,
VacName VARCHAR(30) NOT NULL,
Dog VARCHAR(10) NULL,
Cat VARCHAR(10) NULL,
Turtle VARCHAR(10) NULL,
Bird VARCHAR(10) NULL,
Rabbit VARCHAR(10) NULL,
Snake VARCHAR(10) NULL,
PRIMARY KEY(VacID));

CREATE TABLE isDiagnosedWith (
IllnessID INT NOT NULL,
PetID INT NOT NULL,
IllnessDate CHAR(10) NOT NULL,
PRIMARY KEY(IllnessID));

CREATE TABLE Treatment (
IllnessID INT NOT NULL,
PetType VARCHAR(25) NOT NULL,
TreatmentPlan VARCHAR(50) NULL,
PRIMARY KEY(IllnessID, PetType));

CREATE TABLE Prescription (
PrescriptionID INT NOT NULL,
PrescriptionName VARCHAR(40) NOT NULL,
PRIMARY KEY(PrescriptionID));

CREATE TABLE isPrescribed (
PrescriptionID INT NOT NULL,
PetID INT NOT NULL,
DatePrescribed CHAR(10) NOT NULL,
PRIMARY KEY(PrescriptionID, PetID));

CREATE TABLE isAdministered (
VacID INT NOT NULL,
PetID INT NOT NULL,
VaccinationDate CHAR(10) NOT NULL,
PRIMARY KEY(VacID, PetID));

CREATE TABLE Owner ( 
OwnerID INT NOT NULL,
FirstName VARCHAR(30) NOT NULL,
LastName VARCHAR(30) NOT NULL,
InsuranceNumber VARCHAR(20) NULL,
InsuranceCompany VARCHAR(40) NULL,
PhoneNumber INT NOT NULL,
Email VARCHAR(40) NULL,
PhysicalAddress VARCHAR(75) NOT NULL,
SSN INT NOT NULL,
DOB VARCHAR(10) NULL,
PRIMARY KEY(OwnerID));

CREATE TABLE Surgery (
SurgeryID INT NOT NULL,
SurgeryName VARCHAR(40) NOT NULL,
PRIMARY KEY(SurgeryID));

CREATE TABLE isTreatedWith (
SurgeryID INT NOT NULL,
PetID INT NOT NULL,
SurgeryDate VARCHAR(10) NOT NULL,
PRIMARY KEY(SurgeryID, PetID));

ALTER TABLE Pet
ADD FOREIGN KEY (OwnerID) REFERENCES Owner(OwnerID);

INSERT INTO PET (PetID, Name, OwnerID, PetType, DOB, Weight, Height, Sex) VALUES (1, 'Gary', 1, 'Dog', '04/11/18', 38, 15, 'M');
INSERT INTO Owner (OwnerID, FirstName, LastName, InsuranceNumber, InsuranceCompany, PhoneNumber, Email, PhysicalAddress, SSN, DOB) VALUES (1, 'Sarah', 'Dubbert', '1122334455', 'Good Insurance Company', 1234567890, 'sarah@mail.com', '123 Maple St. Kansas City, MO 64521', 87654322, '04/17/97');

SELECT Pet.PetID, Pet.Name, Owner.FirstName, Owner.LastName, Pet.PetType, Pet.DOB, Pet.Weight, Pet.Height, Pet.Sex FROM Pet JOIN Owner ON Pet.OwnerID = Owner.OwnerID WHERE LastName = '' OR FirstName = '' OR PetID = '1' OR Name = '' OR Pet.DOB = '';

ALTER TABLE Owner MODIFY PhoneNumber VARCHAR(12) NOT NULL;
ALTER TABLE Owner MODIFY SSN VARCHAR(12) NOT NULL;

SELECT * FROM Owner;
SELECT * FROM Pet;
DELETE FROM Owner WHERE OwnerID > 0;
DELETE FROM Pet WHERE PetID > 0;


INSERT INTO Illness (IllnessID, IllnessName) VALUES (1, "Cancer"), (2, "Diabetes"), (3, "Fleas/Ticks"), (4, "Arthritis"), (5, "Skin Infection");
INSERT INTO Surgery (SurgeryID, SurgeryName) VALUES (1, "Neutering"), (2, "Internal (foreign object)"), (3, "Dental"), (4, "Cataract"), (5, "Wound Repair"), (6, "Spaying");
INSERT INTO Prescription (PrescriptionID, PrescriptionName) VALUES (1, "Antibiotic"), (2, "Non-steroidal anti-inflammatory"), (3, "Antiparasitic"), (4, "Steroid"), (5, "Pain reliever");
INSERT INTO Vaccination (VacID, VacName) VALUES (1, "Rabies"), (2, "DAPP"), (3, "Bordetella"), (4, "FVRCP"), (5, "FeLV");

DELETE FROM Owner WHERE OwnerID > 0;
DELETE FROM Pet WHERE PetID > 0;
alter table Pet drop foreign key pet_ibfk_1;
alter table Breed drop foreign key breed_ibfk_1;
ALTER TABLE Pet MODIFY PetID INT NOT NULL AUTO_INCREMENT;
ALTER TABLE Owner MODIFY OwnerID INT NOT NULL AUTO_INCREMENT;
ALTER TABLE Pet
ADD FOREIGN KEY (OwnerID) REFERENCES Owner(OwnerID);

ALTER TABLE isPrescribed ADD COLUMN Description VARCHAR(75) NULL;
DROP TABLE Breed;

CREATE TABLE Breed (
PetID INT NOT NULL,
Breed VARCHAR(30) NOT NULL,
PRIMARY KEY(PetID));

ALTER TABLE Breed ADD FOREIGN KEY (PetID) REFERENCES Pet(PetID);
ALTER TABLE isDiagnosedWith ADD FOREIGN KEY (IllnessID) REFERENCES Illness(IllnessID);
ALTER TABLE isPrescribed ADD FOREIGN KEY (PrescriptionID) REFERENCES Prescription(PrescriptionID);
ALTER TABLE isAdministered ADD FOREIGN KEY (VacID) REFERENCES Vaccination(VacID);
ALTER TABLE isTreatedWith ADD FOREIGN KEY (SurgeryID) REFERENCES Surgery(SurgeryID);

ALTER TABLE isDiagnosedWith ADD FOREIGN KEY (PetID) REFERENCES Pet(PetID);
ALTER TABLE isPrescribed ADD FOREIGN KEY (PetID) REFERENCES Pet(PetID);
ALTER TABLE isAdministered ADD FOREIGN KEY (PetID) REFERENCES Pet(PetID);
ALTER TABLE isTreatedWith ADD FOREIGN KEY (PetID) REFERENCES Pet(PetID);

ALTER TABLE Treatment ADD FOREIGN KEY (IllnessID) REFERENCES Illness(IllnessID);

SELECT Name, DOB, Weight, Height FROM Pet WHERE PetID = '1';

