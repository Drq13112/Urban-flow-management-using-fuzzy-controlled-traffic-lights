import os
import sys
import traci
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import time
import matplotlib.pyplot as plt

def fuzzy_setup():
    peatones  = ctrl.Antecedent(np.arange(0, 50, 0.1), 'peatones')
    vehiculos = ctrl.Antecedent(np.arange(0, 30, 0.1), 'vehiculos')
    tiempo_espera_peatones = ctrl.Antecedent(np.arange(0, 460, 1), 'tiempo_espera_peatones')
    semaforo = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'semaforo')

    semaforo['verde'] = fuzz.trimf(semaforo.universe, [0, 0, 0.5]) 
    semaforo['rojo'] = fuzz.trimf(semaforo.universe, [0.5, 1, 1]) 
    #SUGENO semaforo['verde'] = fuzz.trimf(semaforo.universe, [0.5, 0.5, 0.5]) 
    #SUGENO semaforo['rojo'] = fuzz.trimf(semaforo.universe, [1.5, 1.5, 1.5]) 
    #semaforo.view()

    peatones['ninguno'] = fuzz.trapmf(peatones.universe, [-1, 0, 0.8, 0.9])
    peatones['pocos'] = fuzz.trapmf(peatones.universe, [0.9, 1.9, 9, 10])
    peatones['bastantes'] = fuzz.trimf(peatones.universe, [5, 15, 25])
    peatones['muchos'] = fuzz.trapmf(peatones.universe,  [20, 30, 51, 55])
    #peatones.view()

    vehiculos['ninguno'] = fuzz.trapmf(vehiculos.universe, [-1, 0, 0.8, 0.9])
    vehiculos['pocos'] = fuzz.trapmf(vehiculos.universe, [0.9, 1.9, 9, 10])
    vehiculos['bastantes'] = fuzz.trapmf(vehiculos.universe, [8, 10, 18, 20])
    vehiculos['muchos'] = fuzz.trapmf(vehiculos.universe, [15, 25, 30, 35])
    #vehiculos.view()


    tiempo_espera_peatones['poco'] = fuzz.trapmf(tiempo_espera_peatones.universe, [-1,0, 100, 200])
    tiempo_espera_peatones['bastante'] = fuzz.trapmf(tiempo_espera_peatones.universe, [100, 200, 300, 400])
    tiempo_espera_peatones['mucho'] = fuzz.trapmf(tiempo_espera_peatones.universe, [300, 400, 500, 550])
    #tiempo_espera_peatones.view()

    ##REGLAS

    rule1a = ctrl.Rule(peatones['ninguno'] & ~vehiculos['ninguno'], semaforo['verde'])
    rule1b = ctrl.Rule(vehiculos['ninguno'] & ~peatones['ninguno'], semaforo['rojo'])
    rule1c = ctrl.Rule(vehiculos['ninguno'] &  peatones['ninguno'], semaforo['verde'])

    rule2a = ctrl.Rule(peatones['pocos'] & vehiculos['pocos'] & tiempo_espera_peatones['poco'] , semaforo['verde'])
    rule2b = ctrl.Rule(peatones['pocos'] & vehiculos['pocos'] &  ~tiempo_espera_peatones['poco']  , semaforo['rojo'])
    rule2ca = ctrl.Rule(peatones['pocos'] & vehiculos['bastantes'] & ~tiempo_espera_peatones['mucho'] , semaforo['verde'])
    rule2cb = ctrl.Rule(peatones['pocos'] & vehiculos['muchos'] & ~tiempo_espera_peatones['mucho'] , semaforo['verde'])
    rule2da = ctrl.Rule(peatones['pocos'] & vehiculos['bastantes'] &  tiempo_espera_peatones['mucho'] , semaforo['rojo'])
    rule2db = ctrl.Rule(peatones['pocos'] & vehiculos['muchos'] &  tiempo_espera_peatones['mucho'] , semaforo['rojo'])

    rule3a = ctrl.Rule(peatones['bastantes'] & vehiculos['pocos'], semaforo['rojo'])
    rule3ba = ctrl.Rule(peatones['bastantes'] & vehiculos['bastantes'] & ~tiempo_espera_peatones['mucho'], semaforo['verde'])
    rule3bb = ctrl.Rule(peatones['bastantes'] & vehiculos['muchos'] & ~tiempo_espera_peatones['mucho'], semaforo['verde'])
    #La unica regla que no me convence es esta, ya que si por ejemplo hay 16 vehiculos y 8 coches enbtonces da igual el tiempo que lleven esperando porque se activa
    #la regla 3a, pero en el momento en el que los vehiculos pasan de 8 a 9, entonces empiezan a ser bastantes y se activa la regla 3b, lo que supone que los peatones
    #tienen que esperar el tiempo maximo. Es decir por un vehiculo los peatones deben esperar 36 segundos en vez de poder pasar inmediatamente. Estaria bien hacer algo 
    #para que no fuera tan extremo este comportamiento
    rule3ca = ctrl.Rule(peatones['bastantes'] & vehiculos['bastantes'] & tiempo_espera_peatones['mucho'], semaforo['rojo'])
    rule3cb = ctrl.Rule(peatones['bastantes'] & vehiculos['muchos'] & tiempo_espera_peatones['mucho'], semaforo['rojo'])

    rule4a = ctrl.Rule(peatones['muchos'] & vehiculos['pocos']  , semaforo['rojo'])
    rule4b = ctrl.Rule(peatones['muchos'] & vehiculos['bastantes'] & tiempo_espera_peatones['poco'] , semaforo['verde'])
    rule4c = ctrl.Rule(peatones['muchos'] & vehiculos['bastantes'] & ~tiempo_espera_peatones['poco'] , semaforo['rojo'])
    rule4d = ctrl.Rule(peatones['muchos'] & vehiculos['muchos'] & ~tiempo_espera_peatones['mucho'], semaforo['verde'])
    rule4e = ctrl.Rule(peatones['muchos'] & vehiculos['muchos'] & tiempo_espera_peatones['mucho'] , semaforo['rojo'])



    control_semaforizacion = ctrl.ControlSystem([rule1a, rule1b, rule1c, rule2a, rule2b, rule2ca, rule2cb, rule2da, rule2db, rule3a, rule3ba, rule3bb, rule3ca, rule3cb, rule4a, rule4b, rule4c, rule4d, rule4e])
    semaforizacion = ctrl.ControlSystemSimulation(control_semaforizacion)
    return semaforizacion




def get_fuzzy_output(semaforizacion,peatones, vehiculos, tiempo_espera_peatones):
    semaforizacion.input['peatones'] = peatones
    semaforizacion.input['vehiculos'] = vehiculos
    semaforizacion.input['tiempo_espera_peatones'] = tiempo_espera_peatones
    semaforizacion.compute()
    return semaforizacion.output['semaforo']


def calcular_trafico_en_cruce(cruce_id):
    """
    Calcula el tráfico esperando en un cruce en el simulador SUMO.

    Parameters:
    - cruce_id: Identificador del cruce.

    Returns:
    - trafico_esperando: Número de vehículos esperando en el cruce.
    """
    # Obtener la lista de vehículos en el cruce
    vehiculos_en_cruce = traci.junction.getIDList()

    # Contar el número de vehículos esperando en el cruce
    trafico_esperando = 0
    for vehiculo_id in vehiculos_en_cruce:
        if traci.vehicle.isStopped(vehiculo_id):
            trafico_esperando += 1

    return trafico_esperando


if __name__ == "__main__":

    sumoBinary = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui.exe"
    sumoConfig = "C:/Users/User/Downloads/Code/Avenida/Avenida.sumocfg"
    sumoCmd = [sumoBinary, '-c', sumoConfig,"--start"]
    print("here")
    traci.start(sumoCmd)
    
    semaforizacion=fuzzy_setup()
    # Definir la duración del ciclo de semáforo en segundos
    # Bucle principal
    tiempo_espera_peatones=0

    ids = []
    persons = []
    vehicleWaitingTimes = {}
    PersonsWaitingTimes = {}
    temporal_wait_time = []
    Persontemporal_wait_time = []
    #while traci.simulation.getMinExpectedNumber() > 0:
    while traci.simulation.getTime() <= 5000:
        # Obtener el tiempo actual de la simulación
        simulation_time = traci.simulation.getTime()

        #print(current_state)
        peatones = len(traci.multientryexit.getLastStepVehicleIDs('SensorPersonas'))
        stopped_pedestrians_ids = traci.multientryexit.getLastStepVehicleIDs('SensorPersonas')
        vehiculos = len(traci.multientryexit.getLastStepVehicleIDs('SensorCoches'))
        
        for pedestrian_id in stopped_pedestrians_ids:
            waiting_time = traci.person.getWaitingTime(pedestrian_id)
            if waiting_time > tiempo_espera_peatones:
                tiempo_espera_peatones=waiting_time #ahora el tiempo de espera es el tiempo que lleva esperando el primer peaton que llegó al cruce
            #tiempo_espera_peatones=tiempo_espera_peatones+waiting_time #cada vez que llga un nuevo peaton suma su tiempo de espera
        
        idlist = traci.vehicle.getIDList()        
        personslist = traci.person.getIDList()

        for elemento in idlist:
            if elemento not in ids:
                ids.append(elemento)
        
        for elemento in personslist:
            if elemento not in persons:
                persons.append(elemento)
                

        waiting_times = {}
        for elem in idlist:
            # Simulation of traci.vehicle.getAccumulatedWaitingTime()
            waiting_time = traci.vehicle.getAccumulatedWaitingTime(elem)
            waiting_times[elem] = waiting_time if waiting_time is not None else -5

        pwaiting_times = {}
        for elem in personslist:
            # Simulation of traci.vehicle.getAccumulatedWaitingTime()
            pwaiting_time = traci.person.getWaitingTime(elem)
            pwaiting_times[elem] = pwaiting_time if pwaiting_time is not None else -5




        for elem in idlist:
            if elem not in vehicleWaitingTimes:
                vehicleWaitingTimes[elem] = waiting_times.get(elem)  # Inicializar tiempo de espera a 0 si es un nuevo elemento
            if waiting_times.get(elem) > vehicleWaitingTimes[elem]:
                vehicleWaitingTimes[elem] = waiting_times.get(elem, 0)
                #evo temporal
                media_wait_time = sum(vehicleWaitingTimes.values()) / len(vehicleWaitingTimes)
                temporal_wait_time.append(media_wait_time)



        for elem in personslist:
            if elem not in PersonsWaitingTimes:
                PersonsWaitingTimes[elem] = pwaiting_times.get(elem)  # Inicializar tiempo de espera a 0 si es un nuevo elemento
            if pwaiting_times.get(elem) > PersonsWaitingTimes[elem]:
                PersonsWaitingTimes[elem] += pwaiting_times.get(elem, 0)
                #evo temporal
                Personmedia_wait_time = sum(PersonsWaitingTimes.values()) / len(PersonsWaitingTimes)
                Persontemporal_wait_time.append(Personmedia_wait_time)




        # Aplicar el nuevo estado del semáforo
        
        print("peatones: ", peatones)
        print("vehiculos: ", vehiculos)
        print("tiempo_espera_peatones: ", tiempo_espera_peatones)

        output=get_fuzzy_output(semaforizacion, peatones, vehiculos, tiempo_espera_peatones)
        state=traci.trafficlight.getRedYellowGreenState("J1")
        print(output)
        if output <= 0.5 and state == "rrrrG":
            traci.trafficlight.setRedYellowGreenState("J1", "rrrrr")
            for i in range(10):
                traci.simulationStep()
            traci.trafficlight.setRedYellowGreenState("J1", "GGGGr")
            for i in range(10):
                traci.simulationStep()
        elif output > 0.5 and state == "GGGGr":
            traci.trafficlight.setRedYellowGreenState("J1", "yyyyr")
            for i in range(5):
                traci.simulationStep()
            traci.trafficlight.setRedYellowGreenState("J1", "rrrrG")
            tiempo_espera_peatones=0
            for i in range(10):
                traci.simulationStep()
            
        # Avanzar la simulación
        traci.simulationStep()
        #time.sleep(0.1)
    # Detener la simulación y cerrar la conexión TraCI
    traci.close()

    ploting_data = vehicleWaitingTimes
    keys = list(vehicleWaitingTimes.keys())
    values = list(vehicleWaitingTimes.values())
    media = sum(vehicleWaitingTimes.values()) / len(vehicleWaitingTimes)

    keys2 = list(PersonsWaitingTimes.keys())
    values2 = list(PersonsWaitingTimes.values())
    media2 = sum(PersonsWaitingTimes.values()) / len(PersonsWaitingTimes)
    print("Media: ", media)
    # Crear un gráfico de barras
    """
    plt.figure(dpi=200)  # Ajustar la resolución a 300 dpi
    plt.bar(keys, values, color='blue')
    plt.axhline(y=media, color='red', linestyle='--', label=f'Media: {media:.2f}')
    # Personalizar el gráfico
    #plt.title('Gráfico de Barras')
    plt.xlabel('Vehiculos')
    plt.ylabel('Tiempo de espera')
    plt.xticks([])  # Eliminar las etiquetas del eje x
    np.savetxt('AA.txt', values, fmt='%1.2f', newline='\n')

    # Mostrar el gráfico
    plt.show() """
    np.savetxt('ZebraAltaFrec_Fuzzy.txt', values, fmt='%1.2f', newline='\n')
    np.savetxt('ZebraPersonAltaFrec_Fuzzy.txt', values2, fmt='%1.2f', newline='\n')



    # Guardar el diccionario como JSON en un archivo de texto
    """ with open('semaforosPersonBajaFrec_Fuzzy.txt', 'w') as file:
        json.dump(semaforos_data, file) """
    
    #Evolucion temporal vehiculos/personas
    #np.savetxt('ZebraEvolucionPersonAltaFrec_Fuzzy.txt', Persontemporal_wait_time)
    #np.savetxt('ZebraEvolucionAltaFrec_Fuzzy.txt', temporal_wait_time)
    """ # Crear un gráfico de barras para el vector_medias
    plt.bar(range(len(Persontemporal_wait_time)), Persontemporal_wait_time, color='blue')

    # Personalizar el gráfico
    plt.xlabel('Tiempo')
    plt.ylabel('Media de tiempos de espera')
    #plt.xticks(range(len(temporal_wait_time)), [str(i) for i in range(1, len(temporal_wait_time) + 1)])

    # Mostrar el gráfico
    plt.show() """