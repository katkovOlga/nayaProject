#test case file that would run all functionality as GUI
#  Olga Katkov 22/08/22

import Ui_methods
import configuration as c
from  ClassReciept import Receipt
from  PatientClass import Patient
import ProducerReq as pr
import pandas as pd
import time

work="start"
drugId=""
while work != "Q":
    pat1= Patient()
    pat1.TZ=input("Hello, Doctor!/n Find the Patient-insert TZ \n")
    resDf = pd.DataFrame()
    pat1.TZ
    pat1.findPatient()
    print("Patient chronic Diseases List = ")
    print(pat1.DiseasesHistory)
    print("Patient Constant Drugs List = ")
    print( pat1.ConstantDrugsList)
    work=input("Hi, Doctor! What you are going to do? (add NewD disease-(insert D ) or add new medicine (insert M)?  or exit (insert Q)\n ")
    if (work.upper() =='D'):
        diag = input("Please insert new diagnose for patient \n")
        pat1.addDiagnose(diag)
        work =("Hi, Doctor! Do you want to continue to medicine suggestion? Insert M\n")

    if (work.upper() =='M'):
        while work.upper() =='M':
            med=input("Please insert new medicine for patient \n")
            drugId,resDf = Ui_methods.checkDrugKf(med,pat1)
            print(resDf)
            time.sleep(5)
            work = input("hi Doctor, Do you really want to create receipt to this medicine for patient or test another drug \n , for receipt inset R for another medicine insert M or exit (insert Q) \n")
            if (work.upper() =='R'):
                rec1=Receipt()
                rec1.PatientTz=pat1.TZ
                rec1.DrugName=med.lower()
                rec1.DrugId=drugId
                rec1.lstDiag =pat1.DiseasesHistory
                rec1.DfInteraction =resDf
                rec1.DoctorL=c.CurrentDoctorLic
                rec1.lstDrugs=pat1.ConstantDrugsList
                rec1.PatientFName=pat1.FirstName
                rec1.PatientLName=pat1.LastName
                rec1.PatientKH=pat1.KupatHolim
                rec1.DrugDose="500"
                rec1.PatientBD = pat1.Birthdate
                rec1.crReceipt()
                pat1.addDrugToPatientDrugList(med.lower())

    if (work.upper() =='Q'):
        break
