message = "abc"
print(len(message))
print(len(message.encode('utf-8')))
buffer = message +"\x00"*max(1024-len(message ),0)
print(len(buffer))
print(len(buffer.encode('utf-8')))