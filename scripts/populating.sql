
INSERT INTO Startups (id_startup, nome_startup, cidade_sede) VALUES
(10001, 'Tech4Toy', 'Porto Alegre'),
(10002, 'Smart123', 'Belo Horizonte'),
(10003, 'knowledgeUp', 'Rio de Janeiro'),
(10004, 'BSI Next Level', 'Recife'),
(10005, 'QualiHealth', 'São Paulo'),
(10006, 'ProEdu', 'Florianópolis'),
(10007, 'CommerceIA', 'Manaus');

INSERT INTO Programadores (id_programador, nome_programador, genero, data_nasc, id_startup) VALUES
(30001, 'João Pedro', 'M', '1993-06-23', 10001),
(30005, 'Ana Cristina', 'F', '1968-02-19', 10001),
(30002, 'Paula Silva', 'F', '1986-01-10', 10002),
(30007, 'Laura Marques', 'F', '1987-10-04', 10002),
(30003, 'Renata Vieira', 'F', '1991-07-05', 10003),
(30004, 'Felipe Santos', 'M', '1976-11-25', 10004),
(30006, 'Fernando Alves', 'M', '1988-07-07', 10004),
(30008, 'Lucas Lima', 'M', '2000-10-09', 10006),
(30011, 'Alice Lins', 'F', '1995-07-03', 10007),
(30010, 'Leonardo Ramos', 'M', '2005-03-07', 10007);

INSERT INTO Dependentes (nome_dependente, parentesco, data_nasc, id_programador) VALUES
('André Sousa', 'Filho', '2020-05-15', 30001),
('Luciana Silva', 'Filha', '2018-07-26', 30005),
('Elisa Silva', 'Filha', '2020-01-06', 30005),
('Breno Silva', 'Esposo', '1984-05-21', 30005),
('Daniel Marques', 'Filho', '2014-06-06', 30007),
('Rafaela Santos', 'Esposa', '1980-02-12', 30004),
('Marcos Martins', 'Filho', '2008-03-26', 30004),
('Laís Meneses', 'Esposa', '1990-11-09', 30006),
('Lidiane Macedo', 'Filha', '2015-04-14', 30011);

INSERT INTO Linguagens (id_linguagem, nome_linguagem) VALUES
(20001, 'Python'),
(20002, 'PHP'),
(20003, 'Java'),
(20004, 'C'),
(20005, 'JavaScript'),
(20006, 'Dart'),
(20007, 'SQL');

INSERT INTO Programador_Linguagem (id_programador, id_linguagem) VALUES
(30001, 20001),
(30001, 20002),
(30002, 20003),
(30007, 20003),
(30003, 20001),
(30003, 20002),
(30004, 20005),
(30006, 20005),
(30008, 20007),
(30010, 20007),
(30010, 20006);
