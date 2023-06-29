for i in `seq 1 5`; do
  python3 test_model.py random_forest_$i.pkl test_$i.txt > results_$i.txt
done
