==============
Manila Formula
==============

Manila is an OpenStack project to provide “Shared Filesystems as a service”.

Sample pillars
==============

Single manila service

.. code-block:: yaml

    manila:
      common:
        database:
          engine: mysql
          host: 10.20.0.101
          port: 3306
          name: manila
          user: manila
          password: segreto
        identity:
          engine: keystone
          host: 10.20.0.101
          port: 35357
          user: manila
          password: segreto
          region: RegionOne
          tenant: service
          endpoint_type: internalURL
        cache:
          engine: memcached
          members:
          - host: 10.20.0.102
            port: 11211
          - host: 10.20.0.103
            port: 11211
          - host: 10.20.0.104
            port: 11211
      api:
        bind:
          host: 10.20.0.102


More information
================

* https://wiki.openstack.org/wiki/Telemetry
* https://docs.openstack.org/developer/manila/
* https://github.com/openstack/manila
* https://bugs.launchpad.net/manila


Documentation and Bugs
======================

To learn how to install and update salt-formulas, consult the documentation
available online at:

    http://salt-formulas.readthedocs.io/

In the unfortunate event that bugs are discovered, they should be reported to
the appropriate issue tracker. Use GitHub issue tracker for specific salt
formula:

    https://github.com/salt-formulas/salt-formula-manila/issues

For feature requests, bug reports or blueprints affecting entire ecosystem,
use Launchpad salt-formulas project:

    https://launchpad.net/salt-formulas

Developers wishing to work on the salt-formulas projects should always base
their work on master branch and submit pull request against specific formula.

You should also subscribe to mailing list (salt-formulas@freelists.org):

    https://www.freelists.org/list/salt-formulas

Any questions or feedback is always welcome so feel free to join our IRC
channel:

    #salt-formulas @ irc.freenode.net
