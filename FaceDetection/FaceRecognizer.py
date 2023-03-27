from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB, rectangle, imshow, waitKey, destroyAllWindows
from face_recognition import face_locations, compare_faces, face_encodings
from GetFaces import GetFaces
from conn import conn
class FaceRecognizer:
    def __init__(self, cb) -> None:
        self.cam = VideoCapture(0)
        self.cb = cb
        self.cursor = conn.cursor()
        self.getFaces = GetFaces(cursor=self.cursor)
        self.f = self.getFaces.f
        self.webCamFaceDetect()
        destroyAllWindows()
    
    def webCamFaceDetect(self):
        while True:
            ret, frame = self.cam.read()
            if not ret:
                print("Não foi possivel acessar a câmera!")
                continue
            rgb_frame = cvtColor(frame, COLOR_BGR2RGB)

            faces = face_locations(rgb_frame)
            encodings = face_encodings(rgb_frame, faces)

            # Adicionar um retangulo em volta do rosto encontrado
            for (top, right, bottom, left) in faces:
                rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            for encoding in encodings:
                compare = compare_faces(self.f, encoding)
                for c in compare:
                    if c:
                        print("Autorizado!")
            
            imshow("Face Detection - OJoquinhaa", frame)

            # Botão para parar o programa "q"
            if waitKey(1) & 0xFF == ord('q'):
                break    
