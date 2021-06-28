# NetDog

A simple tool as same as NetCat

# Usage

```
NetDog 1.0(http://www.e-wolf.top)
Usage:python3 netdog.py [options]

Client Option List
     -h host   set remote host
     -p port   set romote port
     -f /file  set local file location(Optional)
     
Server Option List
     -l port   set listen mode open and appoint port
     -f /file  set recieve file location(Optional)
     
Util Option List
     -scan        check the remote port status
     	-h        set target ip
     	-p        set target port(format:[1-200],[1,2,3,11])
     -shell       get the system shell



Example:

Connect to somewhere:
python3 netdog.py -h 10.1.1.1 -p 123

run as a server:
python3 netdog.py -l 123
```

