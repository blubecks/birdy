import subprocess, os
from Parser.parser import Parser
class Bird:
    def __init__(self, app):
        self.app = app

    def all_bgp_session(self):
        if self.app.config['DEBUG']:
            fake_data = os.path.join(os.path.dirname(__file__), 'summary.txt')
            f = open(fake_data, 'r')
            output = f.read()
        else:
            output = subprocess.Popen([self.app.config['BIRDC_INSTANCE'], "show protocols all"], stdout=subprocess.PIPE).communicate()[0]
        return Parser.parse_output_to_sessions(output)
