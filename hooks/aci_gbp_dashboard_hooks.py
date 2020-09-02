#!/usr/bin/env python3

import sys
import subprocess
import jinja2
import tempfile

from charmhelpers.core.hookenv import (
    Hooks,
    UnregisteredHookError,
    config,
    log,
    relation_set,
    relation_ids,
)
from charmhelpers import fetch

from charmhelpers.contrib.openstack.utils import (
    os_release,
    CompareOpenStackReleases,
)


hooks = Hooks()

@hooks.hook('config-changed')
def aci_gbp_dashboard_config_changed(relation_id=None):
    pass

#@hooks.hook('dashboard-plugin-relation-joined')
#@hooks.hook('dashboard-plugin-relation-changed')
#def plugin_relation_changed(relation_id=None):
#    pass

@hooks.hook()
@hooks.hook('install')
def aci_gbp_dashboard_install(relation_id=None):
    conf = config()

    if config('aci-repo-key'):
        fetch.add_source(config('aci-repo'), key=config('aci-repo-key'))
        opt = []
    else:
        with open('/etc/apt/apt.conf.d/90insecure', 'w') as ou:
           ou.write('Acquire::AllowInsecureRepositories "true";')
        fetch.add_source(config('aci-repo'))
        opt = ['--allow-unauthenticated']

    fetch.apt_update(fatal=True)
    fetch.apt_upgrade(fatal=True, options=opt)

    myrelease = os_release('openstack-dashboard')

    if CompareOpenStackReleases(myrelease) > 'queens':
        fetch.apt_install('python3-group-based-policy-ui', options=opt, fatal=True)
    else:
        fetch.apt_install('group-based-policy-ui', options=opt, fatal=True)
    
    subprocess.check_call(['/usr/share/openstack-dashboard/manage.py', 'collectstatic', '--noinput'])
    
def main():
    try:
        hooks.execute(sys.argv)
    except UnregisteredHookError as e:
        log('Unknown hook {} - skipping.'.format(e))

if __name__ == '__main__':
    main()
