# Discord Top Level Domain (TLD) Monitor

In efforts to counteract bots and compromised accounts linking malicious websites, this python app currently acts as a proof of concept and executes the following:

1. Detect new user message
2. Determine if the user role is worth looking into message* (optional)
3. Detect a hyperlink in the message
4. Detect the TLD
5. Compare against a list of approved, more likely to be non-malicious TLDs
6. Delete if not on whitelist, notify if unseen TLD is posted