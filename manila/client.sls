{%- from "manila/map.jinja" import client with context %}
{%- if client.enabled %}

manila_client_pkg:
  pkg.installed:
    - names: {{ client.pkgs }}
    - install_recommends: False

{%- endif %}
