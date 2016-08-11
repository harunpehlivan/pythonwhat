import re
from pythonwhat.Feedback import Feedback
import numpy as np
import pandas as pd
from pythonwhat.tasks import *

"""
This file contains all tests that can be done on specific objects. All tests are represented
an object. Tests that are alike can inherit from the same superclass. A test is first initialized
and can then be performed by calling the 'test()' function. The result will be stored inside
the result boolean. A test contains a failure message, which can be used by the reporter to
show when the test failed.
"""


class Test(object):
    """
    The basic Test. It should only contain a failure message, as all tests should result in
    a failure message when they fail.

    Note:
        This test should not be used by itself, subclasses should be used.

    Attributes:
        feedback (str): A string containing the failure message in case the test fails.
        result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, feedback):
        """
        Initialize the standard test.

        Args:
            feedback: string or Feedback object
        """
        if (issubclass(type(feedback), Feedback)):
            self.feedback = feedback
        elif (issubclass(type(feedback), str)):
            self.feedback = Feedback(feedback)
        else:
           raise TypeError("When creating a test, specify either a string or a Feedback object")

        self.result = None

    def test(self):
        """
        Wrapper around specific tests. Tests only get one chance.
        """
        if self.result is None:
            try:
                self.specific_test()
                self.result = np.array(self.result).all()
            except:
                self.result = False

    def specific_test(self):
        """
        Perform the actual test. For the standard test, result will be set to False.
        """
        self.result = False

    def get_feedback(self):
        return(self.feedback)


## Testing definition

class DefinedProcessTest(Test):
    def __init__(self, name, process, feedback):
        super().__init__(feedback)
        self.name = name
        self.process = process

    def specific_test(self):
        self.result = isDefinedInProcess(self.name, self.process)


class DefinedCollTest(Test):
    """
    Check if an object with a certain name is defined in a collection.

    Attributes:
        feedback (str): A string containing the failure message in case the test fails.
        name (str): Contains the name of the object that is searched for.
        collection (list/dict/set): Contains any object on which the 'in' operator can be performed.
        result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """
    def __init__(self, name, collection, feedback):
        super().__init__(feedback)
        self.name = name
        self.collection = collection

    def specific_test(self):
        self.result = self.name in self.collection

class HasKeyProcessTest(Test):
    def __init__(self, name, key, process, feedback):
        super().__init__(feedback)
        self.name = name
        self.key = key
        self.process = process

    def specific_test(self):
        self.result = hasKeyInProcess(self.name, self.key, self.process)


## Testing class

class InstanceTest(Test):
    def __init__(self, obj, cls, feedback):
        super().__init__(feedback)
        self.obj = obj
        self.cls = cls

    def specific_test(self):
        self.result = isinstance(self.obj, self.cls)

class InstanceProcessTest(Test):
    def __init__(self, name, klass, process, feedback):
        super().__init__(feedback)
        self.name = name
        self.klass = klass
        self.process = process

    def specific_test(self):
        self.result = isInstanceInProcess(self.name, self.klass, self.process)




## Testing equality

class EqualTest(Test):
    """
    Check if two objects are equal. Equal means the objects are exactly the same.
    This test should only be used with numeric variables (for now).

    Attributes:
        feedback (str): A string containing the failure message in case the test fails.
        obj1 (str): The first object that should be compared with.
        obj2 (str): This object is compared to obj1.
        result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, obj1, obj2, feedback):
        super().__init__(feedback)
        self.obj1 = obj1
        self.obj2 = obj2

    def objs_are(self, list_of_classes):
        return (
            any([isinstance(self.obj1, x) for x in list_of_classes]) &
            any([isinstance(self.obj2, x) for x in list_of_classes])
        )


    def specific_test(self):
        """
        Perform the actual test. result is set to False if the objects differ, True otherwise.
        """
        self.result = (self.obj1 == self.obj2)
        # try:
        #     if self.objs_are([np.ndarray, dict, list]):
        #         np.testing.assert_equal(self.obj1, self.obj2)
        #         self.result = True
        #     elif self.objs_are([pd.DataFrame]):
        #         pd.util.testing.assert_frame_equal(self.obj1, self.obj2)
        #         self.result = True
        #     elif self.objs_are([pd.Series]):
        #         pd.util.testing.assert_series_equal(self.obj1, self.obj2)
        #         self.result = True
        #     elif self.objs_are([pd.io.excel.ExcelFile]):
        #         data_obj1 = {sheet: self.obj1.parse(sheet) for sheet in self.obj1.sheet_names}
        #         data_obj2 = {sheet: self.obj2.parse(sheet) for sheet in self.obj2.sheet_names}
        #         for k in set(data_obj1.keys()).union(set(data_obj2.keys())):
        #             pd.util.testing.assert_frame_equal(data_obj1[k], data_obj2[k])
        #         self.result = True
        #     else:

        # except Exception:
        #     self.result = False


class EqualProcessTest(Test):

    def __init__(self, name, student_process, sol_obj, feedback):
        super().__init__(feedback)
        self.name = name
        self.student_process = student_process
        self.sol_obj = sol_obj

    def specific_test(self):
        stud_obj = getRepresentation(self.name, self.student_process)
        if stud_obj is None:
            self.result = False
        else:
            self.result = stud_obj == self.sol_obj

class EqualValueProcessTest(Test):
    def __init__(self, name, key, student_process, sol_value, feedback):
        super().__init__(feedback)
        self.name = name
        self.key = key
        self.student_process = student_process
        self.sol_value = sol_value

    def specific_test(self):
        stud_value = getValueInProcess(self.name, self.key, self.student_process)
        if stud_value is None:
            self.result = False
        else:
            self.result = stud_value == self.sol_value


## Others

class BiggerTest(Test):
    """
    Check if one object is greater than another. This test should only be used with numeric variables (for now).

    Attributes:
        feedback (str): A string containing the failure message in case the test fails.
        obj1 (str): The first object, that should be the greatest
        obj2 (str): The second object, that should be smaller
        result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, obj1, obj2, feedback):
        """
        Initialize with two objects.

        Args:
            obj1 (str): The first object, obj1 will be set to this.
            obj2 (str): The second object, obj2 will be set to this.
            feedback (str): The failure message will be set to this.
        """
        super().__init__(feedback)
        self.obj1 = obj1
        self.obj2 = obj2

    def specific_test(self):
        """
        Perform the actual test. result is set to False if the objects differ, True otherwise.
        """
        self.result = (self.obj1 > self.obj2)


class StringContainsTest(Test):
    """
    Check if a string is present in a text. Can use literal strings or a regex.

    Attributes:
        feedback (str): A string containing the failure message in case the test fails.
        string (regex/str):  String or regular expression which is searched for.
        search_string (str): The text in which is searched.
        pattern (bool): If set to True, string is matched with a regex. Literal otherwise.
        result (bool): True if the test succeed, False if it failed. None if it hasn't been tested yet.
    """

    def __init__(self, string, search_string, pattern, feedback):
        """
        Initialize with a string to look for, a string to search and whether or not to look for a pattern.

        Args:
            string (regex/str):  The string to look for will be set to this.
            search_string (str): The string to search in will be set to this.
            pattern (bool): The pattern boolean will be set to this.
            feedback (str): The failure message will be set to this.
        """
        super().__init__(feedback)
        self.string = string
        self.search_string = search_string
        self.pattern = pattern

    def specific_test(self):
        """
        Perform the actual test. result will be True if string is found (whether or not with a pattern),
        False otherwise.
        """
        if self.pattern:
            self.result = (
                re.search(
                    self.search_string,
                    self.string) is not None)
        else:
            self.result = (self.string.find(self.search_string) is not -1)


