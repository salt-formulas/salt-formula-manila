{%- from "manila/map.jinja" import data with context %}
{%- if data.enabled %}
include:
  - manila._common

manila_data_packages:
  pkg.installed:
  - names: {{ data.pkgs }}

{{ data.service }}:
  service.running:
    - enable: true
    - watch:
      - file: /etc/manila/manila.conf
    {%- if grains.get('noservices') %}
    - onlyif: /bin/false
    {%- endif %}

{%- endif %}
