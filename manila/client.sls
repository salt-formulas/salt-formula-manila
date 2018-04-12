{%- from "manila/map.jinja" import client with context %}
{%- if client.enabled %}

manila_client_pkg:
  pkg.installed:
    - names: {{ client.pkgs }}
    - install_recommends: False

{%- for identity_name, identity in client.server.iteritems() %}
{%- if identity.share_type is defined %}
{%- for share_type_name, share_type in identity.share_type.iteritems() %}

manila_share_type_{{ share_type_name }}:
  manilang.share_type_present:
    - cloud_name: {{ identity_name }}
    - name: {{ share_type_name }}
    - extra_specs: {{ share_type.extra_specs }}

{%- endfor %}
{%- endif %}
{%- endfor %}

{%- endif %}
