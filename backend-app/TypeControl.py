class TypeControl:
    def check_instance(self, value, value_type):
        if isinstance(value, (list, tuple)):
            if len(value) == 0:
                return True
            for val in value:
                if isinstance(val, value_type) == False:
                    return False
            return True
        else:
            return isinstance(value, value_type)

    def set_value(self, value, value_type):
        if self.check_instance(value, value_type):
            return value
        else:
            print('invalid type of value')
            return None
