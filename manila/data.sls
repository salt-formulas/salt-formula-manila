{%- from "manila/map.jinja" import data, cfg with context %}
{%- if data.enabled %}
include:
  - manila._common

{{ data.service }}_pkg:
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

{% if not data.get('logging', {}).get('log_appender', False) %}
{%- do data.update({'logging': cfg.logging})%}
{% endif %}

{% if data.logging.log_appender == True %}
{%- set service_name = data.service %}
{%- set config = data %}
{%- include "manila/_logging.sls" %}
{% endif %}

{%- endif %}