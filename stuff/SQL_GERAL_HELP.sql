use ALFA;
commit;

select * from tensor_flow_env;
select * from experiment;

select * from camera c where c.experiment_id = 24;

#delete from camera where experiment_id is null;

select * from person p; # where p.experiment_id = 20;
#update person set nick = name where experiment_id = 20;
commit;
select * from person p where p.experiment_id is null;

##delete from person where experiment_id is null;

select p.name, pfr.* from person_face_records pfr, person p where pfr.experiment_id = 20 and pfr.person_id = p.id;

#delete from person_face_rpersonecords; -- where pfr.experiment_id = 19;

select * from face_record order by id desc;

select * from person_face_records pfr, person p
where pfr.person_id = p.id
and pfr.suspect_confidence is null;


select * from face_record fr, person_face_records pfr, person p
where fr.person_face_records_id = pfr.id 
and pfr.person_id = p.id;
#and pfr.suspect_confidence is null;
#and p.name = 'Denis'

select count(*) as faces_count, p.name, pfr.suspect_name
  from face_record fr, person_face_records pfr , person p
 where fr.person_face_records_id = pfr.id 
   and pfr.person_id = p.id
group by p.name , pfr.suspect_name;


select * from train_configuration;

select * from train_execution where experiment_id = 23;
##delete from train_execution where test_accuracy is null;
##delete from train_execution where experiment_id = 20;

 

select * from person_face_records pfr , person p
where pfr.person_id = p.id
and p.name = 'suspect_20181122-192814';

select * from face_record fr, person_face_records pfr, person p
 where pfr.person_id = p.id 
   and fr.person_face_records_id = pfr.id
   and p.name = 'suspect_20181122-192814';

select * from person_face_records where row_count() < 5 order by id desc;
#insert into person values(null, 'suspect_20181122-190350', 'suspect_20181122-190350', 1, 24 );
#update person_face_records set person_id = 936 where id = 845;
#insert into person_face_records values (843, 24, 'denis intel', 1.0, '2018-11-22 19:02:50', null, 742, 29);
#insert into person_face_records values (844, 24, 'denis intel', 1.0, '2018-11-22 19:04:50', null, 742, 30);
#insert into person_face_records values (845, 24, 'denis intel', 1.0, '2018-11-22 19:03:50', null, 742, 29);

insert into face_record values (null, 'suspect_20181122-190350_1.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_2.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_3.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_4.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_5.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_6.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_7.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_8.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_9.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_10.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_11.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_12.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_13.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_14.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_15.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_16.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_17.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_18.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_19.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_20.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_21.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_22.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_23.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_24.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_25.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_26.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_27.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_28.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_29.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_30.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_31.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_32.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_33.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_34.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_35.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_36.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_37.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_38.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_39.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_40.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_41.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_42.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_43.jpg', null, 845);
insert into face_record values (null, 'suspect_20181122-190350_44.jpg', null, 845);

commit;

select * from face_record where row_count() < 40 order by id desc;


select * from face_record where filename = 'suspect_20181122-190250_3.jpg';




select * from face_record fr , person p
where fr.person_id = p.id
and p.name = 'denis_intel';


select * from face_record where person_face_records_id is null;
select * from face_record where filename like 'suspect_20181122-190250%';

##delete from face_record where person_face_records_id is null;
##delete from face_record where id in (3081, 3082, 3083);



##delete from person_face_records;

select filename from face_record fr where length(filename) > 20;
/*and pfr.person_id = p.id*/

select * from face_record fr order by id;

select  * from person where name = 'Bianca';
#update person set nick = 'deniseiras' where id = 13;



select * from test_configuration;
/*select * from person where id > 30*/