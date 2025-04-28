from helpers.db import *

# add email
token = add_email("mail@example.com", "always")
print(token)
# update email settings
update_settings(token, "burger")
# get emails
print(get_emails())
# print email
print(get_email(token))
# delete email
# delete_email(token)