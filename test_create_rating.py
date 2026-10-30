import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"
AUTH_ERROR = "authentication failed"


# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: a number of stars below 1 or above 5 is refused with a message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: a decimal number of stars is refused, because stars must be whole.
def test_stars_decimal(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3.5}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {
        "error": "json: cannot unmarshal number 3.5 into Go struct field "
        "Rating.stars of type int"
    }


# C2: stars sent as text is refused, even when the text is a number.
def test_stars_text(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": "3"}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {
        "error": "json: cannot unmarshal string into Go struct field "
        "Rating.stars of type int"
    }


# C2: a rating without the stars field is refused.
def test_stars_missing(api, auth, pizza_id):
    new = {"pizza_id": pizza_id}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C3: a rating of a pizza that does not exist is refused.
def test_pizza_does_not_exist(api, auth):
    new = {"pizza_id": 999999999, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}


# C4: a rating without a token is refused with 401.
def test_no_token(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new)
    assert res.status_code == 401
    assert res.json() == {"error": AUTH_ERROR}


# C4: a token of the wrong length is refused with 401.
def test_token_wrong_length(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    short = {"Authorization": "token short"}
    res = api.post("/api/ratings", json=new, headers=short)
    assert res.status_code == 401
    assert res.json() == {"error": AUTH_ERROR}
