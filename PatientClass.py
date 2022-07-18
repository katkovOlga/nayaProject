# Started in 0722
#  Patient Class
# written by Olga Katkov
#

import pandas as pd
import sys
import numpy as np

class Patient:
  TZ=''
  LastName=''
  FirstName=''
  Birthdate=''
  Deathdate=''
  KupatHolim=''
  Doctor=''
  DiseasesHistory=[]
  ConstantDrugsList=[]

  def __init__(self, fields):
        #self.fields = fields
        pass
  def newPatient(self):
    # add new Patient
    pass
  def addDiagnose (self,diagnose):
    # add new diagnose to Patient
    pass
  def getPatientDiagnosis(self):
    # return Patient  diagnosis list
    pass
  def getPatientConstantDrugs(self):
    # return Patient drugs list
    pass
  def addDrugToPatientDiagnose(self, diagnose, drug):
    # add new drug to Patient
    pass
  def rmDrugToPatientDiagnose(self, diagnose, drug):
    # remove drug from Patient
    pass