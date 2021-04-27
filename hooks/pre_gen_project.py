import re

# Regular expression to check for a valid email address — based on the HTML5 standard
# (https://html.spec.whatwg.org/multipage/input.html#valid-e-mail-address). This is more restrictive than the RFC
# standard; see the comments in this SO answer for further information: https://stackoverflow.com/a/201378
REGEX_EMAIL_ADDRESS = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?" \
                      r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"


def check_valid_email_address_format(email: str) -> None:
    """Check that an email address is of a valid format using regular expressions.

    Uses the HTML5 standard for email address format. The regular expression pattern is available `here`_.

    Args:
        email: An email address to validate.

    Returns:
        None - raises an `AssertionError` if `email` is not a valid email address format.

    .. _here:
        https://html.spec.whatwg.org/multipage/input.html#valid-e-mail-address

    """
    assert bool(re.fullmatch(REGEX_EMAIL_ADDRESS, email)), f"Invalid email address supplied: {email}"


if __name__ == "__main__":

    # Check the format of the contact email address supplied is a valid one
    check_valid_email_address_format("{{ cookiecutter.contact_email }}")
