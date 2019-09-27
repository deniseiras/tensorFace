import os, shutil

dest_dir = "/media/denis/dados/face_bds/FEI_dir_sep/"
if os.path.isdir(dest_dir):
    shutil.rmtree(dest_dir)

person_id = "NONE"
for root, dirs, files in os.walk("/media/denis/dados/face_bds/FEI_originalimages"):
    for file in files:
        if file.endswith(".jpg"):
            file_and_path = os.path.join(root, file)
            file_split_trace = file.split("-")
            if file_split_trace[0] != person_id:
                person_id = file_split_trace[0]
                face_dir = dest_dir + person_id
                if not os.path.isdir(face_dir):
                    os.makedirs(face_dir)
            shutil.copy(file_and_path, face_dir)
            file_split_dot = file.split(".")
            # file_copy = file_split_dot[0] + "-copy." + file_split_dot[1]
            # shutil.copy(file_and_path, os.path.join(face_dir, file_copy))
