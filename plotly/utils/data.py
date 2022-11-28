class DataArray:
    def __init__(self, array, unit, label, errors=None):
        self.setArray(array)
        self.setUnit(unit)
        self.setLabel(label)
        self.setErrors(errors)
    
    @property
    def array(self):
        return self.__array
    
    @property
    def unit(self):
        return self.__unit
    
    @property
    def label(self):
        if self.__unit != "" and self.__unit is not None:
            return f"{self.__label} [{self.__unit}]"
        else:
            return self.__label
    
    @property
    def errors(self):
        return self.__errors
    
    def setArray(self, array):
        self.__array = array
    
    def setUnit(self, unit):
        self.__unit = unit
        
    def setLabel(self, label):
        self.__label = label
    
    def setErrors(self, errors):
        self.__errors = errors

class Data:
    def __init__(self, x, y) -> None:
        self.__data = {"x" : DataArray(*x), "y" : DataArray(*y)}
    
    @property
    def x(self):
        return self.__data["x"].array
    
    @property
    def y(self):
        return self.__data["y"].array
    
    @property
    def labels(self):
        return dict(x=self.__data["x"].label, y=self.__data["y"].label)