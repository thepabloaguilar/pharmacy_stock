CREATE TABLE pharmacy_user(
    id              SERIAL,
    username        VARCHAR UNIQUE,
    password        VARCHAR,
    is_active       BOOLEAN DEFAULT TRUE,
    is_admin        BOOLEAN DEFAULT FALSE,
    creation_date   TIMESTAMP DEFAULT NOW(),
    CONSTRAINT pk_users PRIMARY KEY(id)
);

INSERT INTO pharmacy_user(username, password, is_admin)
VALUES ('teste', '$pbkdf2-sha256$29000$z5lz7l0LwVgLoVRK6b2XMg$jTqFf9L8Q1vGZjTpXkaHechcFQJ.2OZIlR12vTfV6Io', TRUE);

CREATE TABLE provider(
    id                  SERIAL,
    name                VARCHAR,
    telephone           VARCHAR,
    is_active           BOOLEAN DEFAULT TRUE,
    creation_date       TIMESTAMP DEFAULT NOW(),
    CONSTRAINT pk_provider PRIMARY KEY(id)
);

INSERT INTO provider(name, telephone)
VALUES
    ('Super Provider', '123456789'),
    ('Medicine Provider', '987654321');

CREATE TABLE medicine_type(
    id              SERIAL,
    description     VARCHAR,
    unit            VARCHAR,
    CONSTRAINT pk_medicine_type PRIMARY KEY(id)
);

INSERT INTO medicine_type(description, unit)
VALUES
    ('pill', 'mg'),
    ('syrup', 'ml'),
    ('drops', 'drops');

CREATE TABLE medicine(
    id                  SERIAL,
    name                VARCHAR,
    medicine_type_id    INTEGER,
    dosage              INTEGER,
    amount              NUMERIC(16, 4),
    quantity            INTEGER,
    provider_id         INTEGER,
    is_active           BOOLEAN DEFAULT TRUE,
    creation_date       TIMESTAMP DEFAULT NOW(),
    CONSTRAINT pk_medicine PRIMARY KEY(id),
    CONSTRAINT fk_medicine_type FOREIGN KEY(medicine_type_id) REFERENCES medicine_type(id),
    CONSTRAINT fk_provider FOREIGN KEY(provider_id) REFERENCES provider(id),
    CONSTRAINT positive_quantity CHECK (quantity >= 0)
);

INSERT INTO medicine(name, medicine_type_id, dosage, amount, quantity, provider_id)
VALUES
    ('Super Medicine', 1, 2, 14.02, 100, 1),
    ('Basic Syrup', 2, 4, 10.00, 20, 2);