-- número de programadores por startups
SELECT s.nome_startup, COUNT(p.id_programador) AS total_programadores
FROM Startups s
LEFT JOIN Programadores p ON s.id_startup = p.id_startup
GROUP BY s.nome_startup
ORDER BY total_programadores DESC;


--  Média de idade dos programadores por startup
SELECT s.nome_startup, 
       ROUND(AVG(YEAR(CURDATE()) - YEAR(p.data_nasc)), 1) AS media_idade
FROM Startups s
LEFT JOIN Programadores p ON s.id_startup = p.id_startup
GROUP BY s.nome_startup
ORDER BY media_idade DESC;


-- Número de dependentes por programador
SELECT p.nome_programador, COUNT(d.id_dependente) AS total_dependentes
FROM Programadores p
LEFT JOIN Dependentes d ON p.id_programador = d.id_programador
GROUP BY p.nome_programador
ORDER BY total_dependentes DESC;

-- Programador mais velho e mais novo
SELECT 
    nome_programador, 
    data_nasc,
    YEAR(CURDATE()) - YEAR(data_nasc) AS idade
FROM Programadores
WHERE data_nasc = (SELECT MIN(data_nasc) FROM Programadores)
   OR data_nasc = (SELECT MAX(data_nasc) FROM Programadores);


-- Número de programadores por gênero
SELECT 
    CASE 
        WHEN genero = 'M' THEN 'Masculino' 
        WHEN genero = 'F' THEN 'Feminino' 
        ELSE 'Outro' 
    END AS genero,
    COUNT(*) AS total
FROM Programadores
GROUP BY genero;


-- Startups mais diversas
SELECT 
    s.nome_startup,
    SUM(CASE WHEN p.genero = 'M' THEN 1 ELSE 0 END) AS total_homens,
    SUM(CASE WHEN p.genero = 'F' THEN 1 ELSE 0 END) AS total_mulheres,
    ABS(SUM(CASE WHEN p.genero = 'M' THEN 1 ELSE 0 END) - 
        SUM(CASE WHEN p.genero = 'F' THEN 1 ELSE 0 END)) AS score_diversidade
FROM Startups s
LEFT JOIN Programadores p ON s.id_startup = p.id_startup
GROUP BY s.nome_startup
ORDER BY score_diversidade ASC;  -- Quanto menor, mais equilibrada é a diversidade


-- Qual startup tem os programadores mais jovens e mais velhos?
SELECT 
    s.nome_startup, 
    MIN(YEAR(CURDATE()) - YEAR(p.data_nasc)) AS idade_minima,
    MAX(YEAR(CURDATE()) - YEAR(p.data_nasc)) AS idade_maxima
FROM Startups s
JOIN Programadores p ON s.id_startup = p.id_startup
GROUP BY s.nome_startup
ORDER BY idade_minima ASC;  -- Alterne para idade_maxima DESC para ver o mais velho

-- Criando uma view
CREATE VIEW vw_programadores_info AS
SELECT 
    p.nome_programador, 
    YEAR(CURDATE()) - YEAR(p.data_nasc) AS idade,
    s.nome_startup,
    s.cidade_sede
FROM Programadores p
JOIN Startups s ON p.id_startup = s.id_startup;

SELECT * FROM vw_programadores_info;
