import numpy as np
import matplotlib.pyplot as plt
import json

# PLOTS de barras
# Función para cargar valores desde un archivo de texto
def cargar_valores(archivo):
    return np.loadtxt(archivo)

# Cargar valores desde los archivos de texto
valores1 = cargar_valores('ZebraPersonAltaFrec_Base.txt')
valores2 = cargar_valores('ZebraPersonAltaFrec_Fuzzy.txt')

# Calcular medias
media1 = np.mean(valores1)
media2 = np.mean(valores2)

# Crear un gráfico de barras con ambos conjuntos de valores
plt.bar(np.arange(len(valores1)), valores1, color='blue', label='Valores sin fuzzy')
plt.bar(np.arange(len(valores2)), valores2, color=(0, 1, 0), label='Valores con fuzzy')  # Color verde (0, 255, 0)

# Dibujar líneas discontinuas para representar las medias
plt.axhline(y=media1, color='blue', linestyle='--', label=f'Media sin fuzzy: {media1:.2f}')
plt.axhline(y=media2, color=(0, 1, 0), linestyle='--', label=f'Media con fuzzy: {media2:.2f}')  # Color verde oscuro (0, 128, 0)

# Personalizar el gráfico
plt.xlabel('Vehículos')
plt.ylabel('Tiempo de espera')
# Invertir el orden de los elementos en la leyenda
handles, labels = plt.gca().get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
plt.legend(handles, labels)
# Mostrar el gráfico
plt.show()



#PLOTS de semaforos
# Función para cargar datos desde un archivo JSON
def cargar_datos(archivo):
    with open(archivo, 'r') as file:
        return json.load(file)

# Cargar datos desde los archivos
datos_semaforos1 = cargar_datos('semaforosAltaFrec_Base.txt')
datos_semaforos2 = cargar_datos('semaforosAltaFrec_Fuzzy.txt')

# Extraer los nombres de las variables y sus valores para ambos conjuntos de datos
nombres_semaforos = list(datos_semaforos1.keys())
valores_semaforos1 = list(datos_semaforos1.values())
valores_semaforos2 = list(datos_semaforos2.values())

# Calcular las medias de ambos conjuntos de datos
media_semaforos1 = np.mean(valores_semaforos1)
media_semaforos2 = np.mean(valores_semaforos2)

# Crear un gráfico de barras con ambos conjuntos de datos
bar_width = 0.35
bar1 = plt.bar(nombres_semaforos, valores_semaforos1, width=bar_width, label='Valores sin fuzzy', color='blue')
bar2 = plt.bar([x + bar_width for x in range(len(nombres_semaforos))], valores_semaforos2, width=bar_width, label='Valores con fuzzy', color=(0, 1, 0))

# Dibujar líneas discontinuas para representar las medias
plt.axhline(y=media_semaforos1, color='blue', linestyle='--', label=f'Media sin fuzzy: {media_semaforos1:.2f}')
plt.axhline(y=media_semaforos2, color=(0, 1, 0), linestyle='--', label=f'Media con fuzzy: {media_semaforos2:.2f}')

# Personalizar el gráfico
plt.xlabel('Semáforo')
plt.ylabel('Tiempo de espera')
plt.xticks([x + bar_width/2 for x in range(len(nombres_semaforos))], nombres_semaforos, rotation=45, ha='right')
# Invertir el orden de los elementos en la leyenda
handles, labels = plt.gca().get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
plt.legend(handles, labels)

# Mostrar el gráfico
plt.tight_layout()
plt.show()


#PLOTS evolucion temporal
# Importar datos desde los archivos
vector1 = np.loadtxt('ZebraEvolucionPersonBajaFrec_Base.txt')
vector2 = np.loadtxt('ZebraEvolucionPersonBajaFrec_Fuzzy.txt')

# Crear un gráfico de línea con ambos vectores
plt.plot(vector1, label='Evolución temporal sin fuzzy', linewidth=1.5)
plt.plot(vector2, label='Evolución temporal con fuzzy', color=(0, 1, 0), linewidth=1.5)  # (0, 1, 0) es verde en RGB



# Personalizar el gráfico
plt.xlabel('Tiempo')
plt.ylabel('Media de tiempos esperados')
plt.legend()

# Mostrar el gráfico
plt.show()