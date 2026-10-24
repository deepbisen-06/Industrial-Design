"""Software-only reference tests of the MATLAB alert policy, not cloud execution."""
def decide(t,h,latched,last_sent,now,age=0):
 import math
 if not(math.isfinite(t) and math.isfinite(h)) or not(-40<=t<=80 and 0<=h<=100) or age>120:return 'ignore'
 if latched and t<=34 and h<=78:return 'rearm'
 if not latched and (t>35 or h>80) and now-last_sent>=1800:return 'send'
 return 'none'
cases=[((25,50,False,0,2000),'none'),((35,80,False,0,2000),'none'),((35.1,50,False,0,2000),'send'),((25,80.1,False,0,2000),'send'),((36,50,True,0,2000),'none'),((34,78,True,0,2000),'rearm'),((34.1,78,True,0,2000),'none'),((36,50,False,1000,2000),'none'),((36,50,False,200,2000),'send'),((36,50,False,0,2000,121),'ignore'),((float('nan'),50,False,0,2000),'ignore'),((25,101,False,0,2000),'ignore')]
for args,expected in cases:assert decide(*args)==expected,(args,expected)
print(f'PASS: {len(cases)} alert-policy reference cases. MATLAB/cloud/API execution not tested.')
