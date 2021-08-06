# Generate documentation by actually running the code.

# Read the contents of the source file and use bash-fu to parse the calling parameters
# and the description of what those parameters will do (we use `_` as the separator).
while IFS="_" read -r item || [ -n "$item" ]
do
  IFS="_" read param comment <<< "${item}"
  # emit a comment that reminds us to NOT edit the rendered text
  echo "[//]: # (Edit doc-gen.txt rather than the following content)"
  # emit the detail of what the next invocation of the
  echo "$comment"
  # emit what the invocation will be
  echo "    (kenpom) $ python kenpom.py $param"
  # finally, emit the actual input of the command we're documenting
  ./kenpom.py "$param"
done < tools/doc-gen.txt
