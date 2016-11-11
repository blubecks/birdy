import subprocess, os
from Parser.parser import Parser
from validator import Required, Pattern, validate, Length


class Bird(object):
    def __init__(self, app):
        self.app = {
            'bird_instance': app.config['BIRDC_INSTANCE'],
            'bird_v6_instance': app.config['BIRDC6_INSTANCE'],
            'secret_key': app.config['SECRET_KEY'],
            'debug': app.config['DEBUG']
        }

    def all_bgp_session(self):
        if self.app['debug']:
            fake_data = os.path.join(os.path.dirname(__file__), 'summary.txt')
            f = open(fake_data, 'r')
            output = f.read()
        else:
            output = subprocess.Popen([self.app['bird_instance'], "show protocols all"], stdout=subprocess.PIPE).communicate()[0]
        return Parser.parse_output_to_sessions(output)

    def configure_new_session(self, data = None):
        if not data:
            return False
        try:
            self._check_params(data)
        except BirdException as b:
            return {
                'status': 'error',
                'message': b.message
            }
        # Write configuration on file
        return {
            'status': 'success',
            'code': 200,
            'message': 'configuration ok!'
        }

    def _check_params(self, data):
        rules = {
            "as": [Required, Length(1, maximum=15)],
            "name": [Required, Length(1, maximum=15)],
            "ip": [Required, Length(1, maximum=15)],
            "ixtype": [Required, Length(1, maximum=15)],
            "asexport": [Required, Length(1, maximum=15)]
        }
        if 'secret' not in data or data['secret'] != self.app['secret_key']:
            raise BirdException('you are unauthorized!')

        result = validate(rules, data)
        if result[0]:
            return True
        else:
            raise BirdException(result[1])


class BirdException(Exception):
    pass

'''
as
name
ip
[11/11/2016, 10:52:24] Enrico Pellegrini: ixtype
[11/11/2016, 10:52:27] Enrico Pellegrini: asexport
[11/11/2016, 10:52:30] Enrico Pellegrini: maxpref
[11/11/2016, 10:52:36] Enrico Pellegrini: custom_commands
'''