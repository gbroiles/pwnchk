# pwnchk


Python scripts to bulk scan haveibeenpwned.com (HIBP) for lists of email addresses or passwords

Email address scanning requires HIBP API key from https://haveibeenpwned.com/API/Key and is rate-limited (1.6 sec per request) per [HIBP API restrictions](https://haveibeenpwned.com/API/v3#RateLimiting). API key should be stored in the environment variable `HIBPKEY`.

Usage example:

    pwnchk text.txt

Password scanning does not require an API key and uses https://github.com/lionheart/pwnedpasswords for access.   

Usage example:

    passchk pass.txt
