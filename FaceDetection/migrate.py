from conn import cursor
a = cursor.execute("""
CREATE TABLE faces (
    id int(9) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(255) NOT NULL,
    cpf varchar(100) NOT NULL,
    email varchar(255) NOT NULL,
    face text NOT NULL
);
""")