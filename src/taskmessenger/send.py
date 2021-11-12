from typing import Any, Callable, Dict
import requests


class EmailData:
    """Contains the email data to send a complete message"""
    def __init__(self, subject: str, body: str):
        """Constructor for EmailData

        Args:
            subject (str): What should appear in the subject of the email
            body (str): Allows for HTML markup of what should appear in the body
        """
        self.subject = subject
        self.body = body.replace("\n", "<br>")

    def attachments_to(self, email):
        pass


class CompleteMessage:

    _form_url: str = "https://docs.google.com/forms/d/e/1FAIpQLScVaOeD69Y7SQUaOPuAtHfuEAhNB_3C-jaF_i3LuIxAUaArUQ/formResponse"
    _form_post_names: Dict[str, str] = {
        "email": "entry.1686550249",
        "subject": "entry.159044383",
        "body": "entry.1804805684"
    }

    def __init__(self, email_addr: str, sending_warning_mode: bool = True):
        """Constructor for CompleteMessage

        Args:
            email_addr (str): The email address to send the message to
            sending_warning_mode (bool, optional): Whether to send a warning (True) or raise an exception (False) if POST fails to send message. Defaults to True.
        """
        self.email_addr: str = email_addr
        self.sending_warning_mode: bool = sending_warning_mode

    def _send_email(self, email_data: EmailData):
        data: Dict[str, str] = {
            CompleteMessage._form_post_names["email"]: self.email_addr,
            CompleteMessage._form_post_names["subject"]: email_data.subject,
            CompleteMessage._form_post_names["body"]: email_data.body
        }
        res = requests.post(CompleteMessage._form_url, data=data)
        if (res.status_code != 200):
            raise Exception("Couldn't POST email")

    def send(self, email_data: EmailData):
        self._send_email(email_data)

    def send_email_after(self, email_data: EmailData):
        """Decorator to send message upon completion of function

        Args:
            email_data (EmailData): The email to send
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                res = func(*args, **kwargs)
                self._send_email(email_data)
                return res
            return wrapper
        return decorator

    def send_function_specific_email(self, output_to_email: Callable[[Any], EmailData]):
        """Decorator to send message upon completion of function (depending on specific value of function)

        Args:
            output_to_email (Callable[[Any], EmailData]): turns the output of the function to the EmailData
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                res = func(*args, **kwargs)
                self._send_email(output_to_email(res))
                return res
            return wrapper
        return decorator
