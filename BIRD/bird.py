import subprocess

def greetings(name):
    output = subprocess.Popen(["/usr/local/sbin/birdc", "show protocols all"], stdout=subprocess.PIPE).communicate()[0]
    for line in output.split():
        print "#########"
        print line
        print "#########"
    return output
