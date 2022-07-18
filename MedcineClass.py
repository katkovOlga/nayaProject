#Olga Katkov
#started 060622
#doctor's warning about a possible drug conflict
import pandas as pd
import sys
import numpy as np


class Medcine:
    ActiveComponent=''  #List in future
    Name=''
    Company=''
    Contraindications=[]
    Indications=[]
    fname = "drugs.txt"
    MedcineConflictList=[]
    MedcineSynergyList=[]
    PillDose=0
    apiId=''


    #def __init__(self, ActiveComponent,Name,Company,PillDose, Contraindications,Indications,MedcineConflictSynergyList):
    def __init__(self):
       # self.fields = fields
        pass


    def newMedcine(self):
        # new Medcine saved to file drugs, each record is XML
        # records devided by newline
        #  self.n_records += 1
        medcine={'ActiveComponent':self.ActiveComponent,'Company':self.Company,'Name': self.Name,'PillDose':self.PillDose,
       'Indications':self.Indications,  'Contraindications':self.Contraindications,'MedcineConflictList':self.MedcineConflictList,
        'MedcineSynergyList':self.MedcineSynergyList}
        # df= pd.DataFrame(self.ActiveComponent,self.Company,self.Name,self.PillDose,self.Indications,self.Contraindications,self.MedcineConflictSynergyList)
        # df = pd.DataFrame(medcine,index='Name')#index=range(1))
        df = pd.DataFrame(medcine,index=range(1))
        df.set_index('Name', inplace=True)
        # df = pd.DataFrame(data=medcine, index= self.Name)
        xml= df.to_xml(root_name='medcines', row_name='medcine', ).replace('\n','') + "\n"
        print(type(xml))
        print(xml)
        with open(self.fname, 'a') as f:
          f.write(xml)
          f.close()

    def  IsSynergyOrConflict(self,ListOfUsedDrugs):
        #pandas.read_xml
        typeRes= 'positive'
        levRes=2
        return  typeRes, levRes





    def IsIndicated( self,MainDiagnosis, listOfChronicDiagnosis):
      # return Boolean Indicated and range of indication, negative range- contraindicatedc,
      # positive 1-only main, >1- main+chronic ,
      #3d output parameter dataframe of drag cooperation according to chronic diagnosis llist
      res=False
      levRes=0
      dfCooperation= pd.DataFrame()
      listOfChronicDiagnosis = [di.lower() for di in listOfChronicDiagnosis]
      lstInd= [di.lower() for di in self.Indications]
      lstContr = [di.lower() for di in self.Contraindications]
      #np.Series(listOfChronicDiagnosis)
      lstChronicGrugPositive= [True if d in lstInd else False for d in listOfChronicDiagnosis ]
      lstChronicGrugNegative= [True if d in  lstContr else False for d in listOfChronicDiagnosis ]
      srN=pd.Series( lstChronicGrugNegative)
      srP=pd.Series( lstChronicGrugPositive)

      if MainDiagnosis.lower() in lstInd:
           res=True
           dfCooperation['ChronicDiagnosis'] =pd.Series(listOfChronicDiagnosis)
           dfCooperation['Indications'] =srP
           dfCooperation['Contraindications'] =srN
           cntN=len(srN.where(srN == True))
           cntP= len(srP.where(srP == True))
           if cntN>0:
             levRes= -(cntN)
           elif  cntP>0:
             levRes=cntP +1
           else:
             levRes=1




      return res,levRes,dfCooperation





# test class code

# myDrag =  Medcine()
# #print(myDrag.fname)
# myDrag.ActiveComponent=input("Insert new medcine Active Component: ")
# myDrag.Company=input("Insert new medcine Producer Company: ")
# myDrag.pillDose=input("Insert new medcine pill Dose: ")
# myDrag.Contraindications=input("Insert new medcine Contraindications separeted by ,: ")
# myDrag.Indications=input("Insert new medcine Iindications separeted by ,: ")
# myDrag.MedcineConflictList=input("Insert new medcine Drag Conflict list separeted by ,: ")
# myDrag.MedcineSynergyList=input("Insert new medcine Drag Synergy list separeted by ,: ")
# myDrag.Name=input("Insert new medcine Name: ")
# print(myDrag)
# myDrag.newMedcine()