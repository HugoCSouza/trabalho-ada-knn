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
        
        
        for variable in variables:
            values_list = variables[variable]
            # Verifica se todos os valores são numericos 
            if all([value.replace('.','').isnumeric() for value in values_list]):
                converted_list = tuple(map(float, values_list))
                # Verifica se todos os valores são 0 ou 1
                if all([(value == True or value == False) for value in converted_list]):
                    converted_list = tuple(map(bool, converted_list))
                    variables[variable] = converted_list
                else:
                    variables[variable] = converted_list
            # Se não cumprir nenhum do dois requisitos deixa como está, só convertendo em tupla
            else:
                converted_list = tuple(map(str, values_list))
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
        self.path_bd = path_bd
        self.weight_euclidian = weight_euclidian
        self.neighbours = neighbours
        self.percent_data_train = percent_data_train
        self.database = tratamento_dados(self.path_bd)
        self.points = transform_data_points(self.database)
        self.datatrain, self.datatest = self.divide_data()
        
    def normalizacao(self, type = "minmax"):
        if type == "minmax":
            # Encontrar o valor mínimo e máximo na lista
            for variable, values in self.database.items():
                if variable.lower() != 'outcome':
                    valor_minimo = min(values)
                    valor_maximo = max(values)

                    # Normalizar os valores utilizando a fórmula (x - min) / (max - min)
                    valores_normalizados = [(x - valor_minimo) / (valor_maximo - valor_minimo) for x in values]
                    self.database[variable] = valores_normalizados
                    
            self.points = transform_data_points(self.database)
            self.datatrain, self.datatest = self.divide_data()
        elif type == "zscore":
            # Encontrar o valor mínimo e máximo na lista
            for variable, values in self.database.items():
                if variable.lower() != 'outcome':
                    n = len(values)
                    mean = sum(values)/n
                    std = (sum([(x - mean)**2 for x in values]) / n) ** (1/2)
                    # Normalizar os valores utilizando a fórmula (x - min) / (max - min)
                    valores_normalizados = [(x - mean) / std for x in values]
                    self.database[variable] = valores_normalizados
            
            self.points = transform_data_points(self.database)
            self.datatrain, self.datatest = self.divide_data()
        
            
            
    def divide_data(self, print_informations = True):
        size_data = len(self.points)
        #Seleciona uma amostra aleatória de pontos e seleciona os valores que não está na lista para treino
        list_train = random.sample(self.points,int(size_data*self.percent_data_train))
        list_test = [point for point in self.points if point not in list_train]
        if len(list_test) == 0 or len(list_train) == 0:
            print('Não foi possivel dividir os dados')
            return [], []
        if print_informations:
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
        
    def results(self, print_matrix=True):
        y_real = [point[-1] for point in self.datatest]
        y_pred = self.test()
        tp, fp, tn, fn = 0, 0, 0, 0
        
        for real, pred in zip(y_real, y_pred):
            if real and pred:
                tp += 1
            elif (not real) and pred:
                fp += 1
            elif (not real) and (not pred):
                tn += 1
            elif real and (not pred):
                fn += 1
        try:
            sensitivity = tp / (tp + fn)
            specificity = tn / (tn + fp)
            accuracy = (tp + tn) / (tp + tn + fp + fn)
            precision = tp / (tp + fp)
            negative_predictive_value = tn / (tn + fn)
        except:
            pass
        
        if print_matrix:
            print(f"{'Matriz de Confusão':^50}")
            print()
            print(f"{'True v Pred >':<15}|{'Positivo':^10}|{'Negativo':^10}")
            print("-" * 37)
            print(f"{'Positivo':<15}|{tp:^10}|{fn:^10}")
            print("-" * 37)
            print(f"{'Negativo':<15}|{fp:^10}|{tn:^10}")
            print("-" * 37)
            print(f"Sensitivity: {sensitivity:>20.2f}")
            print(f"Specificity: {specificity:>20.2f}")
            print(f"Precision: {precision:>22.2f}")
            print(f"Negative Predictive Value: {negative_predictive_value:>6.2f}")
            print(f"Accurrancy: {accuracy:>21.2f}")
            print('\n' * 3)
        
        return accuracy
    
    def fitting(self):
        print("Começo do Fitting")
        print('-'*150)
        best_acc = 0
        for type in range(3):
            self.database = tratamento_dados(self.path_bd)
            if type == 1:
                self.database = self.normalizacao()
            elif type == 2:
                self.database = self.normalizacao(type='zscore')
            for percent_data in range(0,99,5):
                percent_data = percent_data * 0.01
                print('')
                if percent_data != 0:
                    self.percent_data_train = percent_data
                    self.datatrain, self.datatest = self.divide_data(print_informations = False)
                    for neighbours in range(1,int(len(self.datatest)/2)):
                        self.neighbours = neighbours
                        print('|', end='')
                        for weight in range(2,10):
                            self.weight_euclidian = weight
                            print('.',end='')
                            acc = self.results(print_matrix=False)
                            if best_acc <= acc:
                                best_percent = self.percent_data_train
                                best_acc = acc
                                best_neighbours = self.neighbours
                        
                
        print(f"O melhor valor de acurácia foi atingido com a divisão de dados com tamanho de {best_percent*100:.2f}% e quantidade de vizinhos igual á {best_neighbours}. \
            A accurácia atingida foi de {best_acc*100:.2f}%")
                
            
        
            
                
        
        
        
        
        
            
            
    

        

## Entrada de dados









caminho_arquivo = 'bd\diabetes.csv'
modelo_knn = knn(caminho_arquivo, percent_data_train=0.7, neighbours= 7)
modelo_knn.fitting()
# print('Sem normalização!')
# print('-'*100)
# modelo_knn.test()
# modelo_knn.confusion_matrix()
# print('Normalização Min-Max')
# print('-'*100)
# modelo_knn.normalizacao()
# modelo_knn.test()
# modelo_knn.confusion_matrix()
# print('Normalização Zscore')
# print('-'*100)
# modelo_knn.normalizacao(type="zscore")
# modelo_knn.test()
# modelo_knn.confusion_matrix()
