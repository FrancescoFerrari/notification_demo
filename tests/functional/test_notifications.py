
from datetime import datetime
import os
import time
from demo.notifications.model import NewNotificationCostants
from demo.db.database import Database


BASE_URL = "http://127.0.0.1:5000"

first_three_customers = [
    [ 
      1,
      "Yvonne Nash",
      "Los Angeles"
    ],
    [
      2,
      "Justin Wright",
      "Jeddah"
    ],
    [
      3,
      "Thomas Hamilton",
      "Bangkok"
    ],]


def test_create_db(client):
    if os.path.isfile(os.path.join(os.getcwd(), "database.db")):
        os.remove(os.path.join(os.getcwd(), "database.db"))
    db = Database.instance
    db._create_connection()
    
    assert os.path.isfile(os.path.join(os.getcwd(), "database.db")) == True
    
    # check if the customers table is created 
    response = client.get(BASE_URL + "/customers")
    assert len(response.json[NewNotificationCostants.CUSTOMERS]) > 1 
    assert response.json[NewNotificationCostants.CUSTOMERS][:3] ==  first_three_customers
    
    # check if the notification table is created and empty
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 0 
    assert response.json[NewNotificationCostants.NOTIFICATION] ==  []
    
    # check if the notification counters table is created and empty
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 0
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  []
    
    
def test_get_customers(client):
    response = client.get(BASE_URL + "/customers")
    assert len(response.json[NewNotificationCostants.CUSTOMERS]) > 1 
    assert response.json[NewNotificationCostants.CUSTOMERS][:3] ==  first_three_customers
    

def test_push_notification_first_time(client):
    test_create_db(client)
    # check if the notification table is empty
    response = client.get(BASE_URL + "/notifications")
    response_notification = response.json[NewNotificationCostants.NOTIFICATION]
    assert len(response_notification) == 0 
    assert response_notification ==  []
    
    # check if the notification counters table is  empty
    response = client.get(BASE_URL + "/notifications_counters")
    response_counter = response.json[NewNotificationCostants.NOTIFICATION_COUNTER]
    assert len(response_counter) == 0
    assert response_counter ==  []
    
    payload = {NewNotificationCostants.BODY: 'LOS ANGELES, NOISE TEXTTTTTTTTTT'}
    
    response = client.post(BASE_URL + "/push", json=payload)
    
    assert response.json[NewNotificationCostants.RESPONSE] == 200 
    assert response.json[NewNotificationCostants.MESSAGE] == 'notification pushed'
    
    time.sleep(1)
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 1 
    assert response.json[NewNotificationCostants.NOTIFICATION] ==  [[1, 'LOS ANGELES, NOISE TEXTTTTTTTTTT', 1]]
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 1 
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  [[1, 1, datetime.now().day]]    
    
   
def test_push_notification_more_than_one_customer(client):
    test_create_db(client)
    # check if the notification table is empty
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 0 
    assert response.json[NewNotificationCostants.NOTIFICATION] ==  []
    
    # check if the notification counters table is  empty
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 0
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  []
    
    payload_1 = {NewNotificationCostants.BODY: 'LOS ANGELES, NOISE TEXTTTTTTTTTT'}
    response = client.post(BASE_URL + "/push", json=payload_1)
    
    assert response.json[NewNotificationCostants.RESPONSE] == 200 
    assert response.json[NewNotificationCostants.MESSAGE] == 'notification pushed'
    
    time.sleep(1)
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 1 
    assert response.json[NewNotificationCostants.NOTIFICATION] ==  [[1, 'LOS ANGELES, NOISE TEXTTTTTTTTTT', 1]]
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 1 
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  [[1, 1, datetime.now().day]]

    payload_2 = {NewNotificationCostants.BODY: ' NOISE TEXTTTTTTTTTT JeDdaH '}
    response = client.post(BASE_URL + "/push", json=payload_2)
    
    assert response.json[NewNotificationCostants.RESPONSE] == 200 
    assert response.json[NewNotificationCostants.MESSAGE] == 'notification pushed'
    
    time.sleep(1)
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 2 
    assert response.json[NewNotificationCostants.NOTIFICATION] == [[1, 'LOS ANGELES, NOISE TEXTTTTTTTTTT', 1], [2, ' NOISE TEXTTTTTTTTTT JeDdaH ', 2]]
    
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 2 
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  [[1, 1, datetime.now().day], [2, 1, datetime.now().day]]
       
  
def test_push_two_notification_same_customer(client):
    test_create_db(client)
    # check if the notification table is empty
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 0 
    assert response.json[NewNotificationCostants.NOTIFICATION] ==  []
    
    # check if the notification counters table is  empty
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 0
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  []
    
    payload_1 = {NewNotificationCostants.BODY: 'LOS ANGELES, NOISE TEXTTTTTTTTTT'}
    response = client.post(BASE_URL + "/push", json=payload_1)
    
    assert response.json[NewNotificationCostants.RESPONSE] == 200 
    assert response.json[NewNotificationCostants.MESSAGE] == 'notification pushed'
    
    time.sleep(1)
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 1 
    assert response.json[NewNotificationCostants.NOTIFICATION] ==  [[1, 'LOS ANGELES, NOISE TEXTTTTTTTTTT', 1]]
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 1 
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  [[1, 1, datetime.now().day]]

    payload_2 = {NewNotificationCostants.BODY: 'Noise noise noise JetNo Los angeLES, NOISE'}
    response = client.post(BASE_URL + "/push", json=payload_2)
    
    assert response.json[NewNotificationCostants.RESPONSE] == 200 
    assert response.json[NewNotificationCostants.MESSAGE] == 'notification pushed'
    
    time.sleep(1)
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 2 
    assert response.json[NewNotificationCostants.NOTIFICATION] == [[1, 'LOS ANGELES, NOISE TEXTTTTTTTTTT', 1], [2, 'Noise noise noise JetNo Los angeLES, NOISE', 1]]
    
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 1 
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  [[1, 2, datetime.now().day],]
    
       
def test_trim_payload_more_than_300_char(client):
    test_create_db(client)
    # check if the notification table is empty
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 0 
    assert response.json[NewNotificationCostants.NOTIFICATION] ==  []
    
    # check if the notification counters table is  empty
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 0
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  []
    
    str_too_big = 'Los Angeles'.join(f'{i}' for i in range (0,500) )
    payload_1 = {NewNotificationCostants.BODY: str_too_big}
    response = client.post(BASE_URL + "/push", json=payload_1)
    
    assert response.json[NewNotificationCostants.RESPONSE] == 200 
    assert response.json[NewNotificationCostants.MESSAGE] == 'notification pushed'
    
    time.sleep(1)
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 1 
    assert len(response.json[NewNotificationCostants.NOTIFICATION][0][1]) == 300 
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 1 
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  [[1, 1, datetime.now().day]]



     
def test_more_than_one_customer_in_notification(client):
    test_create_db(client)
    # check if the notification table is empty
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 0 
    assert response.json[NewNotificationCostants.NOTIFICATION] ==  []
    
    # check if the notification counters table is  empty
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 0
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  []
    
    payload_1 = {NewNotificationCostants.BODY: 'Jeddah, los angeles'}
    response = client.post(BASE_URL + "/push", json=payload_1)
    
    assert response.json[NewNotificationCostants.RESPONSE] == 200 
    assert response.json[NewNotificationCostants.MESSAGE] == 'notification pushed'
    
    time.sleep(1)
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 1 
    assert response.json[NewNotificationCostants.NOTIFICATION] ==  [[1, 'Jeddah, los angeles', None]]
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 0
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  []
    
          
def test_no_customer_found(client):
    test_create_db(client)
    # check if the notification table is empty
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 0 
    assert response.json[NewNotificationCostants.NOTIFICATION] ==  []
    
    # check if the notification counters table is  empty
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 0
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  []
    
    payload_1 = {NewNotificationCostants.BODY: 'Jeddih, los Engeles'}
    response = client.post(BASE_URL + "/push", json=payload_1)
    
    assert response.json[NewNotificationCostants.RESPONSE] == 500 
    assert response.json[NewNotificationCostants.MESSAGE] == 'customer_id not found for the notification body provided'
    
    time.sleep(1)
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications")
    assert len(response.json[NewNotificationCostants.NOTIFICATION]) == 0 
    assert response.json[NewNotificationCostants.NOTIFICATION] ==  []
    
    # check if the notification table is now updated with the new notification
    response = client.get(BASE_URL + "/notifications_counters")
    assert len(response.json[NewNotificationCostants.NOTIFICATION_COUNTER]) == 0
    assert response.json[NewNotificationCostants.NOTIFICATION_COUNTER] ==  []
    
      