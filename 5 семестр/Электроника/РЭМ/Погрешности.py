import numpy as np

# Исходные данные
U_kV = np.array([30, 25, 20, 17, 15, 12, 10, 5, 2, 1.5, 1, 0.5])
I_pov_nA = np.array([0.444, 0.357, 0.307, 0.267, 0.286, 0.285, 0.243, 0.239, 0.296, 0.283, 0.298, 0.095])
I_otv_nA = np.array([0.570, 0.469, 0.395, 0.345, 0.370, 0.367, 0.310, 0.300, 0.349, 0.326, 0.332, 0.100])

# Погрешность измерения тока: 1 пА = 0.001 нА
dI_nA = 0.001 

# Расчёт коэффициента вторичной эмиссии
sigma = (I_otv_nA - I_pov_nA) / I_otv_nA

# Расчёт погрешности sigma по формуле передачи ошибок:
# sigma = 1 - I_pov / I_otv
# d(sigma) = sqrt( (dI_pov / I_otv)^2 + (I_pov * dI_otv / I_otv^2)^2 )
# При dI_pov = dI_otv = dI:
d_sigma = (dI_nA / I_otv_nA) * np.sqrt(1 + (I_pov_nA / I_otv_nA)**2)

# Функция для форматирования с запятой как десятичным разделителем
def fmt(val, decimals=4):
    return f"{val:.{decimals}f}".replace('.', ',')

# Вывод результатов в формате, готовом для вставки в LaTeX
print("U, кВ & I_пов, нА & I_отв, нА & \\Delta I, пА & \\sigma & \\Delta \\sigma \\\\")
print("\\hline")
for i in range(len(U_kV)):
    print(f"{fmt(U_kV[i], 1)} & {fmt(I_pov_nA[i], 3)} & {fmt(I_otv_nA[i], 3)} & 1 & {fmt(sigma[i], 4)} & {fmt(d_sigma[i], 4)} \\\\")