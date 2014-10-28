perl -0777 -i -pe 's#```\nusage: '$1'.*?```#```\n'"$($1 -h | sed 's/@/\\@/g')"'\n```#igs' README.md
