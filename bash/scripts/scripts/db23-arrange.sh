#! /usr/bin/bash
filename=$1
arrangedFolder=${PWD}/arranged
newFilename=${filename:0:3}db23-arranged.pdf
echo "Arranging $filename"
/usr/bin/pdfjam --nup 2x2 --landscape --outfile $newFilename $filename
echo "Moving $new-filename to $arranged-folder"
mv $newFilename $arrangedFolder
echo "Done"
