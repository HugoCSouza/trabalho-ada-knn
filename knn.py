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

class knn():
    def __init__(self, path_bd: str):
        print('Começou!')
        self.database = tratamento_dados(path_bd)
        
    def normalizacao(self):
        # Encontrar o valor mínimo e máximo na lista
        for variable, values in self.database.items():
            
            valor_minimo = min(values)
            valor_maximo = max(values)

            # Normalizar os valores utilizando a fórmula (x - min) / (max - min)
            valores_normalizados = [(x - valor_minimo) / (valor_maximo - valor_minimo) for x in values]
            self.database[variable] = valores_normalizados

def a():
    pass

## Entrada de dados









caminho_arquivo = 'bd\diabetes.csv'
modelo_knn = knn(caminho_arquivo)
modelo_knn.normalizacao()
print(modelo_knn.database)
