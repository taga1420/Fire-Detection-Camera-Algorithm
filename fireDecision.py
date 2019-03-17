import heatAnalysis
import matplotlib.pyplot as plt
from dbOperations import insertData

index_list, r_list, area_list, temp_list, r_eq, area_eq, temp_eq, directory, go, now = heatAnalysis.heatAnalysis()

# Pesquisar sobre caracteristicas de deflagração de incendio para confirmar condições
if r_eq[0] < abs(2) and area_eq[0] > 1 and temp_eq[0] > 1:
    resposta = 'INCENDIO!!!!'

else:
    resposta = 'Esta tudo bem'

file = open('%s/Temp_Info.txt' % directory, 'a')
file.writelines(f'\n {resposta}')
file.close()

# SEND INFORMATION TO DATABASE
insertData([go.year, go.month, go.day], resposta, now)
print(resposta)

plt.figure(1)
plt.title('Evolution Analysis')

plt.subplot(311)
plt.plot(index_list, r_list)
plt.xlabel('Time (s)')
plt.ylabel('Euclidean Distance (pixels)')

plt.subplot(312)
plt.plot(index_list, area_list)
plt.xlabel('Time (s)')
plt.ylabel('Area (pixels)')

plt.subplot(313)
plt.plot(index_list, temp_list)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (ºC')

plt.show()
