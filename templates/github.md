# {{ name }} v{{ version }} Bill of Materials
| Ref | Value | Part Number / Footprint |
|:---:|:-----:|------------------------:|
{% for component in components %}
| {{ component.ref }} | {{ component.value }} | {{ component.MPN|default(component.footprint.split(':')[1]) }} |
{% endfor %}
---
_Generated {{ time }} by kicad-bom-gen_

