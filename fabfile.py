from __future__ import with_statement
from fabric.api import *

# Deploy release
@hosts(['root@10.49.0.218'])
def deploy():
     with cd('/root/work/birdy'):
        run('git checkout .')
        run('git pull')
        run('service birdy restart')
