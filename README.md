# python-stocks-api

- python_stocks/
  - __ init __.py
  - auth.py: 
    - Authorization handlers
    - JWT token
  - finance.py
    - some finance functions
  - models.py
    - sqlalchemy models
    - database interface
  - schemas.py
    - pydantic models

# env vars
- SENTRY_DNS= [**optional**]
- userdb=
- passwordb=
- hostdb=
- database=


# setup
- install python ^3.8
- install packages
  - install poetry 1.1.13 https://python-poetry.org/ -> then poetry shell
  - or pip install requirements.txt
- setup database, there's a Dockerfile that I use to create a docker image of mysql, just replaces the variables by your guest. (dont forget about env vars)
  - docker build -t {YOUR IMAGE NAME}
  - docker run --name {NAME} -p{PORT}:{PORT} -d {YOUR IMAGE NAME}
- set up the ambient variables (by .env or global)
- run create.py to create the tables on database.
- run: uvicorn app:app --reload

# case of use
there's a case of use on case.ipynb (you need jupyter to open this or google colab)

# mysql dependency
at models.py we define the database interface with mysql+aiomysql


# Diagrams

general use
``` mermaid 
sequenceDiagram

    participant Client
    participant API
    participant db
    
   Client->>API: request Login
   
        activate Client
        activate API
   
   API->>API: Authenticate
   API->>Client: response token
   
        deactivate Client
        deactivate API
   
   Client->>API: request data
   
        activate Client
        activate API
   
   API->>API: Authenticate Token
   API->>db: request data
        
        activate db
        
   db->>API: response data
   
        deactivate db
        
   API->>Client: response view
   
        deactivate Client
        deactivate API
```

/register/user endpoint - POST
``` mermaid
sequenceDiagram
    participant Client
    participant API
    participant db
    
    Client->>API: request register
        activate Client
        activate API
    API->>db: request data
        activate db
    db->>API: response data
        deactivate db
    API->>Client: User created
        deactivate Client
        deactivate API
```


/register/stock endpoint - POST
``` mermaid
sequenceDiagram
    participant Client
    participant API
    participant db
    
    Client->>API: login
        activate Client
        activate API
    API->>API: Autheticate
    API->>Client: Token
        deactivate Client
        deactivate API
    Client->>API: /register/stock
        activate Client
        activate API
    API->>API: Authenticate Token
    API->>db: stock data
        activate db
    db->>API: obj created
        deactivate db
    API->>Client: obj created
        deactivate Client
        deactivate API
    

```

/operations endpoint - GET
``` mermaid
sequenceDiagram
    participant Client
    participant API
    participant db
    
    Client->>API: request Login
        activate Client
        activate API
   
   API->>API: Authenticate
   API->>Client: response token
   
        deactivate Client
        deactivate API
   
   Client->>API: /operations
   
        activate Client
        activate API
   
   API->>API: Authenticate Token
   API->>db: request operations
        
        activate db
   
   db->>API: response operations
   
        deactivate db
   
   API->>Client: reponse operations
        
        deactivate Client
        deactivate API
```


/patrimony and /rentabilidade endpoint (VIEW patrimony and rentabilidade are almos the same process) - GET
``` mermaid 
sequenceDiagram
    participant Client
    participant API
    participant db
    participant Yahoo Finance
    
    Client->>API: request Login
        activate Client
        activate API
   
   API->>API: Authenticate
   API->>Client: response token
   
        deactivate Client
        deactivate API
        
   Client->>API: /patrimony
   
        activate Client
        activate API
   
   API->>API: Authenticate Token
   API->>db: request patrimony
        
        activate db
   
   db->>API: response patrimony
        
        deactivate db
        
   API->>Yahoo Finance: request last Price
        
        activate Yahoo Finance
        
   Yahoo Finance->>API: response Last Price
   
        deactivate Yahoo Finance
        
   API->>API: Combine data
   API->>Client: Response data
        
        deactivate Client
        deactivate API
```
