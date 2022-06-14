# [CS118] Python Web Server
A simple web server with session-based authentication using Python http module.

## Requirements
This project requires Python 3.9+  
Since the server uses `bcrypt` for password hashing, please make sure you have this module installed as well.

## Configure
By default the server runs on `localhost:8080`, but you can change this configuration by editing `config.py` file.

### Warning
If you change the socket configuration, please update all the html pages too!
All static html pages are stored inside the `/pages` folder.

## Run the server
Move inside the project folder and run:

```
python main.py
```
Enjoy

# Author
[Luca Samorè](https://github.com/LucaSamore)
