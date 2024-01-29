import os
import sys
import traci
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import time
import matplotlib.pyplot as plt
import threading
from collections import deque
import json


# Definir variables globales
SemaforoJ55WaitingTime = 0
SemaforoJ58WaitingTime = 0
SemaforoJ61WaitingTime = 0
SemaforoJ15WaitingTime = 0
SemaforoJ14WaitingTime = 0
SemaforoJ13WaitingTime = 0
SemaforoJ4WaitingTime = 0
SemaforoJ19WaitingTime = 0
SemaforoJ54WaitingTime = 0
SemaforoJ3WaitingTime = 0
SemaforoJ56WaitingTime = 0

def SemaforosWaitingTime(input_str,tiempoV,tiempoH):
    global SemaforoJ55WaitingTime
    variable_name = "Semaforo" + input_str + "WaitingTime"
    globals()[variable_name] = globals().get(variable_name, 0) + tiempoV + tiempoH


    if "J55" in input_str:
        print("Realizando acción para el caso 1")
        #SemaforoJ55WaitingTime += tiempoV + tiempoH

                
    elif "J58" in input_str:
        # Acción para el caso 2
        print("Realizando acción para el caso 2")
    elif "J61" in input_str:
        # Acción para el caso 3
        print("Realizando acción para el caso 3")
    elif "J57" in input_str:
        # Acción para el caso 3
        print("Realizando acción para el caso 3")
    elif "J15" in input_str:
        # Acción para el caso 3
        print("Realizando acción para el caso 3")
    elif "J14" in input_str:
        # Acción para el caso 3
        print("Realizando acción para el caso 3")
    elif "J13" in input_str:
        # Acción para el caso 3
        print("Realizando acción para el caso 3")
    elif "J4" in input_str:
        # Acción para el caso 3
        print("Realizando acción para el caso 3")
    elif "J19" in input_str:
        # Acción para el caso 3
        print("Realizando acción para el caso 3")
    elif "J54" in input_str:
        # Acción para el caso 3
        print("Realizando acción para el caso 3")
    elif "J3" in input_str:
        # Acción para el caso 3
        print("Realizando acción para el caso 3")
    elif "J56" in input_str:
        # Acción para el caso 3
        print("Realizando acción para el caso 3")
    else:
        # Acción por defecto si no coincide con ningún caso
        print("String no reconocido. Realizando acción por defecto")


def fuzzy_setup():
    peatones_vert   = ctrl.Antecedent(np.arange(0, 50, 0.1), 'peatones_vert')
    peatones_horiz  = ctrl.Antecedent(np.arange(0, 50, 0.1), 'peatones_horiz')
    vehiculos_vert  = ctrl.Antecedent(np.arange(0, 30, 0.1), 'vehiculos_vert')
    vehiculos_horiz = ctrl.Antecedent(np.arange(0, 30, 0.1), 'vehiculos_horiz')
    tiempo_peatones_vert   = ctrl.Antecedent(np.arange(0, 460, 1), 'tiempo_peatones_vert')
    tiempo_peatones_horiz  = ctrl.Antecedent(np.arange(0, 460, 1), 'tiempo_peatones_horiz')
    tiempo_vehiculos_vert  = ctrl.Antecedent(np.arange(0, 250, 1), 'tiempo_vehiculos_vert')
    tiempo_vehiculos_horiz = ctrl.Antecedent(np.arange(0, 250, 1), 'tiempo_vehiculos_horiz')
    semaforo = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'semaforo')

    semaforo['VerdeHoriz_RojoVert'] = fuzz.trimf(semaforo.universe, [0, 0, 0.5]) 
    semaforo['RojoHoriz_VerdeVert'] = fuzz.trimf(semaforo.universe, [0.5, 1, 1]) 
    #semaforo.view()

    peatones_vert['ninguno'] = fuzz.trapmf(peatones_vert.universe, [-1, 0, 0.8, 0.9])
    peatones_vert['pocos'] = fuzz.trapmf(peatones_vert.universe, [0.9, 1.9, 9, 10])
    peatones_vert['bastantes'] = fuzz.trapmf(peatones_vert.universe, [8, 13,23, 28])
    peatones_vert['muchos'] = fuzz.trapmf(peatones_vert.universe,  [20, 30, 51, 55])
    #peatones_vert.view()

    peatones_horiz['ninguno'] = fuzz.trapmf(peatones_horiz.universe, [-1, 0, 0.8, 0.9])
    peatones_horiz['pocos'] = fuzz.trapmf(peatones_horiz.universe, [0.9, 1.9, 9, 10])
    peatones_horiz['bastantes'] = fuzz.trapmf(peatones_horiz.universe, [8, 13,23, 28])
    peatones_horiz['muchos'] = fuzz.trapmf(peatones_horiz.universe,  [20, 30, 51, 55])
    #peatones_horiz.view()

    vehiculos_vert['ninguno'] = fuzz.trapmf(vehiculos_vert.universe, [-1, 0, 0.8, 0.9])
    vehiculos_vert['pocos'] = fuzz.trapmf(vehiculos_vert.universe, [0.9, 1.9, 9, 10])
    vehiculos_vert['bastantes'] = fuzz.trapmf(vehiculos_vert.universe, [8, 10, 18, 20])
    vehiculos_vert['muchos'] = fuzz.trapmf(vehiculos_vert.universe, [15, 25, 30, 35])
    #vehiculos_vert.view()

    vehiculos_horiz['ninguno'] = fuzz.trapmf(vehiculos_horiz.universe, [-1, 0, 0.8, 0.9])
    vehiculos_horiz['pocos'] = fuzz.trapmf(vehiculos_horiz.universe, [0.9, 1.9, 9, 10])
    vehiculos_horiz['bastantes'] = fuzz.trapmf(vehiculos_horiz.universe, [8, 10, 18, 20])
    vehiculos_horiz['muchos'] = fuzz.trapmf(vehiculos_horiz.universe, [15, 25, 30, 35])
    #vehiculos_horiz.view()

    tiempo_peatones_vert['poco'] = fuzz.trapmf(tiempo_peatones_vert.universe, [-1,0, 100, 200])
    tiempo_peatones_vert['bastante'] = fuzz.trapmf(tiempo_peatones_vert.universe, [100, 200, 300, 400])
    tiempo_peatones_vert['mucho'] = fuzz.trapmf(tiempo_peatones_vert.universe, [300, 400, 500, 550 ])
    #tiempo_peatones_vert.view()

    tiempo_peatones_horiz['poco'] = fuzz.trapmf(tiempo_peatones_horiz.universe, [-1,0, 100, 200])
    tiempo_peatones_horiz['bastante'] = fuzz.trapmf(tiempo_peatones_horiz.universe, [100, 200, 300, 400])
    tiempo_peatones_horiz['mucho'] = fuzz.trapmf(tiempo_peatones_horiz.universe, [300, 400, 500, 550 ])
    #tiempo_peatones_horiz.view()

    tiempo_vehiculos_vert['poco'] = fuzz.trapmf(tiempo_vehiculos_vert.universe, [-1,0, 50, 100])
    tiempo_vehiculos_vert['bastante'] = fuzz.trapmf(tiempo_vehiculos_vert.universe, [50, 100, 150, 200])
    tiempo_vehiculos_vert['mucho'] = fuzz.trapmf(tiempo_vehiculos_vert.universe, [150, 200, 250, 300])
    #tiempo_vehiculos_vert.view()

    tiempo_vehiculos_horiz['poco'] = fuzz.trapmf(tiempo_vehiculos_horiz.universe, [-1,0, 50, 100])
    tiempo_vehiculos_horiz['bastante'] = fuzz.trapmf(tiempo_vehiculos_horiz.universe, [50, 100, 150, 200])
    tiempo_vehiculos_horiz['mucho'] = fuzz.trapmf(tiempo_vehiculos_horiz.universe, [150, 200, 250, 300])
    #tiempo_vehiculos_horiz.view()

    ##REGLAS---------------------------------
    #Gestion del paso de los peatones(cuando no hay vehiculos)
    # Como el cambio de color para los vehiculos tambien genera fases de color verde para los peatones, la unica condicion para que los peatones modifiquen el estado del semaforo
    # es que lleven mucho tiempo esperando. Esto puede generar situaciones en la que los peatones esperen demasiado de forma estupida, por ejemplo, que una masa grande de peatones 
    # tenga que esperar para cruzar cuando solo viene un vehiculo. Es un fallo asumible, ya que la idea del trabajo es gestionar mejor los atascos y el trafico vehicular, y de esta forma
    # se reduce bastante el numero de reglas y su dificultad. 
    # Ademas en la vida real en situaciones de este tipo los peatones crucarían aunque su semaforo esté en rojo al ver que no viene ningun vehiculo
    rule1a = ctrl.Rule( vehiculos_horiz['ninguno'] & vehiculos_vert['ninguno'] &  peatones_horiz['ninguno'] &  peatones_vert['ninguno']                                                                        , semaforo['VerdeHoriz_RojoVert'])
    rule1b = ctrl.Rule( vehiculos_horiz['ninguno'] & vehiculos_vert['ninguno'] &  peatones_horiz['ninguno'] & ~peatones_vert['ninguno']                                                                        , semaforo['RojoHoriz_VerdeVert'])
    rule1c = ctrl.Rule( vehiculos_horiz['ninguno'] & vehiculos_vert['ninguno'] & ~peatones_horiz['ninguno'] &  peatones_vert['ninguno']                                                                        , semaforo['VerdeHoriz_RojoVert'])
    rule1d = ctrl.Rule( vehiculos_horiz['ninguno'] & vehiculos_vert['ninguno'] & ~peatones_horiz['ninguno'] & ~peatones_vert['ninguno'] & tiempo_peatones_horiz['poco']     & tiempo_peatones_vert['poco']     , semaforo['VerdeHoriz_RojoVert'])
    rule1e = ctrl.Rule( vehiculos_horiz['ninguno'] & vehiculos_vert['ninguno'] & ~peatones_horiz['ninguno'] & ~peatones_vert['ninguno'] & tiempo_peatones_horiz['poco']     & tiempo_peatones_vert['bastante'] , semaforo['RojoHoriz_VerdeVert'])
    rule1f = ctrl.Rule( vehiculos_horiz['ninguno'] & vehiculos_vert['ninguno'] & ~peatones_horiz['ninguno'] & ~peatones_vert['ninguno'] & tiempo_peatones_horiz['bastante'] & tiempo_peatones_vert['poco']     , semaforo['VerdeHoriz_RojoVert'])
    rule1g = ctrl.Rule( vehiculos_horiz['ninguno'] & vehiculos_vert['ninguno'] & ~peatones_horiz['ninguno'] & ~peatones_vert['ninguno'] & tiempo_peatones_horiz['bastante'] & tiempo_peatones_vert['bastante'] , semaforo['VerdeHoriz_RojoVert'])
    rule1h = ctrl.Rule(                                                          ~peatones_horiz['ninguno']                             & tiempo_peatones_horiz['mucho']                                       , semaforo['VerdeHoriz_RojoVert'])
    rule1i = ctrl.Rule(                                                                                       ~peatones_vert['ninguno']                                     & tiempo_peatones_vert['mucho']    , semaforo['RojoHoriz_VerdeVert'])

    #Gestion del paso de los vehiculos: 
    rule2a = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['ninguno'] & ~vehiculos_vert['ninguno'], semaforo['RojoHoriz_VerdeVert'])

    rule3a = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['ninguno']                                                                          , semaforo['VerdeHoriz_RojoVert'])
    rule3b = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['pocos']     &  tiempo_vehiculos_horiz['poco']     &  tiempo_vehiculos_vert['poco'] , semaforo['VerdeHoriz_RojoVert'])
    rule3c = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['pocos']     &  tiempo_vehiculos_horiz['poco']     & ~tiempo_vehiculos_vert['poco'] , semaforo['RojoHoriz_VerdeVert'])
    rule3d = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['pocos']     &  tiempo_vehiculos_horiz['bastante'] & ~tiempo_vehiculos_vert['mucho'], semaforo['VerdeHoriz_RojoVert'])
    rule3e = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['pocos']     &  tiempo_vehiculos_horiz['bastante'] &  tiempo_vehiculos_vert['mucho'], semaforo['RojoHoriz_VerdeVert'])
    rule3f = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['pocos']     &  tiempo_vehiculos_horiz['mucho']                                     , semaforo['VerdeHoriz_RojoVert'])
    rule3g = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['bastantes'] &  tiempo_vehiculos_horiz['poco']                                      , semaforo['RojoHoriz_VerdeVert'])
    rule3h = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['bastantes'] &  tiempo_vehiculos_horiz['bastante'] &  tiempo_vehiculos_vert['poco'] , semaforo['VerdeHoriz_RojoVert'])
    rule3i = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['bastantes'] &  tiempo_vehiculos_horiz['bastante'] & ~tiempo_vehiculos_vert['poco'] , semaforo['RojoHoriz_VerdeVert'])
    rule3j = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['bastantes'] &  tiempo_vehiculos_horiz['mucho']    & ~tiempo_vehiculos_vert['mucho'], semaforo['VerdeHoriz_RojoVert'])
    rule3k = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['bastantes'] &  tiempo_vehiculos_horiz['mucho']    &  tiempo_vehiculos_vert['mucho'], semaforo['RojoHoriz_VerdeVert'])
    rule3l = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['muchos']    &  tiempo_vehiculos_horiz['poco']                                      , semaforo['RojoHoriz_VerdeVert'])
    rule3m = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['muchos']    &  tiempo_vehiculos_horiz['bastante']                                  , semaforo['RojoHoriz_VerdeVert'])
    rule3n = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['muchos']    &  tiempo_vehiculos_horiz['mucho']    &  tiempo_vehiculos_vert['poco'] , semaforo['VerdeHoriz_RojoVert'])
    rule3o = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['pocos'] & vehiculos_vert['muchos']    &  tiempo_vehiculos_horiz['mucho']    & ~tiempo_vehiculos_vert['poco'] , semaforo['RojoHoriz_VerdeVert'])

    rule4a = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['ninguno']                                                                          , semaforo['VerdeHoriz_RojoVert'])
    rule4b = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['pocos']     &  tiempo_vehiculos_horiz['poco']     & ~tiempo_vehiculos_vert['mucho'], semaforo['VerdeHoriz_RojoVert'])
    rule4c = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['pocos']     &  tiempo_vehiculos_horiz['poco']     &  tiempo_vehiculos_vert['mucho'], semaforo['RojoHoriz_VerdeVert'])
    rule4d = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['pocos']     &  tiempo_vehiculos_horiz['bastante'] & ~tiempo_vehiculos_vert['mucho'], semaforo['VerdeHoriz_RojoVert'])
    rule4e = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['pocos']     &  tiempo_vehiculos_horiz['bastante'] &  tiempo_vehiculos_vert['mucho'], semaforo['RojoHoriz_VerdeVert'])
    rule4f = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['pocos']     &  tiempo_vehiculos_horiz['mucho']                                     , semaforo['VerdeHoriz_RojoVert'])
    rule4g = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['bastantes'] & tiempo_vehiculos_horiz['poco']      &  tiempo_vehiculos_vert['poco'] , semaforo['VerdeHoriz_RojoVert'])
    rule4h = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['bastantes'] & tiempo_vehiculos_horiz['poco']      & ~tiempo_vehiculos_vert['poco'] , semaforo['RojoHoriz_VerdeVert'])
    rule4i = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['bastantes'] & tiempo_vehiculos_horiz['bastante']  & ~tiempo_vehiculos_vert['mucho'], semaforo['VerdeHoriz_RojoVert'])
    rule4j = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['bastantes'] & tiempo_vehiculos_horiz['bastante']  &  tiempo_vehiculos_vert['mucho'], semaforo['RojoHoriz_VerdeVert'])
    rule4k = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['bastantes'] & tiempo_vehiculos_horiz['mucho']                                      , semaforo['VerdeHoriz_RojoVert'])
    rule4l = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['muchos']    & tiempo_vehiculos_horiz['poco']                                       , semaforo['RojoHoriz_VerdeVert'])
    rule4m = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['muchos']    & tiempo_vehiculos_horiz['bastante']  &  tiempo_vehiculos_vert['poco'] , semaforo['VerdeHoriz_RojoVert'])
    rule4n = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['muchos']    & tiempo_vehiculos_horiz['bastante']  & ~tiempo_vehiculos_vert['poco'] , semaforo['RojoHoriz_VerdeVert'])
    rule4o = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['muchos']    & tiempo_vehiculos_horiz['mucho']     & ~tiempo_vehiculos_vert['mucho'], semaforo['VerdeHoriz_RojoVert'])
    rule4p = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['bastantes'] & vehiculos_vert['muchos']    & tiempo_vehiculos_horiz['mucho']     &  tiempo_vehiculos_vert['mucho'], semaforo['RojoHoriz_VerdeVert'])

    rule5a = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['ninguno']                                                                         , semaforo['VerdeHoriz_RojoVert'])
    rule5b = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['pocos']     & tiempo_vehiculos_horiz['poco']     & ~tiempo_vehiculos_vert['mucho'], semaforo['VerdeHoriz_RojoVert'])
    rule5c = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['pocos']     & tiempo_vehiculos_horiz['poco']     &  tiempo_vehiculos_vert['mucho'], semaforo['RojoHoriz_VerdeVert'])
    rule5d = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['pocos']     & tiempo_vehiculos_horiz['bastante']                                  , semaforo['VerdeHoriz_RojoVert'])
    rule5e = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['pocos']     & tiempo_vehiculos_horiz['mucho']                                     , semaforo['VerdeHoriz_RojoVert'])
    rule5f = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['bastantes'] & tiempo_vehiculos_horiz['poco']     & ~tiempo_vehiculos_vert['mucho'], semaforo['VerdeHoriz_RojoVert'])
    rule5g = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['bastantes'] & tiempo_vehiculos_horiz['poco']     & tiempo_vehiculos_vert['mucho'] , semaforo['RojoHoriz_VerdeVert'])              
    rule5h = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['bastantes'] & tiempo_vehiculos_horiz['bastante'] & ~tiempo_vehiculos_vert['mucho'], semaforo['VerdeHoriz_RojoVert'])                    
    rule5i = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['bastantes'] & tiempo_vehiculos_horiz['bastante'] &  tiempo_vehiculos_vert['mucho'], semaforo['RojoHoriz_VerdeVert']) 
    rule5j = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['bastantes'] & tiempo_vehiculos_horiz['mucho']                                     , semaforo['VerdeHoriz_RojoVert'])  
    rule5k = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['muchos']    & tiempo_vehiculos_horiz['poco']     &  tiempo_vehiculos_vert['poco'] , semaforo['VerdeHoriz_RojoVert'])
    rule5l = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['muchos']    & tiempo_vehiculos_horiz['poco']     & ~tiempo_vehiculos_vert['poco'] , semaforo['RojoHoriz_VerdeVert'])
    rule5m = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['muchos']    & tiempo_vehiculos_horiz['bastante'] & ~tiempo_vehiculos_vert['mucho'], semaforo['VerdeHoriz_RojoVert'])
    rule5n = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['muchos']    & tiempo_vehiculos_horiz['bastante'] &  tiempo_vehiculos_vert['mucho'], semaforo['RojoHoriz_VerdeVert'])
    rule5o = ctrl.Rule(~tiempo_peatones_horiz['mucho'] & ~tiempo_peatones_vert['mucho'] & vehiculos_horiz['muchos'] & vehiculos_vert['muchos']    & tiempo_vehiculos_horiz['mucho']                                     , semaforo['VerdeHoriz_RojoVert'])

    control_semaforizacion = ctrl.ControlSystem([rule1a, rule1b, rule1c, rule1d, rule1e, rule1f, rule1g, rule1h, rule1i, rule2a, rule3a, rule3b, rule3c, rule3d, rule3e, rule3f, rule3g, rule3h, rule3i, rule3j, rule3k, rule3l, rule3m, rule3n, rule3o, rule4a, rule4b, rule4c, rule4d, rule4e, rule4f, rule4g, rule4h, rule4i, rule4j, rule4k, rule4l, rule4m, rule4n, rule4o, rule4p, rule5a, rule5b, rule5c, rule5d, rule5e, rule5f, rule5g, rule5h, rule5i, rule5j, rule5k, rule5l, rule5m, rule5n, rule5o])
    semaforizacion = ctrl.ControlSystemSimulation(control_semaforizacion)
    return semaforizacion

def fuzzy_setup2():
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

def get_fuzzy_output(num_peatones_vertical, num_peatones_horizontal,tiempo_espera_peatones_vertical, tiempo_espera_peatones_horizontal,num_coches_vertical,num_coches_horizontal,tiempo_espera_coches_vertical, tiempo_espera_coches_horizontal):
    semaforizacion.input['vehiculos_horiz'] = num_coches_horizontal
    semaforizacion.input['tiempo_vehiculos_horiz'] = tiempo_espera_coches_horizontal

    semaforizacion.input['vehiculos_vert'] = num_coches_vertical
    semaforizacion.input['tiempo_vehiculos_vert'] = tiempo_espera_coches_vertical

    semaforizacion.input['peatones_horiz'] = num_peatones_horizontal
    semaforizacion.input['tiempo_peatones_horiz'] = tiempo_espera_peatones_horizontal

    semaforizacion.input['peatones_vert'] = num_peatones_vertical
    semaforizacion.input['tiempo_peatones_vert'] = tiempo_espera_peatones_vertical
    semaforizacion.compute()
    return semaforizacion.output['semaforo']

def get_fuzzy2_output(num_peatones,tiempo_espera_peatones,num_coches):
    semaforizacion2.input['peatones'] = num_peatones
    semaforizacion2.input['vehiculos'] = num_coches
    semaforizacion2.input['tiempo_espera_peatones'] = tiempo_espera_peatones
    semaforizacion2.compute()
    return semaforizacion2.output['semaforo']
Diccionario = {
    "J55": ["Ped7_ArribaIzq","Ped7_AbajoIzq","Ped7_Arribadcha","Ped7_Abajodcha","Veh7_Horiz","Veh7_Vert"],
    "J58": ["Ped11_Abajo","Ped11_ArribaDcha","Ped11_ArribaIzq","Veh11_Vert","Veh11_Horiz"],
    "J61": ["Ped12_Arriba","Ped12_Abajo","Veh12"],
    "J57": ["Ped10_ArribaIzq","Ped10_AbajoDcha","Ped10_AbajoIzq","Ped10_ArribaDcha","Veh10_Vert","Veh10_Horiz"],
    "J15": ["Ped4_Dcha","Ped4_AbajoIzq","Ped4_ArribaIzq","Veh4_Horiz","Veh4_Vert"],
    "J14": ["Ped3_Arriba","Ped3_AbajoIzq","Ped3_AbajoDcha","Veh3_Vert","Veh3_Horiz"],
    "J13": ["Ped8_ArribaIzq","Ped8_Abajo","Ped8_ArribaDcha","Veh8_Vert","Veh8_Horiz"],
    "J4" : ["Ped2_Arriba","Ped2_Abajo","Veh2"],
    "J19": ["Ped1_AbajoIzq","Ped1_AbajoDcha","Ped1_Arriba","Veh1_Horiz","Veh1_Vert"],
    "J54": ["Ped5_ArribaIzq","Ped5_Abajo","Ped5_ArribaDcha","Veh5_Horiz","Veh5_Vert"],
    "J3" : ["Ped6_Arriba","Ped6_Abajo","Veh6"],
    "J56": ["Ped9_ArribaIzq","Ped9_Abajo","Ped9_ArribaDcha","Veh9_Horiz","Veh9_Vert"]
}

def process_traffic_data(IntersectionID):
    detectores_id = Diccionario[IntersectionID]
    all_ids=[]
    vehicle_ids = traci.vehicle.getIDList()
    for detector_id in detectores_id:
        all_ids.extend(traci.multientryexit.getLastStepVehicleIDs(detector_id))

    peatones_ids = [id for id in all_ids if id not in vehicle_ids]
    vehiculos_ids = [id for id in all_ids if id in vehicle_ids]
    tiempo_espera_peatones_vertical = 0
    tiempo_espera_peatones_horizontal = 0
    tiempo_espera_coches_vertical = 0
    tiempo_espera_coches_horizontal = 0
    num_peatones_vertical = 0
    num_peatones_horizontal = 0
    num_coches_vertical = 0
    num_coches_horizontal = 0
    for peaton_id in peatones_ids:
        if(traci.person.getSpeed(peaton_id) <= 1):
            angle = traci.person.getAngle(peaton_id)
            if 355 < angle < 360:
                angle = 0
            if angle<=5 or 175<=angle<=185:
                waiting_time = traci.person.getWaitingTime(peaton_id)
                tiempo_espera_peatones_vertical += waiting_time
                num_peatones_vertical += 1
            elif 85<=angle<=95 or 265<=angle<=275:
                waiting_time = traci.person.getWaitingTime(peaton_id)
                tiempo_espera_peatones_horizontal += waiting_time
                num_peatones_horizontal += 1

    for coche_id in vehiculos_ids:
        angle = traci.vehicle.getAngle(coche_id)
        if 355 < angle < 360:
            angle = 0
        if angle<=5 or 175<=angle<=185:
            waiting_time = traci.vehicle.getWaitingTime(coche_id)
            tiempo_espera_coches_vertical += waiting_time
            num_coches_vertical += 1 
        elif 85<=angle<=95 or 265<=angle<=275:
            waiting_time = traci.vehicle.getWaitingTime(coche_id)
            tiempo_espera_coches_horizontal += waiting_time
            num_coches_horizontal += 1

    print("En:",IntersectionID)
    print("num_peatones_vertical: ",num_peatones_vertical)
    print("num_peatones_horizontal: ",num_peatones_horizontal)
    print("tiempo_espera_peatones_vertical: ",tiempo_espera_peatones_vertical)
    print("tiempo_espera_peatones_horizontal: ",tiempo_espera_peatones_horizontal)
    print("num_coches_vertical: ",num_coches_vertical) 
    print("num_coches_horizontal: ",num_coches_horizontal)
    print("tiempo_espera_coches_vertical: ",tiempo_espera_coches_vertical)
    print("tiempo_espera_coches_horizontal: ",tiempo_espera_coches_horizontal)
    #Analisis semaforos
    SemaforosWaitingTime(IntersectionID,tiempo_espera_coches_vertical,tiempo_espera_coches_horizontal)
    print('AAAAAAAAAAAAA',SemaforoJ55WaitingTime)

    if IntersectionID == 'J61' or IntersectionID == 'J3' or IntersectionID == 'J4':
        semaforizacion = semaforizacion2
        output = get_fuzzy2_output(num_peatones_vertical,tiempo_espera_peatones_vertical, num_coches_horizontal)
    else:
        output = get_fuzzy_output(num_peatones_vertical, num_peatones_horizontal,tiempo_espera_peatones_vertical, tiempo_espera_peatones_horizontal,num_coches_vertical,num_coches_horizontal,tiempo_espera_coches_vertical, tiempo_espera_coches_horizontal)
    return output
"""
def manage_traffic_lights(IntersectionID):
    right_now = traci.simulation.getTime()
    margen = 0
    while (True):
        simulation_time = traci.simulation.getTime()
        if right_now+margen <= simulation_time and orden_acceso[0] == IntersectionID:
            sem.acquire()
            try:
                output=process_traffic_data(IntersectionID)
                print(output)
                pre_state = traci.trafficlight.getPhase(IntersectionID)
                if output <= 0.5:
                    state = traci.trafficlight.setPhase(IntersectionID, 0)
                elif output > 0.5:
                    state = traci.trafficlight.setPhase(IntersectionID, 3)
                if state != pre_state:
                    margen=10
                else:
                    margen=1
            finally:
                sem.release()
                right_now = traci.simulation.getTime()
                orden_acceso.popleft()
                orden_acceso.append(IntersectionID)
                print(orden_acceso)
                if IntersectionID == 'J56':
                    traci.simulationStep()
        else:
            orden_acceso.popleft()
            orden_acceso.append(IntersectionID)
            print(orden_acceso)
            if IntersectionID == 'J56':
                    traci.simulationStep()
                    
"""
""" def manage_traffic_lights(IntersectionID, margen):
    time=traci.simulation.getTime()
    if time >= margen:   
        output=process_traffic_data(IntersectionID)
        pre_state = traci.trafficlight.getPhase(IntersectionID)
        if output <= 0.5:
            state = traci.trafficlight.setPhase(IntersectionID, 0)
        elif output > 0.5:
            state = traci.trafficlight.setPhase(IntersectionID, 3)  
        if (IntersectionID=='J3'):
            if  output>0.5:
                margen=20+time
        elif (IntersectionID=='J4'):
            if  output>0.5:
                margen=20+time
        elif (IntersectionID=='J61'):
            if  output>0.5:
                margen=20+time
        else:
            margen=5+time   
        print(output)
    return margen """

def manage_traffic_lights(IntersectionID, margen):
    time=traci.simulation.getTime()
    if time >= margen:
        output=process_traffic_data(IntersectionID)
        pre_state = traci.trafficlight.getPhase(IntersectionID)
        if output <= 0.5:
            state = traci.trafficlight.setPhase(IntersectionID, 0)
            if state != pre_state:
                gain=int((abs(output-0.5))*15)
                margen=gain+time
        elif output > 0.5:
            state = traci.trafficlight.setPhase(IntersectionID, 3)
            if state != pre_state:
                gain=int((abs(output-0.5))*15)
                margen=gain+time
    return margen

semaforizacion=fuzzy_setup()
semaforizacion2=fuzzy_setup2()
#sem = threading.Semaphore()
orden_acceso=deque()



if __name__ == "__main__":
    
    sumoBinary = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui.exe"
    sumoConfig = "C:/Users/User/Downloads/Code/Mapa Grande/tutorial.sumocfg"
    sumoCmd = [sumoBinary, '-c', sumoConfig,"--start"]
    print("here")
    traci.start(sumoCmd)
    tiempo_espera_peatones=0
    vehicle_ids = traci.vehicle.getIDList()
    """
    for id in Diccionario:
        orden_acceso.append(id)
    for id in Diccionario:
        threading.Thread(target=manage_traffic_lights, args=(id,)).start()
    """
    T_J55 = 0
    T_J58 = 0
    T_J61 = 0
    T_J57 = 0
    T_J15 = 0
    T_J14 = 0
    T_J13 = 0
    T_J4 = 0
    T_J19 = 0 
    T_J54 = 0
    T_J3 = 0
    T_J56 = 0
    ids = []
    persons = []
    vehicleWaitingTimes = {}
    PersonsWaitingTimes = {}
    temporal_wait_time = []
    Persontemporal_wait_time = []
    while traci.simulation.getTime() <= 1000:
        #if traci.simulation.getTime() == 1:
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



        
        T_J55 = manage_traffic_lights('J55',T_J55)
        T_J58 = manage_traffic_lights('J58',T_J58)

        T_J61 = manage_traffic_lights('J61',T_J61)

        T_J57 = manage_traffic_lights('J57',T_J57)

        T_J15 = manage_traffic_lights('J15',T_J15)

        T_J14 = manage_traffic_lights('J14',T_J14)
        T_J13 = manage_traffic_lights('J13',T_J13)
        T_J4 = manage_traffic_lights('J4',T_J4)
        T_J19 = manage_traffic_lights('J19',T_J19)
        T_J54 = manage_traffic_lights('J54',T_J54)
        T_J3 = manage_traffic_lights('J3',T_J3)
        T_J56 = manage_traffic_lights('J56',T_J56) 
        
        traci.simulationStep()     
    # Detener la simulación y cerrar la conexión TraCI
    #idlist = traci.vehicle.getIDList()
    # Extraer las claves y los valores
    
    """ ploting_data = PersonsWaitingTimes
    keys = list(ploting_data.keys())
    values = list(ploting_data.values())
    media = sum(ploting_data.values()) / len(ploting_data)
    print("Media: ", media)
    # Crear un gráfico de barras
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
    keys = list(vehicleWaitingTimes.keys())
    values = list(vehicleWaitingTimes.values())
    media = sum(vehicleWaitingTimes.values()) / len(vehicleWaitingTimes)

    keys2 = list(PersonsWaitingTimes.keys())
    values2 = list(PersonsWaitingTimes.values())
    media2 = sum(PersonsWaitingTimes.values()) / len(PersonsWaitingTimes)

    np.savetxt('AltaFrec_Fuzzy.txt', values, fmt='%1.2f', newline='\n')
    np.savetxt('PersonAltaFrec_Fuzzy.txt', values2, fmt='%1.2f', newline='\n')


    print(len(idlist))
    print(idlist)
    print("SemaforoJ55WaitingTime:", SemaforoJ55WaitingTime)
    print("SemaforoJ58WaitingTime:", SemaforoJ58WaitingTime)
    print("SemaforoJ61WaitingTime:", SemaforoJ61WaitingTime)
    print("SemaforoJ15WaitingTime:", SemaforoJ15WaitingTime)
    print("SemaforoJ14WaitingTime:", SemaforoJ14WaitingTime)
    print("SemaforoJ13WaitingTime:", SemaforoJ13WaitingTime)
    print("SemaforoJ4WaitingTime:", SemaforoJ4WaitingTime)
    print("SemaforoJ19WaitingTime:", SemaforoJ19WaitingTime)
    print("SemaforoJ54WaitingTime:", SemaforoJ54WaitingTime)
    print("SemaforoJ3WaitingTime:", SemaforoJ3WaitingTime)
    print("SemaforoJ56WaitingTime:", SemaforoJ56WaitingTime)

    semaforos_data = {
    "SemaforoJ55": SemaforoJ55WaitingTime,
    "SemaforoJ58": SemaforoJ58WaitingTime,
    "SemaforoJ61": SemaforoJ61WaitingTime,
    "SemaforoJ15": SemaforoJ15WaitingTime,
    "SemaforoJ14": SemaforoJ14WaitingTime,
    "SemaforoJ13": SemaforoJ13WaitingTime,
    "SemaforoJ4": SemaforoJ4WaitingTime,
    "SemaforoJ19": SemaforoJ19WaitingTime,
    "SemaforoJ54": SemaforoJ54WaitingTime,
    "SemaforoJ3": SemaforoJ3WaitingTime,
    "SemaforoJ56": SemaforoJ56WaitingTime,
}

    # Guardar el diccionario como JSON en un archivo de texto
    with open('semaforosPersonBajaFrec_Fuzzy.txt', 'w') as file:
        json.dump(semaforos_data, file)
    
    #Evolucion temporal vehiculos/personas
    np.savetxt('EvolucionPersonAltaFrec_Base.txt', Persontemporal_wait_time)
    np.savetxt('EvolucionAltaFrec_Base.txt', temporal_wait_time)
    # Crear un gráfico de barras para el vector_medias
    """ plt.bar(range(len(Persontemporal_wait_time)), Persontemporal_wait_time, color='blue')

    # Personalizar el gráfico
    plt.xlabel('Tiempo')
    plt.ylabel('Media de tiempos de espera')
    #plt.xticks(range(len(temporal_wait_time)), [str(i) for i in range(1, len(temporal_wait_time) + 1)])

    # Mostrar el gráfico
    plt.show()
    """
    traci.close()

    
