# ethical-networks
Simple Flask application to demonstrate various hacking techniques, ethically, to year 9 students.

## Basic plan is to have:

- an HTTP server that can be DDoS'd (can then protect with simple firewall filtering SYN packets)
- login methods open to SQL injection (can then protect by switching to use parameterized queries)
- registration methods that demonstrate plain text passwords, hashed passwords and salted-hash passwords

## To run:

- Be in the root project directory (ie above the ethical folder)
- Set an environment variable FLASK_APP=ethical
- Optionally set an environment variable FLASK_ENV=development (if you've going to be making code changes and want Flask to auto-reload them)
- Execute `python3 -m flask run --host=0.0.0.0`
