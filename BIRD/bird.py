import subprocess
template = """
BIRD 1.6.2 ready.
name     proto    table    state  since       info
device1  Device   master   up     2016-10-24 16:24:28
  Preference:     240
  Input filter:   ACCEPT
  Output filter:  REJECT
  Routes:         0 imported, 0 exported, 0 preferred
  Route change stats:     received   rejected   filtered    ignored   accepted
    Import updates:              0          0          0          0          0
    Import withdraws:            0          0        ---          0          0
    Export updates:              0          0          0        ---          0
    Export withdraws:            0        ---        ---        ---          0

PIPE_DIGISAT Pipe     master   up     2016-10-24 16:24:28  => TABLE_DIGISAT
  Preference:     70
  Input filter:   (unnamed)
  Output filter:  (unnamed)
  Routes:         1 imported, 13 exported
  Route change stats:     received   rejected   filtered    ignored   accepted
    Import updates:             76         71          0          4          1
    Import withdraws:           13          0        ---          0          0
    Export updates:             81          5          5         45         26
    Export withdraws:           13          0        ---          4         13
    """
def greetings(name):
    #output = subprocess.Popen(["/usr/local/sbin/birdc", "show protocols all"], stdout=subprocess.PIPE).communicate()[0]
    print template
