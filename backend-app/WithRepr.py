class WithRepr:
    def __repr__(self):
        return '[%s object]' % self.__class__.__name__
