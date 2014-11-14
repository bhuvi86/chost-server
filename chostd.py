import random
import string
import json
import subprocess

import cherrypy

class StringGenerator(object):
    cherrypy.server.socket_host = '0.0.0.0'
    sudo_password = 'admin'
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
        devices ={}
        #remove 1st entry [KNAME, TYPE]
        del lines[0]
        #remove last empty entry
        del lines[size-2]
        #extract only those devices where type = disk
        count =0;
        for line in lines:
            data = line.split()
            if(data[1]=="disk"):
                count+=1
                key = "device" + str(count)
                devices[key]=data[0]
        message= {"devices" : devices}
        return json.dumps(devices)
    
    @cherrypy.expose
    def mkfs(self, name):
        if ("dev" not in name):
              name = "/dev/"+name
        print name
        p = subprocess.Popen(["sudo","-S","mkfs","-F",name], stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        (output, err) = p.communicate(self.sudo_password)
        return json.dumps(output)

    @cherrypy.expose
    def mount(self, name, path):    
        if ("dev" not in name):
              name = "/dev/"+name
        print name
        print path
        #create path
        p = subprocess.Popen(["sudo","-S","mkdir","-p", path],stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        (output, err) = p.communicate(self.sudo_password)
        #mount
        p = subprocess.Popen(["sudo","-S","mount",name, path],stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        (output, err) = p.communicate(self.sudo_password)
        return json.dumps(output)
      
if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator())
