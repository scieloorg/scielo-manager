export LINDG4="/usr/local/Environment/bireme/cisis/5.5.pre02/linux/lindG4/"

$LINDG4/mx iso=bases/$1/title.iso create=bases/$1/title -all now
$LINDG4/mx bases/$1/title "gizmo=sql_gizmo" "pft=@title.pft" "btell=0" "lw=0" -all now > titles.txt
