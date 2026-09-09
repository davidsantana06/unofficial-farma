CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    dosage TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE comment (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    author_name TEXT NOT NULL,
    author_email TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO company (name) VALUES
    ('Laboratório Vale Verde'),
    ('Farmacêutica Serra Azul');

INSERT INTO product (company_id, name, description, price, dosage) VALUES
    (1, 'Dipirona Sódica', 'Analgésico e antitérmico em comprimidos, caixa com 20 unidades.', 12.90, '500 mg'),
    (1, 'Amoxicilina', 'Antibiótico de amplo espectro em cápsulas, caixa com 21 unidades.', 38.50, '875 mg'),
    (2, 'Ibuprofeno', 'Anti-inflamatório não esteroidal em comprimidos revestidos, caixa com 30 unidades.', 21.75, '400 mg');

INSERT INTO comment (product_id, author_name, author_email, content) VALUES
    (1, 'Marina Alcântara', 'marina.alcantara@exemplo.com', 'Alívio rápido para dor de cabeça e o preço continua acessível.'),
    (1, 'Rogério Bastos', 'rogerio.bastos@exemplo.com', 'A cartela vem bem lacrada, mas a caixa poderia trazer mais comprimidos.'),
    (2, 'Helena Vasconcelos', 'helena.vasconcelos@exemplo.com', 'Tratamento completo em sete dias, exatamente como o médico indicou.'),
    (3, 'Tiago Moreira', 'tiago.moreira@exemplo.com', 'Funcionou bem para dor muscular depois do treino, sem irritar o estômago.');
