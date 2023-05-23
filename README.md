## Specifiche
   Per le specifiche leggere il file Traccia.md

## Avviare il progetto

 clone/download the project and open a terminal, type: 
 ```cd <project folder>```
 create the virtual env
 ```python3 -m venv venv```
 activate it
 ```source venv/bin/activate```
 install the dependencies
 ```pip install -r requirements.txt```
 run the application
 ```cd demo```
 ```flask run -p 30123```
 Now the application is running
 then go to : `http://127.0.0.1:30123/docs` to access the swagger of APIFLASK

from here you can test the api built clicking the `try out` button

for pushing a notification try the api: ```/push```
you can check the result thanks to the other api provided 


## Testing 
from the project root folder open a terminal and type: 
```pytest```

as you can see all 8 test passed
