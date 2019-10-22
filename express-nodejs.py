#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
from random import randint

class color:
    PURPLE = '\\033[95m'
    CYAN = '\\033[96m'
    DARKCYAN = '\\033[36m'
    BLUE = '\\033[94m'
    GREEN = '\\033[92m'
    YELLOW = '\\033[93m'
    RED = '\\033[91m'
    BOLD = '\\033[1m'
    UNDERLINE = '\\033[4m'
    END = '\\033[0m'

global colorArray
colorArray = ['\\033[95m', '\\033[96m', '\\033[36m', '\\033[94m', '\\033[92m', '\\033[93m', '\\033[91m', '\\033[4m']

def clonar():
    # TODO: ask first the user, before delting
    # subprocess.call("rm -rf express-app-template-nodeJS")
    p = subprocess.Popen("git clone https://github.com/carlosvillasanchez/express-app-template-nodeJS", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    
    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()
    print("Command output : ", output)
    print("Command exit status/return code : ", p_status)

class Endpoint:
    def __init__(self, method, route):
        self.method = method
        self.route = route


class NodeInfo:
    def __init__(self):
        self.routersName = self.obtain_routers()
        self.routers = {}
        for name in self.routersName:
            self.routers[name] = self.obtain_router_info(name)

    '''
    This function gets the info from the user about a router
    '''
    def obtain_router_info(self, name):
        print("\n\n")
        # Getting the amount of endpoints
        noEndPoints = 0
        while(True):
            noEndPoints = input("How many endpoints do you want in router " + name + " (0):")
            if (noEndPoints == ""):
                noEndPoints = 0
                break
            try:
                noEndPoints = int(noEndPoints)
            except:
                print("You must put an integer as the number of endpoints")
                continue
            break
        
        # Obtain the method and route
        print("\n")
        endpoints = []
        for i in range(noEndPoints):
            method = ""
            while True:
                valid_input = ["g", "get", "po", "post", "pu", "put", "d", "delete"]
                methods = ["Get", "Post", "Put", "Delete"]
                method = input("Method for the endpoint #" + str(i)+ " (Get, POst, PUt, Delete):")
                if method.lower() not in valid_input:
                    print("Enter a valid method: Get, POst, PUt, Delete")
                    continue
                method = methods[int(valid_input.index(method)/2)]
                break
            
            route = input("Route for the endpoint #" + str(i)+ " (" + name + "/[...]):")
            endpoint = Endpoint(method, route)
            endpoints.append(endpoint)
        
        print("\nEndpoints for router " + name + ":")
        for endpoint in endpoints:
            print("\t" + endpoint.method + ": " + name + "/" + endpoint.route)

        return endpoints
            


    '''
    This function gets the needed info from the user
    '''
    def obtain_routers(self):
        # Getting the amount of routers
        noRouters = 0
        while(True):
            noRouters = input("Amount of routers (1): ")
            if (noRouters == ""):
                noRouters = 1
                break
            try:
                noRouters = int(noRouters)
            except:
                print("You must put an integer as the number of routers")
                continue
            break

        # Name of the routers
        routersName = []
        for i in range(noRouters):
            name = input("Name of your router #" + str(i)+ ": ")
            # TODO: Check for duplicates
            # TODO: A router cannot be called "", but a route yes
            routersName.append(name)
            
        print("Your node.js app will have " + str(noRouters) + " routers: ")
        global colorArray
        for name in routersName:
            print("\t-->" + name)
        return routersName

    def generateCode(self):
        self.editApp()
    
    def editApp(self):
        print("EJE")
        # Read the app file
        with open('express-app-template-nodeJS/app.js', encoding="utf8") as f:
            filedata = f.read()

        # Generating code to be placed
        importRoutersCode = ""
        appUseRoutersCode = ""
        for router in self.routersName:
            importRoutersCode += "let " + router + "Router = require('./routes/" + router + "');\n"
            appUseRoutersCode += "app.use('/" + router + "', " + router + "Router);\n"
        
        
        # Replace the comments with the correct code
        filedata = filedata.replace("//ImportingRouters", importRoutersCode)
        filedata = filedata.replace("//AppUseRouters", appUseRoutersCode)

        # Re-write the new document
        with open('express-app-template-nodeJS/app.js', 'w',  encoding="utf8") as file:
            file.write(filedata)

    def generateRouters(self):
        os.mkdir("express-app-template-nodeJS/routes")
        for routerName in self.routersName:
            self._generateRouter(routerName)
        
    def _generateRouter(self, routerName):
        endpoints = self.routers[routerName]

        # Generate file and opening it
        f= open("express-app-template-nodeJS/routes/" + routerName + ".js","w+") 

        # Edit file
        f.write("let express = require('express');\n")
        f.write("let router = express.Router();\n\n")
        for endpoint in endpoints:
            f.write("\n/* %s /%s/%s */\n" % (endpoint.method.upper(), routerName, endpoint.route))
            f.write("router.%s('/%s', function(req, res, next) {\n\n});" % (endpoint.method.lower(), endpoint.route))
        f.write("\n\nmodule.exports = router;")

        # Closing the file
        f.close()
  
    
if __name__ == "__main__":
    # TODO: Check is python 3
    clonar()
    nodeInfo = NodeInfo()
    nodeInfo.generateCode()
    nodeInfo.generateRouters()
