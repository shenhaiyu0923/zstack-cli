import threading
import time

def threadinc_create(target,*args):
    t = threading.Thread(target=target, *args)
    t.start()
    t.join()

def aaa(a,b,c):
    time.sleep(4)
    print(a+b+c)
    return a+b+c

def bbb(a,b,c,d):
    time.sleep(2)
    print(a+b+c+d)
    return a+b+c+d

threadinc_create(aaa,(1,2,3))