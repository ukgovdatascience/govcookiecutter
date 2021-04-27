from hooks.pre_gen_project import check_valid_email_address_format
import pytest

# Define test cases for the `TestCheckValidEmailAddressFormat` test class
args_invalid_email_addresses = [
    "hello.world",
    "foo_bar"
]
args_valid_email_addresses = [
    "hello@world.com",
    "foo@bar"
]


class TestCheckValidEmailAddressFormat:

    @pytest.mark.parametrize("test_input_email", args_invalid_email_addresses)
    def test_raises_assertion_error_for_invalid_emails(self, test_input_email: str) -> None:
        """Test an `AssertionError` is raised for invalid email addresses."""

        # Execute the `check_valid_email_address_format` function, and check it raises an `AssertionError`
        with pytest.raises(AssertionError):
            check_valid_email_address_format(test_input_email)

    @pytest.mark.parametrize("test_input_email", args_valid_email_addresses)
    def test_passes_for_valid_emails(self, test_input_email: str) -> None:
        """Test no errors are raised for valid email addresses."""

        # Execute the `check_valid_email_address_format` function, which should not raise any exceptions for a valid
        # email address
        try:
            check_valid_email_address_format(test_input_email)
        except Exception as e:
            pytest.fail(f"Error raised: {e}")
