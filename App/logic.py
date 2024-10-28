"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones
 *
 * Dario Correal
 """

import os
import csv
import datetime

# Importación del Árbol Rojo Negro
from DataStructures.Tree import red_black_tree as rbt
# Importación de ArrayList o SingleLinked como estructura de datos auxiliar
from DataStructures.Map import map_linear_probing as lp
from DataStructures.List import array_list  as al


data_dir = r"C:\\Users\\danie\\Downloads\\lab9\\Laboratorio9-G02\\Data\\Boston Crimes\\crime-utf8.csv"



def new_logic():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {"crimes": None,
                "dateIndex": None,
                "areaIndex": None,
                }

    analyzer["crimes"] = al.new_list()
    analyzer["dateIndex"] = rbt.new_map()
    analyzer["areaIndex"] = rbt.new_map() 
    # TODO Crear el índice ordenado por áreas reportadas
    return analyzer

# Funciones para realizar la carga

def load_data(analyzer, crimesfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    crimesfile = crimesfile
    input_file = csv.DictReader(open(crimesfile, encoding="utf-8"),
                                delimiter=",")
    for crime in input_file:
        add_crime(analyzer, crime)
    return analyzer



# Funciones para agregar informacion al analizador


def add_crime(analyzer, crime):
    """
    funcion que agrega un crimen al catalogo
    """
    al.add_last(analyzer['crimes'], crime)
    update_date_index(analyzer['dateIndex'], crime)
    # TODO Actualizar el indice por areas reportadas
    update_area_index(analyzer['areaIndex'], crime)
    return analyzer

def update_area_index(map, crime):
    """
    actualiza el indice de areas reportadas con un nuevo crimen
    si el area ya existe en el indice, se adiciona el crimen a la lista
    si el area es nueva, se crea una entrada para el indice y se adiciona
    y si el area son ["", " ", None] se utiliza el valor por defecto 9999
    """
    # TODO Implementar actualizacion del indice por areas reportadas
    # revisar si el area es un str vacio ["", " ", None]
    # area desconocida es 9999

    # revisar si el area ya esta en el indice

    # si el area ya esta en el indice, adicionar el crimen a la lista
    # Obtener el área del crimen
    area = crime.get('area')
    
    # Si el área es un string vacío, espacio o None, usar 9999 como valor por defecto
    if area in ["", " ", None]:
        area = 9999

    # Revisar si el área ya está en el índice
    if area not in map:
        # Si el área no existe, crear una nueva entrada en el índice
        map[area] = []

    # Adicionar el crimen a la lista correspondiente
    map[area].append(crime)

    return map


def update_date_index(map, crime):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = crime['OCCURRED_ON_DATE']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = rbt.get(map, crimedate.date())
    if entry is None:
        datentry = new_data_entry(crime)
        rbt.put(map, crimedate.date(), datentry)
    else:
        datentry = entry
    add_date_index(datentry, crime)
    return map


def add_date_index(datentry, crime):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry["lstcrimes"]
    al.add_last(lst, crime)
    offenseIndex = datentry["offenseIndex"]
    offentry = lp.get(offenseIndex, crime["OFFENSE_CODE_GROUP"])
    if (offentry is None):
        entry = new_offense_entry(crime["OFFENSE_CODE_GROUP"], crime)
        al.add_last(entry["lstoffenses"], crime)
        lp.put(offenseIndex, crime["OFFENSE_CODE_GROUP"], entry)
    else:
        entry = offentry
        al.add_last(entry["lstoffenses"], crime)
    return datentry


def new_data_entry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstcrimes': None}
    entry['offenseIndex'] = lp.new_map(num_elements=30,
                                        load_factor=0.5)
    entry['lstcrimes'] = al.new_list()
    return entry


def new_offense_entry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = al.new_list()
    return ofentry


# ==============================
# Funciones de consulta
# ==============================


def crimes_size(analyzer):
    """
    Número de crimenes
    """
    return al.size(analyzer['crimes'])


def index_height(analyzer):
    """
    Altura del arbol
    """
    return rbt.height(analyzer["dateIndex"])


def index_size(analyzer):
    """
    Numero de elementos en el indice
    """
    return rbt.size(analyzer["dateIndex"])


def min_key(analyzer):
    """
    Llave mas pequena
    """
    return rbt.min_key(analyzer["dateIndex"])


def max_key(analyzer):
    """
    Llave mas grande
    """
    return rbt.max_key(analyzer["dateIndex"])


def index_height_areas(analyzer):
    """
    Altura del árbol por áreas.
    """
    # Verifica si el atributo 'area_tree' existe y no es None
    if "areaIndex" in analyzer and analyzer["areaIndex"] is not None:
        return rbt.height_tree(analyzer["areaIndex"])
    return 0  # Retorna 0 si el árbol por áreas no existe


def index_size_areas(analyzer):
    """
    Número de elementos en el índice por áreas.
    """
    # Verifica si el índice de áreas existe en el analizador
    if "areaIndex" in analyzer:
        return len(analyzer["areaIndex"])
    return 0  # Retorna 0 si el índice de áreas no existe


def min_key_areas(analyzer):
    """
    Llave más pequeña por áreas.
    """
    # Verifica si el árbol de áreas existe
    if "areaIndex" in analyzer and analyzer["areaIndex"] is not None:
        current_node = analyzer["areaIndex"]['root']
        
        while current_node['left'] is not None:
            current_node = current_node['left']
        
        return current_node['key']  # Suponiendo que la llave está en 'key'
    
    return None  # Retorna None si no hay áreas


def max_key_areas(analyzer):
    """
    Llave más grande por áreas.
    """
    # Verifica si el árbol de áreas existe
    if "areaIndex" in analyzer:
        return rbt.right_key(analyzer["areaIndex"])
    return None  # Retorna None si el árbol por áreas no existe

def get_crimes_by_range_area(analyzer, initialArea, finalArea):
    """
    Retorna el número de crímenes en un rango de áreas.
    """
    # Obtener todas las llaves (áreas) del índice de áreas
    keys = rbt.key_set(analyzer["areaIndex"])

    num_crimes = 0
    
    # Iterar sobre las áreas en el índice
    for area in keys["elements"]:
        if initialArea <= area <= finalArea:
            # Obtener la lista de crímenes para el área actual
            crimes_list = rbt.get(analyzer["areaIndex"], area)
            # Sumar la cantidad de crímenes en esa área
            num_crimes += len(crimes_list["crimes"])  # Asumiendo que los crímenes están en "crimes"
    
    return num_crimes

def get_crimes_by_range(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    lst = rbt.values(analyzer["dateIndex"], initialDate.date(), finalDate.date())
    totalcrimes = 0
    for lstdate in lst["elements"]:
        totalcrimes += al.size(lstdate["lstcrimes"])
    return totalcrimes


def get_crimes_by_range_code(analyzer, initialDate, offensecode):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    crimedate = rbt.get(analyzer["dateIndex"], initialDate.date())
    if crimedate is not None:
        offensemap = crimedate["offenseIndex"]
        numoffenses = lp.get(offensemap, offensecode)
        if numoffenses is not None:
            return lp.size(numoffenses["lstoffenses"])
    return 0
