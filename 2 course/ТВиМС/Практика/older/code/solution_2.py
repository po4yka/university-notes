# -*- coding: utf-8 -*-

import math
from scipy import special
from itertools import product

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def comb(n, k):
    """Генерация сочетаний из `n` по `k` без повторений."""

    d = list(range(0, k))
    yield d

    while True:
        i = k - 1
        while i >= 0 and d[i] + k - i + 1 > n:
            i -= 1
        if i < 0:
            return

        d[i] += 1
        for j in range(i + 1, k):
            d[j] = d[j - 1] + 1

        yield d

def comb_sets(sets, m):
    """Генерация сочетаний из элементов множеств `sets` по `m` элементов."""

    for ci in comb(len(sets), m):
        for cj in product(*(sets[i] for i in ci)):
            yield cj

resultFile = open('result.txt', 'w')

FIRST_BOX_BALLS=8
FIRST_BOX_WHITE=50
FIRST_BOX_BLACK=30

SECOND_BOX_BALLS=7
SECOND_BOX_WHITE=40
SECOND_BOX_BLACK=20

allVar_1 = special.binom(80, 8)
allVar_2 = special.binom(60, 7)
resBinom_1=[]
resProb_1=[]
resBinom_2=[]
resProb_2=[]

# РАСЧЁТЫ ДЛЯ ПЕРВОГО ЯЩИКА

resultFile.write("Всего 8 шаров из ящика с 80 шарами можно достать: " + toFixed(allVar_1) + " способами\n\n")

resultFile.write("Все варианты достать шары из 1-ого ящика:\n\n")
for num in range(FIRST_BOX_BALLS+1):
    firstBinom = special.binom(FIRST_BOX_WHITE, num)
    secondBinom = special.binom(FIRST_BOX_BLACK, FIRST_BOX_BALLS-num)
    resBinom_1.append(firstBinom * secondBinom)
    res = "$A_" + str(num) + " = C_{" + str(FIRST_BOX_WHITE) +"}^" + str(num) + " \\cdot C_{" + str(FIRST_BOX_BLACK) +"}^" + str(FIRST_BOX_BALLS-num) + " = " + toFixed(firstBinom) + " \\cdot " + toFixed(secondBinom) + " = " + toFixed(resBinom_1[num]) + "$\n\n"
    resultFile.write(res)

resultFile.write("Соответствующие вероятности событий для 1-ого ящика:\n\n")
for num in range(FIRST_BOX_BALLS+1):
    resProb_1.append(resBinom_1[num]/allVar_1)
    res = "$P(A_" + str(num) + ") = \\dfrac{A_" + str(num) + "}{\\# \\Omega} = \\dfrac{" + str(toFixed(resBinom_1[num])) + "}{" + str(toFixed(allVar_1)) + "} = " + str(resProb_1[num]) + "$\n\n"
    resultFile.write(res)

# РАСЧЁТЫ ДЛЯ ВТОРОГО ЯЩИКА

resultFile.write("Всего 7 шаров из ящика с 60 шарами можно достать: " + toFixed(allVar_2) + " способами\n\n")

resultFile.write("Все варианты достать шары из 2-ого ящика:\n\n")
for num in range(SECOND_BOX_BALLS+1):
    firstBinom = special.binom(SECOND_BOX_WHITE, num)
    secondBinom = special.binom(SECOND_BOX_BLACK, SECOND_BOX_BALLS-num)
    resBinom_2.append(firstBinom * secondBinom)
    res = "$B_" + str(num) + " = C_{" + str(SECOND_BOX_WHITE) + "}^" + str(num) + " \\cdot C_{" + str(SECOND_BOX_BLACK) + "}^" + str(SECOND_BOX_BALLS-num) + " = " + toFixed(firstBinom) + " \\cdot " + toFixed(secondBinom) + " = " + toFixed(resBinom_2[num]) + "$\n\n"
    resultFile.write(res)

resultFile.write("Соответствующие вероятности событий для 2-ого ящика:\n\n")
for num in range(SECOND_BOX_BALLS+1):
    resProb_2.append(resBinom_2[num]/allVar_2)
    res = "$P(B_" + str(num) + ") = \\dfrac{B_" + str(num) + "}{\\# \\Omega} = \\dfrac{" + str(toFixed(resBinom_2[num])) + "}{" + str(toFixed(allVar_2)) + "} = " + str(resProb_2[num]) + "$\n\n"
    resultFile.write(res)


resultFile.write("\n\nВозможные сочатания событий $A$ и $B$ для получения от 1 до 15 белых шаров в 3-ем ящике:\n\n")

combSet_1=['A_0', 'A_1', 'A_2', 'A_3', 'A_4', 'A_5', 'A_6', 'A_7', 'A_8']
combSet_2=['B_0', 'B_1', 'B_2', 'B_3', 'B_4', 'B_5', 'B_6', 'B_7']

combRes=[]
for comb in comb_sets([combSet_1, combSet_2], 2):
    combRes.append(comb)


combResProb=[]
for i in range(1, 16):
    resultFile.write("\nКомбинации для " + str(i) + " шаров в 3-ем ящике:\n")
    res = 0
    for curr in combRes:
        if (int(curr[0][2]) + int(curr[1][2])) == i:
            resultFile.write("$(" + curr[0] + ", " + curr[1] + ")$\n")
            resultFile.write("$P(A_" + (curr[0][2]) + ") \\cdot P(B_" + (curr[1][2]) + ") = " + str(resProb_1[int(curr[0][2])] * resProb_2[int(curr[1][2])]) + "$\n")
            res += resProb_1[int(curr[0][2])] * resProb_2[int(curr[1][2])]
    resultFile.write("Итоговая вероятность: " + str(res) + "\n")
    combResProb.append(res)

resultCombH=0
for i in combResProb:
    resultCombH += i
resultFile.write("\n\nРезультат сложения данных вероятностей: " + str(resultCombH) + "\n")

result=0
for i in range(1,16):
    result += ((i / 15.0) * combResProb[i - 1])

resultFile.write("\nОТВЕТ: " + str(result) + "\n")

resultFile.write("\nРасчёты 2-ого пункта:\n\n")

for i in range(1,8):
    resultFile.write(str(combResProb[i] * (i / 15.0) / result) + "\n")

resultFile.write("P(A_0|H_1) = \n")
resultFile.write(str((0.004014428327695423 * 0.000201911772280385) / 1.515395415152839e-06) + "\n")

resultFile.write("P(P(A_0|(H_1|C))) = \n")
resultFile.write(str(0.5348837209302326 * 2.633348913284238e-06) + "\n\n")


resultFile.write("P(A_0|H_2) = \n")
resultFile.write(str((0.0313125409560243 * 0.000201911772280385) / 2.5455706161747633e-05) + "\n")

resultFile.write("P(P(A_0|(H_2|C))) = \n")
resultFile.write(str(0.2483675211703085 * 5.276972620662395e-05) + "\n\n")


resultFile.write("P(A_0|H_3) = \n")
resultFile.write(str((0.12394547461759618 * 0.000201911772280385) / 0.00025505367666534906) + "\n")

resultFile.write("P(P(A_0|(H_3|C))) = \n")
resultFile.write(str(0.0005294281035637105 * 0.09812072020827407) + "\n\n")


resultFile.write("P(A_0|H_4) = \n")
resultFile.write(str((0.2697636800500623 * 0.000201911772280385) / 0.001705935000371956) + "\n")

resultFile.write("P(P(A_0|(H_4|C))) = \n")
resultFile.write(str(0.031928803104403575 * 0.0033407673354175073) + "\n\n")


resultFile.write("P(A_0|H_5) = \n")
resultFile.write(str((0.32371641606007473 * 0.000201911772280385) / 0.008073521060592307) + "\n")

resultFile.write("P(P(A_0|(H_5|C))) = \n")
resultFile.write(str(0.008095867316428222 * 0.014454606217420484) + "\n\n")


resultFile.write("P(A_0|H_6) = \n")
resultFile.write(str((0.19877323793162485 * 0.000201911772280385) / 0.02794557202034627) + "\n")

resultFile.write("P(P(A_0|(H_6|C))) = \n")
resultFile.write(str(0.0014361723110718318 * 0.044739552725894506) + "\n\n")


resultFile.write("P(A_0|H_7) = \n")
resultFile.write(str((0.04827350064053746 * 0.000201911772280385) / 0.07208039050283002) + "\n")

resultFile.write("P(P(A_0|(H_7|C))) = \n")
resultFile.write(str(0.00013522385215333335 * 0.10119897439084223) + "\n\n")

resultFile.write("Результат: " + str(1.4085354652450578e-06 + 1.3106286090775058e-05 + 5.194786682017199e-05 + 0.00010666670247016857 + 0.00011702257404745466 + 6.425370683466798e-05 + 1.3684515151096217e-05))

resultFile.close()