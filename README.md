# burgerBot
Get emails every morning to see if there are burgers at the ETH Polymensa.

## setup
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fkepler-69c%2FburgerBot&env=EMAIL,PASSWORD,RECIPIENTS&envDescription=see%20project%20readme&envLink=https%3A%2F%2Fgithub.com%2Fkepler-69c%2FburgerBot%2Fblob%2Fmain%2FREADME.md)

**.env variables**
- `email` email address from which the emails are sent
- `password` password / app password of the email address

**recipients**
stored in Google Firestore DB. See `helpers/db.py`. To access the DB, one must have a service account key file named `serviceAccountKey.json`.

For vercel, the `.json` file with the credentials must be converted to base64 and stored in the environment variable `B64_FIREBASE_CREDENTIALS`. Convert with

```bash
base64 serviceAccountKey.json > key.b64
```

**api, settings**
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