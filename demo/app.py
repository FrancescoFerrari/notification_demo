# -*- coding: utf-8 -*-
import logging

from apiflask import APIFlask

from demo.db.database import Database

# blueprints
from demo.notifications.endpoint import notification_bp


# app factory 
def create_app():
    app = APIFlask(__name__)    
    app.register_blueprint(notification_bp)
    # init Db
    db = Database()
    return app


app = create_app()



logging.basicConfig(filename='notification.log',
                    level=logging.DEBUG, 
                    format='[' + __name__ + '][%(asctime)s][%(levelname)s]: %(message)s')


