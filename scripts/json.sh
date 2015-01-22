echo '['
for i in `seq 1 10000`; do
	echo '{"a": '$i', "b":"'$i'.'$i'-'$i':'$i'"},'
	if [ "$(expr $i % 500)" = "0" ]; then
		sleep 1
	fi
done
echo '{"a": 6}'
echo ']'