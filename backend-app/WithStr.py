class WithStr:
    def __str__(self):
        return '[%s object]' % self.__class__.__name__
