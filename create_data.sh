for i in `ls plaintext`; do
  for j in `ls encrypted`; do 
    p="plaintext/$i/";
    e="encrypted/$j/$i/";
    a=`echo "$i"0.csv`;
    b=`echo "$j"1.csv`;
    c=`echo "$j.$i.csv"`; 
    echo $p $e $a $b $c;

    #run python code to generate data 
    python3 make_csv.py $p 0 $a;
    python3 make_csv.py $e 1 $b;

    #remove header row before concatenating
    sed -i '' "1d" $b

    #concatenate CSVs
    cat $a $b > $c;

    #remove temporary CSVs
    rm $a $b
  done
done
