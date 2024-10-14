-- Check if the database exists, if not, create it
SELECT 'CREATE DATABASE libros'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'libros')\gexec

-- Connect to the database
\c libros

-- Rest of your script remains the same
CREATE TABLE IF NOT EXISTS Autor (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL
);

-- Create the Libro table if it doesn't exist
CREATE TABLE IF NOT EXISTS Libro (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    fecha_publicacion DATE NOT NULL,
    autor_id INTEGER NOT NULL,
    FOREIGN KEY (autor_id) REFERENCES Autor(id)
);

-- Add constraint to prevent deletion of authors with associated books
ALTER TABLE Libro DROP CONSTRAINT IF EXISTS fk_autor;
ALTER TABLE Libro ADD CONSTRAINT fk_autor
    FOREIGN KEY (autor_id) 
    REFERENCES Autor(id)
    ON DELETE RESTRICT;

-- Insert dummy data into Autor table if it's empty
INSERT INTO Autor (nombre, apellido, fecha_nacimiento)
SELECT 'Gabriel', 'García Márquez', '1927-03-06'
WHERE NOT EXISTS (SELECT 1 FROM Autor LIMIT 1);

INSERT INTO Autor (nombre, apellido, fecha_nacimiento)
SELECT 'Jorge Luis', 'Borges', '1899-08-24'
WHERE NOT EXISTS (SELECT 1 FROM Autor LIMIT 1);

-- Insert dummy data into Libro table if it's empty
INSERT INTO Libro (titulo, fecha_publicacion, autor_id)
SELECT 'Cien años de soledad', '1967-05-30', 1
WHERE NOT EXISTS (SELECT 1 FROM Libro LIMIT 1);

INSERT INTO Libro (titulo, fecha_publicacion, autor_id)
SELECT 'El Aleph', '1949-06-30', 2
WHERE NOT EXISTS (SELECT 1 FROM Libro LIMIT 1);
