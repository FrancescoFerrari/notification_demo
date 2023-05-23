import logging

def get_customer_id_from_notification_body(list_customer_label_id, notification_body):
    customer_id = None
    conflict = False
    customer_label_dict = {notify_id[0].lower() :notify_id[1] for notify_id in list_customer_label_id}
    for customer_label in customer_label_dict:
        if customer_label in notification_body:
            if customer_id:
                logging.debug(f"CONFLICT: {customer_label} of the customer's Id:{customer_label_dict[customer_label]}  \
                                already found also in the customer ID:{customer_id}")
                conflict = True
            else:    
                customer_id = customer_label_dict[customer_label]
                logging.info(f"Customer ID:{customer_id}, found for the label {customer_label}")
                
    return customer_id, conflict 


def get_customer_id_conflict(db, body_str):
     # first find the customer finding the notification_label in the body_str
    all_list_customer_label_id = db.get_all_notification_label()
    logging.info(all_list_customer_label_id)
    
    customer_id, conflict = get_customer_id_from_notification_body(all_list_customer_label_id, body_str.lower())

    return customer_id if not conflict else None, conflict