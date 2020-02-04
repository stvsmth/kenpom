while IFS="_" read -r item || [ -n "$item" ]
do
  IFS="_" read param comment <<< "${item}"
  echo "$comment"
  echo "    (kenpom) $ python kenpom.py $param"
  ./kenpom.py "$param"
done < tools/doc-gen.txt
