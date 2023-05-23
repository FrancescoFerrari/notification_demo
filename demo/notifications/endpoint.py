from datetime import datetime
import logging
from threading import Thread
from apiflask import APIBlueprint
from demo.db.database import Database

from demo.notifications.model import NewNotificationCostants, NewNotificationRequest
from demo.notifications.utils import get_customer_id_conflict


notification_bp = APIBlueprint('notification', __name__, url_prefix='/')


@notification_bp.post('/push')
@notification_bp.input(NewNotificationRequest)
def push_notification(data):
    """
    Method POST
    Servizio per raccogliere notifiche che sono stringhe di testo, 
    ogni connessione rappresenta una notifica (troncare a 300 caratteri massimo).
    Trovare a quale cliente appartiene la notifica in base a ricerca case insensitive di una label nel testo della notifica
    (tabella customers campo notification_label).
    Salvare la notifica su DB Sql con ID cliente di appartenenza.
    Incrementare contatore notifiche giornaliero per cliente.
    Il salvataggio della notifica e l'incremento del contatore devono essere eseguiti in modo atomico.
    ogni connessione deve durare il meno possibile e non dev'essere dipendente dai tempi di I/O wait del DB.
    """
    try:
        #  trim just first 300 char
        body_data = data[NewNotificationCostants.BODY][:300]    
        
        db = Database.instance
        #  get the customer_id and if there was a conflict 
        customer_id, conflict = get_customer_id_conflict(db, body_data)
        
        if not conflict and not customer_id:
            logging.error(f'No customrr_id_found, conflict:{conflict}, body: {body_data}')
            return {'response': 500, 'message': 'customer_id not found for the notification body provided'}    
  
            
        t = Thread(target=db.save_notification, args=[body_data, customer_id])
        t.start()
                
        return {'response': 200, 'message': 'notification pushed'}    
    
    except Exception as e:
        return {'response': 500,'error': e.args[0]}



@notification_bp.get('/notifications')
def get_all_notification():
    """ 
    Method GET
    Return all notification in the db
    """
    try:
        db = Database.instance
        
        notification_list = db.get_all_notifications()
        logging.info(f"Notification lists: {notification_list}")
        return {'notifications': notification_list}
    
    except Exception as e:
        return {'response': 500,'error': e.args[0]}


@notification_bp.get('/notifications_counters')
def get_all_notification_counter():
    """ 
    Method GET
    Return all notification counter in the db
    """
    try:
        db = Database.instance
        
        notification_counters_list = db.get_all_notification_counters()
        logging.info(f"Notification counters lists: {notification_counters_list}")
                
        return {'notification_counter': notification_counters_list}
    
    except Exception as e:
        return {'response': 500,'error': e.args[0]}


@notification_bp.get('/customers')
def get_all_customers():
    """ 
    Method GET
    Return all customers in the db
    """
    try:
        db = Database.instance
        
        customers_list = db.get_all_customers()
                
        return {'customers': customers_list}
    
    except Exception as e:
        return {'response': 500,'error': e.args[0]}
