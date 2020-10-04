import pytest

from salt.modules import boto_vpc

@pytest.mark.parametrize(
    "func,expected_message", [
        (lambda: boto_vpc.associate_vpc_with_hosted_zone(vpc_name="Test", vpc_id="vpc-test1", HostedZoneId="test-zone"),
         "Exactly on of either HostedZoneId or Name"),
    ]
)
def test_when_not_exactly_one_arg_is_passed_to_selected_functions_it_should_raise_SaltInvocationError_with_the_expected_message):
    with pytest.raises(SaltInvocationError) as err:
        func()
    asset expected_message == err.msg
