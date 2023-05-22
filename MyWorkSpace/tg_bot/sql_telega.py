import MySQLdb


class Database:
    def __init__(self):
        self.db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                                  user="Nikita_admin",  # your username
                                  passwd="311098ASDFzxc",  # your password
                                  db="telegram")
        self.cur = self.db.cursor()

    # def info_output(self):
    #     self.cur.execute("select * from user_tele")
    #     for row in self.cur.fetchall():
    #         print(row)
    #     self.db.close()
    #     return row

    def user_found(self, user_id):
        self.cur.execute("select * from user_tele where user_id = %s", [user_id])
        information = self.cur.fetchall()
        return bool(len(information))

    def user_id_found(self, user_id):
        self.cur.execute("select * from user_tele where id = %s", [user_id])
        information = self.cur.fetchall()
        return bool(len(information))

    def update_user(self, login, passw, user_id):
        self.cur.execute("update user_tele set login = %s, pass = $s where id = %s;", [login, passw, user_id])
        self.db.commit()

    def user_protect(self, user_id):
        self.cur.execute("select admin from user_tele where id = %s", [user_id])
        information = self.cur.fetchall()
        admin_id = []
        for info in information:
            admin_id = info
        return admin_id

    def user_log(self, user_login, user_id):
        self.cur.execute("select * from user_tele where login = %s and user_id = %s", [user_login, user_id])
        information = self.cur.fetchall()
        return bool(len(information))

    def web_found(self, user_login, user_id):
        self.cur.execute("select * from user_tele where hook = %s and user_id = %s", [user_login, user_id])  # >>

    def set_web(self, user_login, user_id):
        self.cur.execute("select * from user_tele where login = %s and user_id = %s", [user_login, user_id])  # >>

    def delete_web(self, user_login, user_id):
        self.cur.execute("select * from user_tele where login = %s and user_id = %s", [user_login, user_id])  # >>

    def user_pass(self, user_pw, user_id):
        self.cur.execute("select * from user_tele where pass = %s and user_id = %s", [user_pw, user_id])
        information = self.cur.fetchall()
        return bool(len(information))

    def add_user(self, login, password, username, date, is_admin, user_id):
        self.cur.execute(
            "insert into user_tele(login,pass,username, registrated,admin,user_id) values (%s,%s,%s,%s,%s,%s)",
            [login, password, username, date, is_admin, user_id]) #Добавить хук + статус хука
        self.db.commit()

    def show_users(self):
        self.cur.execute("select id,username,registrated,admin from user_tele")
        information = self.cur.fetchall()
        return information

    # Сделать удаление юзера по id
    def delete_user(self, user_id):
        try:
            self.cur.execute("delete from user_tele where id = %s", [user_id])
            self.cur.execute("ALTER TABLE user_tele DROP id;)")
            # # ALTER TABLE user_tele AUTO_INCREMENT = 1; ALTER TABLE user_tele ADD id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;")
            self.cur.execute("ALTER TABLE user_tele AUTO_INCREMENT = 1;")
            self.cur.execute("ALTER TABLE user_tele ADD id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;")
            self.db.commit()
        except:
            self.cur.execute("ALTER TABLE user_tele ADD id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;")

    def user_info(self, user_name):
        self.cur.execute("select * from user_tele where name = %s", [user_name])
        information = self.cur.fetchall()
        return information

    def is_admin(self, user_id):
        self.cur.execute("select * from user_tele where user_id = %s and admin = 1", [user_id])
        information = self.cur.fetchall()
        return bool(len(information))

    def list_user(self):
        self.cur.execute("select user_id from user_tele where admin = 0")
        information = self.cur.fetchall()
        info = []
        for i in information:
            info += i
        return info

    def list_admin(self):
        self.cur.execute("select user_id from user_tele where admin = 1")
        information = self.cur.fetchall()
        info = []
        for i in information:
            info += i
        return info

# Добавить в базу данных id пользователя которое будет инкрементируемо и фиксирует изменения в таблицу.
# Добавить логирование пользователя.
# Структура БД - id, login, pass, username, date, hook, status_hook
