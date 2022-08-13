"""
    @package
    Generate a PDF BOM Checklist, useful for assembly.
    Output: AsciiDoc, PDF
    Sorted By: Ref
    Fields: Ref, Value, MPN/Footprint, UPN

    Command line:
    python "pathToFile/bom-gen-pdf.py" "%I" "%O.adoc"
"""

# We do some simple argument parsing so sys.argv is sufficient.
from sys import argv

# We use os.system to make system calls and delete files
from os import system, remove

print("Generating intermediate asciidoc...")
# Generate our intermediate format of asciidoc with bom-gen.py:
# - Using the checklist template
# - Not grouped
system("python /home/rex/code/python/kicad-bom-gen/bom-gen.py %s -o %s -t checklist.adoc %s" % (argv[1], argv[2], ' '.join(argv[3:])))

print("Generating final PDF from asciidoc...")
# Generate a pdf from the asciidoc using asciidoctor-pdf
system("asciidoctor-pdf %s" % argv[2])

print("Cleaning up build files...")
remove(argv[2])     # Delete intermediate .adoc
