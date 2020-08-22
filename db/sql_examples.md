Create centroids table:

## Per region analysis - summary
```
create table delano_ids_2016 as
select centroids_census16.objectid_1 from centroids_census16, delano_sce
where ST_CONTAINS(delano_sce.wkb_geometry, centroids_census16.center)

copy ( select *  from eta_census16 as c16 where c16.objectid_1 in (select objectid_1 from delano_ids_2016)) to '/tmp/eta_c16.csv' CSV delimiter ';' header;

create table eta_census16 (
OBJECTID_1 integer not null,
Acres numeric,
Crop2016 character varying,
Shape_Area numeric,
_mean numeric,
date timestamp,
inches numeric
);

copy eta_census16(OBJECTID_1,Acres,Crop2016,Shape_Area,_sum,_mean,date,inches) from '/tmp/2017eta_census16.csv' DELIMITER ';' CSV HEADER;
```
Expanded:
```
create table eta_census16 (
OBJECTID_1 integer not null,
Region character varying,
Acres numeric,
County character varying,
Comments character varying,
Source character varying,
Crop2016 character varying,
Date_Data_ character varying,
Last_Modif character varying,
GlobalID character varying,
Shape_Leng numeric,
Shape_Area numeric,
_count numeric,
_sum numeric,
_mean numeric,
_median numeric,
year numeric,
month numeric,
day numeric );
```

## Per crop analysis and KMLs
```
copy ( 
select ST_AsKML( wkb_geometry) from delano_fields where crop2016='Pistachios'
 union
select ST_AsKML ( wkb_geometry) from huron_fields where crop2016='Pistachios'
) to '/tmp/pistachios.kml' ;

copy (
 select as_kmldoc(
  ST_Union(
   ST_Collect(ARRAY(select wkb_geometry from delano_fields where crop2016='Idle')),
   ST_Collect(ARRAY(select wkb_geometry from huron_fields where crop2016='Idle'))
  )
 )
) to '/tmp/Idle.kml' ;

copy ( select ST_AsKML( wkb_geometry) from crop2016_cutout where crop2016='Grapes' ) to '/tmp/Grapes.kml' ;

copy ( select ST_AsText(ST_Collect(ARRAY(select wkb_geometry from huron_fields where crop2016='Tomatoes'))) ) to '/tmp/huron_Tomatoes.txt' ;
```

## KMLs for clusters

### create a table from the CSV with cluster labels
```
create table huron_tomatoes_cluster (
Region character varying,
Acres numeric,
County character varying,
Crop2016 character varying,
st_askml character varying,
center      character varying,
latitude numeric,
longitude numeric,
OBJECTID_1 integer not null,
_mean numeric,
labels integer);
```
### import the file
```
copy huron_tomatoes_cluster(Region,Acres,County,Crop2016,st_askml,center,latitude,longitude,OBJECTID_1,_mean,labels) from '/tmp/huron_tomatoes.csv' DELIMITER ',' CSV HEADER;
```
### select only one specific cluster
```
copy(select ST_AsKML( s1.wkb_geometry) 
from (select wkb_geometry as wkb_geometry, labels as l 
from huron_fields inner join huron_tomatoes_cluster on huron_fields.objectid_1=huron_tomatoes_cluster.OBJECTID_1 ) s1 where s1.l=1)
to '/tmp/huron_tomatoes1.kml';    ## COPY 88
```



