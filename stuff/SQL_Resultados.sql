use ALFA;

update face_record set person_id = 789 where person_id in (782, 783, 788);
select * from face_record where person_id in (782, 783, 788, 789);

select * from person_face_records pfr where 
-- pfr.suspect_name like '%arah%';
pfr.person_id in (782, 783, 788, 789);

select * from face_record fr where 
-- pfr.suspect_name like '%arah%';
fr.person_id in (742);
-- group by fr.person_id;

insert into face_record values(null, 'sface_20.jpg', 742, null);


insert into face_record values(null, 'suspect_20181122-190250_3.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_4.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_5.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_6.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_7.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_8.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_9.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_10.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_11.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_12.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_13.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_14.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_15.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_16.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_17.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_18.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_19.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_20.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_21.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_22.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_23.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_24.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_25.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_26.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_27.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_28.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_29.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_30.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_31.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_32.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_33.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_34.jpg', 742, null);
insert into face_record values(null, 'suspect_20181122-190250_35.jpg', 742, null);

update face_record fr set fr.person_id = 782 where fr.person_id in (782, 783, 788, 789);


select * from person p
where experiment_id = 24
-- where id in (782, 783, 788, 789)
-- and p.name like '%arah%'
order by p.name;
 

select * from face_record fr, person_face_records pfr
where pfr.experiment_id = 24 
-- and pfr.person_id = 788
and pfr.person_id in (782, 783, 788, 789)
and fr.person_face_records_id = pfr.id;

select * from person_face_records pfr
where pfr.experiment_id = 24 
and pfr.person_id = (782, 783, 788, 789);
-- order by suspect_name;
-- and pfr.suspect_name like 'sarahlo'
-- order by date_time desc;

select 
count(*) as conta
-- , pfr.id 
from face_record fr, person_face_records pfr
where pfr.experiment_id = 24 and fr.person_face_records_id = pfr.id;
-- group by pfr.id
-- order by conta;

select count(*) as conta
-- , pfr.id 
from face_record fr, person p
where p.experiment_id = 24 and fr.person_id = p.id;
-- and p.is_suspect = 1;
-- group by pfr.id
-- order by conta;

-- order by suspect_confidence;
-- group by camera_id;

select * from camera where experiment_id = 24;


use ALFA;
-- PARA testar somente suspeitos
select *
from person_face_records pfr, person p
where pfr.experiment_id = 24 
and pfr.person_id = p.id
and p.is_suspect = 1
order by date_time desc;
-- group by pfr.id
-- order by conta;


select * from person_face_records where id = 809;