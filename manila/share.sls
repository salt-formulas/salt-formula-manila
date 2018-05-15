{%- from "manila/map.jinja" import share, cfg with context %}
{%- if share.enabled %}
include:
  - manila._common

{{ share.service }}_pkg:
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

{% if not share.get('logging', {}).get('log_appender', False) %}
{%- do share.update({'logging': cfg.logging})%}
{% endif %}

{% if share.logging.log_appender == True %}
{%- set service_name = share.service %}
{%- set config = share %}
{%- include "manila/_logging.sls" %}
{% endif %}

{%- endif %}