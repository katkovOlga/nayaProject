# Started in 0722
#  Patient Class
# written by Olga Katkov
#

import pandas as pd
import sys
import numpy as np
import pyarrow as pa
import mysql.connector as mc
import configuration as c

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

  def __init__(self):
        #self.fields = fields
        pass
  def newPatient(self):
    # add new Patient
    pass
  def addDiagnose (self,diagnose):
    # add new diagnose to Patient
    cnMS = mc.connect(
      user=c.mysql_username,
      password=c.mysql_password,
      host=c.mysql_host,
      port=c.mysql_port,
      autocommit=True,
      database=c.mysql_database_name)
    cursor = cnMS.cursor()
    self.DiseasesHistory.append(diagnose)
    print (self.DiseasesHistory)
    print (",".join(self.DiseasesHistory))
    sql = "update patients set DisesesList='" + ",".join(self.DiseasesHistory) +"' where tz='"  + self.TZ + "';"
    print (sql)
    cursor.execute(sql)
    print(cursor.rowcount, "record(s) affected")
    cnMS.commit()

    cursor.close()


    cnMS.close
  def getPatientDiagnosis(self):
    # return Patient  diagnosis list
    pass
  def getPatientConstantDrugs(self):
    # return Patient drugs list
    pass
  def addDrugToPatientDiagnose(self, drug):
    # add new drug to Patient
    cnMS = mc.connect(
      user=c.mysql_username,
      password=c.mysql_password,
      host=c.mysql_host,
      port=c.mysql_port,
      autocommit=True,
      database=c.mysql_database_name)
    cursor = cnMS.cursor()
    self.ConstantDrugsList.append(drug)
    print(",".join(self.ConstantDrugsList))
    sql = "update patients set DrugsTreatmentList='" + ",".join(self.ConstantDrugsList) + "' where tz='" + self.TZ + "';"
    print(sql)
    cursor.execute(sql)
    print(cursor.rowcount, "record(s) affected")
    cnMS.commit()

    cursor.close()
    cnMS.close

  def rmDrugToPatientDiagnose(self, diagnose, drug):
    # remove drug from Patient
    pass

  def findPatient(self):
    # doctors.patients
    cnMS = mc.connect(
        user=c.mysql_username,
        password=c.mysql_password,
        host=c.mysql_host,
        port=c.mysql_port,
        autocommit=True,
        database=c.mysql_database_name)
    cursor = cnMS.cursor()
    com1 = "select FName,LNAme ,Bithdate,Deathdate ,ADress ,Mobile , Doctor , " \
       + "KypatHolim ,DisesesList ,DrugsTreatmentList from patients where tz='" + self.TZ + "';"
    #print (com1)
    cursor.execute(com1)
    row = cursor.fetchone()   #.fetchall()
    #print (type(row))
    #print (row)
    self.DiseasesHistory =row[8].split(",")

    #row= [t[0] for t in rows]
    self.ConstantDrugsList=row[9].split(",")
    print( type(self.DiseasesHistory))
    self.Birthdate=row[2]
    self.FirstName=row[0]
    self.LastName=row[1]
    self.KupatHolim=row[7]
    self.Doctor = row[6]
    cursor.close()
    cnMS.close()
    #return self

## try code
p1=Patient()
p1.TZ='1212121212'
p1.findPatient()
#print(type(p1.DiseasesHistory))

p1.addDiagnose("Cancer")