{%- from "manila/map.jinja" import cfg with context %}

manila_common.pkgs:
  pkg.installed:
    - name: 'manila-common'
    - install_recommends: False

/etc/manila/manila.conf:
  file.managed:
  - source: salt://manila/files/{{ cfg.version }}/manila.conf
  - template: jinja
  - require:
    - pkg: manila_common.pkgs

{%- if cfg.message_queue.get('ssl',{}).get('enabled', False) %}
rabbitmq_ca_manila_file:
{%- if cfg.message_queue.ssl.cacert is defined %}
  file.managed:
    - name: {{ cfg.message_queue.ssl.cacert_file }}
    - contents_pillar: cfg.message_queue:ssl:cacert
    - mode: 0444
    - makedirs: true
{%- else %}
  file.exists:
   - name: {{ cfg.message_queue.ssl.get('cacert_file', cfg.cacert_file) }}
{%- endif %}
{%- endif %}

{%- if cfg.database.get('ssl',{}).get('enabled', False) %}
mysql_ca_manila_file:
{%- if cfg.database.ssl.cacert is defined %}
  file.managed:
    - name: {{ cfg.databse.ssl.cacert_file }}
    - contents_pillar: cfg.database:ssl:cacert
    - mode: 0444
    - makedirs: true
{%- else %}
  file.exists:
   - name: {{ cfg.database.ssl.get('cacert_file', cfg.cacert_file) }}
{%- endif %}
{%- endif %}
