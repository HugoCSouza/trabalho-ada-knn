## Entrada de dados
pregnancies, glucose, blood_presure, skin_thicknesss, insulin, bmi, diabetes_pedrigree_function, age, outcome = list(), list(), list(),  \
    list(), list(), list(), list(), list(), list()
with open('bd\diabetes.csv','r') as bd:
    for linha in bd.readlines():
        elements = linha.split(',')
        pregnancies.append(elements[0]), glucose.append(elements[1]), blood_presure.append(elements[2]), skin_thicknesss.append(elements[3]), \
            insulin.append(elements[4]), bmi.append(elements[5]),diabetes_pedrigree_function.append(elements[6]), age.append(elements[7]), \
                outcome.append(elements[8])
    print(pregnancies)