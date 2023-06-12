for f in `ls csv/`; do
  csv=`echo $f | sed 's/^/ascii_freq\./g'`
  echo $f $csv
  python3 ascii_freqs.py csv/$f $csv 2> /dev/null 
done
