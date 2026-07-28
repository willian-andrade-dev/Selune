-- Seed das receitas de crafting, usando fn_seed_receita() (definida no postgre.sql).
-- Uma linha por receita: nome do resultado, quantidade produzida, nível de crafting
-- mínimo, tipo de estação, e os ingredientes em JSON ([{"nome":..,"qty":..}, ...]).


-- ===== FERRARIA =====
SELECT fn_seed_receita('Espada de Bronze', 1, 1, 'Ferraria', '[{"nome": "Minério de Cobre", "qty": 3}, {"nome": "Minério de Estanho", "qty": 2}, {"nome": "Madeira de Carvalho", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Espada Longa', 1, 6, 'Ferraria', '[{"nome": "Minério de Ferro", "qty": 5}, {"nome": "Couro Curado", "qty": 2}, {"nome": "Madeira Negra", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Machado de Ferro', 1, 8, 'Ferraria', '[{"nome": "Minério de Ferro", "qty": 6}, {"nome": "Presa de Javali", "qty": 1}, {"nome": "Madeira de Carvalho", "qty": 2}]'::jsonb);
SELECT fn_seed_receita('Lança de Ferro', 1, 10, 'Ferraria', '[{"nome": "Minério de Ferro", "qty": 5}, {"nome": "Madeira Negra", "qty": 2}, {"nome": "Garra de Lobo Filhote", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Sabre do Guarda', 1, 14, 'Ferraria', '[{"nome": "Espada Longa", "qty": 1}, {"nome": "Minério de Aço", "qty": 2}, {"nome": "Fragmento de Pedra", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Espada de Aço', 1, 18, 'Ferraria', '[{"nome": "Espada Longa", "qty": 1}, {"nome": "Minério de Ferro", "qty": 8}, {"nome": "Carvão Mineral", "qty": 2}, {"nome": "Casca de Urso", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Machado de Batalha', 1, 20, 'Ferraria', '[{"nome": "Machado de Ferro", "qty": 1}, {"nome": "Minério de Ferro", "qty": 6}, {"nome": "Presa de Orc", "qty": 2}]'::jsonb);
SELECT fn_seed_receita('Espada do Cavaleiro', 1, 26, 'Ferraria', '[{"nome": "Espada de Aço", "qty": 1}, {"nome": "Prata", "qty": 10}, {"nome": "Fragmento de Armadura Caída", "qty": 2}]'::jsonb);
SELECT fn_seed_receita('Alabarda Imperial', 1, 28, 'Ferraria', '[{"nome": "Lança de Ferro", "qty": 1}, {"nome": "Prata", "qty": 10}, {"nome": "Pena de Harpia", "qty": 2}]'::jsonb);
SELECT fn_seed_receita('Espada de Mithril', 1, 36, 'Ferraria', '[{"nome": "Espada do Cavaleiro", "qty": 1}, {"nome": "Mithril", "qty": 12}, {"nome": "Essência de Djinn", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Martelo Sagrado', 1, 40, 'Ferraria', '[{"nome": "Martelo de Guerra", "qty": 1}, {"nome": "Mithril", "qty": 1}, {"nome": "Água Benta", "qty": 1}, {"nome": "Fragmento Espiritual", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Espada Dracônica', 1, 46, 'Ferraria', '[{"nome": "Espada de Mithril", "qty": 1}, {"nome": "Escama de Dragão Ancião", "qty": 1}, {"nome": "Adamantita", "qty": 1}, {"nome": "Pena de Fênix", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Espada de Adamantium', 1, 58, 'Ferraria', '[{"nome": "Espada Dracônica", "qty": 1}, {"nome": "Adamantita", "qty": 1}, {"nome": "Núcleo Mágico", "qty": 1}, {"nome": "Fragmento de Cristal", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Colete de Couro', 1, 1, 'Ferraria', '[{"nome": "Couro Curado", "qty": 1}, {"nome": "Linha de Seda", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Couro Reforçado', 1, 9, 'Ferraria', '[{"nome": "Colete de Couro", "qty": 1}, {"nome": "Pelagem de Lobo Sombrio", "qty": 1}, {"nome": "Resina", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Peitoral de Bronze', 1, 2, 'Ferraria', '[{"nome": "Bronze", "qty": 1}, {"nome": "Couro Curado", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Armadura de Bronze', 1, 5, 'Ferraria', '[{"nome": "Peitoral de Bronze", "qty": 1}, {"nome": "Casca de Urso", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Cota de Malha', 1, 7, 'Ferraria', '[{"nome": "Minério de Ferro", "qty": 1}, {"nome": "Corrente", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Peitoral de Ferro', 1, 10, 'Ferraria', '[{"nome": "Minério de Ferro", "qty": 1}, {"nome": "Fragmento de Pedra", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Armadura de Ferro', 1, 13, 'Ferraria', '[{"nome": "Peitoral de Ferro", "qty": 1}, {"nome": "Casca de Urso", "qty": 1}, {"nome": "Couro Curado", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Armadura do Guarda', 1, 16, 'Ferraria', '[{"nome": "Armadura de Ferro", "qty": 1}, {"nome": "Fragmento de Armadura Caída", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Peitoral de Aço', 1, 19, 'Ferraria', '[{"nome": "Minério de Aço", "qty": 1}, {"nome": "Escama de Crocodilo", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Armadura Escamada', 1, 22, 'Ferraria', '[{"nome": "Peitoral de Aço", "qty": 1}, {"nome": "Escama de Crocodilo", "qty": 1}, {"nome": "Casca de Escorpião", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Armadura Prateada', 1, 30, 'Ferraria', '[{"nome": "Armadura do Cavaleiro", "qty": 1}, {"nome": "Prata", "qty": 1}, {"nome": "Bandagem de Múmia", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Armadura de Mithril', 1, 38, 'Ferraria', '[{"nome": "Armadura Prateada", "qty": 1}, {"nome": "Mithril", "qty": 1}, {"nome": "Essência de Djinn", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Armadura Sagrada', 1, 44, 'Ferraria', '[{"nome": "Armadura de Mithril", "qty": 1}, {"nome": "Água Benta", "qty": 1}, {"nome": "Fragmento Espiritual", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Armadura do Paladino', 1, 50, 'Ferraria', '[{"nome": "Armadura Sagrada", "qty": 1}, {"nome": "Pena de Fênix", "qty": 1}, {"nome": "Diamante Bruto", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Armadura Dracônica', 1, 55, 'Ferraria', '[{"nome": "Armadura do Paladino", "qty": 1}, {"nome": "Escama de Dragão", "qty": 1}, {"nome": "Adamantita", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Armadura Glacial', 1, 60, 'Ferraria', '[{"nome": "Armadura Dracônica", "qty": 1}, {"nome": "Núcleo de Gelo", "qty": 1}, {"nome": "Pelo Glacial", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Armadura Flamejante', 1, 60, 'Ferraria', '[{"nome": "Armadura Dracônica", "qty": 1}, {"nome": "Escama de Salamandra", "qty": 1}, {"nome": "Cinzas Vulcânicas", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Armadura Sombria', 1, 65, 'Ferraria', '[{"nome": "Armadura Flamejante", "qty": 1}, {"nome": "Pó de Lich", "qty": 1}, {"nome": "Essência Sombria", "qty": 1}]'::jsonb);

-- ===== JOALHERIA =====
SELECT fn_seed_receita('Colar de Osso', 1, 1, 'Joalheria', '[{"nome": "Osso de Esqueleto", "qty": 1}, {"nome": "Barbante", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Amuleto de Pedra', 1, 3, 'Joalheria', '[{"nome": "Pedra Comum", "qty": 1}, {"nome": "Quartzo Arcano", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Anel do Caçador', 1, 8, 'Joalheria', '[{"nome": "Prata", "qty": 1}, {"nome": "Garra de Lobo Filhote", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Colar do Mago', 1, 20, 'Joalheria', '[{"nome": "Safira", "qty": 1}, {"nome": "Núcleo Mágico", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Amuleto Rúnico', 1, 24, 'Joalheria', '[{"nome": "Runa Completa", "qty": 1}, {"nome": "Quartzo Arcano", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Brinco Élfico', 1, 12, 'Joalheria', '[{"nome": "Esmeralda", "qty": 1}, {"nome": "Linha de Seda", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Colar da Fênix', 1, 40, 'Joalheria', '[{"nome": "Pena de Fênix", "qty": 1}, {"nome": "Rubi", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Colar Dracônico', 1, 48, 'Joalheria', '[{"nome": "Escama de Dragão", "qty": 1}, {"nome": "Diamante", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Amuleto do Vazio', 1, 52, 'Joalheria', '[{"nome": "Pó de Lich", "qty": 1}, {"nome": "Ônix", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Anel Glacial', 1, 30, 'Joalheria', '[{"nome": "Núcleo de Gelo", "qty": 1}, {"nome": "Safira", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Colar Flamejante', 1, 32, 'Joalheria', '[{"nome": "Cinzas Vulcânicas", "qty": 1}, {"nome": "Rubi", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Amuleto Sombrio', 1, 56, 'Joalheria', '[{"nome": "Essência Sombria", "qty": 1}, {"nome": "Areia Amaldiçoada", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Anel do Guardião', 1, 42, 'Joalheria', '[{"nome": "Fragmento de Cristal", "qty": 1}, {"nome": "Diamante", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Colar do Criador', 1, 60, 'Joalheria', '[{"nome": "Escama de Dragão", "qty": 1}, {"nome": "Pena de Fênix", "qty": 1}, {"nome": "Diamante", "qty": 1}]'::jsonb);

-- ===== ALQUIMIA =====
SELECT fn_seed_receita('Poção de Cura Menor', 1, 1, 'Alquimia', '[{"nome": "Erva Medicinal", "qty": 1}, {"nome": "Água Pura", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção de Cura', 1, 8, 'Alquimia', '[{"nome": "Erva Medicinal", "qty": 2}, {"nome": "Flor Solar", "qty": 1}, {"nome": "Frasco", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção de Cura Superior', 1, 20, 'Alquimia', '[{"nome": "Flor de Sangue", "qty": 1}, {"nome": "Essência Vital", "qty": 1}, {"nome": "Água Pura", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção de Cura Suprema', 1, 45, 'Alquimia', '[{"nome": "Essência Celestial", "qty": 1}, {"nome": "Pena de Fênix", "qty": 1}, {"nome": "Água Benta", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção de Mana Menor', 1, 1, 'Alquimia', '[{"nome": "Flor Lunar", "qty": 1}, {"nome": "Água Pura", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção de Mana Superior', 1, 22, 'Alquimia', '[{"nome": "Flor Lunar", "qty": 1}, {"nome": "Quartzo Arcano", "qty": 1}, {"nome": "Pó Arcano", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Elixir da Força', 1, 15, 'Alquimia', '[{"nome": "Fruta Rubra", "qty": 1}, {"nome": "Essência Vital", "qty": 1}, {"nome": "Presa de Orc", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Tônico Defensivo', 1, 12, 'Alquimia', '[{"nome": "Casca de Urso", "qty": 1}, {"nome": "Musgo Ancião", "qty": 1}, {"nome": "Escama de Crocodilo", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção da Experiência', 1, 34, 'Alquimia', '[{"nome": "Essência de Djinn", "qty": 1}, {"nome": "Fragmento Espiritual", "qty": 1}, {"nome": "Diamante Bruto", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Elixir do Herói', 1, 50, 'Alquimia', '[{"nome": "Pena de Fênix", "qty": 1}, {"nome": "Essência Celestial", "qty": 1}, {"nome": "Água Benta", "qty": 1}, {"nome": "Diamante Bruto", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção de Vida Pequena', 1, 1, 'Alquimia', '[{"nome": "Erva Medicinal", "qty": 1}, {"nome": "Água Pura", "qty": 1}, {"nome": "Frasco", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção de Vida Média', 1, 8, 'Alquimia', '[{"nome": "Erva Medicinal", "qty": 1}, {"nome": "Flor Solar", "qty": 1}, {"nome": "Frasco Vazio", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção de Mana Pequena', 1, 1, 'Alquimia', '[{"nome": "Flor Lunar", "qty": 1}, {"nome": "Água Pura", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção de Mana Média', 1, 10, 'Alquimia', '[{"nome": "Flor Lunar", "qty": 1}, {"nome": "Pó Arcano", "qty": 1}, {"nome": "Frasco", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção Revigorante', 1, 6, 'Alquimia', '[{"nome": "Erva Revigorante", "qty": 1}, {"nome": "Mel Silvestre", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Antídoto', 1, 5, 'Alquimia', '[{"nome": "Erva Medicinal", "qty": 1}, {"nome": "Musgo Ancião", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Veneno Fraco', 1, 10, 'Alquimia', '[{"nome": "Veneno de Aranha", "qty": 1}, {"nome": "Muco Pegajoso", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Veneno Forte', 1, 28, 'Alquimia', '[{"nome": "Veneno de Aranha", "qty": 1}, {"nome": "Essência Sombria", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Óleo Flamejante', 1, 20, 'Alquimia', '[{"nome": "Óleo Vegetal", "qty": 1}, {"nome": "Cinzas Vulcânicas", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Óleo Congelante', 1, 20, 'Alquimia', '[{"nome": "Óleo Vegetal", "qty": 1}, {"nome": "Núcleo de Gelo", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção de Resistência', 1, 10, 'Alquimia', '[{"nome": "Casca de Árvore", "qty": 1}, {"nome": "Erva Revigorante", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção de Agilidade', 1, 12, 'Alquimia', '[{"nome": "Trevo Dourado", "qty": 1}, {"nome": "Hortelã Selvagem", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção de Força', 1, 15, 'Alquimia', '[{"nome": "Fruta Rubra", "qty": 1}, {"nome": "Essência Vital", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção Arcana', 1, 22, 'Alquimia', '[{"nome": "Quartzo Arcano", "qty": 1}, {"nome": "Pó Arcano", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Elixir da Regeneração', 1, 24, 'Alquimia', '[{"nome": "Flor de Sangue", "qty": 1}, {"nome": "Essência Vital", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Elixir Sagrado', 1, 30, 'Alquimia', '[{"nome": "Água Benta", "qty": 1}, {"nome": "Lírio Azul", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Elixir Sombrio', 1, 36, 'Alquimia', '[{"nome": "Essência Sombria", "qty": 1}, {"nome": "Bandagem de Múmia", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção Antifogo', 1, 18, 'Alquimia', '[{"nome": "Escama de Salamandra", "qty": 1}, {"nome": "Água Pura", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Poção Antigelo', 1, 18, 'Alquimia', '[{"nome": "Pelo Glacial", "qty": 1}, {"nome": "Água Pura", "qty": 1}]'::jsonb);
SELECT fn_seed_receita('Elixir da Fênix', 1, 50, 'Alquimia', '[{"nome": "Pena de Fênix", "qty": 1}, {"nome": "Essência Celestial", "qty": 1}]'::jsonb);