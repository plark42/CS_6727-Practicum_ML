for f in `ls csv/`; do
  png=`echo $f | sed 's/csv/png/g'`
  echo $f
  echo $png
  python3 classify.py csv/$f $png 2> /dev/null >> results.csv
done
