# Luxafor Pomodoro team status changer


Reads current pomodoro status from [Pomodoro timer](https://luxafor.dk/luxafor-brugerdefineret-led-pomodoro-timer/) and sends the availability status to Microsoft Teams

###  Setup 
```
$ pip install -r requirements.txt 
$ cp .env.example .env 
# Fetch auth token from https://teams.microsoft.com/go# and add it to .env
$ python main.py 
```
