import random
import string
import json
import subprocess

import cherrypy

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def generate(self):
        message= {"message" :''.join(random.sample(string.hexdigits, 8))}
        return json.dumps(message)

    @cherrypy.expose
    def listdevices(self):
        p = subprocess.Popen(["lsblk","-d","-o","KNAME,TYPE"], stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        lines = output.split("\n")
        size = len(lines)
        devices =[]
        #remove 1st entry [KNAME, TYPE]
        del lines[0]
        #remove last empty entry
        del lines[size-2]
        #extract only those devices where type = disk
        for line in lines:
            data = line.split()
            if(data[1]=="disk"):
                devices.append(data[0])
        message= {"devices" : devices}
        return json.dumps(devices)

if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator())
