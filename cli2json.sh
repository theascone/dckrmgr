#!/bin/bash

if [ -z "$1" ]; then
    read -p "No file provided, enter create-command: " comm
else
    comm=`cat "$1"`
fi

function search() {
    #echo "search() $*" 1>&2
    val=`grep -Po "(?<=$1 ).*(?= )"  <<< "$comm"`
    if [ -z "$val" ] && [ -n "$2" ]; then
        val=`grep -Po "(?<=$2 ).*(?= )"  <<< "$comm"`
    fi
    echo "$val"
}

function part() {
    #echo "part() $*" 1>&2
    cut --delimiter=':' --fields=$2 <<< "$1"
}

indent="  "
hspace="\n\n"
function add() {
    #echo "add() $*" 1>&2
    if [ "$1" == "-l" ]; then
      shift
      [ -n "$3" ] && c_hspace="$3" || c_hspace="$hspace"
      json+="$indent\"$1\":\"$2\"$c_hspace"
    else
      [ -n "$3" ] && c_hspace="$3" || c_hspace="$hspace"
      json+="$indent\"$1\":\"$2\",$c_hspace"
    fi
}

function begin_multi() {
    json+="$indent\"$1\": {\n"
}
function multi() {
    json+="$indent"
    [ $# -eq 2 ] && add "$1" "$2" "\n" || add "$1" "$2" "$3" "\n"
}
function end_multi() {
    if [ "$1" == "-l" ]; then
      json+="$indent}$hspace"
    else
      json+="$indent},$hspace"
    fi
}

function begin_arr() {
    json+="$indent\"$1\": [\n"
}
function begin_elem() {
    json+="$indent$indent{\n"
}
function elem() {
    json+="$indent"
    multi $*
}
function end_elem() {
    if [ "$1" == "-l" ]; then
        json+="$indent$indent}\n"
    else
        json+="$indent$indent},\n"
    fi
}
function end_arr() {
    if [ "$1" == "-l" ]; then
        json+="$indent]\n"
    else
        json+="$indent],$hspace"
    fi
}

function arr() {
    #echo "arr() $*" 1>&2
    local cut_pwd=false last=false
    if [ "$1" == "--cut-pwd" ]; then
      cut_pwd=true
      shift
    fi
    if [ "$1" == "-l" ]; then
      last=true
      shift
    fi
    local arr_name="$1" arr_value="$2" elem1="$3" elem2="$4" elem3="$5" elem3def="$6"
    local part1 part2 part3 Values Values_length
    
    [ -n "$arr_value" ] && begin_arr "$arr_name"
    
    Values=()
    while read val
    do
        Values+=("$val")
    done <<< "$arr_value"
    
    Values_length=${#Values[@]}
    for (( i=0; i < $Values_length; i++ ));
    do
      val="${Values[$i]}"
      
      begin_elem
      part1="`part $val 1`"
      [ "$cut_pwd" == true ] && part1=`sed -e 's/$pwd\///I' <<< "$part1"`
      part2="`part $val 2`"
      part3="`part $val 3`"
      
      elem "$elem1" "$part1"        
      if [ -n "$elem3" ]; then
        part3=${part3:-$elem3def}
        elem "$elem2" "$part2"
        elem -l "$elem3" "$part3"
      else
        elem -l "$elem2" "$part2"
      fi
      
      [ $i -lt $(($Values_length-1)) ] && end_elem || end_elem -l
    done
      
    if [ -n "$arr_value" ];then
      [ "$last" == true ] && end_arr -l || end_arr
    fi
}
output() {
  local text
  local bldwht='\e[1;37m' # White
  local txtrst='\e[0m'    # Text Reset
  if [ "$1" == "-n" ]; then
    shift
    text="$bldwht""$1: $txtrst""$2"
    echo -e -n "$text" 1>&2
  else
    text="$bldwht""$1: $txtrst""$2"
    echo -e "$text" 1>&2
  fi
}

bldgrn='\e[1;32m' # Green

json='{\n'
name=`search "--name"`
output "Name" "$name"
add "name" "$name"

img_temp=`grep -P -v "(?<=-)[[:alnum:]]+ [^\s]+" <<< "$comm" | sed -n 2p | cut -d ' ' -f 1`
img=`part "$img_temp" 1`
ver=`part "$img_temp" 2`
[ -n "$ver" ] && ver=latest
output -n "Image" "$img, "
output "Version" "$ver"
begin_multi "image"
multi "name" "$img"
multi -l "version" "$ver"
end_multi

host=`search "-h" "--hostname"`
output "Hostname" "$host"
[ -n "$host" ] && add "hostname" "$host"

env=`search "-e"`
output "\nENV" "\n$env\n"
arr "environment" "$env" "name" "value"

vol=`search "-v"`
output "Volumes" "\n$vol\n"
arr --cut-pwd "volumes" "$vol" "host_path" "container_path" "mode" "rw"

links=`search "--link"`
output "Links" "\n$links\n"
arr -l "links" "$links" "name" "alias"

json+='}'

output "Json" "\n"
echo "$json"
