class Worklist():
    _items=[]
    _original_string=""
    _charset=[]
    
    def __init__(self, charset):
        self._charset= list(charset)

    def addtoworklist(self,value, holderstring="", replacecode="#1"):
        if (holderstring != ""):
            tmp = holderstring.replace(replacecode,value)
        else:
            tmp = value
        self._items.append(tmp)
    
    def generate(self,prefix, length, holder_string="", replacecode="#1",fixedlength=1):
        for char in self._charset:
            if (len(prefix)+1 < length):
                self.generate(prefix + char, length, holder_string,replacecode,fixedlength)
                if (fixedlength == 0): self.addtoworklist(prefix+char,holder_string,replacecode)
            else:
                self.addtoworklist(prefix+char,holder_string,replacecode)
    
    def loadfromfile(self, lsfile, holder_string="", replacecode="#1"):
        f = open(lsfile,"r")
        fdata = f.read().split("\n")
        for line in fdata:
            line = line.replace("\n","")
            if len(line)>0:
                if not line.startswith("#"): #escape comment lines)
                    if holder_string != "": self._items.append(holder_string.replace(replacecode,line))
                    else: self._items.append(line)
        f = None

    def clean(self):
        self._items=[]

#end class
