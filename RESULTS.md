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
1. A test against the real server can find failures that a stub hides: (a) integration and
   configuration faults, such as the load balancer sending a request to a server that does not
   know the user, or a header or JSON field that the client and the server name differently;
   (b) faults in the real server's error handling, such as the 500 with an empty body in
   Step 0.16, which a stub would never return because we write the stub's answers ourselves.
   Unit tests with stubs are still worth writing: they are fast, repeatable, and do not depend
   on the network or on shared data, so they can check each rule in detail and point straight
   at the function that broke.
2. Ratings made with the public token belong to everyone, so another student could change or
   delete them while my test runs, and my tests could break theirs. A new user per test gives
   every test its own clean data, so the tests are independent and can run alone or in any
   order. In Project 2 every test will create its own customer, cart or booking through a
   fixture, with a unique name, delete what it created at the end, and never touch the data
   of other groups.
3. QuickPizza runs on several servers behind a load balancer, and each server keeps its own
   users and ratings. The session keeps the AWSALB cookie that the load balancer sends back,
   so every request in the run reaches the same server that created the user. Without it, a
   login could reach a server that has never seen the new user and fail with 401, so the test
   would be flaky. I did not do the optional Step 0.12.
4. The block "all three tools excluded" revealed the defect. A 500 with an empty body tells the
   calling app nothing: it cannot show the user what is wrong, it looks the same as a server
   crash, and the app may retry a request that will never succeed. A 400 with a message says
   that the input is the problem and how to fix it. The test stays as `xfail` so the defect
   stays visible in every run while the rest of the suite stays green, and with `strict=True`
   the run tells us as soon as QuickPizza fixes the bug, so we can remove the mark. Deleting
   the test would hide the defect.
5. Base choice coverage: 1 base test + (blocks - 1) for each characteristic
   = 1 + (3-1) + (4-1) + (2-1) + (3-1) = 1 + 2 + 3 + 1 + 2 = **9 tests**.
   All combinations coverage: 3 x 4 x 2 x 3 = **72 tests**.
6. Read gave 404, change gave 400, delete gave 400. I would expect the same code for all three:
   404 Not Found (which does not reveal that the rating exists) or 403 Forbidden. The rating
   was never changed or deleted, so access control works. The difference is still a small
   defect: 400 Bad Request means the request itself was malformed, which is not true here, and
   the same situation gets different codes for different methods, which makes error handling
   in a client app harder.
7. `curl -H "@madeup.txt" https://quickpizza.grafana.com/api/ratings` answered **200** with a
   list of ratings that I never created (ids 1, 2, 3, ...), the shared ratings of the practice
   account. Two runs returned different lists because they reached different servers, but
   both accepted the token. QuickPizza accepts any token of 16 characters without checking
   that a user logged in to get it, while `token short` is refused only because of its length.
   This is a defect (broken authentication). On a real system a stranger could invent a token
   and read, and probably change or delete, other people's data without any password.
8. An API test checks the data and the rules directly: exact status codes, every field of the
   JSON body, error messages, and requests that the web page would never send, such as
   0 stars, a decimal, or another user's rating. Only a test through the web pages can check
   what the user actually sees and does: the layout, that buttons and forms work, that the page
   shows the error message, and the whole flow in a real browser.
