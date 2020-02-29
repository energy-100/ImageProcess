class A(object):
    bb=5
    def p(self):
        print("ok")

a=A()
# a.bb=1
print(a.bb)


A.ff=5
# c.bb=5
print(A.bb)
print(a.ff)

