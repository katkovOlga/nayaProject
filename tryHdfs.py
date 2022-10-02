import pandas as pd
import sys
import numpy as np
import pyarrow as pa
import configuration as c
import pyarrow.parquet as pq
import json
from datetime import date,datetime, timedelta
import PatientClass
import os
from pyhive import hive


class Receipt:
  DoctorL=""
  PatientTz=""
  PatientFName = ""
  PatientLName = ""
  PatientBD=""
  PatientKH=""
  DrugId=""
  DrugName=""
  DrugDose=""
  lstDiag=""
  lstDrugs =""
  Diagnosys=""
  DfInteraction=pd.DataFrame()
  #DfIndications= pd.DataFrame()

  def crReceipt(self):
    # save to hdfs all data for receipt for followed analysis
    try:
      Interactions= self.DfInteraction.to_json()
    #  print (Interactions)
     # print(type(Interactions) )
      #### Generating Today's date ####
      today = date.today()
      current_date = today.strftime("%d_%m_%Y")
      currDT = today.strftime( "%m/%d/%Y, %H:%M:%S")
      ConflictSExists=False
      df =pd.DataFrame(data={"DoctorLicense" : [self.DoctorL], "PatientTZ": [self.PatientTz], "PatientFirstName": [self.PatientFName]\
              , "ConflictSExists": ConflictSExists,"PatientLastName": [self.PatientLName], "KupatHolim": [self.PatientKH], "PtienBirthdate": [self.PatientBD] \
             ,  "DrugName": [self.DrugName]  , "DrugId": [self.DrugId] ,"DrugDose": [self.DrugDose]  , "dateCreated":  [currDT] \
            ,"PatientDiseasesLqist": [self.lstDiag] \
              , "PatientTreatmentsList": [self.lstDrugs] , "drugDrugInteractionJson":   [Interactions] })



      path_tbl = "Receipt"+ self.PatientTz + self.DrugName+ current_date
    #  print (path_tbl)
      fs = pa.hdfs.connect(host='Cnt7-naya-cdh63', port=8020, user='hdfs', kerb_ticket=None, extra_conf=None)
      #2. Create/clean the staging folder in HDFS

      if not (fs.exists(c.hdfs_json_path)):
            fs.mkdir(c.hdfs_json_path)

      df_for_hdfs = pa.Table.from_pandas(df)
      print(c.hdfs_json_path + path_tbl)
      with fs.open(c.hdfs_json_path + path_tbl, "wb") as fw:
        pq.write_table(df_for_hdfs, fw)
        #print(df_for_hdfs)
      fs.close()





    except Exception as e:
      PatientClass.WriteLog("crReceipt error =" +str(e), "Error", self.PatientTz)
      print(e)

# test class
# Desloratadine 275635
myR =Receipt()
myR.lstDiag=",".join(["diabets","heart failure","myocardial infarction"])
myR.lstDrugs=",".join(["glucomin","aspirin"])
myR.DrugId="5640"
myR.PatientKH="Clalit"
myR.PatientBD="1960-11-10"

myR.DfInteraction= pd.DataFrame(data={"grugName":["ibuprofen","streptomycin"], "Synergy": ["Positive","Negative"] \
    , "Interaction Description": ["increase the anticoagulant activities","Risk"] , "severity": ["3","-2"] } )
 # .set_index("grugName")

#print (myR.DfInteraction)
myR.DrugName="bromhexine"
myR.DrugDose="400"
myR.DoctorL="123456"
myR.PatientTz ="1234564"
myR.PatientLName ="orlov"
myR.PatientFName="igal"

myR.crReceipt()