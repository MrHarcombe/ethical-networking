# ethical-networking
Simple Flask application to demonstrate various hacking techniques, ethically, to year 9 students.

Basic plan is to have:

- an HTTP server that can be DDoS'd (can then protect with simple firewall filtering SYN packets)
- login methods open to SQL injection (can then protect by switching to use parameterized queries)
- registration methods that demonstrate plain text passwords, hashed passwords and salted-hash passwords
