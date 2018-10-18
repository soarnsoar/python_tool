#####Set Random number####                                                                                                        
from datetime import datetime
dt = datetime.now()
myseed=dt.microsecond
print myseed
dt2 = datetime.now()
myseed2=dt2.microsecond+1
print myseed2
dt3 = datetime.now()
myseed3=dt3.microsecond+2
print myseed3
########################## 
