from db import *

# add email
token = add_email("bob@example.com", "always")
# update email settings
update_email_setting("bob@example.com", "burger", token)
# get emails
print(get_emails())