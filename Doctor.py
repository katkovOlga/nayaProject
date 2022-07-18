#  main doctor interface ,
# started as first project on 0622
# Olga Katkov
#
#

import pandas as pd
#Doctor Wook room


import sys
from MedcineClass import Medcine
from patient import get_diseases_for_patient_by_id
#import Patients

def checkNewTretment(drugName,DiagLst,mainDiagnosis):
    #find drug in list of drugs,
    #get create instance medcine from found
    #run check methods
    data=""

    with open(Medcine.fname, 'r') as f:
        data=f.read()
        f.close()
    print(data)
    lstxml = data.split('\n')
    lstdf = [pd.read_xml(xml) for xml in lstxml if len(xml)>20]
    df = pd.concat(lstdf, axis=0)
    print(df)
    #dfDrug = df.where(df['Name'] == drugName)
    dfDrug = df.loc[df['Name']== drugName]
    drug = Medcine()
    drug.Name = drugName
    drug.Contraindications  = dfDrug['Contraindications'].tolist()[0].split(',')
    drug.Indications = dfDrug['Indications'].tolist()[0].split(',')
    result, level, dfCoop = drug.IsIndicated( mainDiagnosis.lower(), DiagLst)
    return result, level, dfCoop





def findPatient(IdNum):
    #ora return list of chronic diagnosis
    # ora return list of chronic diagnosis
     #lstRes = ['heart failure', 'myocardial infarction']
     debug_flg = False
     #ls= Patient.get_diseasesFrom()
     lstRes = get_diseases_for_patient_by_id(debug_flg, IdNum)

     if (debug_flg):
            print(lstRes)
     return lstRes
Diagnosis = ['pregnancy','allergy','angina','tonsillitis','diabets','bronchitis','heart attack',
             'influenza','pneumonia','gipertoniya','asthma','heart disease','heart failure','myocardial infarction','apoplexy','Liver disease',
             'kidney disease','pain syndrome','arthritis','cancer','holesterol high','peptic ulcer of the stomach','Crohn''s disease','hemophilia','pain syndrome']
work=input("Hello, Doctor!/n What you are going to do? (addNewPatient-(insert P ) or insert new medcine (insert M) or new diagnosis add (insert D)? ")
if (work.upper() =='P'):
    #  ora
    pass
elif (work.upper() =='M'):
    myDrag = Medcine()
    #print(myDrag.fname)
    myDrag.ActiveComponent=input("Insert new medcine Active Component: ")
    myDrag.Company=input("Insert new medcine Producer Company: ")
    myDrag.pillDose=input("Insert new medcine pill Dose: ")
    myDrag.Contraindications=input("Insert new medcine Contraindications separeted by ,: ")
    myDrag.Indications=input("Insert new medcine Iindications separeted by ,: ")
    myDrag.MedcineConflictList=input("Insert new medcine Drag Conflict list separeted by ,: ")
    myDrag.MedcineSynergyList=input("Insert new medcine Drag Synergy list separeted by ,: ")
    myDrag.Name=input("Insert new medcine Name: ")
    print(myDrag)
    myDrag.newMedcine()
elif (work.upper() =='D'):
    #v read patient
    #get his diagnosis+ treatment lists
    #check Conflicts
    tz = input("Insert patient Id :")
    mainDiag = input("Insert current Diagnosis :")

    while mainDiag not in Diagnosis:
        mainDiag =input('not existing diagnosis, please use 1 from ' + ', '.join(Diagnosis) + " or type exit:")
        if mainDiag.lower() == 'exit':
            break
    if mainDiag.lower() != 'exit':
        newDrag = input("insert you recommendated drug: ")
        dfRes = pd.DataFrame()
        #lstDiag= findPatient(tz)
        strD = input('insert list of chronic diseases:  ')
        lstDiag =strD.split(',')
        result, level, dfCoop = checkNewTretment(newDrag, lstDiag, mainDiag)
        if (result == True) and (level>1):
           print ("Indicated Excellent")
        elif (result == True)  and (level>=0):
            print("Indicated Good")
            print (dfCoop)
        elif (result == False):
            print("is not Indicated ")
        else:
            print('please see conflicts details:')
            print(dfCoop)



        # result for doctor + recept < add drag to medcines list, diagnosis to ilness list
else:
  print ("Illegal work mode")
