{%- if pillar.manila is defined %}
include:
{%- if pillar.manila.api is defined %}
- manila.api
{%- endif %}
{%- if pillar.manila.data is defined %}
- manila.data
{%- endif %}
{%- if pillar.manila.scheduler is defined %}
- manila.scheduler
{%- endif %}
{%- if pillar.manila.share is defined %}
- manila.share
{%- endif %}
{%- if pillar.manila.client is defined %}
- manila.client
{%- endif %}
{%- endif %}
