#! /usr/bin/bash

filename=$1
arrangedFolder=${PWD}/arranged
newFilename=${filename}-pr23-arranged.pdf
echo "Arranging $filename"
/usr/bin/pdfjam --nup 2x1 --landscape --outfile $newFilename $filename
echo "Moving $newFilename to $arrangedFolder"
mv $newFilename $arrangedFolder
echo "Done"
