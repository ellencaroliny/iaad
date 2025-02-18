drop database startup;
Create database startup;
use startup;

CREATE TABLE Startups (
    id_startup INT PRIMARY KEY,
    nome_startup VARCHAR(255),
    cidade_sede VARCHAR(255)
);

CREATE TABLE Programadores (
    id_programador INT PRIMARY KEY,
    nome_programador VARCHAR(255),
    genero CHAR(1),
    data_nasc DATE,
    id_startup INT,
    FOREIGN KEY (id_startup) REFERENCES Startups(id_startup) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Dependentes (
    id_dependente INT AUTO_INCREMENT PRIMARY KEY,
    nome_dependente VARCHAR(255),
    parentesco VARCHAR(50),
    data_nasc DATE,
    id_programador INT,
    FOREIGN KEY (id_programador) REFERENCES Programadores(id_programador) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Linguagens (
    id_linguagem INT PRIMARY KEY,
    nome_linguagem VARCHAR(100)
);

CREATE TABLE Programador_Linguagem (
    id_programador INT,
    id_linguagem INT,
    PRIMARY KEY (id_programador, id_linguagem),
    FOREIGN KEY (id_programador) REFERENCES Programadores(id_programador) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_linguagem) REFERENCES Linguagens(id_linguagem) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Trigger para impedir que programadores sejam inseridos sem startup
DELIMITER $$

CREATE TRIGGER before_insert_programador
BEFORE INSERT ON Programadores
FOR EACH ROW
BEGIN
    IF NEW.id_startup IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cada programador deve estar vinculado a uma startup!';
    END IF;
END $$

DELIMITER ;
