# PyLS30
Python Tools and Libraries to control LifeSOS LS-30 home security appliance via TCP/IP and WEB

Project is in active development so not that many things really work.

Currently available:
* Simple WEB interface
* Event browser
* Sensor devices list

## What do I need to begin?
First, you need LifeSOS LS-30 security system. If you do not own one, this software makes no sense for you at all.

Second, you need to purchase a special module for LifeSOS LS-30 which will expose LS-30's built-in RSR232 COM-port via TCP protocol. Its model name is BF-450 and it is availble in same stores that sell LifeSOS LS-30 as well.

## How to make PyLS30 working?
Grab the source code from Github:
```
git clone https://github.com/rpavlyuk/PyLS30.git
```
Install additional modules that PyLS30 requires to run:
```
sudo easy_install bottle pyserial
```
Open file `./LS30Util/Config.py` and set the variable `ls30_socket_url` to propper value. For example: 
```python
ls30_socket_url = "socket://192.168.1.220:1681"
```
Start `PyLS30` webserver:
```
python ./tools/webserver.py
```
Open URL http://localhost:8080/ and enjoy!

## Notes
* There is no security implemented yet, so beware -- do not expose this service externally.
* This software will not work if you have your LS-30 setup to require a password for RSR232 communication.
* 

## See also
* http://www.scientech.co - a manufacturer of LifeSOS LS-30
* http://www.scientech.co/HyperSecureWeb/showproductdetail.action?product.id=21 - BF-450 module
* https://github.com/nickandrew/LS30 - PERL library for LS-30

