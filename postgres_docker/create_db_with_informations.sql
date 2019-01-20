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