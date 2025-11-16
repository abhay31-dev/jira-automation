Overview for the usage of Scripts.

1. add_comment.py
   Adds a new comment to a Jira issue using:
   python add_comment.py ISSUE_KEY "Your comment text"

Example:
python add_comment.py SRE-1 "1st Comment"

2. get_comments.py
   Fetches all comments from a Jira issue and prints:
   python get_comments.py ISSUE_KEY

Example:
python get_comments.py SRE-1

3. update_comment.py
   Updates an existing comment on a Jira issue using its comment ID.
   python update_comment.py ISSUE_KEY COMMENT_ID "Updated text"

Example:
python update_comment.py SRE-1 10001 "Updated comment via automation"
