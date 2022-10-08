## Items
```mermaid
erDiagram
    LOCATION ||--o{ LOCATION : nested
    LOCATION ||--o{ ITEM : many
    ITEM ||--o{ ITEM : nested
```
