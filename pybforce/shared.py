from time import localtime, strftime

def ScanTime():
     return str(strftime("%H:%M:%S", localtime()))

class ResultTrapMode():
    (regex,status,absolutetime)=range(0,3)
