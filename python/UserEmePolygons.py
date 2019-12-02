# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:50:53 2019

@author: Jarvis
"""

import json
import sys

from shapely.geometry import Point
from shapely.geometry import Polygon

# user location and radius

deg_dis = 10 ** 3 / 111319.49079327357


def userinpol(userlatlon, radius, jsondata):
    # look thriugh emergency code]
    #  print(jsondata)
    listlist = jsondata["poldata"]
    # loop through coodinated and get them as cloud then make them a Polygon
    for pol in listlist[0:len(listlist)]:
        plotpol = []
        for cor in pol:
            cor = [float(i) for i in cor]
            plotpol.append(cor)

        pol = Polygon(plotpol)
        # check the use is in the palyon
        usercir = Point(*userlatlon).buffer(radius * deg_dis)
        # print(pol.intersects(usercir))
        if pol.intersects(usercir):
            return True
    return False


def userdanger(latlon, radius):
    # get emergency data
    with open("emergency.json") as json_file:
        data = json.load(json_file)
        # loop through data find is user is in poldata

    useremejson = {}  # dictionay for the emergency the use is close by
    for code, item in data.items():
        try:
            if userinpol(latlon, radius, item):
                useremejson[code] = item
            print("User in Emergeny area:" + code)
        except Exception as e:
            print("Error in GPS distance, check columns names")
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            print(type(e))
            print(e.args)
            pass
    return useremejson


if __name__ == '__main__':
    polygons = userdanger((60, 24), 2222)
    print(polygons)
