from src.business.Camera import Camera, TYPE_ENTRANCE, TYPE_EXIT, TYPE_AUXILIAR
from src.dao.GenericDao import GenericDao

dao = GenericDao


def create_camera(name, source, experiment):
    cam = Camera(name=name, camera_string=source, experiment=experiment)
    cam.make_default_values()
    dao.update_object(cam)
    return cam


def get_object_by_id(q_id):
    return dao.get_object_by_id(Camera, q_id)


def get_localization(camera):
    dict_trans = {TYPE_ENTRANCE: 'Inside',
                  TYPE_EXIT: 'Outside',
                  TYPE_AUXILIAR: 'Going'}
    return dict_trans[camera.type]
