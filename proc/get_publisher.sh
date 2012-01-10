export LINDG4="/usr/local/Environment/bireme/cisis/5.5.pre02/linux/lindG4/"

$LINDG4/mx iso=bases/$1/title.iso create=bases/$1/title -all now
$LINDG4/mx bases/$1/title "gizmo=sql_gizmo" "pft='insert into title_publisher (name,country,state,city,address,mail,sponsor) values (\"'v480,'\",\"',v310,'\",\"',v320,'\",\"',v490,'\",\"',(v63,', '),'\",\"',v64,'\",\"',v62,'\");',/" btell=0 lw=0 -all now > publishers.txt
