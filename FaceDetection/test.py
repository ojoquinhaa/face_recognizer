from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB, rectangle, imshow, waitKey, destroyAllWindows
from face_recognition import face_locations, compare_faces, face_encodings
from conn import conn,commit
from numpy import array
cam = VideoCapture(0)
while(True):
    ret, frame = cam.read() # Iniciando a camera

    # Caso não seja possivel acessar nenhuma câmera
    if not ret:
        print("Não foi possivel acessar a câmera!")
        continue

    rgb_frame = cvtColor(frame, COLOR_BGR2RGB) # Mudando a cor da camera para rgb

    # Localizando todas os rostos na câmera e criando os encodings 
    faces = face_locations(rgb_frame)
    encodings = face_encodings(rgb_frame, faces)

    # Adicionar um retangulo em volta do rosto encontrado
    for (top, right, bottom, left) in faces:
        rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    if (len(encodings) == 1):
        encoding = encodings[0]
        cam.release() # Liberando a camera
        destroyAllWindows() # Fechando todas as janelas
        print(encodings)         
        break

    # Mostrar a janela
    imshow("Frame", frame)

    # Botão para parar o programa "q"
    if waitKey(1) & 0xFF == ord('q'):
        cam.release() # Liberando a camera
        destroyAllWindows() # Fechando todas as janelas
        break