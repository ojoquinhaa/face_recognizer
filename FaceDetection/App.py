from cv2 import (
    VideoCapture, cvtColor, COLOR_BGR2RGB, rectangle, imshow, waitKey, destroyAllWindows
)
from face_recognition import face_locations, face_encodings
from conn import conn, commit
import tkinter as tk
from FaceRecognizer import FaceRecognizer
from datetime import datetime
from time import sleep
class App:
    def __init__(self, master: tk.Tk, status:str="") -> None:
        self.root: tk.Tk = master # Criando o root
        self.status: str = status # Status de resultado
        self.run() # Rodando a classe
    
    def font(self, size: int) -> tuple:
        return ("Arial", size, "bold") # Configurações da fonte
    
    def new(self):
        for child in self.root.winfo_children(): child.destroy() # Apaga todas os elementos já na tela
        NewFace(master=self.root) # Adiciona os elementos de nova face

    def startRecognizer(self):
        self.root.destroy() # Fecha o programa 
        FaceRecognizer(cb=lambda: sleep(2)) # Inicia o reconhecimento facial

    def run(self) -> None:
        # Configurando o root
        self.root.title("Face recognizer - Ojoquinhaa")
        self.root.geometry("400x125")
        self.root.resizable(False, False)
        self.root.configure(background="#332D2D")

        # Adicionando um titulo
        title = tk.Label(master=self.root,text="INDENTIFICADOR DE ROSTOS",background="#332D2D",foreground="#FDFDFD")
        title.pack()
        title.configure(font=self.font(size=15))
        title.place(x=50, y=10)

        # Botão para a classe de nova face
        newFaceButton = tk.Button(master=self.root,text="Novo",width=10,height=2,
        background="#3B71CA",fg="#ffffff",command=lambda:self.new())
        newFaceButton.pack()
        newFaceButton.place(x=25,y=50)
        newFaceButton.configure(font=self.font(size=10))

        # Botão para iniciar o reconhecimento facial
        initButton = tk.Button(master=self.root,text="Iniciar",width=10,height=2,
        background="#FBFBFB",foreground="#000000",command=self.startRecognizer)
        initButton.pack()
        initButton.place(x=150, y=50)
        initButton.configure(font=self.font(size=10))

        # Botão para fechar o programa
        exitButton = tk.Button(master=self.root,text="Sair",width=10,height=2,
        background="#DC4C64",foreground="#ffffff",command=self.root.destroy)
        exitButton.pack()
        exitButton.place(x=275, y=50)
        exitButton.configure(font=self.font(size=10))

        # Tratamento de erros e retornando respostas
        if self.status == "saved":
            self.root.geometry("400x150")
            statusLabel = tk.Label(
                master=self.root,text="Salvo com sucesso!",bg="#332D2D",fg="#5cb85c"
            )
            statusLabel.pack()
            statusLabel.place(x=125,y=125)

        self.root.mainloop()

class NewFace:
    def __init__(self, master: tk.Tk) -> None:
        self.root = master # iniciando o root
        self.encoding = "" # preparando o encoding

        # inputs
        self.emailEntry = None
        self.nameEntry = None
        self.cpfEntry = None
        self.error = None
        self.run() # Rodando

    def font(self, size: int, type: str = "normal") -> tuple:
        return ("Arial", size, type) # Configurações de fonte

    def run(self) -> None:
        # Configurações da aplicação
        self.root.title("New Face - Ojoquinhaa")
        self.root.geometry("500x320")
        self.root.resizable(False, False)
        self.root.configure(background="#332D2D")
        
        # Titulo
        title = tk.Label(master=self.root,text="NOVO ROSTO",
        background="#332D2D",foreground="#FDFDFD")
        title.pack()
        title.configure(font=self.font(size=15, type="bold"))
        title.place(x=180, y=10)

        # Nome
        nameLabel = tk.Label(master=self.root,text="Nome",
        background="#332D2D",foreground="#FDFDFD")
        nameLabel.pack()
        nameLabel.configure(font=self.font(size=10))
        nameLabel.place(x=15, y=50)

        self.nameEntry = tk.Entry(master=self.root,width=30,bd=0,background="#FDFDFD",foreground="#000000")
        self.nameEntry.pack()
        self.nameEntry.configure(font=self.font(size=10))
        self.nameEntry.place(x=15,y=75)

        # CPF
        cpfLabel = tk.Label(master=self.root,text="CPF",
        background="#332D2D",foreground="#FDFDFD")
        cpfLabel.pack()
        cpfLabel.configure(font=self.font(size=10))
        cpfLabel.place(x=250, y=50)

        self.cpfEntry = tk.Entry(master=self.root,width=32,bd=0,background="#FDFDFD",foreground="#000000")
        self.cpfEntry.pack()
        self.cpfEntry.configure(font=self.font(size=10))
        self.cpfEntry.place(x=250,y=75)

        # Email
        emailLabel = tk.Label(master=self.root,text="Email",
        background="#332D2D",foreground="#FDFDFD")
        emailLabel.pack()
        emailLabel.configure(font=self.font(size=10))
        emailLabel.place(x=15, y=100)

        self.emailEntry = tk.Entry(master=self.root,width=66,bd=0,background="#FDFDFD",foreground="#000000")
        self.emailEntry.pack()
        self.emailEntry.configure(font=self.font(size=10))
        self.emailEntry.place(x=15,y=125)

        # Photo
        photoButton = tk.Button(master=self.root,text="Enviar",height=2,width=63,
        background="#3B71CA",fg="#ffffff",command=self.showWebCam)
        photoButton.pack()
        photoButton.place(x=15,y=180)
        photoButton.configure(font=self.font(size=10))

        # Error
        self.error = tk.Label(master=self.root, text="Credenciáis inválidas.",background="#332D2D",foreground="#DC4C64")
        self.error.configure(font=self.font(size=13))

        # Back
        exit = tk.Button(master=self.root,text="Voltar",background="#332D2D",foreground="#FDFDFD",cursor="mouse",command=self.exit)
        exit.configure(font=self.font(size=12))
        exit.pack()
        exit.place(x=220,y=280)

        self.root.mainloop()

    def exit(self,status:str=None):
       for child in self.root.winfo_children(): child.destroy() # Destroi os elementos no root
       App(master=self.root) # Escreve os elementos iniciais

    def saveFace(self):
        email = self.emailEntry.get()
        cpf = self.cpfEntry.get()
        name = self.nameEntry.get()
        sql = "INSERT INTO faces (name,cpf,email,face) VALUES (%s,%s,%s,%s)"
        data = (name,cpf,email,self.encoding)
        cursor = conn.cursor()
        cursor.execute(sql,data)
        commit()
        self.exit(status="saved")

    def showWebCam(self):
        self.cam = VideoCapture(0)
        email = self.emailEntry.get()
        cpf = self.cpfEntry.get()
        name = self.nameEntry.get()
        if name == "" or email == "" or cpf == "":
            self.error.pack()
            self.error.place(x=160,y=250)
            return
        while(True):
            ret, frame = self.cam.read() # Iniciando a camera

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
                self.cam.release() # Liberando a camera
                destroyAllWindows() # Fechando todas as janelas
                for x in encoding:
                    self.encoding += f"{x} "
                self.saveFace()             
                break
            
            # Mostrar a janela
            imshow("Frame", frame)

            # Botão para parar o programa "q"
            if waitKey(1) & 0xFF == ord('q'):
                self.cam.release() # Liberando a camera
                destroyAllWindows() # Fechando todas as janelas
                break

root = tk.Tk()
application = App(master=root)
application.run()