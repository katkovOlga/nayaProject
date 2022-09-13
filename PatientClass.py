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


def WriteLog( msg,msgType, tz):
  cnDB=mc.connect(
      user=c.mysql_username,
      password=c.mysql_password,
      host=c.mysql_host,
      port=c.mysql_port,
      autocommit=True,
      database=c.mysql_database_name)

  curIns = cnDB.cursor()
  sql = "insert into Doctor_Assistance_App_Error_Log (doctorId,PatientTz,MsgType,Msg_text ) values('" + c.CurrentDoctorLic \
        + "','"+ tz +"','" + msgType + "','" + msg    +"');"
  print (sql)

  curIns.execute(sql)
  cnDB.commit()
  curIns.close()
  cnDB.close()

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
  KnownPersonalDrugConflictsList=[]

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
    if diagnose.lower() in self.DiseasesHistory:
      WriteLog("the diagnosis already exist in patient history" + diagnose.lower() , "Info", self.TZ )
      exit
    cursor = cnMS.cursor()
    self.DiseasesHistory.append(diagnose.lower())
    #print (self.DiseasesHistory)
    #print (",".join(self.DiseasesHistory))
    sql = "update patients set DisesesList='" + ",".join(self.DiseasesHistory) +"' where tz='"  + self.TZ + "';"
    #print (sql)
    WriteLog("Patient addDiagnose sql=" + sql.replace("'","") , "Info",self.TZ)
    cursor.execute(sql)
    #print(cursor.rowcount, "record(s) affected")
    WriteLog("Patient addDiagnose rows affected=" + str(cursor.rowcount) , "Info",self.TZ)
    cnMS.commit()

    cursor.close()


    cnMS.close
  def getPatientDiagnosis(self):
    # return Patient  diagnosis list
    pass
  def getPatientConstantDrugs(self):
    # return Patient drugs list
    pass
  def addDrugToPatientDrugList(self, drug):
    # add new drug to Patient
    cnMS = mc.connect(
      user=c.mysql_username,
      password=c.mysql_password,
      host=c.mysql_host,
      port=c.mysql_port,
      autocommit=True,
      database=c.mysql_database_name)
    drug=drug.lower()
    cursor = cnMS.cursor()
    if drug not in self.ConstantDrugsList:
      self.ConstantDrugsList.append(drug)
    else:
      WriteLog(drug + "already exists in Patient.addDrugToPatientDrugList=" + "".join(self.ConstantDrugsList) , "Info", self.TZ)
      exit
    #print(",".join(self.ConstantDrugsList))
    sql = "update patients set DrugsTreatmentList='" + ",".join(self.ConstantDrugsList) + "' where tz='" + self.TZ + "';"
    print(sql)
    WriteLog("Patient.addDrugToPatientDrugList sql=" + sql.replace("'","") , "Info",self.TZ)
    cursor.execute(sql)
    #print(cursor.rowcount, "record(s) affected")
    WriteLog("Patient.addDrugToPatientDrugList  rows affected=" + str(cursor.rowcount), "Info",self.TZ)
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
       + "KypatHolim ,DisesesList ,DrugsTreatmentList,Contraindications from patients where tz='" + self.TZ + "';"
    #print (com1)

   # WriteLog("Patient.findPatient sql=" + com1.replace("'",""), "Info",self.TZ, cnMS)
    cursor.execute(com1)
    if cursor.with_rows:
      WriteLog("Patient.findPatient row found="   , "Info",self.TZ)
      row = cursor.fetchone()   #.fetchall()
      #print (row)
      if row[8] != None:
        self.DiseasesHistory =row[8].split(",")
      #print(type(row[10]))
      #row= [t[0] for t in rows]
      if row[9]!= None:
        self.ConstantDrugsList=row[9].split(",")
      if row[10]!= None:
        self.KnownPersonalDrugConflictsList=row[10].split(",")

      self.Birthdate=row[2]
      self.FirstName=row[0]
      self.LastName=row[1]
      self.KupatHolim=row[7]
      self.Doctor = row[6]
    else:
      WriteLog("Patient.findPatient row not found=", "Info", self.TZ)
    cursor.close()
    cnMS.close()
    #return self

# try code
# p1=Patient()
# p1.TZ='1122112211'
# p1.findPatient()
# print(type(p1.DiseasesHistory))
# print(p1.ConstantDrugsList)
# #
# # p1.addDiagnose("Back pain")
# p1.addDrugToPatientDrugList("Glymidine")