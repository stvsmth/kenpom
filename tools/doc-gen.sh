# Generate documentation by actually running the code.
# Should just be able to run tools/doc-gen.sh and paste over the entire last section
# of the README.md file.

# Read the contents of the file and use bash-fu to parse the calling parameters
{
  # ... read over the first two lines, where we have simple comments
  read -r
  read -r
  # ... then each line, composed of the sample input and an explanatory comment
  # TODO: Add a -1 or --once command that bypasses REPL.
  while IFS="_" read -r item || [ -n "$item" ]
  do
    IFS="_" read -r param comment <<< "${item}"
    # emit a Markdown comment that reminds us to NOT edit the rendered text
    echo "[//]: # (Edit doc-gen.txt rather than the following content)"
    # emit the detail of what the upcoming invocation will do
    echo "${comment}"
    # emit what the invocation itself
    echo ""  # Markdown wants whitespace around code blocks
    echo "    (kenpom) $ python kenpom.py ${param}"
    # finally, emit the actual output of the command we're documenting
    ./kenpom.py "${param}" --once --indent=4 | grep -v "Data through"
  done
} < tools/doc-gen.txt
