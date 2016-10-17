from datetime import datetime
x = datetime(2013,1,1).time()
y = datetime(2013,1,1).date()
if x== y:
    print "gg"
else:
    print "GGGGG"
    
z = datetime.combine(y,x)
print z