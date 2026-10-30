# api-lab

API tests for [QuickPizza](https://quickpizza.grafana.com) with pytest and requests
(ITCS386, API Testing lab).

## Input domain model: POST /api/ratings

| Characteristic | Blocks | Values in the tests |
|---|---|---|
| C1 Value of `stars` | below 1, 1 to 5 (base), above 5 | 0, 3, 6 |
| C2 Type of `stars` | whole number (base), decimal, text, missing | 3, 3.5, "3", no field |
| C3 Pizza | exists (base), does not exist | a new pizza, 999999999 |
| C4 Token | the user's own (base), none, wrong length | from `auth`, no header, `token short` |

## Tests that cover each block (base choice coverage)

All tests are in `test_create_rating.py`. Each non-base test changes one
characteristic and keeps the others at their base.

| Characteristic | Block | Test |
|---|---|---|
| all | base: 3, whole number, existing pizza, own token | `test_base_choice_is_saved` |
| C1 | below 1 (0) | `test_stars_out_of_range[0]` |
| C1 | above 5 (6) | `test_stars_out_of_range[6]` |
| C2 | decimal (3.5) | `test_stars_decimal` |
| C2 | text ("3") | `test_stars_text` |
| C2 | missing | `test_stars_missing` |
| C3 | does not exist (999999999) | `test_pizza_does_not_exist` |
| C4 | none | `test_no_token` |
| C4 | wrong length | `test_token_wrong_length` |
