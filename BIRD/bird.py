import subprocess, re
class Bird:
    def __init__(self, app):
        self.app = app

    def all_bgp_session(self):
        sessions = []
        output = subprocess.Popen([self.app.config['BIRDC_INSTANCE'], "show protocols all"], stdout=subprocess.PIPE).communicate()[0]
        for line in output.split('\n'):
            object_parsed = re.match( r'^(\w+)\s+BGP\s+(\w+)\s+(\w+)\s+([0-9\-\:]+)\s+(\w+).*$', line, re.M|re.I)
            if object_parsed:
                s = {}
                s['name'] = object_parsed.group(1)
                s['table'] = object_parsed.group(2)
                s['bird_protocol'] = 'BGP'
                s['connection'] = object_parsed.group(3)
                s['state_change'] = object_parsed.group(4)
            object_parsed = re.match( r'^\s+BGP state:\s+(\w+)\s*$', line, re.M|re.I)
            if object_parsed:
                s['bgp_info'] = {}
                s['bgp_info']['bgp_state'] = object_parsed.group(1)
            object_parsed = re.match( r'^\s+Neighbor address:\s+([^\s]+)\s*$', line, re.M|re.I)
            if object_parsed:
                s['bgp_info']['neighbor_address'] = object_parsed.group(1)
            object_parsed = re.match( r'^\s+Neighbor AS:\s+([\d]+)\s*$', line, re.M|re.I)
            if object_parsed:
                s['bgp_info']['neighbor_as'] = object_parsed.group(1)
            sessions.append(s)
        return sessions
