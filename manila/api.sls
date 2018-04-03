{%- from "manila/map.jinja" import api with context %}
{%- if api.enabled %}
include:
  - apache
  - manila._common

manila_api_packages:
  pkg.installed:
  - names: {{ api.pkgs }}

manila_install_database:
  cmd.run:
  - names:
    - manila-manage --config-file /etc/manila/manila.conf db sync
  - require:
    - file: /etc/manila/manila.conf
  {%- if grains.get('noservices') %}
  - onlyif: /bin/false
  {%- endif %}

manila_api_service_dead:
  service.dead:
  - name: manila-api
  - enable: False

manila_site_enabled:
  apache_site.enabled:
    - name: wsgi_manila

manila_apache_wsgi_config:
  file.exists:
    - name: /etc/apache2/sites-available/wsgi_manila.conf
    - require:
      - manila_site_enabled

{{ api.service }}:
  service.running:
    - enable: true
    - watch:
      - file: /etc/manila/manila.conf
      - file: /etc/manila/policy.json
      - manila_apache_wsgi_config
      - manila_site_enabled
    {%- if grains.get('noservices') %}
    - onlyif: /bin/false
    {%- endif %}
    - require:
      - manila_api_service_dead
      - manila_site_enabled

/etc/manila/policy.json:
  file.managed:
  - source: salt://manila/files/{{ api.version }}/policy.json
  - template: jinja
  - require:
    - pkg: manila_api_packages

{%- endif %}
