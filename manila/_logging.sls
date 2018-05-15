{%- if config.logging.log_handlers.get('fluentd', {}).get('enabled', False) %}
{{ service_name }}_fluentd_logger_package:
  pkg.installed:
    - name: python-fluent-logger
{%- endif %}

{{ service_name }}_logging_conf:
  file.managed:
    - name: /etc/manila/logging/logging-{{ service_name }}.conf
    - source: salt://manila/files/logging.conf
    - template: jinja
    - makedirs: True
    - user: manila
    - group: manila
    - defaults:
        service_name: {{ service_name }}
        values: {{ config }}
    - require:
      - pkg: {{ service_name }}_pkg
{%- if config.logging.log_handlers.get('fluentd', {}).get('enabled', False) %}
      - pkg: {{ service_name }}_fluentd_logger_package
{%- endif %}
    - watch_in:
      - service: {{ service_name }}

{{ service_name }}_default:
  file.managed:
    - name: /etc/default/{{ service_name }}
    - source: salt://manila/files/default
    - template: jinja
    - require:
      - pkg: {{ service_name }}_pkg
    - defaults:
        service_name: {{ service_name }}
        values: {{ config }}
    - watch_in:
      - service: {{ service_name }}