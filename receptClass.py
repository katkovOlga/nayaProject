#  started 0822 by Olga Katkov
# saved new recept in hdfs for statistics
#
#
import pandas as pd

class Recept:
  TZ=''
  PatientLastName=''#  PatientFirstName=''
  DoctorLicense=''
  DoctorLastName=''
  DoctorFirstName=''
  DrugName=''
  DrugDose=''
  DateCreated=''
  Period=''
  PatientDiagnos=''
  PatientChronicList=[]
  PatientConstantDrugsList=[]
  receptWarnings=pd.DataFrame()

  def __init__(self, fields):
      self.fields = fields
      pass
  def createRecept(self):
      pass