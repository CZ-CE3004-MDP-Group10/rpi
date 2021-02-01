ANDROID_HEADER = 'AND'
ARDUINO_HEADER = 'ARD'
ALGORITHM_HEADER = 'ALG'
SEPERATOR = '|'
a = "AND|w 100"

for word in a.split("|"):
    print(word)


movement = ("w1", "a10","s50","w10")
try:
    for i in movement:
        message = ARDUINO_HEADER+SEPERATOR+i
        print(message," enoded>>>",message.encode)
except Exception as e:
    print(e)