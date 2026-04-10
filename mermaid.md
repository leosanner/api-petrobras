flowchart TD
subgraph Frontend
A[React App<br/>Cloudflare Pages]
end

    subgraph Backend["Backend Unificado"]
        B[API Principal]
        C[Autenticação]
        D[Autorização / Usuários]
        E[Painel Admin]
        F[Consulta de Resultados]
    end

    subgraph Pipeline["Fluxo de Dados / ML"]
        H[Cron Job Mensal]
        I[Busca em Repositórios]
        J[Intersecção / Deduplicação]
        K[Modelos de ML]
        L[Processamento Final]
    end

    G[(PostgreSQL)]

    A --> B
    B --> C
    B --> D
    B --> E
    B --> F

    E --> G
    F --> G

    H --> I
    I --> J
    J --> K
    K --> L
    L --> G

    F --> A
