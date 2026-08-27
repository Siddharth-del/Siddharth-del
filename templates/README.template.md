<!--
  AUTO-GENERATED FILE — do not edit directly.
  Edit config.yml instead; this file is rebuilt by the GitHub Action
  (.github/workflows/update-profile.yml) on every push and on a daily
  schedule, so contribution/skills data stays current.
-->

<div align="center">

<a href="{{ socials.github }}">
  <img src="assets/portrait.svg" width="220" alt="{{ identity.name }} — dot-matrix portrait" />
</a>

<br>

<a href="{{ socials.github }}">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=28&duration=3000&pause=1200&color={{ typing_color }}&center=true&vCenter=true&width=650&lines={{ typing_lines }}" alt="Typing SVG" />
</a>

<p>{{ identity.summary }}</p>

<br>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)]({{ socials.linkedin }})
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:{{ socials.email }})
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)]({{ socials.github }})
[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=vercel&logoColor=white)]({{ socials.portfolio }})

</div>

<br>

## About

{% for line in about %}
- {{ line }}
{% endfor %}

<br>

## Skills Radar

<div align="center">
<img src="assets/skills.svg" width="70%" alt="Skills radar chart" />
</div>

<br>

## Tech Stack

<table>
<tr>
{% for category, items in tech_stack.items() %}
<td valign="top" width="33%">

**{{ category }}**

{% for item in items %}{{ badge(item) }} {% endfor %}

</td>
{% if loop.index % 3 == 0 and not loop.last %}</tr><tr>{% endif %}
{% endfor %}
</tr>
</table>

<br>

## Featured Projects

<div align="center">
<img src="assets/bento.svg" width="100%" alt="Project showcase" />
</div>

{% for project in projects %}
### {{ project.name }}
{{ project.description }}

**Stack:** {{ project.stack | join(', ') }}

**Highlights:**
{% for h in project.highlights %}
- {{ h }}
{% endfor %}

{% if project.repo_url %}[Repository]({{ project.repo_url }}){% endif %}{% if project.demo_url %} &nbsp;·&nbsp; [Live Demo]({{ project.demo_url }}){% endif %}

<br>

{% endfor %}

<br>

## Contribution Activity

<div align="center">
<img src="assets/contributions.svg" width="100%" alt="Contribution graph" />
</div>

<br>

## Certifications

{% for c in certifications %}
- {{ c }}
{% endfor %}

<br>

## Currently Learning

{% for c in currently_learning %}
- {{ c }}
{% endfor %}

<br>

## Connect

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)]({{ socials.linkedin }})
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:{{ socials.email }})
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)]({{ socials.github }})
[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=vercel&logoColor=white)]({{ socials.portfolio }})

</div>

<br>

<div align="center">

*{{ footer_statement }}*

</div>
