
from datetime import datetime
import sqlite3
from sqlite3 import Error
import logging
import os.path

from demo.notifications.utils import get_customer_id_from_notification_body


class Database():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
            return cls.instance
        
    def __init__(self):
        self.db_file_path = "database.db"
        self._create_connection()

    
    def _create_connection(self):
        """ create a database connection to a SQLite database """
        con = None
        try:
         #  pass if db file already exist
            if os.path.isfile(self.db_file_path):
                pass
                
            con = sqlite3.connect(self.db_file_path)
            print(sqlite3.version)
            cur = con.cursor()
                        
            # new db
            cur.execute("CREATE TABLE customers ( \
                        id INTEGER PRIMARY KEY, \
                        name TEXT NOT NULL, \
                        notification_label TEXT NOT NULL UNIQUE \
                        );")
            cur.execute("CREATE TABLE notifications ( \
                        id INTEGER PRIMARY KEY AUTOINCREMENT, \
                        body TEXT NOT NULL, \
                        id_customer INTEGER, \
                        FOREIGN KEY (id_customer) REFERENCES customers(id) \
                        );")
            cur.execute("CREATE TABLE notification_counters ( \
                        id_customer INTEGER NOT NULL, \
                        num INTEGER NOT NULL DEFAULT 0, \
                        day DATE NOT NULL, \
                        PRIMARY KEY (id_customer, day), \
                        FOREIGN KEY (id_customer) REFERENCES customers(id) \
                        );")       
            cur.execute("INSERT INTO customers VALUES \
                        (1, 'Yvonne Nash', 'Los Angeles'), \
                        (2, 'Justin Wright', 'Jeddah'), \
                        (3, 'Thomas Hamilton', 'Bangkok'), \
                        (4, 'Lily Lee', 'Casablanca'), \
                        (5, 'Angela Davies', 'Addis Ababa'), \
                        (6, 'Dan Skinner', 'Lahore'), \
                        (7, 'Dylan Butler', 'Kinshasa'), \
                        (8, 'Carl Reid', 'Dhaka'), \
                        (9, 'Jasmine Rampling', 'Karachi'), \
                        (10, 'Amelia Ross', 'Abidjan') \
                        ;")
            con.commit()
            
            con.close()
        
        except Error as e:
            print(e)
            
    
    def save_notification(self, body_str, customer_id):
        con = sqlite3.connect(self.db_file_path)
            
        try: 
            # post notification in the db
            self.insert_notification_record(con, body_str, customer_id)
            if customer_id:
                # update the notification counter in the db
                self.update_notification_counter(con, customer_id)

            con.commit()      
                    
        except Exception as e:
            logging.error(e)
            return e
        
        finally:
            if con:
                con.close()
                logging.info("Connection closed")
            
            
    def get_all_notification_label(self):
        connection = sqlite3.connect(self.db_file_path)
        query = ''' SELECT notification_label, id FROM customers ORDER BY id '''
        res = connection.cursor().execute(query)
        response = res.fetchall()
        logging.info('Query and resposnse as follow')
        logging.debug(response)
        connection.close()
        
        return response
    
    
    def insert_notification_record(self, connection, body_str, customer_id):
        query = ''' INSERT INTO notifications(body,id_customer) VALUES(?,?) '''
        values = (body_str, customer_id)
        cur = connection.cursor()
        cur.execute(query, values)
        logging.debug(query)
        logging.debug(values)
        
        
    def get_notification_counter(self, connection, customer_id):
        cur = connection.cursor()
        
        query = f''' SELECT * FROM notification_counters WHERE id_customer=?'''
        res = cur.execute(query, (customer_id, ))
        notification_counter = res.fetchone()
        logging.debug(query)
        logging.info("Notification to update")
        logging.debug(notification_counter)
        
        return notification_counter
    
    
    def update_notification_counter_record(self, connection, notification_2_update):
        query = ''' UPDATE notification_counters
                    SET num = ?,
                        day = ? 
                    WHERE id_customer = ?'''
        
        # 0: customer_id, 1: num, 2: day
        values = (notification_2_update[1] + 1, notification_2_update[2], notification_2_update[0])      
        cur = connection.cursor()  
        cur.execute(query, values)
        logging.debug(query)
        logging.debug(values)    
    
    
    def insert_notification_counter_record(self, connection, customer_id, today):
        query = ''' INSERT INTO notification_counters(id_customer, num, day) VALUES(?,?,?) '''
        values = (customer_id, 1, today)
        cur = connection.cursor()  
        cur.execute(query, values)
        logging.debug(query)
        logging.debug(values)    
        
              
    def update_notification_counter(self, connection, customer_id):
        today = datetime.now().day
        notification_2_update = self.get_notification_counter(connection, customer_id)
        
        if notification_2_update:
           self.update_notification_counter_record(connection, notification_2_update)
            
        else:
        # Insert value
            self.insert_notification_counter_record(connection, customer_id, today)   
            
    
    def get_all_notifications(self):
        connection = sqlite3.connect(self.db_file_path)
        cur = connection.cursor()
        
        query = ''' SELECT * FROM notifications ORDER BY id  '''
        res = cur.execute(query)
        response = res.fetchall()
        
        logging.debug(query)
        logging.debug(response)
        connection.close()
        return response
      
                
    def get_all_notification_counters(self):
        connection = sqlite3.connect(self.db_file_path)
        cur = connection.cursor()
        
        query = ''' SELECT * FROM notification_counters ORDER BY id_customer  '''
        res = cur.execute(query)
        response = res.fetchall()
        
        logging.debug(query)
        logging.debug(response)
        connection.close()
        return response
                 
            
    def get_all_customers(self):
        connection = sqlite3.connect(self.db_file_path)
        cur = connection.cursor()
        
        query = ''' SELECT * FROM customers ORDER BY id  '''
        res = cur.execute(query)
        response = res.fetchall()
        
        logging.debug(query)
        logging.debug(response)
        connection.close()
        return response
    
        