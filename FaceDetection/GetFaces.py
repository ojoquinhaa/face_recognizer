from numpy import array
from conn import commit
class GetFaces:
    def __init__(self, cursor) -> None:
        self.cursor = cursor # Criando conexão com o cursor

        self.cursor.execute("SELECT face FROM faces") # Seleciona todas as faces do banco de dados

        self.allFaces = self.cursor.fetchall() # Fetch nos valores para uma lista

        self.floatFaces = [] # Array com os valores passados para float
        self.arrayFaces = [] # Array com as arrays
        self.f = [] # Definindo a array onde vai ficar os encodings das faces
 
        self.splitFaces() # Chamando função para separar os dados
        commit() # Faz commit das alterações
        self.cursor.close() # Fechando o cursor


    def splitFaces(self):
        for rface in self.allFaces: # Pega todos os dados do banco de dados
            for x in rface: # Pega todos os valores das faces do banco de dados
                splitedValues = x.split(' ') # Separa todos os valores das faces
                splitedValues = [x for x in splitedValues if x != ''] # Remove os espaços em branco
                for y in splitedValues: # Pega todos os valores sozinho para passa-lós para float
                    # Passando todos os valores de string pra float e depois adicionando a uma array fora do loop
                    self.floatFaces.append(float(y))
            # Pegando a array e armazenando ela em outra array
            self.arrayFaces.append(self.floatFaces)
            self.floatFaces = []
        for z in self.arrayFaces: # para z entraga todas as arrays com os valores em float
            self.f.append(array(z)) # Formata todos os valores para serem comparados