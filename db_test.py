from helpers.db import *

# add email
token = add_email("mail@example.com", "always")
# update email settings
update_settings(token, "burger")
# get emails
print(get_emails())