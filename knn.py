## Entrada de dados
points = list()
with open('bd\diabetes.csv','r') as bd:
    for linha in bd.readlines():
        linha = linha.replace('\n','')
        elements = linha.split(',')
        if all([element.replace('.','').isnumeric() for element in elements]):
            lista_convertida = tuple(map(float, elements))
            points.append(lista_convertida)
print(len(points))

