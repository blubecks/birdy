import subprocess

def greetings(name):
    output = subprocess.Popen(["/usr/bin/birdc", "show protocols all"], stdout=subprocess.PIPE).communicate()[0]
    print output
