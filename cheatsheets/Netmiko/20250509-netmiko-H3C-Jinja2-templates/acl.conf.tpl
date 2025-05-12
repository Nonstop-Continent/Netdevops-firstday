user-interface{{interface}}

acl number 2000 inbound
acl number 2000

{% for host in disallow_ip %}
rule deny source {{host}} 0
{% endfor %}

{% for host in allow_ip %}
rule permit source {{host}} 0
{% endfor %}
