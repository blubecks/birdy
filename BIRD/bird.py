import subprocess, os
from Parser.parser import Parser
from validator import Required, Pattern, validate, Length


class Bird(object):
    def __init__(self, app):
        self.app = {
            'bird_instance': app.config['BIRDC_INSTANCE'],
            'bird_v6_instance': app.config['BIRDC6_INSTANCE'],
            'bird_config_file': app.config['BIRD_CONFIG_FILE'],
            'bird_config_file_ipv6':app.config['BIRD_CONFIG_FILE_IPV6'],
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

    def configure_new_session(self, data= None):
        if not data:
            return False
        try:
            self._check_password(data)
            if 'ipv4' in data:
                self._check_params(data['ipv4'])
                self.configure_ipv4(data['ipv4'])
            if 'ipv6' in data:
                self._check_params(data['ipv6'])
                self.configure_ipv6(data['ipv6'])
        except BirdException as b:
            return {
                'status': 'error',
                'message': b.message
            }
        # Write configuration on file
        print "config ok"
        return {
            'status': 'success',
            'code': 200,
            'message': 'configuration ok!'
        }

    def _check_password(self, data):
        if 'secret' not in data or data['secret'] != self.app['secret_key']:
            raise BirdException('The password is wrong!')

    def _check_params(self, data):
        rules = {
            "as": [Required, Length(1, maximum=15)],
            "name": [Required, Length(1, maximum=15)],
            "ip": [Required, Length(1, maximum=15)],
            "ixtype": [Required, Length(1, maximum=15)],
            "asexport": [Required, Length(1, maximum=15)]
        }
        result = validate(rules, data)
        if not result[0]:
            raise BirdException(['{0}  {1}'.format(key, value) for key, value in result[1].iteritems()])

    def configure_ipv4(self, param):
        pass

    def configure_ipv6(self, param):
        pass


class BirdException(Exception):
    pass

'''
as
nome
ip
ixtype
asexport
maxpref
custom_commands
'''