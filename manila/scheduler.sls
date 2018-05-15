{%- from "manila/map.jinja" import scheduler, cfg with context %}
{%- if scheduler.enabled %}
include:
  - manila._common

{{ scheduler.service }}_pkg:
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

{% if not scheduler.get('logging', {}).get('log_appender', False) %}
{%- do scheduler.update({'logging': cfg.logging})%}
{% endif %}

{% if scheduler.logging.log_appender == True %}
{%- set service_name = scheduler.service %}
{%- set config = scheduler %}
{%- include "manila/_logging.sls" %}
{% endif %}

{%- endif %}
