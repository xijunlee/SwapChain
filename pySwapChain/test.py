class test:
    def __init__(self,a,b):
        self.A=a
        self.B=b
        
    def out1(self,a,b):
        print a,b

    def out(self):
        self.out1(self.A,self.B)

    

if __name__ == "__main__":
    t = test(1,2)
    t.out()
