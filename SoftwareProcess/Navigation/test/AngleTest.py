import Navigation.prod.Angle as Angle

angle1 = Angle.Angle()
angle2 = Angle.Angle()
angle3 = Angle.Angle()
angle4 = Angle.Angle()

try:
    angle1degree = angle1.setDegreesAndMinutes('-89.0d4')
    angle2degree = angle2.setDegreesAndMinutes('745d2')
    angle3degree = angle3.setDegrees(-95)
    print (angle1degree,angle2degree,angle3degree)
    result = angle1.compare(789)
    angle2degree = angle2.subtract(angle1)
    angle1degree = angle1.add(angle3)
    print (result,angle2degree,angle1degree)
    result = angle1.compare(angle2)
    angle1string = angle1.getString()
    angle1showndegree = angle1.getDegrees()
    angle2string = angle2.getString()
    angle2showndegree = angle2.getDegrees()
    print(angle1showndegree,angle1string)
    print(angle2showndegree,angle2string)
except ValueError as e:
    print(e)