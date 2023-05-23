from apiflask import Schema
from apiflask.fields import Integer, String, Nested, List
from apiflask.validators import Length



class NewNotificationRequest(Schema):
    body = String(required=True)


class NewNotificationCostants():
    BODY = 'body'
    CUSTOMERS = 'customers'
    NOTIFICATION = 'notifications'
    NOTIFICATION_COUNTER = 'notification_counter'
    RESPONSE = 'response'
    ERROR = 'error'
    MESSAGE = 'message'