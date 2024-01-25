from src.db import get_pool

pool = get_pool()
def execute():
    with pool.connection() as conn:
        conn.execute(
        '''CREATE TABLE restaurant (
            restaurant_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(100) NOT NULL,
            location VARCHAR(255),
            owner_name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255) NOT NULL,
            contact_number VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
        )

execute()
