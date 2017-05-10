import subprocess
import os
from Parser.parser import Parser
from validator import Required, Pattern, validate, Length
from datetime import datetime

import logging

logging.basicConfig(
  format='[%(asctime)s] %(message)s',
  filename='./logger.log',
  level=logging.INFO)


class Bird(object):
    def __init__(self, app):
        self.app = {
            'bird_instance_ipv4': app.config['BIRDC_INSTANCE'],
            'bird_instance_ipv6': app.config['BIRDC6_INSTANCE'],
            'bird_config_file': app.config['BIRD_CONFIG_FILE'],
            'bird_config_file_ipv6': app.config['BIRD_CONFIG_FILE_IPV6'],
            'secret_key': app.config['SECRET_KEY'],
            'debug': app.config['DEBUG'],
            'bird_update_script': app.config['BIRD_UPDATE_SCRIPT']
        }

    def enrich_session(self, sessions=None):
        if sessions:
            for session in sessions:
                output = subprocess.Popen(
                  [
                    self.app['bird_instance_'+session['protocol']],
                    "sh route export {} count".format(session['name'])
                    ],
                  stdout=subprocess.PIPE).communicate()[0]
                session['exported_routes'] = Parser.parse_output_to_routes_count(output)
                output = subprocess.Popen(
                  [
                    self.app['bird_instance_'+session['protocol']],
                    "sh route protocol {} count".format(session['name'])
                    ],
                  stdout=subprocess.PIPE).communicate()[0]
                session['announced_routes'] = Parser.parse_output_to_routes_count(output)
        return sessions

    def all_bgp_session(self, protocol=None):
        if self.app['debug']:
            fake_data = os.path.join(os.path.dirname(__file__), 'summary.txt')
            f = open(fake_data, 'r')
            output = f.read()
        else:
            if protocol:
                output = subprocess.Popen(
                  [self.app['bird_instance_'+protocol], "show protocols all"],
                  stdout=subprocess.PIPE).communicate()[0]
            else:
                output = subprocess.Popen(
                  [self.app['bird_instance_ipv4'], "show protocols all"],
                  stdout=subprocess.PIPE).communicate()[0]
                output += subprocess.Popen(
                  [self.app['bird_instance_ipv6'], "show protocols all"],
                  stdout=subprocess.PIPE).communicate()[0]
        return Parser.parse_output_to_sessions(output)

    def configure_new_session(self, data=None):
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
        subprocess.call(self.app['bird_update_script'], shell=True)
        return {
            'status': 'success',
            'code': 200,
            'message': 'configuration ok!'
        }

    def _check_password(self, data):
        """
        Check if the password which has been sent is correct
        :param data: the whole post request
        :return: nothing, raise an exception in case of negative matching
        """
        if 'secret' not in data or data['secret'] != self.app['secret_key']:
            raise BirdException('The password is wrong!')

    @staticmethod
    def _check_params(data):
        """
        Check if all the required parameters have been sent
        :param data: just a part of the post request, ipv4 or ipv6
        :return: nothing, raise an exception in case of missing value
        """
        rules = {
            "as": [Required, Length(1, maximum=15)],
            "name": [Required, Length(1, maximum=15)],
            "ip": [Required, Length(1, maximum=15)],
            "ixtype": [Required, Length(1, maximum=15)],
            "asexport": [Required, Length(1, maximum=15)],
            "import": [Required, Length(1, maximum=15)]
        }
        result = validate(rules, data)
        if not result[0]:
            raise BirdException(['{0}  {1}'.format(key, value) for key, value in result[1].iteritems()])

    def configure_ipv4(self, param):
        """
        Prepare the string for Bird's config file, then append the config
        :param param: params for ipv4 configuration
        :return: nothing, raise an exception in case of failure
        """
        configuration = ['  {0}:  {1}'.format(key, value) for key, value in param.iteritems()]
        configuration = "\n".join(configuration)
        now = datetime.now()
        configuration += "\n# insert_date: {0}\n\n".format(now.strftime("%Y-%m-%d %H:%M"))
        configuration = list(configuration)
        configuration[0] = '-'
        with open(self.app['bird_config_file'], "a") as myfile:
            myfile.write("".join(configuration))

    def configure_ipv6(self, param):
        """
        Prepare the string for Bird's config file, then append the config
        :param param: params for ipv6 configuration
        :return: nothing, raise an exception in case of failure
        """
        configuration = ['  {0}:  {1}'.format(key, value) for key, value in param.iteritems()]
        configuration = "\n".join(configuration)
        now = datetime.now()
        configuration += "\n# insert_date: {0}\n\n".format(now.strftime("%Y-%m-%d %H:%M"))
        configuration = list(configuration)
        configuration[0] = '-'
        with open(self.app['bird_config_file'], "a") as myfile:
            myfile.write("".join(configuration))


class BirdException(Exception):
    pass
