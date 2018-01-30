{%- from "manila/map.jinja" import scheduler with context %}
{%- if scheduler.enabled %}
include:
  - manila._common

manila_scheduler_packages:
  pkg.installed:
  - names: {{ scheduler.pkgs }}

{{ scheduler.service }}:
  service.running:
    - enable: true
    - watch:
      - file: /etc/manila/manila.conf
    {%- if grains.get('noservices') %}
    - onlyif: /bin/false
    {%- endif %}

{%- endif %}
