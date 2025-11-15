# SQLI Challenge

## Executing the SQL injection

This challenge runs a flask webpage that uses a sqlite database. You can view a page of products, and add products to that page. There is also an admin page behind a login portal, which has the flag.

The vulnerability in the web app lies in the unfiltered input used to add items to the list of products, allowing an attacker to modiy an `INSERT INTO` statement with arbitrary sqlite code. While you can't directly bypass authentication, you can create a new item that reads information from the Users table.

## Identifying the Users Table

When you look at the login functionality, you can inspect the page source to see a commented out field for a debug mode.

```html
<form method="POST">
            <div>
                <input name="name" placeholder="Enter Username" autofocus="">
            </div>
            <div>
                <input type="password" name="password" placeholder="Enter Password">
            </div>
            <div>
                <!-- <input type="checkbox" name="DEV_ONLY_debug_mode"> -->
            </div>
            <div>
                <button type="submit">Login</button>
            </div>
        </form>
```

If you enable that element and check the box, or just add `&DEV_ONLY_debug_mode` to your post request parameters, you can attempt to turn on debug mode. However, the login page flashes that "the debug mode can only be used from the loopback interface". To bypass this, include a `X-Forwarded-For` header for the 127.0.0.1 loopback address. After doing that, users can see debug messages on the screen containing a SQL query that contains the table and column names needed for the injection. Note, the login parameters are not intentionally vulnerable to SQLI, and the statement in Debug mode is only supposed to reveal the table name and values.

## Executing the SQLi

Now armed with the user Table to target, you can carry out your SQLi from above on the new product submission form.

Target SQL statement (can be seen from entering a `'` on the create product page and reading the flask output):
```
INSERT INTO Products name, price, desc FROM VALUES ('{user input}', '{user input}', '{user input}');
```

Target injection:
```sql
FOO', (SELECT name FROM Users LIMIT 1 OFFSET 2), (SELECT password FROM Users LIMIT 1 OFFSET 2)); --
```

Carrying out this injection will create a new item visible in the products page, the contents of which will be the username and password hash for the users. Incrementing "OFFSET" will let you find the admin account.

## Cracking the Hash

Once you have the hash, it should look like this (note ~ individual salt and hash values will change):

```
pbkdf2:sha256:600000$DoXQV0VfWjR8O6AE$faba73b1f6e8a8f682f64c2904a593f7be45a67202d0cbb0a255cd2eb65f49fe
```

This hash, while valid and crackable, will not plug and play into hashcat or john the ripper (at least in my experience). Note that the salt is stored in base64, while the hash itself is stored in hex. A person can click around google and figure this out, but I added a hint with these two links to help figure out what to do.

- https://www.dcode.fr/pbkdf2-hash
- https://lincolnloop.com/insights/crack-django-passwords/

Basically, to make the hash crackable with hashcat, you need to do the following:

1. Change the hash identifier from `pbkdf2:sha256` to `pbkdf2_sha256`
2. Change the hash from hex to base64 (note: do not just base64 encode the hex string. Use a tool like cyberchef to decode the hex to binary, then base64 encode the binary)
3. (If using hashcat) change the `:` deliminators to `$`.

The modified hash should look like this:

```
pbkdf2_sha256$600000$DoXQV0VfWjR8O6AE$+rpzsfboqPaC9kwpBKWT975FpnIC0MuwolXNLrZfSf4=
```

Once you have the hash in the correct form, you can crack with hashcat and `rockyou.txt` using:

```
hashcat -m 10000 hash.txt /usr/share/wordlists/rockyou.txt [-w 3]
```

This is not the quickest hash in the world to crack. However, my 3080 on Ubuntu got it in 8 minutes. Running all of rockyou.txt on an incorrectly formatted hash took me about 45-50 minutes. The cracked password will be `ntadmin1234`.

## Getting the flag

Once you have the username `website_admin_account` and the password `ntadmin1234`, simply navigtate to the admin page and log in with those credentials to retreive the flag.

```
flag{87257f24fd71ea9ed8aa62837e768ec0}
```

## Hints

- Once the error on the webpage is found, think about what you can do with the vulnerable statement. Authentication bypass might not be possible, but what can you read in a database?

- The hash might prove a little tricky to format and crack. Check out these resources to get going in the right direction. https://www.dcode.fr/pbkdf2-hash, https://lincolnloop.com/insights/crack-django-passwords/ Note: rockyou.txt will suffice :)

- P.S. remember that 3090 you bought yourself during lockdown for "work"... aren't you glad you have it now?
