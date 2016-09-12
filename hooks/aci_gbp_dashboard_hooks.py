#!/usr/bin/env python

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

hooks = Hooks()

@hooks.hook('config-changed')
def aci_gbp_dashboard_config_changed(relation_id=None):
    pass

@hooks.hook()
@hooks.hook('install')
def aci_gbp_dashboard_install(relation_id=None):
    conf = config()

    if 'aci-repo-key' in conf.keys():
        fetch.add_source(conf['aci-repo'], key=conf['aci-repo-key'])
        opt = []
    else:
        fetch.add_source(conf['aci-repo'])
        opt = ['--allow-unauthenticated']

    fetch.apt_update(fatal=True)
    fetch.apt_upgrade(fatal=True)

    fetch.apt_install('group-based-policy-ui', options=opt, fatal=True)
    
def main():
    try:
        hooks.execute(sys.argv)
    except UnregisteredHookError as e:
        log('Unknown hook {} - skipping.'.format(e))

if __name__ == '__main__':
    main()
