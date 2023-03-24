from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB, rectangle, imshow, waitKey, destroyAllWindows
from face_recognition import face_locations, compare_faces, face_encodings
from conn import conn,commit
from numpy import array

cursor = conn.cursor() # Cria um cursor
cursor.execute("SELECT face FROM faces") # Seleciona todas as faces do banco de dados
allFaces = cursor.fetchall() # Fetch nos valores para uma lista
floatFaces = [] # Array com os valores passados para float
arrayFaces = [] # Array com as arrays
for rface in allFaces: # Pega todos os dados do banco de dados
    for x in rface: # Pega todos os valores das faces do banco de dados
        splitedValues = x.split(' ') # Separa todos os valores das faces
        splitedValues = [x for x in splitedValues if x != ''] # Remove os espaços em branco
        for y in splitedValues: # Pega todos os valores sozinho para passa-lós para float
            # Passando todos os valores de string pra float e depois adicionando a uma array fora do loop
            floatFaces.append(float(y))
    # Pegando a array e armazenando ela em outra array
    arrayFaces.append(floatFaces)
    floatFaces = [] # Apagando os valores para caso haver mais de uma face
f = [] # Definindo a array onde vai ficar os encodings das faces
for z in arrayFaces: # para z entraga todas as arrays com os valores em float
    f.append(array(z)) # Formata todos os valores para serem comparados
commit() # Faz commit das alterações
cursor.close() # Fechando o cursor
cursor = None # Apagando a conexão com o banco de dados

captura = VideoCapture(0) # Criando instancia de camera

while True:
    ret, frame = captura.read() # Iniciando a camera

    # Caso não seja possivel acessar nenhuma câmera
    if not ret:
        print("Não foi possivel acessar a câmera!")
        continue

    rgb_frame = cvtColor(frame, COLOR_BGR2RGB) # Mudando a cor da camera para rgb

    # Localizando todas os rostos na câmera e criando os encodings 
    faces = face_locations(rgb_frame)
    encodings = face_encodings(rgb_frame, faces)

    # Analisando todos os conjuntos de encoding
    for encoding in encodings:
        comparacao = compare_faces(f, encoding)

        # Verificar se o usuário está cadastrado
        for c in comparacao:
            if c:
                print("Autorizado!")

    # Adicionar um retangulo em volta do rosto encontrado
    for (top, right, bottom, left) in faces:
        rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    
    # Mostrar a janela
    imshow("Frame", frame)

    # Botão para parar o programa "q"
    if waitKey(1) & 0xFF == ord('q'):
        break

captura.release() # Liberando a camera
destroyAllWindows() # Fechando todas as janelas
