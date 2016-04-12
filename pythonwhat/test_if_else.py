import ast
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Test import Test


def test_if_else(index=1,
                 test=None,
                 body=None,
                 orelse=None,
                 expand_message=True):
    """Test parts of the if statement.

    This test function will allow you to extract parts of a specific if statement and perform a set of tests
    specifically on these parts. A for loop consists of three potential parts: the condition test, `test`,
    which specifies the condition of the if statement, the `body`, which is what's executed if the condition is
    True and a else part, `orelse`, which will be executed if the condition is not True.

        ``if 5 == 3:``
        ``    print("success")``
        ``else:``
        ``    print("fail")``


    Has `5 == 3` as the condition test, `print("success")` as the body and `print("fail")` as the else part.

    Example:
      student_code
        | ``a = 12``
        | ``if a > 3:``
        | ``    print('test %d' % a)``
      solution_code
        | ``a = 4``
        | ``if a > 3:``
        | ``    print('test %d' % a)``
      sct
        | ``test_if_else(1,``
        | ``             body = lambda: test_expression_output(extra_env = { 'a': 5 }``
        | ``                                                   incorrect_msg = "Print out the correct things"))``
      This SCT will pass as `test_expression_output()` is ran on the body of the if statement and it will output
      the same thing in the solution as in the student code.

    Args:
      index (int): index of the function call to be checked. Defaults to 1.
      test: this argument holds the part of code that will be ran to check the condition test of the if statement.
        It should be passed as a lambda expression or a function definition. The functions that are ran should
        be other pythonwhat test functions, and they will be tested specifically on only the condition test of
        the if statement.
      body: this argument holds the part of code that will be ran to check the body of the if statement.
        It should be passed as a lambda expression or a function definition. The functions that are ran should
        be other pythonwhat test functions, and they will be tested specifically on only the body of
        the if statement.
      orelse: this argument holds the part of code that will be ran to check the else part of the if statement.
        It should be passed as a lambda expression or a function definition. The functions that are ran should
        be other pythonwhat test functions, and they will be tested specifically on only the else part of
        the if statement.
      expand_message (bool): if true, feedback messages will be expanded with `in the ___ of the if statement on
        line ___`. Defaults to True. If False, `test_if_else()` will generate no extra feedback.
    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_if_else")

    index = index - 1

    student_env, solution_env = state.student_env, state.solution_env

    state.extract_if_calls()
    student_ifs = state.student_if_calls
    solution_ifs = state.solution_if_calls

    try:
        lineno_student, test_student, body_student, orelse_student = student_ifs[
            index]
    except:
        rep.do_test(Test("Define more `if` statements."))
        return

    lineno_solution, test_solution, body_solution, orelse_solution = solution_ifs[
        index]

    def sub_test(closure, subtree_student, subtree_solution, incorrect_part):
        if closure:
            failed_before = rep.failed_test
            child = state.to_child_state(subtree_student, subtree_solution)
            closure()
            child.to_parent_state()
            if expand_message and (failed_before is not rep.failed_test):
                rep.feedback_msg = rep.feedback_msg + " in the " + incorrect_part + \
                    " of the `if` statement on line " + str(lineno_student) + "."

    sub_test(test, test_student, test_solution, "condition")
    sub_test(body, body_student, body_solution, "body")
    sub_test(orelse, orelse_student, orelse_solution, "else part")