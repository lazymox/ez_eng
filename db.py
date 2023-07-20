import datetime
import json
from json import dumps
from datetime import *
import mysql.connector
from config import host, user, password, db_name
import re
import dateutil.parser as parser
import locale

locale.setlocale(locale.LC_ALL, "Russian")
try:
    connection = mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
    )
    cursor = connection.cursor()
    print("База данных спарилась с ботом успешно")
except Exception as ex:
    print('У базы данных болит голова(')


class Database:
    def user_exists(self, user_id):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = '{}'".format(user_id))
        result = cursor.fetchmany(1)
        connection.close()
        return bool(len(result))

    # except ex:
    # print("ошибка", ex)

    def first_add(self, user_id):
        try:
            connection.ping(reconnect=True)
        except mysql.connector.Error as ex:
            print("Error while reconnecting to the database:", ex)
            return

        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (user_id) VALUES (%s)", (user_id,))
            connection.commit()
        except mysql.connector.Error as ex:
            print("Error while executing the query:", ex)
        finally:
            cursor.close()

    # except ex:
    # print("ошибка1", ex)

    def get_user_ids(self):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE subscription = TRUE AND level IS NOT NULL")
        result = [row[0] for row in cursor.fetchall()]
        connection.close()
        return result

    def get_users_name(self):
        try:
            connection.ping()
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("SELECT fio FROM users")
        result = cursor.fetchall()
        connection.close()
        return result

    def get_fio(self, user_id):
        try:
            connection.ping()
        except:
            pass
        cursor = connection.cursor()
        cursor.execute(f"SELECT fio FROM users WHERE user_id = {user_id}")
        result = cursor.fetchone()
        connection.close()
        return result

    def set_fio(self, user_id, fio):
        try:
            connection.ping(reconnect=True)
        except:
            pass

        cursor = connection.cursor()
        cursor.execute("UPDATE users SET fio = %s WHERE user_id = %s", (fio, user_id))
        connection.commit()
        connection.close()

    def check_sub(self, user_id):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("SELECT subscription FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result

    # TESTBASE
    def get_passed(self, user_id):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("SELECT passed FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result

    def upd_passed(self, user_id, passed):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET passed = %s WHERE user_id = %s", (passed, user_id))
        connection.commit()
        connection.close()

    def get_process(self, user_id):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("SELECT process FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result

    def upd_process(self, user_id, process):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET process = %s WHERE user_id = %s", (process, user_id))
        connection.commit()
        connection.close()

    def get_msg(self, user_id):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("SELECT msg FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result

    def upd_msg(self, user_id, msg):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET msg = %s WHERE user_id = %s", (msg, user_id))
        connection.commit()
        connection.close()

    def get_level(self, user_id):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("SELECT level FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result

    def upd_level(self, user_id, level):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET level = %s WHERE user_id = %s", (level, user_id))
        connection.commit()
        connection.close()

    # DAILY MAILING
    def get_leveling(self, user_id):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("SELECT leveling_process FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result

    def upd_leveling(self, user_id, leveling):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET leveling_process = %s WHERE user_id = %s", (leveling, user_id))
        connection.commit()
        connection.close()

    def get_coin(self, user_id):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("SELECT coin FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result

    def upd_coin(self, user_id, coin):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET coin = %s WHERE user_id = %s", (coin, user_id))
        connection.commit()
        connection.close()

    # получение данных пользователя
    def get_full_info(self, user_id):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute(f"SELECT fio,level,subscription,coin,reg_date,end_date  FROM  users WHERE user_id={user_id} ")
        result = cursor.fetchone()
        connection.close()
        return result

    def get_subscritions_time(self):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute(f"SELECT reg_date,end_date,user_id  FROM  users where subscription=1")
        result = cursor.fetchall()
        connection.close()
        return result

    def give_subscription(self, user_id, months):
        end_day = datetime.now() + timedelta(days=30 * months)
        sql = f"UPDATE users SET reg_date = '{datetime.now().strftime('%Y-%m-%d')}', end_date='{end_day.strftime('%Y-%m-%d')}' WHERE user_id ={user_id}"

    def remove_subscrition(self, user_id):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute(f"UPDATE users set subscription=0 where WHERE user_id = {user_id} ")

    def get_try(self, user_id):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("SELECT try FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result

    def upd_try(self, user_id, tries):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET try = %s WHERE user_id = %s", (tries, user_id))
        connection.commit()
        connection.close()

    def get_all_users():

        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor(dictionary=True)  # этот аргумент просто имба
        cursor.execute('SELECT user_id,fio,subscription,reg_date,end_date FROM users')
        result = cursor.fetchall()
        return result

    def update_data(data: [], table):

        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        match table:
            case 'users':
                for x in data:
                    cursor.execute(
                        'UPDATE users SET fio=%s , subscription=%s, reg_date=%s,end_date=%s where user_id=%s',
                        (x['fio'], x['subscription'],
                         datetime.fromisoformat(parser.parse(x['reg_date']).isoformat()).strftime('%Y-%m-%d'),
                         datetime.fromisoformat(parser.parse(x['end_date']).isoformat()).strftime('%Y-%m-%d'),
                         x['user_id']))
            case 'completed':
                for x in data:
                    cursor.execute(
                        f'UPDATE completed set checked={x["checked"]},answer="{x["answer"]}" where user_id={x["user_id"]}')


    def delete_user(user_ids, table):
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor()
        for x in user_ids:
            cursor.execute(f'DELETE FROM {table} WHERE user_id = {x} LIMIT 1;')

    def get_completed_data():
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor(dictionary=True)  # этот аргумент просто имба
        cursor.execute('SELECT * FROM completed')
        result = cursor.fetchall()
        return result

    def get_payments():
        try:
            connection.ping(reconnect=True)
        except:
            pass
        cursor = connection.cursor(dictionary=True)  # этот аргумент просто имба
        cursor.execute('SELECT * FROM payments order by user_id')
        result = cursor.fetchall()

        print(result)
        return result
    def insert_payments(data):
        try:
            cursor.execute(f"INSERT INTO payments (user_id, fio, payment_data) VALUES ({data[0]},{data[1]},{data[2]})")
            connection.commit()
        except mysql.connector.Error as ex:
            print("Error while executing the query:", ex)
        finally:
            cursor.close()
    def insert_complited(data):
        try:
            cursor.execute(f"INSERT INTO completed (user_id, fio, phone_number, checked, answer) VALUES ({data[0]},{data[1]},{data[2]})")
            connection.commit()
        except mysql.connector.Error as ex:
            print("Error while executing the query:", ex)
        finally:
            cursor.close()