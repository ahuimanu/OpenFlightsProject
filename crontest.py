
#!/usr/bin/python3
import sys
from datetime import datetime

target = open('/home/<your_user_name_here>/hello.txt','a')
target.truncate()
date = datetime.now()
target.write("hello at " + str(date) + "\n")
target.close()
