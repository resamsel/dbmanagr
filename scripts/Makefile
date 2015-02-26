postgres_url = https://pypi.python.org/packages/source/p/pg8000/pg8000-1.10.1.tar.gz
postgres_file = pg8000-1.10.1.tar.gz
postgres_dir = $(patsubst %.tar.gz,%,$(postgres_file))
postgres_file2 = $(basename $(postgres_url:https:/%=%))

download-%:
	echo $(postgres_url)
	echo $(postgres_file2)
	echo $($(@:download-%=%)_url) into $($(@:download-%=%)_file): $($(@:download-%=%)_dir)

assemble-%:
	make download-$(@:assemble-%=%)

all: assemble-postgres
