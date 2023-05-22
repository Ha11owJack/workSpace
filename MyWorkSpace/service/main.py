# -*- coding: utf-8 -*-
import psycopg2
from time import sleep
import datetime
import os
import subprocess

class Database:
    resurce_array = [
            "User",
            " ",
            "Configuration of Zabbix",
            "Media type",
            "Host",
            "Action",
            "Graph",
            "Graph element",
            "",
            "",
            "",
            "User group",
            "Application",
            "Trigger",
            "Host group",
            "Item",
            "Image",
            "Value map",
            "Service",
            "Map",
            "Screen",
            "",
            "Web scenario",
            "Discovery rule",
            "Slide show",
            "Script",
            "Proxy",
            "Maintenance",
            "Regular expression",
            "Macro",
            "Template",
            "Trigger prototype",
            "Icon mapping",
            "Dashboard",
            "Event correlation",
            "Graph prototype",
            "Item prototype",
            "Host prototype",

    ]

    def __init__(self):
        try:
            self.conn = psycopg2.connect(dbname=self.db_acs("db"), user=self.db_acs("login"),
                                         password=self.db_acs("pass"),host='localhost')
        except:
             print("Ошибка перенаправлена в syslog")
             with open("/var/log/syslog", 'a') as l:
                  l.write("___________\nZabbix-log: База данных недоступна\n___________\n")
                  l.close()
        self.cursor = self.conn.cursor()

    def db_acs(self, name):
	if name == "login":
                message = subprocess.check_output("grep '^DBUser=' /etc/zabbix/zabbix_server.conf | awk '{split($0, array,/\=/); print array[2]}'", shell=True).split('\n')[0]
        elif name == "pass":
                message = subprocess.check_output("grep '^DBPassword=' /etc/zabbix/zabbix_server.conf | awk '{split($0, array,/\=/); print substr(array[2],2, length(array[2])-2)}'", shell=True).split('\n')[0]
        elif name == "db":
                message = subprocess.check_output("grep '^DBName=' /etc/zabbix/zabbix_server.conf | awk '{split($0, array,/\=/); print array[2]}'", shell=True).split('\n')[0]
        return message

    def logging_reform(self, number):
        message = subprocess.check_output("awk '/last_log/{print $2}' /usr/local/bin/status.conf", shell=True).split('\n')[0]
        os.system("sed -i 's/last_log[[:space:]]" + str(message) + "/last_log\t" + str(number) + "/' /usr/local/bin/status.conf")

    def logging_check(self):
        message = subprocess.check_output("awk '/last_log/{print $2}' /usr/local/bin/status.conf", shell=True).split('\n')[0]
        return message

    def string_remove(self, number):
        item = ""
        i = 0
        self.cursor.execute("SELECT * FROM auditlog where auditid > " + str(number) + ";")
        information = self.cursor.fetchall()
        print(bool(len(information[0])))
        for info in information:
            item += "_______\nzabbix.log@\n[" + str(datetime.datetime.fromtimestamp(info[2])) + ", " + str(info[0]) + " ] " +  str(self.audit_action(info[3])) + ": " + str(self.resurce_array[info[4]]) + ",    Source Name: " + \
                     str(info[8]) + ",    User Name: " + str(self.user_id(info[1])) + ",    ip: " +  str(info[6]) + \
                     ",    resourceid: " + str(info[7]) + "    " + str(info[5]) + "\n_______\n"
        return item

    def last_id(self):
        query = "SELECT MAX(auditid) FROM auditlog;"
        self.cursor.execute(query)
        information = self.cursor.fetchone()
        return information[0]


    def user_id(self, id):
        query = "SELECT * FROM users WHERE userid = %s;"
        self.cursor.execute(query, [id])
        information = self.cursor.fetchall()
        return information[0][1]

    def audit_action(self, message):
        if message == 0:
            return "Added"
        elif message == 1:
            return "Updated"
        elif message == 2:
            return "Deleted"
        elif message == 3:
            return "Login"
        elif message == 4:
            return "Logout"
        elif message == 5:
            return "Enabled"
        elif message == 6:
            return "Disabled"
        else:
            return "Unknown action"

    def inform_data(self):
        start_string = self.last_id()
        if self.logging_check() == "null":
            pass
        elif int(self.logging_check()) < start_string:
           start_string = int(self.logging_check())
           print(type(start_string))
        else:
           print("WOW")
        for _ in iter(int, 1):
            sleep(5)
            last_string = self.last_id()
            if start_string < last_string:
                print(self.string_remove(start_string))
                start_string = last_string
#            elif last_string < start_string:
#                start_string = last_string

    def status_conf(self, info):
        if not bool(os.system("grep 'Status' /usr/local/bin/status.conf | grep -q " + info)):
            return True
        else:
            return False

    def data_insert(self):
        start_string = self.last_id()
        if self.logging_check() == "null" or int(self.logging_check()) == start_string:
            pass
        elif int(self.logging_check()) < start_string or int(self.logging_check()) > start_string:
           start_string = int(self.logging_check())
        else:
           print("Ошибка перенаправлена в syslog")
           with open("/var/log/syslog", 'a') as l:
                l.write("___________\nZabbix-log: Неверная нумерация в last_log в .conf файле\n___________\n")
                l.close()
                exit()
        for _ in iter(int, 1):
            sleep(5)
            last_string = self.last_id()
            if self.status_conf("loop"):
                if start_string < last_string:
                    with open("/var/log/syslog", 'a') as f:
                         f.write(self.string_remove(start_string))
                         f.close()
                    self.logging_reform(last_string)
                    start_string = last_string
                elif last_string < start_string:
                    start_string = last_string
            elif self.status_conf("stop"):
                with open("/var/log/syslog", 'a') as l:
                     l.write("___________\nZabbix-log: Остановил работу\n___________\n")
                     l.close()
                break
            else:
                print("Ошибка перенаправлена в syslog")
                with open("/var/log/syslog", 'a') as l:
                     l.write("___________\nZabbix-log: Неправильная запись данных в .conf файле - нарушение работы записи цикла\n___________\n")
                     l.close()
                break
        exit()

Database().data_insert()
#Database().inform_data()


#Database().logging_reform(3)
