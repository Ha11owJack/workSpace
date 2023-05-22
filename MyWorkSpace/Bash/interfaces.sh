    #!/bin/bash
    if [ "-h" == "$1" ]
    then
        	echo -e "-a - добавление портов\n-d - очищение портов\n\n***ФАЙЛ***"
    	cat /etc/network/interfaces
    #/etc/network/interfaces
    	echo -e "**********\n"
    fi
       if [ "-a" == "$1" ]
       then
       if grep -q bond0 "/etc/network/interfaces"
       then
              awk 'BEGIN {p=1} /^iface eth2/ {print''; p=0} /^auto eth3/ {p=1} p' /etc/network/interfaces > interfaces.tmp && mv interfaces.tmp /etc/network/interfaces
              sed '/^iface eth3 inet/q' /etc/network/interfaces > interfaces.tmp && mv interfaces.tmp /etc/network/interfaces
              for z in 2 3
              do
                    sed -i '/^iface eth'$z'/ a\\taddress 192.168.'$z'.10\ \n\tnetmask 255.255.255.0' /etc/network/interfaces
                    sed -i 's/iface eth'$z' inet manual/iface eth'$z' inet static/g' /etc/network/interfaces
       	 done
	Perem=$(bash intefaces.sd -t)
        echo $Perem
       else
              awk 'BEGIN {p=1} /^iface eth1/ {print''; p=0} /^auto eth2/ {p=1} p' /etc/network/interfaces > interfaces.tmp && mv interfaces.tmp /etc/network/interfaces
              awk 'BEGIN {p=1} /^iface eth2/ {print''; p=0} /^auto eth3/ {p=1} p' /etc/network/interfaces > interfaces.tmp && mv interfaces.tmp /etc/network/interfaces
        	  sed '/^iface eth3 inet/q' /etc/network/interfaces > interfaces.tmp && mv interfaces.tmp /etc/network/interfaces
        	  for z in 1 2 3
        	  do
        	  	sed -i '/^iface eth'$z'/ a\\taddress 192.168.'$z'.10\ \n\tnetmask 255.255.255.0' /etc/network/interfaces
    		sed -i 's/iface eth'$z' inet manual/iface eth'$z' inet static/g' /etc/network/interfaces
              done
	Perem=$(bash interfaces.sh -t)
	echo $Perem
       fi
    fi
    if [ "-d" == "$1" ]
    then
        if grep -q bond0 "/etc/network/interfaces"
        then
            awk 'BEGIN {p=1} /^iface eth2/ {print''; p=0} /^auto eth3/ {p=1} p' /etc/network/interfaces > interfaces.tmp && mv interfaces.tmp /etc/network/interfaces
            sed -i '/^iface eth2/ a\\n' /etc/network/interfaces
        	sed '/^iface eth3 inet/q' /etc/network/interfaces > interfaces.tmp && mv interfaces.tmp /etc/network/interfaces
    	for z in 2 3
            do
                    sed -i 's/iface eth'$z' inet static/iface eth'$z' inet manual/g' /etc/network/interfaces
            done
        else
        	awk 'BEGIN {p=1} /^iface eth1/ {print''; p=0} /^auto eth2/ {p=1} p' /etc/network/interfaces > interfaces.tmp && mv interfaces.tmp /etc/network/interfaces
        	sed -i '/^iface eth1/ a\\n' /etc/network/interfaces
        	awk 'BEGIN {p=1} /^iface eth2/ {print''; p=0} /^auto eth3/ {p=1} p' /etc/network/interfaces > interfaces.tmp && mv interfaces.tmp /etc/network/interfaces
        	sed -i '/^iface eth2/ a\\n' /etc/network/interfaces
        	sed '/^iface eth3 inet/q' /etc/network/interfaces > interfaces.tmp && mv interfaces.tmp /etc/network/interfaces
    	for z in 1 2 3
            do
                    sed -i 's/iface eth'$z' inet static/iface eth'$z' inet manual/g' /etc/network/interfaces
            done
        fi
    fi

    if [ "-t" == "$1" ]
    then
    if grep -q bond0 "/etc/network/interfaces"
    then

    sed -n -e '/iface eth2 inet static/,/^auto eth3/p' /etc/network/interfaces | grep address | sed 's/address/eth2/g' | xargs | tr -d '\r\n' | sed 's\$\/24\g' |sed 's/$/;/g'
    if grep -q "iface eth3 inet static" "/etc/network/interfaces"
    then
    sed -n -e '/^iface eth3 inet static/,$p' /etc/network/interfaces | grep address | sed 's/address/eth3/g' | xargs | sed 's\$\/24\g' | sed 's/$/;/g'
    fi
    else
    sed -n -e '/iface eth1 inet static/,/auto eth2/p' /etc/network/interfaces | grep address | sed 's/address/eth1/g' | xargs | tr -d '\r\n' | sed 's\$\/24\g' | sed 's/$/;/g' 
    sed -n -e '/^iface eth2 inet static/,/^auto eth3/p' /etc/network/interfaces | grep address | sed 's/address/eth2/g' | xargs | tr -d '\r\n' | sed 's\$\/24\g' | sed 's/$/;/g'
    if grep -q "iface eth3 inet static" "/etc/network/interfaces"
    then
    sed -n -e '/^iface eth3 inet static/,$p' /etc/network/interfaces | grep address | sed 's/address/eth3/g' | xargs |  sed 's\$\/24\g' | sed 's/$/;/g'
    fi
    fi
    fi
