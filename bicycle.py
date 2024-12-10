import numpy as np
from matplotlib import pyplot as pp
import gpxpy


def f(P,m,v,C,rho,A,eta,h,g,theta,crr):
    return ((P-3)/v - (0.5*C*rho*A*v**2)-eta*A*(v/h)-(m*g*np.sin(theta))-crr*(m*g*np.sin(theta)))/m #https://www.hambini.com/testing-to-find-the-fastest-bicycle-wheel-hubs/
def euler(P,m,v,h,C,rho,A,eta,height,g,theta,crr):
    return v + f(P,m,v,C,rho,A,eta,height,g,theta,crr)*h

C=0.9
rho=1.1889
A=0.33
eta=2e-5
h=2
g=9.81
crr=0.0035 #https://www.bicyclerollingresistance.com/specials/crr-speed-test
P=300
m=50
v=[4]
path=[]


gpx_file = open("D:/New folder/SciComp stuff/New folder/SS-Getaria.gpx", 'r')

gpx = gpxpy.parse(gpx_file)

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            path.append([point.latitude,point.longitude,point.elevation])

          
totaldist=0
theta=[]

for i in range(len(path)-1):
        a = abs(np.array(path[i]))
        b = abs(np.array(path[i+1]))
        c = b - a
        c[1] = c[1]*111320*np.cos(c[0]) #delta longitude to meters
        c[0] = c[0] * 110574 #delta latitude to meters
        length=np.sqrt(c[0]**2+c[1]**2+c[2]**2)
        totaldist+=int(length)
        for j in range(int(length)):
            theta.append(np.arcsin(c[2]/length))

start=0
step=1
final=totaldist
x=np.arange(start,totaldist+step,step)
for i in range(len(x)-1):
    v.append(euler(P,m,v[-1],step,C,rho,A,eta,h,g,theta[i],crr))

avg = 0
for i in range(len(v)):
    avg += v[i]
print(avg/len(v))

pp.plot(x,v)
pp.xlabel('position (m)')
pp.ylabel('velocity (m/s)')
pp.show()

