# Werk.nu
This repo demonstrates using an internal Domain-Specific Language (DSL) for describing acceptance tests. The language is defined using Python. This is often discussed on https://www.youtube.com/@ModernSoftwareEngineeringYT

I made an application to help me with this. It can be used by companies to post vacancies, on which applicants can apply to. Having multiple types of users makes testing the app more complicated. Therefore, it is a good fit for demonstrating more advanced testing techniques.

## Installation and run instructions
The repo contains multiple roots. Each uses uv for package management.

https://docs.astral.sh/uv/getting-started/installation/

Acceptance tests use Mailpit as a dev SMTP server on localhost:1025, and the API on localhost:8025.

https://mailpit.axllent.org/docs/install/

### Backend
```
cd backend
uv sync
backend runserver
```

### Acceptance tests
```
cd accept
uv sync
```
To run the acceptance tests, run both commands inside /accept and from different terminals.
```
backend runserver
pytest
```
/accept has its own .env, which will be used by the backend. This .env contains the url to the test database.