import pytest
from . import setup
from webapp.common.exceptions import domain


def from_json_to_entity(json):
    cls = json['cls']
    params = {}
    for name, value in json.items():
        if name == 'cls':
            continue

        if name == 'members':
            value = [
                from_json_to_entity(member)
                for member in value
            ]

        params[name] = value

    return cls(**params)


def test_participate_success():
    taxi_group = from_json_to_entity(setup.taxi_group_1)

    user_id = 'user3'
    taxi_group.participate(user_id)

    assert user_id in [member.user_id for member in taxi_group.members]


def test_participate_fail_duplicate_member():
    taxi_group = from_json_to_entity(setup.taxi_group_1)
    user_id = taxi_group.members[0].user_id

    with pytest.raises(domain.ParticipationFailed) as e:
        taxi_group.participate(user_id)
    assert str(e.value) == '그룹장 유저는 참여가 불가능합니다'

