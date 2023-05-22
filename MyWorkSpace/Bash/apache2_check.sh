function port {
        info=0
        for i in ${@}
        do
                if netstat -plant | grep  ":$i " | grep -q "LISTEN"
                then
                        printf ""
                else
                        let "info++"
                fi
        done
        echo "$info"
}

function apache2_check {
if ( dpkg -s apache2 &>/dev/null )
then
      if ( systemctl status apache2 | grep -oP "Active: \K[^.]+" | grep -q inactive )
      then
             echo -e "\napache2: доступен, \033[93mотключен\033[0m\n"
      else
	     per=$(port 9000 9001 9004)
    	     if [ $per == 0 ]
    	     then
                    echo -e "\napache2: доступен, \033[92mработоспособен\033[0m\n"
	     else
	            echo -e "\napache2: доступен, \033[91mнеработоспособен\033[0m\n"
             fi
      fi
fi
}
apache2_check
