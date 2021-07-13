#!/bin/bash

size=0x$(echo $(objdump -h $1.elf|egrep -w "(Idx|load1)" | tr -s " " |  cut -d " " -f 4) | cut -d " " -f 2)
off=0x$(echo $(echo "obase=16;ibase=16;`objdump -h $1.elf|egrep -w "(Idx|load1)" | tr -s " " |  cut -d " " -f 7 | tr /a-z/ /A-Z/`" | bc) | cut -d " " -f 2)

head -c $(($size+$off)) $1.elf|tail -c +$(($off+1)) > $1.raw