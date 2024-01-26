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

def distance_points(point1, point2, weight = 2):
    #Calcula a distancia euclidiana como padrão, e modificando o peso conforme requerido.
    all_distances = [abs(value_point1 - value_point2) ** weight for value_point1, value_point2 in zip(point1, point2)]
    distance_euclidian = (sum(all_distances)) ** (1/weight)
    return distance_euclidian


            
    
class knn():
    def __init__(self, path_bd: str, percent_data_train = 0.7, weight_euclidian = 2, neighbours = 3):
        print('Começou!')
        self.weight_euclidian = weight_euclidian
        self.neighbours = neighbours
        self.percent_data_train = percent_data_train
        self.database = tratamento_dados(path_bd)
        self.points = transform_data_points(self.database)
        self.datatrain, self.datatest = self.divide_data()
        
    def normalizacao(self):
        # Encontrar o valor mínimo e máximo na lista
        for variable, values in self.database.items():
            
            valor_minimo = min(values)
            valor_maximo = max(values)

            # Normalizar os valores utilizando a fórmula (x - min) / (max - min)
            valores_normalizados = [(x - valor_minimo) / (valor_maximo - valor_minimo) for x in values]
            self.database[variable] = valores_normalizados
        self.points = transform_data_points(self.database)
        self.datatrain, self.datatest = self.divide_data()
            
            
    def divide_data(self):
        size_data = len(self.points)
        #Seleciona uma amostra aleatória de pontos e seleciona os valores que não está na lista para treino
        list_train = random.sample(self.points,int(size_data*self.percent_data_train))
        list_test = [point for point in self.points if point not in list_train]
        print(f"Os dados de treino terá tamanho de {len(list_train)} elementos e os dados de teste terá tamanho de {len(list_test)} elementos")
        return list_train, list_test
    
    def test(self):
        # Salva no Y de previsão na lista
        y_pred = list()
        for point in self.datatest:
            index_neighbours = self.discover_neighbours(point[:-1])
            #Verifica a resposta de cada K vizinhos mais próximos e ve qual tem a maior quantidade
            response_neighbours = [self.datatrain[index][-1] for index in index_neighbours]
            group = max(set(response_neighbours), key=response_neighbours.count)
            y_pred.append(group)
        return y_pred
        
            
    def discover_neighbours(self, point):
        #Calcula a distancia entre o ponto de teste e os pontos de treino e salva em uma lista com o indice e o valor da distancia
        distances_point_test = []
        for index_train, point_train in enumerate(self.datatrain):
            distances_point_test.append([index_train, distance_points(point, point_train[:-1])])
        #Ordena a lista de distancia e seleciona os K vizinhos mais próximos
        list_k_neighbours = sorted(distances_point_test, key = lambda x:x[1])
        return [x[0] for x in list_k_neighbours[0:self.neighbours]]
        
    def confusion_matrix(self):
        y_real = [point[-1] for point in self.datatest]
        y_pred = self.test()
        tp, fp, tn, fn = 0, 0, 0, 0
        
        for real, pred in zip(y_real, y_pred):
            if real == 1 and pred == 1:
                tp += 1
            elif real == 0 and pred == 1:
                fp += 1
            elif real == 0 and pred == 0:
                tn += 1
            elif real == 1 and pred == 0:
                fn += 1
        
        sensitivity = tp / (tp + fn)
        specificity = tn / (tn + fp)
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        precision = tp / (tp + fp)
        negative_predictive_value = tn / (tn + fn)
        
        print(f"{'Matriz de Confusão':^50}")
        print()
        print(f"{'True v Pred >':<15}|{'Positivo':^10}|{'Negativo':^10}|")
        print("-" * 50)
        print(f"{'Positivo':<15}|{tp:^10}|{fn:^10}|{sensitivity:^10.2f}")
        print("-" * 50)
        print(f"{'Negativo':<15}|{fp:^10}|{tn:^10}|{specificity:^10.2f}")
        print("-" * 50)
        print(f"{' ':<15}|{precision:^10.2f}|{negative_predictive_value:^10.2f}|{accuracy:^10.2f}")
            
                
        
        
        
        
        
            
            
    

        

## Entrada de dados









caminho_arquivo = 'bd\diabetes.csv'
modelo_knn = knn(caminho_arquivo, percent_data_train=0.7, neighbours= 7)
modelo_knn.test()
modelo_knn.normalizacao()
modelo_knn.test()
modelo_knn.confusion_matrix()
