import os
import re
import shutil
from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.exc import InvalidRequestError

from src.business.Person import Person
from src.controller import camera_controller
from src.controller.video_capture.VideoCaptureOpenCV import VideoCaptureOpenCV
from src.dao.FaceRecordDao import FaceRecordDao
from src.dao.PersonFaceRecordsDao import PersonFaceRecordsDao
from src.debug.debugutils import DebugUtils

dao = PersonFaceRecordsDao

debug = DebugUtils.get_instance()


def record_faces_identified_person(experiment, fr, camera, source, person_name):
    camera_controller.dao.update_object(camera, {'camera_string': source})
    pfr = dao.create_person_face_records(experiment, person_name, camera)
    dao.update_object(pfr.person)
    video_capture = VideoCaptureOpenCV(camera)
    if not video_capture.initialize():
        return False

    fr.initialize(pfr.person, video_capture)
    fr.capture_loop()
    fr.record_faces()
    return pfr.person


#TODO trocar exp por cam.exp
def recognize_suspect_faces(train_exec, experiment, face_recognizer, camera, source=None):
    if source:
        camera_controller.dao.update_object(camera, {'camera_string': source})
    pfr = create_pfr(camera)
    video_capture = VideoCaptureOpenCV(camera)
    if not video_capture.initialize():
        return False
    return face_recognizer.initialize(train_exec, pfr, video_capture)


def create_pfr(camera):
    # TODO remove name if necessary
    suspect_name = "suspect_{date:%Y%m%d-%H%M%S}".format(date=datetime.now())
    pfr = dao.create_person_face_records(camera.experiment, suspect_name, camera, is_suspect=True)
    generate_nick(pfr.person)
    dao.update_object(pfr)
    return pfr


def person_add_face_record(person, filename, commit=True):
    face_rec = FaceRecordDao.create_face_record(filename)
    person.add_face_record(face_rec)
    dao.update_object(person, commit=commit)


def pfr_add_face_record(pfr, filename, commit=True):
    face_rec = FaceRecordDao.create_face_record(filename)
    pfr.add_face_record(face_rec)
    dao.update_object(pfr, commit=commit)


def delete_person(person):
    try:
        pfrs = person.person_face_records
        if pfrs is not None:
            for pfr in pfrs:
                shutil.rmtree(pfr.suspect_db_dir(), ignore_errors=True)
        shutil.rmtree(person.person_db_dir(), ignore_errors=True)
        dao.delete_person(person)
    except Exception as e:
        print(e)
        pass


def delete_face_record(face_rec, commit=True):
    try:
        os.remove(face_rec.filepath())
    except:
        pass
    if face_rec.person is None:
        face_rec.person_face_records.remove_face_record(face_rec)
        dao.update_object(face_rec.person_face_records, commit=commit)
    else:
        face_rec.person.remove_face_record(face_rec)
        dao.update_object(face_rec.person, commit=commit)


def create_person(name, experiment):
    p = dao.create_person(name, experiment)
    return p


def update_person_threshold(person, thres):
    person.threshold = thres
    dao.update_object(person)


def save_person(person, person_name):
    person.name = person_name
    generate_nick(person)
    dao.update_object(person)


def get_person_by_nick(person_nick, experiment):
    try:
        existent_person = dao.session().query(Person).filter(
            and_(Person.nick == person_nick, Person.experiment_id == experiment.id)).one_or_none()
    except InvalidRequestError as e:
        return "More than one person with nickname {} found! Faces not transfered!!".format(person_nick)
    return existent_person


def convert_suspect_into_person(person, person_nick):
    try:
        existent_person = dao.session().query(Person).filter(
            and_(Person.nick == person_nick, Person.is_suspect == 0, Person.id != person.id,
                 Person.experiment_id == person.experiment_id)).one_or_none()
    except InvalidRequestError as e:
        return "More than one person with nickname {} found! Faces not transfered!!".format(person_nick)

    # Copy face records to existent
    if existent_person is not None:
        pfr_suspect = person.person_face_records[0]
        for face in pfr_suspect.face_records:
            person_add_face_record(existent_person, face.filename, commit=True)
            shutil.copy(face.filepath(), existent_person.person_db_dir())
        existent_person.add_person_face_records(pfr_suspect)
        dao.update_object(existent_person)
        dao.delete_object(person)
        dao.session().commit()
        return existent_person, "Faces transfered to existent Person {}".format(existent_person.name)

    # Convert into person
    else:
        try:
            pfr_suspect = person.person_face_records[0]
            suspect_dir_files = pfr_suspect.suspect_db_dir()
            person.name = person_nick
            person.nick = get_nick(person_nick)
            person.is_suspect = False
            dao.update_object(person)
            shutil.move(suspect_dir_files, person.person_db_dir())
            for face in pfr_suspect.face_records:
                person_add_face_record(person, face.filename, commit=True)
            person.add_person_face_records(pfr_suspect)
            dao.update_object(person)
            dao.session().commit()
        except Exception as e:
            return "Error while converting person!" + e
        return person, "Faces transfered to new Person {}".format(person.name)


def get_nick(person_name):
    # TODO person update name musta update directory
    chars_remove = [' ', '/', '\\', ':', '*', '?', '<', '>', '|', '\'', '\"']
    rx = '[' + re.escape(''.join(chars_remove)) + ']'
    nick = re.sub(rx, '', person_name).lower()
    return nick


def generate_nick(person):
    if not person.nick:
        person.nick = get_nick(person.name)


def get_person_faces(person):
    frs = []
    if person.is_suspect:
        for pfr in person.person_face_records:
            frs.extend(pfr.face_records)
    else:
        frs = person.face_records
    return frs


def get_person_faces_len(person):
    frs = get_person_faces(person)
    if frs is None:
        return 0
    else:
        return len(frs)


def get_person_localization(person):
    records = person.person_face_records
    localization = 'Undefined'
    if len(records) > 0:
        last_rec = records[len(records) - 1]
        localization = camera_controller.get_localization(last_rec.camera)
    return localization


def calculate_median_accuracy(recognizer_method, label_results_accum, curr_pfr):
    import operator

    if recognizer_method == 'median_sum_accuracy':
        suspect = '**unrecognized**'
        confidence_median = 0
        if len(label_results_accum) > 0:
            confidence_median_arr = {}
            total_accur = sum(label_results_accum.values())
            for name, summ in label_results_accum.items():
                confidence_median_arr[name] = summ / total_accur
                debug.msg('Median accuracy of {} = {}'.format(name, confidence_median_arr[name]))

            suspects = max(confidence_median_arr.items(), key=operator.itemgetter(1))
            suspect = suspects[0]
            confidence_median = confidence_median_arr[suspect]

        dao.update_object(curr_pfr,
                               {'is_suspect': True, 'suspect_name': suspect,
                                'suspect_confidence': confidence_median})
    else:
        # TODO count
        pass
    debug.msg(
        'Suspect {} recognized with {}% of confidence '.format(curr_pfr.suspect_name,
                                                               curr_pfr.suspect_confidence * 100))
