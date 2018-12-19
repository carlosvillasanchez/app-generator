#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import subprocess
from anytree import Node, RenderTree


def clonar():
    p = subprocess.Popen("git clone https://github.com/carlosvillasanchez/express-app-template-nodeJS", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    
    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()
    print "Command output : ", output
    print "Command exit status/return code : ", p_status


def obtain_info():
    #Number of routers
    global noRouters
    aux = True
    while(aux):
        noRouters = raw_input("Amount of routers (1): ")
        if (noRouters == ""):
            noRouters = 1
            aux = False
            continue
        try:
            noRouters = int(noRouters)
        except:
            print "You must put an integer"
            continue
        aux = False

    #Name of the routers
    global routerNames
    routerNames = []
    global routes
    routes = Node("routes")
    for i in range(noRouters):
        name = raw_input("Name of your router #" + str(i)+ ": ")
        routerNames.append(name)
        var_name = "router" + str(i) 
        st = "Node(\""+ name+ "\", parent=routes)"
        exec("%s = %s" % (var_name, st))
    print routerNames
    for pre, fill, node in RenderTree(routes):
        print("%s%s" % (pre, node.name))
    
     
    


        

    
    

#clonar()
obtain_info()
