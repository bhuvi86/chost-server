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
        # get all block devices (filter out slaves)
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
    
    @cherrypy.expose
    def mkfs(self, name):
        if ("dev" not in name):
              name = "/dev/"+name
        #set root access
        # p = subprocess.Popen(["sudo","bash"], stdout=subprocess.PIPE)
        #(output, err) = p.communicate()
        #do mkfs
        p = subprocess.Popen(["sudo","mkfs","-F","-t","ext3",name], stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        message = output.split("\n")
        return json.dumps(message)

    @cherrypy.expose
    def mount(self, name, path):    
        if ("dev" not in name):
              name = "/dev/"+name
        #create path
        p = subprocess.Popen(["sudo","mkdir","-p", path], stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        #mount
        p = subprocess.Popen(["sudo","mount",name, path], stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        return json.dumps(output)
      
if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator())
