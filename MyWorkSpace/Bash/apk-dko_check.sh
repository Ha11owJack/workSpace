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

function apk-dko {
if ( systemctl status update_client &>/dev/null )
then
	apk_port=$(port 80 20)
	if [ $apk_port == 0 ]
	then
		if ( systemctl status update_client | grep -q "ERROR" )
		then
			echo -e "\nАПК ДКО: доступен, \033[93mбыли найдены ошибки\033[0m\n"
		else
			echo -e "\nАПК ДКО: доступен, \033[92mработоспособен\033[0m\n"
		fi
	else
		echo -e "\nАПК ДКО: доступер, \033[91mнеработоспособе\033[0m\n"
	fi
fi
}
apk-dko
