#!/bin/sh -e
#Author: liwei <anbutu@gmail.com>
pydict $( head -$(( $RANDOM % $( wc -l ~/dic.txt | cut -d " " -f 1 ) + 1 )) ~/dic.txt | tail -1 ) 
