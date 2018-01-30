{%- from "manila/map.jinja" import share with context %}
{%- if share.enabled %}
include:
  - manila._common

manila_share_packages:
  pkg.installed:
  - names: {{ share.pkgs }}

{{ share.service }}:
  service.running:
    - enable: true
    - watch:
      - file: /etc/manila/manila.conf
    {%- if grains.get('noservices') %}
    - onlyif: /bin/false
    {%- endif %}

{%- endif %}
