mv ../Script/*.dmp ./lab
for entry in "./lab"/*
do
    python3 bin2png.py -infile $entry -o $entry.png -resize 300 300
done

mv ./lab/*.png ./png
mv ./lab/* ./dump
