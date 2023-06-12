# {{ workload.name }} suppression's
{% if workload.accounts %}
The {{ workload.name }} workload has the following accounts:

**Account Name** | **Account ID**
-----------------|---------------
{% for account in workload.accounts %}{{ account.name }} | {{ account.account_id }}
{% endfor %}{% else %}There are no accounts registered under the {{ workload.name }} workload.
{% endif %}{% if workload.accounts %}{% for account in workload.accounts %}

## {{ account.name }}
{% if account.suppressions %}
The {{ account.name }} has the following suppressions registered:

**Name** | **Findings** | **Reason**
---------|--------------|---------------
{% for suppression in account.suppressions %}{{ suppression.name }} | <ul>{% for finding in suppression.findings %}<li>{{ finding }}</li>{% endfor %}</ul> | {{ suppression.reason }}
{% endfor %}{% else %}
There are no suppression's registered under the {{ account.name }} account.{% endif %}{% endfor %}{% endif %}
