
class SetElement():

    def __init__(self):
        self.avg = None
        self.elements = []
        self.datas = []

    def push_element(self, element, data):

        self.datas.append(data)
        self.elements.append(element)
        self.avg = sum(self.elements) / float(len(self.elements))

    def valid_push_ratio(self, newElement, ratio):

        if self.avg == 0:
            return True
        elif newElement <= (1.0+ratio)*self.avg and newElement >= (1.0-ratio)*self.avg:
            return True
        else:
            return False

    def valid_push_const(self, newElement, const):

        if self.avg == None:
            return True
        elif newElement <= self.avg + const and newElement >= self.avg - const:
            return True
        else:
            return False
