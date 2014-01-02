Projekt Candela
-----------------------
Candela to open source'owy portal społecznościowy, przeznaczony w szczególności dla studentów Wydziału Fizyki PW.


Zależności:
* Python 2.7+
* Virtualenv
* Flask + biblioteki (podane niżej)
* Sqlite3

Uruchomienie:
	Będąc w folderze Candela:
	1. Instalacja virtualenv z https://raw.github.com/pypa/virtualenv/1.9.X/virtualenv.py
		python virtualenv.py flask
	2. Instalacja paczek:
		flask/bin/pip install flask==0.9
		flask/bin/pip install flask-login
		flask/bin/pip install flask-openid
		flask/bin/pip install flask-mail==0.7.6
		flask/bin/pip install sqlalchemy==0.7.9
		flask/bin/pip install flask-sqlalchemy==0.16
		flask/bin/pip install sqlalchemy-migrate==0.7.2
		flask/bin/pip install flask-whooshalchemy==0.54a
		flask/bin/pip install flask-wtf==0.8.4

Przewidywany start portalu: pierwszy kwartał roku 2014
