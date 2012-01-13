#!/bin/bash

#carrega config
. import_config.sh

	#scp do arquivo ISO
	#scp $database_server:/$database_dir/$dbname/$dbname.iso in_isis/
	
	#gerar ISO da base
	#$cisis_dir/mx $in_isis/$dbname iso=$iso_file -all now tell=10


#cria .json a partir de base isis
python ../isis2couchdb/tools/isis2json.py $iso_file -o out_json/$json_file
