select field, name, urlStr from DiseasesFile 
where field like 'DOID:%' and name not like '%isease%'  and name not like '%DOID:%'
limit 1050


create table diagnoses as select field, name, urlStr  from DiseasesFile 
where field like 'DOID:%' and name not like '%isease%'  and name not like '%DOID:%'

select * from diagnoses limit 100

drop table diagnoses


create database IF NOT EXISTS doctors;
USE  doctors;

create table  patients(tz varchar(15),
FName varchar(20),
LNAme varchar(40),
Bithdate DATE,
Deathdate DATE,
ADress varchar(100),
Mobile varchar(16),
Doctor varchar(15),
KypatHolim varchar(15),
DisesesList varchar (500),
DrugsTreatmentList varchar (500)

);
drop table doctors;
create table doctors( tz varchar(15),
licienNum varchar(40),
FName varchar(20),
LNAme varchar(40),
specialisation varchar(50),
workPlaceList varchar (500)
) 