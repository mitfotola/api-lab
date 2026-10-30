# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401 ({"error":"authentication failed"})
- Step 0.4, the name of your pizza: The Deep Americana
- Step 0.12, results of the three runs without a session (optional):
- Step 0.16, blocks of "how many of the three tools are excluded":
  - none excluded (0) → `[]` → 200
  - one excluded (1) → `["Knife"]`, `["Scissors"]` (the two original inputs, both in this block) → 200
  - two excluded (2) → `["Knife", "Scissors"]` → 200
  - all three excluded (3) → `["Knife", "Pizza cutter", "Scissors"]` → **500 with an empty body** (Defect 1)

## Defect report
- Title: Defect 1 — POST /api/pizza answers 500 with an empty body when all three tools are excluded
- Request:
  ```
  POST https://quickpizza.grafana.com/api/pizza
  Authorization: token <token of a logged-in user>
  Content-Type: application/json

  {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
  ```
  With curl: `curl -i -H "@auth.txt" -d "@no_tools.json" https://quickpizza.grafana.com/api/pizza`
- Expected result: status 400 with a JSON error message that says no pizza can be made without any tool.
- Actual result: status 500 Internal Server Error, `content-length: 0`, no JSON body.
- Severity: Medium. Other customers are not affected and the input is unusual, but an app that calls
  the API gets no message to show, cannot tell this case apart from a real server outage, and may
  retry a request that will never succeed. Covered by
  `test_excluded_tools.py::test_all_tools_excluded_is_refused`, marked `xfail(strict=True)`.

## Part A
- Step A4, status codes when the other user reads, changes and deletes:
  - read (GET /api/ratings/{id}): 404 `{"error":"not found"}`
  - change (PUT /api/ratings/{id}): 400 `{"error":"rating ID <id> not found"}`
  - delete (DELETE /api/ratings/{id}): 400 `{"error":"rating ID <id> not found"}`
  - In every case the owner could still read the rating afterwards with the same stars.

## Part B
1.
2.
3.
4.
5.
6.
7.
8.
