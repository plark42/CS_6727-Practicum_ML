grep ",0$" features.csv | grep "aes" > plain.csv
grep ",1$" features.csv > encrypted.csv
head -1 features.csv > header.csv
cat header.csv plain.csv encrypted.csv > features.csv
