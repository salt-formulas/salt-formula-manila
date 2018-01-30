manila:
  api:
    region: RegionOne
    enabled: true
    version: pike
    bind:
      host: 127.0.0.1
      port: 8977
    identity:
      engine: keystone
      host: 127.0.0.1
      port: 35357
      tenant: service
      user: manila
      password: misterio
      endpoint_type: internalURL
    database:
      engine: mysql
      host: 127.0.0.1
      port: 3306
      name: manila
      user: manila
      password: misterio
    message_queue:
      engine: rabbitmq
      host: '127.0.0.1'
      port: 5672
      user: openstack
      password: workshop
      virtual_host: '/openstack'
apache:
  server:
    enabled: true
    default_mpm: event
    mpm:
      prefork:
        enabled: true
        servers:
          start: 5
          spare:
            min: 2
            max: 10
        max_requests: 0
        max_clients: 20
        limit: 20
    site:
      manila:
        enabled: false
        available: true
        type: wsgi
        name: manila
        host:
          name: manila.ci.local
          address: 127.0.0.1
          port: 8041
        log:
          custom:
            format: >-
              %v:%p %{X-Forwarded-For}i %h %l %u %t \"%r\" %>s %D %O \"%{Referer}i\" \"%{User-Agent}i\"
        wsgi:
          daemon_process: manila-api
          processes: 2
          threads: 10
          user: manila
          group: manila
          display_name: '%{GROUP}'
          script_alias: '/ /usr/bin/manila-api'
          application_group: '%{GLOBAL}'
          authorization: 'On'
