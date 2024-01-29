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
        true_positive, false_positive, true_negative, false_negative = 0, 0, 0, 0
        #Verifica os Positivos Verdadeiros e Falsos e idem Negativos
        for real, pred in zip(y_real, y_pred):
            if real and pred:
                true_positive += 1
            elif (not real) and pred:
                false_positive += 1
            elif (not real) and (not pred):
                true_negative += 1
            elif real and (not pred):
                false_negative += 1
        try:
            sensitivity = true_positive / (true_positive + false_negative)
            nfr = false_negative / (true_positive + false_negative)
            specificity_positive = true_negative / (true_negative + false_positive)
            specificity_negative = false_positive / (true_negative + false_positive)
            accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
            precision = true_positive / (true_positive + false_positive)
            
            negative_predictive_value = true_negative / (true_negative + false_positive)
        except:
            if true_positive == 0 and false_positive == 0:
                precision = 0
                sensitivity = true_positive / (true_positive + false_negative)
                nfr = false_negative / (true_positive + false_negative)
                specificity_positive = true_negative / (true_negative + false_positive)
                specificity_negative = false_positive / (true_negative + false_positive)
                accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
                negative_predictive_value = true_negative / (true_negative + false_positive)
            
        #Se o print_matrix for verdadeiro printa a matriz de confusão
        if print_matrix:
            print(f"{'Matriz de Confusão':^50}")
            print()
            print(f"{'True v Pred >':<15}|{'Positivo':^10}|{'Negativo':^10}")
            print("-" * 37)
            print(f"{'Positivo':<15}|{true_positive:^10}|{false_negative:^10}")
            print("-" * 37)
            print(f"{'Negativo':<15}|{false_positive:^10}|{true_negative:^10}")
            print("-" * 37)
            print(  f"Sensibilidade ou Recall (Taxa de verdadeiro positivos): {sensitivity*100:.2f} % \n"  
                    f"Taxa de falso negativo: {nfr*100:.2f} %  \n"
                    f"Especificidade Positiva (Taxa de verdadeiro negativo): {specificity_positive*100:.2f} %\n" 
                    f"Especificidade Negativo (Taxa de falso positivo): {specificity_negative*100:.2f} %\n" 
                    f"Precisão: {precision*100:.2f} %\n"
                    f"Precisão Negativa: {negative_predictive_value*100:.2f} %\n" 
                    f"Acurácia: {accuracy*100:.2f} %\n")
            print('\n' * 2)
        return sensitivity, nfr, specificity_positive, specificity_negative, precision, negative_predictive_value, accuracy
    
    def fitting(self):
        print("Começo do Fitting")
        print('-'*150)
        best_acc = 0
        # Type tem relação com os tipos de tratamento de valores, sem normalização, normalização min-max e zscore
        for type in range(2):
            self.database = tratamento_dados(self.path_bd)
            if type == 1:
                self.database = self.normalizacao()
            elif type == 2:
                self.database = self.normalizacao(type='zscore')
            # Varia a porcentagem dos dados que são divididos entre treino e teste
            for percent_data in range(0,99,5):
                percent_data = percent_data * 0.01
                if percent_data != 0:
                    self.percent_data_train = percent_data
                    self.datatrain, self.datatest = self.divide_data(print_informations = False)
                    # Varia a quantidade de vizinhos
                    for neighbours in range(1,30):
                        self.neighbours = neighbours
                        # Varia o peso da distancia euclidiana
                        for weight in range(2,5):
                            self.weight_euclidian = weight
                            *values, acc = self.results(print_matrix=False)
                            if best_acc < acc:
                                best_percent = self.percent_data_train
                                best_acc = acc
                                best_neighbours = self.neighbours
                                best_weight = self.weight_euclidian
                                best_type = type
                        
        if best_type == 0:
            str_type = 'Sem Normalizar'       
        elif best_type == 1:
            str_type = 'Normalização Max-Min'
        elif best_type == 2:
            str_type = 'Normalização Z-Score'
            
        print(f"O melhor valor de acurácia foi atingido com os seguinte valores \n \
            Divisão dos dados: {best_percent*100:.2f}% \n \
            Quantidade de vizinhos: {best_neighbours}. \n \
            Peso da distancia euclidiana: {best_weight} \n \
            Tipo de normalização: {str_type} \n \
            A accurácia atingida foi de {best_acc*100:.2f}%")
        
        print('Com estes parâmetros, realizando novamente o código teremos ... ')
        self.path_bd = self.path_bd
        self.weight_euclidian = best_weight
        self.neighbours = best_neighbours
        self.percent_data_train = best_percent
        self.database = tratamento_dados(self.path_bd)
        if best_type == 1:
            self.normalizacao()
        elif best_type == 2:
            self.normalizacao(type="zscore")
            
        self.points = transform_data_points(self.database)
        self.datatrain, self.datatest = self.divide_data()
        self.results()
        
        
        
                
            
        
            
                
        
        
        
        
        
            
            
    

        

## Entrada de dados









caminho_arquivo = 'bd\diabetes.csv'
modelo_knn = knn(caminho_arquivo, percent_data_train=0.7, neighbours= 7)
print('Sem normalização!')
print('-'*100)
modelo_knn.test()
modelo_knn.results()
print('Normalização Min-Max')
print('-'*100)
modelo_knn = knn(caminho_arquivo, percent_data_train=0.7, neighbours= 7)
modelo_knn.normalizacao()
modelo_knn.test()
modelo_knn.results()
print('Normalização Zscore')
print('-'*100)
modelo_knn.normalizacao(type="zscore")
modelo_knn.test()
modelo_knn.results()
print('Sintonização')
print('-'*100)
modelo_knn.fitting()
