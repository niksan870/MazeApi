import copy

from tests.utils.apis import signin_route, signup_route, user_creds


def test_successful_signin(client):
    response = signin_route(client, creds=user_creds)
    assert response.data == b"Could not verify"


def test_signup_and_sign_up(client):
    signup_response = signup_route(client, creds=user_creds)
    assert signup_response.status_code == 201
    signin_response = signin_route(client, user_creds)
    assert signin_response.json["token"]
    assert signup_response.data == b"Successfully registered."


def test_signup_password_with_redundant_fields(client):
    response = signup_route(
        client,
        creds={"name": "happyUser", "password": "iTk19!n", "email": "email@gmail.com"},
    )
    assert response.status_code == 401
    assert response.json == {"message": "Field(s) redundant: email"}


def test_signup_password_with_only_numbers(client):
    new_user_creds = copy.deepcopy(user_creds)
    new_user_creds["password"] = "4334433"
    response = signup_route(client, creds=new_user_creds)
    assert response.status_code == 401
    assert response.json == {"message": "Password should include letters"}


def test_signup_password_with_whitespace(client):
    new_user_creds = copy.deepcopy(user_creds)
    new_user_creds["password"] = "iTk1 9!n"
    response = signup_route(client, creds=new_user_creds)
    assert response.status_code == 401
    assert response.json == {"message": "Password should contain any whitespace"}


def test_signup_password_with_only_letters(client):
    new_user_creds = copy.deepcopy(user_creds)
    new_user_creds["password"] = "sdfdsf"
    response = signup_route(client, creds=new_user_creds)
    assert response.status_code == 401
    assert response.json == {"message": "Password should include numbers"}


def test_signup_password_without_capital_letters(client):
    new_user_creds = copy.deepcopy(user_creds)
    new_user_creds["password"] = "sdfdsf22"
    response = signup_route(client, creds=new_user_creds)
    assert response.status_code == 401
    assert response.json == {"message": "Password should include capital letters"}


def test_signup_password_without_unique_symbol(client):
    new_user_creds = copy.deepcopy(user_creds)
    new_user_creds["password"] = "sdfdsf22A"
    response = signup_route(client, creds=new_user_creds)
    assert response.status_code == 401
    assert response.json == {"message": "Password should include unique symbols"}


def test_signup_with_only_name_field(client):
    response = signup_route(client, creds={"name": "38437847"})
    assert response.status_code == 401
    assert response.json == {"message": "Field(s) missing: password"}


def test_signup_with_empty_name_field(client):
    response = signup_route(client, creds={"name": ""})
    assert response.status_code == 401
    assert response.json == {"message": "Field(s) empty: name"}


def test_signup_with_only_password_field(client):
    response = signup_route(client, creds={"password": "38437847"})
    assert response.status_code == 401
    assert response.json == {"message": "Field(s) missing: name"}


def test_signup_with_empty_password_field(client):
    response = signup_route(client, creds={"password": ""})
    assert response.status_code == 401
    assert response.json == {"message": "Field(s) empty: password"}
