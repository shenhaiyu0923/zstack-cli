class opt_object():
    def __init__(self):
        self.name = None
        self.age = None
        self.sex = False

    def set_name(self,name):
        self.name = name

    def get_name(self):
        return self.name

    def set_age(self,age):
        self.age = age

    def get_age(self):
        return self.age

    def set_sex(self,sex):
        self.sex = sex

    def get_sex(self):
        return self.sex

    def ress(self,mm):
        return mm


def res_test():
    name = 'admin'
    age = 123
    sex = True
    opt = opt_object()
    opt.name = name
    opt.sex = sex
    opt.age = age
    res = opt.ress('dfsdf')
    print(res)
    return opt

a = res_test()
print(a.__dict__)