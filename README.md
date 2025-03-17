# ELL887
```mermaid
graph TD;
    A[User Request] --> B[Azure App Service];
    B --> C[Flask Backend];
    C --> D[Azure SQL Database];
    C --> E[Static Files (HTML, CSS)];
    
    subgraph Cloud Deployment
        B
        C
        D
    end
