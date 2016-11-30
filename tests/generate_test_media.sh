mkdir -p ./test-media/
for i in {0..9}
do
	convert -size 640x480 -gravity Center -density 96 -pointsize 56 -background gray -fill yellow caption:$i ./test-media/$i.png
	exiftool "-AllDates=2001:12:31 23:59:59" ./test-media/$i.png;
done

ffmpeg -y -framerate 1 -i ./test-media/%d.png -r 25 -f lavfi -i "sine=frequency=220:beep_factor=4:duration=10" -vcodec mpeg4 ./test-media/test.avi
