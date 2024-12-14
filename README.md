# burgerBot
Get emails every morning to see if there are burgers at the ETH Polymensa.

## setup
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fkepler-69c%2FburgerBot&env=EMAIL,PASSWORD,RECIPIENTS&envDescription=see%20project%20readme&envLink=https%3A%2F%2Fgithub.com%2Fkepler-69c%2FburgerBot%2Fblob%2Fmain%2FREADME.md)

**.env variables**
- `email` email address from which the emails are sent
- `password` password / app password of the email address
- `recipients` list of email addresses that should receive the emails
    - the email addresses are separated by commas, e.g. `burger@gmail.com,max@example.org`.

**api, send settings**
specified and explained in `config.toml`

**timing**
specified by the crontab in vercel.json

**other**
- [burgerBot image](https://unsplash.com/photos/photo-of-burger-with-tomato-and-cheese-OCHMcVOWRAU?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)

## tests
All tests are in the `/test/` folder, in files ending in `_test.py`.
To run the tests (using unittest), run

```bash
python3 -m unittest discover -s test -p "*.py"
```