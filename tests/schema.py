from PyDictConfig import *


class TestSchema(Section):
    test1 = StrOption(default="TestValue")
    test2 = IntOption(doc="TestDoc")

    class InSec(Section):
        test3 = FloatOption(default=1.1)
        test4 = BoolOption(default=True)
