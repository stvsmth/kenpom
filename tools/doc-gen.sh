while IFS="_" read -r item || [ -n "$item" ]
do
  IFS="_" read param comment <<< "${item}"
  echo "[//]: # (Edit doc-gen.txt rather than the following content)"
  echo "$comment"
  echo "    (kenpom) $ python kenpom.py $param"
  ./kenpom.py "$param"
done < tools/doc-gen.txt
