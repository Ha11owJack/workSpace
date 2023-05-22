#!/bin/bash
function back_file() {
  if [ -f $1$2 ]
  then
    mv -f $1$2 $1$3
    echo "$3 файл вернулся в исходное состояние"
  else
    echo "$2 файл не был обнаружен"
  fi
}

function repo_mount() {
  cp /etc/apt/sources.list /etc/apt/sources.list.old
  if [ -f $PWD/$1 ]
    then
		  if [[ ! -d $PWD/$2 ]]
      then
        mkdir $PWD/$2
      fi
      mount $PWD/$1 $PWD/$2
      echo -e "deb file:$PWD/$2 leningrad main contrib non-free" > /etc/apt/sources.list
		  apt update
  else
      echo -e "Апдейт не обнаружен в данной папке, пожалуйста перейдите в нужную директорию с наличием файла $1"
      back_file /etc/apt/ sources.list.old sources.list
      exit 1
  fi
}

function clean_file() {
  if lsblk | grep -q $1
  then
    umount $PWD/$1 
    rm -rf $PWD/$1
  fi
}

function repo_main() {
  if [ $1 == "-n" ]
  then
       echo "main репозиторий не будет монтирован"
  else
       if [ -f $PWD/mounted-main-leningrad.iso ]
       then
		      if [[ ! -d $PWD/local_repo ]]
          then
            mkdir $PWD/local_repo
          fi
          mount $PWD/mounted-main-leningrad.iso $PWD/local_repo
          echo -e "deb file:$PWD/local_repo leningrad main contrib non-free" >> /etc/apt/sources.list
		      apt update
      else
          echo -e "Апдейт не обнаружен в данной папке, пожалуйста перейдите в нужную директорию с наличием файла mounted-main-leningrad.iso"
          back_file /etc/apt/ sources.list.old sources.list
          exit 1
      fi
  fi
}

if [ "$(id -u)" != 0 ]
then
  echo -e "Необходимы права суперпользователя!\nПопробуйте использовать sudo."
  exit 1
fi
case $1 in
  -help)
    #Помощь/Общая инфомрация по скрипту
    echo -e "Информация"
    echo -e "Данный скрипт предназначен для упрощения работы с серверным оборудованием.\n"
    echo -e "Примеры использования:"
    echo -e "Настройка сетевых интерфейсов\n./suns.sh -eth -10th 10.20.13.{1-255}\n./suns.sh -eth -20th {gateway}\n"
    echo -e "Установка локального репозитория\n./suns.sh -iso\n"
    echo -e "Установка обновлений\n./suns.sh -2upd\n./suns.sh -3upd\n"
    echo -e "Установка основного репозитория (по сети)\n./suns.sh -repo\n"
    echo -e "Очистка мусора после данного скрипта\n./suns.sh -clean\n"
    echo -e "Используйте осторожно и только если знаете, что делаете."
   ;;
	-eth)
    #Настройка сетевых интерфейсов и перезапуск сервиса
    #Сеть 10.20.13.ххх
		if [ $2 == "-10th" ]
		then
			echo -e "#\n#\n\nsource /etc/network/intefaces.d/*\n\n#The loopback network interface\nauto lo\niface lo inet loopback\n" > /etc/network/interfaces
			echo -e "auto eth0\niface eth0 inet static\n     address $3\n     netmask 255.255.255.0\n     gateway 10.20.13.1\n" >> /etc/network/interfaces
			for i in 1 2 3
			do
				echo -e "auto eth$i\niface eth$i inet manual\n" >> /etc/network/interfaces
			done
			ip addr flush label eth*
			systemctl restart networking.service
      #Проверка, запустился ли сервис, макс время ожидания - 5 мин, интервал проверки - 20 сек
      i=0
      while true
      do
        ((i++))
        echo "attempt $i"
        sleep 20s
        status=$(systemctl is-active networking.service)
        if [ $status == "active" ]
        then
          echo -e "Настройки сетевых интерфейсов для сети $2 успешно установлены. Сеть готова к эксплуатации."
          break
        fi
        if [ $i -ge 15 ]
        then
          echo -e "Сервис networking.service не может запуститься на протяжении 5 минут."
          exit 1
        fi
      done
      exit 0
    #Сеть 20.ххх.ххх.ххх    
		elif [ $2 == "-20th" ]
		then
      #luna - Счетчик
			luna=2
      #prisma - Делит введеный IP на первые три сектора
			prisma=$(echo "$3" | awk '{ split( $0 ,port,"."); print port[1]"."port[2]"."port[3]"."}')
			echo -e "#\n#\n\nsource /etc/network/intefaces.d/*\n\n#The loopback network interface\nauto lo\niface lo inet loopback\n" > /etc/network/interfaces
			echo -e "auto eth0\niface eth0 inet static\n     address $prisma$luna\n     netmask 255.255.255.0\n     gateway $3\n" >> /etc/network/interfaces
			for i in 1 2 3
			do
				luna=$[$luna+1]
				echo -e "auto eth$i\niface eth$i inet static\n     address $prisma$luna\n     netmask 255.255.255.0\n" >> /etc/network/interfaces
			done
			ip addr flush label eth*
			systemctl restart networking.service
      #Проверка, запустился ли сервис, макс время ожидания - 5 мин, интервал проверки - 20 сек
      i=0
      while true
      do
        ((i++))
        echo "attempt $i"
        sleep 20s
        status=$(systemctl is-active networking.service)
        if [ $status == "active" ]
        then
          echo -e "Настройки сетевых интерфейсов для сети $2 успешно установлены. Сеть готова к эксплуатации."
          break
        fi
        if [ $i -ge 15 ]
        then
          echo -e "Сервис networking.service не может запуститься на протяжении 5 минут."
          exit 1
        fi
      done
      exit 0
    #Если сеть не была указана  
		else
			echo -e "Скрипт был запущен с аргументом $1, однако была указана неверная сеть.\nУказано: $2\nВозможные аргументы: \n\t-10th \n\t-20th\n"
      exit -1
		fi
		;;
 	-iso)
    #Установка локального репозитория
    repo_mount mounted-main-leningrad.iso local_repo 
		echo -e "Локальный репозиторий установлен и готов к эксплуатации"
    exit 0
		;;
	-2upd)
    #Обновление 2
    repo_mount repository-update-2-version-2.iso upd_2
    repo_main $2
		echo -e "2-update успешно подключен введите:\napt dist-upgrade"
    exit 0
		;;
	-3upd)
    #Обновление 3
    repo_mount update-3-main-leningrad.iso upd_3
    repo_main $2
    apt install astra-update -y
		echo -e "3-й update успешно подлючен введите :\nastra-update -A -r -T"
    exit 0
		;;
  -clean)
    #Принудительная чистка после исполнения скрипта
    clean_file local_repo
    clean_file upd_3
    clean_file upd_2
    #Очистка настроек сетевых интерфейсов
    back_file /etc/network/ interfaces.old interfaces
    back_file /etc/apt/ sources.list.old sources.list
    echo -e "Успешно очищено"
    exit 0
    ;;
	-repo)
    #Установка репозитория
		if [ $2 == "-10th" ]
		then
				echo -e "deb http://10.20.13.120/repo/leningrad/mounted-iso-main leningrad main contrib non-free" > /etc/apt/sources.list
				echo -e "deb http://10.20.13.120/repo/leningrad/mounted-iso-devel leningrad main contrib non-free" >> /etc/apt/sources.list
				echo -e "deb http://10.20.13.120/repo/leningrad/repository-update-actual-dev leningrad main contrib non-free" >> /etc/apt/sources.list
				echo -e "deb http://10.20.13.120/repo/leningrad/repository-update-actual leningrad main contrib non-free" >> /etc/apt/sources.list
        exit 0
		else
				echo -e "deb http://$2/repo/leningrad/main leningrad main contrib non-free" > /etc/apt/sources.list 
				echo -e "deb http://$2/repo/leningrad/devel leningrad main contrib non-free" >> /etc/apt/sources.list
				echo -e "deb http://$2/repo/leningrad/update-actual-dev leningrad main contrib non-free" >> /etc/apt/sources.list
				echo -e "deb http://$2/repo/leningrad/update-actual leningrad main contrib non-free" >> /etc/apt/sources.list
        exit 0
		fi
		;;
	*)
		echo -e "Скрипт был запущен с неверным аргументом.\nУказано: $1\nВозможные аргументы: \n\t-help \n\t-eth \n\t-iso \n\t-2upd \n\t-3upd \n\t-clean \n\t-repo"
    echo -e "ЕСЛИ ВЫ ИМЕЕТЕ ДЕЛО СО СКРИПТОМ ВПЕРВЫЕ, ИЗУЧИТЕ sudo ./suns.sh -help"
    exit -1
		;;
esac