
#!/usr/bin/python3
import sys
from datetime import datetime

target = open('/home/jeff/hello.txt','a')
target.truncate()
date = datetime.now()
target.write("hello at " + str(date) + "\n")
target.close()
