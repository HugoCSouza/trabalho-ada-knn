import random

def tratamento_dados(arquivo):
        # Inicialização da variáveis
        variables = dict()
        # Manipulação do Arquivos
        with open(arquivo,'r') as bd:
            for linha in bd:
                elements = linha.strip().split(',')
                # Verifica se o dicionário já inicializou
                if variables:
                    for variable, element in zip(variables, elements):
                        variables[variable].append(element)
                else:
                    for variable in elements:
                        variables[variable] = []   
        
        # Verifica se todos os valores são numericos 
        for variable in variables:
            values_list = variables[variable]
            check_all_values = all([value.replace('.','').isnumeric() for value in values_list])
            # Se todos os valores forem numéricos, substitui a lista por uma tratada
            if check_all_values:
                converted_list = tuple(map(float, values_list))
                variables[variable] = converted_list
        print("Banco de dados tratado!")
        return variables

def transform_data_points(variables):
    # Adquire a lista de nomes de variaveis 
    keys_list = variables.keys()
    size_points = 99999999999999
    # Verifica que variavel tem o menor numero de pontos para não haver ponto sem valores
    for key in keys_list:
        size_variable = len(variables[key])
        if size_variable < size_points:
            size_points = size_variable
    points = []
    #Itera por todos os valores das variáveis, fazendo com que seja criada uma tupla com cada ponto
    for i in range(size_points):
        actual_point = list()
        for key in keys_list:
            list_values = variables[key]
            actual_point.append(list_values[i])
        points.append(tuple(actual_point))
    # Retorna o conjunto de pontos para verificação
    return points
            
    
class knn():
    def __init__(self, path_bd: str, percent_data_train = 0.7):
        print('Começou!')
        self.database = tratamento_dados(path_bd)
        self.points = transform_data_points(self.database)
        self.datatrain, self.datatest = self.divide_data(percent_data_train)
        
    def normalizacao(self):
        # Encontrar o valor mínimo e máximo na lista
        for variable, values in self.database.items():
            
            valor_minimo = min(values)
            valor_maximo = max(values)

            # Normalizar os valores utilizando a fórmula (x - min) / (max - min)
            valores_normalizados = [(x - valor_minimo) / (valor_maximo - valor_minimo) for x in values]
            self.database[variable] = valores_normalizados
            
    def divide_data(self, percent_train):
        size_data = len(self.points)
        list_train = random.sample(self.points,int(size_data*percent_train))
        list_test = [point for point in self.points if point not in list_train]
        print(f"Os dados de treino terá tamanho de {len(list_train)} elementos e os dados de teste terá tamanho de {len(list_test)} elementos")
        return list_train, list_test
        
        
            
            
    

        

## Entrada de dados









caminho_arquivo = 'bd\diabetes.csv'
modelo_knn = knn(caminho_arquivo, percent_data_train=0.5)
modelo_knn.normalizacao()
