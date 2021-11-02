from typing import Any, Callable
import pytest

from taskmessenger.send import CompleteMessage, EmailData


def func(a):
    return a**2


@pytest.mark.parametrize("email_addr, create_email_data, input", [
    ("taskmessengerpy@gmail.com", lambda x: EmailData("Data for func", str(x)), 8)
])
def test_send_function_specific_email(email_addr: str, create_email_data: Callable[[Any], EmailData], input: int):
    c = CompleteMessage(email_addr)

    @c.send_function_specific_email(create_email_data)
    def func_function_specific(a):
        return func(a)

    func_function_specific(input)


@pytest.mark.parametrize("email_addr, email_data, input", [
    ("taskmessengerpy@gmail.com", EmailData("Func finished", "DONE"), 8)
])
def test_send_email(email_addr: str, email_data: EmailData, input: int):
    c = CompleteMessage(email_addr)

    @c.send_email_after(email_data)
    def func_function_specific(a):
        return func(a)
    func_function_specific(input)


@pytest.mark.skip(reason="Attachments not yet supported")
def test_send_with_attachments():
    EmailData("", "").attachments_to("")
