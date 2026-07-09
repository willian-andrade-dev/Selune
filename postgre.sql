-- ITEMS (não depende de nenhuma outra tabela)
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    tipo VARCHAR(20),
    valor INTEGER NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    armadura INTEGER,
    dano INTEGER,
    funcao VARCHAR(50),
    propriedade VARCHAR(50)
);

-- LOCATIONS (não depende de nenhuma outra tabela)
CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    dificuldade INTEGER NOT NULL,
    regiao VARCHAR(50) NOT NULL
);

-- PLAYERS (não depende de nenhuma outra tabela)
CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    hp INTEGER NOT NULL,
    hp_maximo INTEGER NOT NULL,
    mana INTEGER NOT NULL,
    gold INTEGER NOT NULL,
    xp INTEGER NOT NULL,
    xp_para_upar INTEGER NOT NULL,
    level INTEGER NOT NULL,
    ataque_base INTEGER NOT NULL,
    ataque INTEGER NOT NULL,
    armadura INTEGER NOT NULL,
    armadura_base INTEGER NOT NULL
);

-- MONSTERS (depende de ITEMS por causa do loot_item_id)
CREATE TABLE IF NOT EXISTS monsters (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    hp INTEGER NOT NULL,
    ataque INTEGER NOT NULL,
    xp INTEGER NOT NULL,
    ouro INTEGER NOT NULL,
    loot_item_id INTEGER,

    CONSTRAINT fk_monster_loot
        FOREIGN KEY (loot_item_id) REFERENCES items(id)
);

-- INVENTORY (depende de PLAYERS e ITEMS)
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    quantidade INTEGER NOT NULL DEFAULT 1,
    player_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,

    FOREIGN KEY (player_id)
        REFERENCES players(id),

    FOREIGN KEY (item_id)
        REFERENCES items(id)
);

-- MONSTER_LOCATIONS (depende de MONSTERS e LOCATIONS)
CREATE TABLE IF NOT EXISTS monster_locations (
    id SERIAL PRIMARY KEY,
    monster_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,

    FOREIGN KEY (monster_id)
        REFERENCES monsters(id),

    FOREIGN KEY (location_id)
        REFERENCES locations(id)
);