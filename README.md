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

/patrimony endpoint (VIEW patrimony) - GET
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