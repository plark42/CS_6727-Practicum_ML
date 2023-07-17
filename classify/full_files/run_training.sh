for i in `seq 1 5`; do
  python3 train_model.py train_$i.txt random_forest_$i.pkl 
done
