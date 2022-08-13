"""
    @package
Generate BOM's using Jinja2 templates.
    Output: Template Specific (Markdown, AsciiDoc, plaintext, etc.)
    Fields: Template Specific
    Sort By: -g, --group [group_by] (default 'value')

    Command Line:
    python bom-gen.py "%I" -o "%O<.ext>" -t template<.ext> [-g [value]]

    Included Templates:
      * table.txt - Generate a formatted plain text table.
      * github.md - Generate a github flavoured Markdown table.
      * checklist.adoc - Generate a assembly BOM checklist in asciidoc format.
          Can be used to generate a PDF with asciidoctor-pdf.
"""

import os
import argparse
import xml.etree.ElementTree as ET
from jinja2 import Template


# Parse arguments
parser = argparse.ArgumentParser()
# Paths to needed files
parser.add_argument('infile', help='Path to KiCad netlist xml file to parse.')
parser.add_argument('-o','--output', dest='outfile', help='Path to output rendered BOM. Includes extension.')
parser.add_argument('-t','--template', help='Path to template file, or name of installed template.')

# Options
parser.add_argument('-g', '--group', nargs='?', const='value', help="Group components in rows by [group] (default 'value').")
parser.add_argument('--no-clean', action='store_false', default=True, dest='clean', help='Do not delete input xml file')

args = parser.parse_args()

template_vars = {'components': []}

# Parse input .xml file
print("Parsing input file: %s..." % args.infile)
xml_data = ET.parse(args.infile).getroot()

# Extract general information about the project
print("Extracting general info about project...")
design_xml = xml_data.find('design')
sheet1_xml = design_xml.find('sheet').find('title_block')
template_vars['name'] = sheet1_xml.find('title').text
template_vars['version'] = sheet1_xml.find('rev').text
template_vars['time'] = design_xml.find('date').text
template_vars['source'] = sheet1_xml.find('source').text

# Extract component values
print("Extracting component values...")
components = xml_data.find('components')
for component in components.findall('comp'):

    # Every component is required to have a ref and val
    comp_temp = {
        'ref': component.attrib['ref'],
        'value': component.find('value').text
    }

    # Footprint
    comp_temp['footprint'] = component.find('footprint').text

    # Lib details
    comp_lib = component.find('libsource')
    comp_temp['lib'] = comp_lib.attrib['lib']
    comp_temp['part'] = comp_lib.attrib['part']
    comp_temp['description'] = comp_lib.attrib['description']

    # Add all user defined fields
    user_fields = component.find('fields')
    if user_fields:
        for field in user_fields.findall('field'):
            comp_temp[field.attrib['name']] = field.text

    # Check for duplicates
    duplicate = None
    for added_comp in template_vars['components']:
        if args.group in added_comp and args.group in comp_temp \
                and comp_temp[args.group] == added_comp[args.group]:
            duplicate = added_comp
            break
    
    # If the grouping flag was used, and the field was duplicated
    if (args.group and duplicate is not None):
        # Stick that bad boy on the end of the Ref string and hope everything else is the same
        duplicate['ref'] = duplicate['ref'] + ', ' + comp_temp['ref']

    # Create a new BOM entry if none of the same group exist or grouping is off
    else:
        # Add component to list
        template_vars['components'].append(comp_temp)

if args.template:
    # Render template file with extracted values
    print("Rendering template: %s..." % args.template)
    try:
        # Attempt to read file as full path
        with open(args.template, 'r') as template_file:
            bom_template = Template(template_file.read(), trim_blocks=True)
    except:
        # If the file is not found attempt to load it from the templates/ directory
        with open(os.path.abspath(os.path.dirname(__file__))+'/templates/'+args.template, 'r') as template_file:
            bom_template = Template(template_file.read(), trim_blocks=True)

    rendered_bom = bom_template.render(template_vars)
else:
    print("No template defined, outputting raw values...")
    # Don't use a template
    rendered_bom = template_vars

# Remove input file
if args.clean:
    print("Cleaning up build files...")
    os.remove(args.infile)

# Output rendered BOM
if args.outfile:
    print("Writing output file: %s..." % args.outfile)
    with open(args.outfile, 'w') as f:
        f.write(rendered_bom)
    print('Done.')
else:
    print()
    print(rendered_bom)
