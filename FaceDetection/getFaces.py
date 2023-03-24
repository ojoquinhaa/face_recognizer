from os import listdir, getcwd
from face_recognition import face_encodings, load_image_file
def getFaces(filePath):
    files = listdir(filePath)
    imgs = [arquivo for arquivo in files if arquivo.endswith((".jpg", ".jpeg", ".png", ".gif"))]
    e = []
    for img in imgs:
        img = f"{getcwd()}/faces/{img}"
        load = load_image_file(img)
        encodings_referencia = face_encodings(load)[0]
        e.append(encodings_referencia)
    return e
        