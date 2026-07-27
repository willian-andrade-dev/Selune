-- ITEMS (não depende de nenhuma outra tabela)
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,

    tipo VARCHAR(20) NOT NULL,
    valor INTEGER NOT NULL,
    nivel_requerido INTEGER NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    funcao VARCHAR(50),
    dano INTEGER,
    armadura INTEGER,
    raridade VARCHAR(20) NOT NULL,
    subtipo VARCHAR(20),

    CONSTRAINT chk_item_tipo
        CHECK (tipo IN (
            'Arma',
            'Armadura',
            'Consumivel',
            'Acessorio',
            'Loot'
        )),

    CONSTRAINT chk_item_raridade
        CHECK (raridade IN (
            'Comum',
            'Incomum',
            'Raro',
            'Épico',
            'Lendário',
            'Mítico',
            'Artefato',
            'Relíquia'
        )),

    -- subtipo só existe pra Acessorio (Anel, Colar, Amuleto, Brinco); NULL pra qualquer outro tipo
    CONSTRAINT chk_item_subtipo
        CHECK (
            (tipo = 'Acessorio' AND subtipo IN ('Anel', 'Colar', 'Amuleto', 'Brinco'))
            OR (tipo != 'Acessorio' AND subtipo IS NULL)
        ),

    -- funcao só existe pra Consumivel; qualquer outro tipo deve ter funcao NULL
    CONSTRAINT chk_item_funcao
        CHECK (
            (tipo = 'Consumivel' AND funcao IN (
                'curar_10',
                'curar_25',
                'curar_50',
                'curar_total',
                'mana_15',
                'mana_40',
                'buff_ataque',
                'buff_armadura',
                'bonus_xp',
                'elixir_heroi'
            ))
            OR (tipo != 'Consumivel' AND funcao IS NULL)
        )
);

-- ATTRIBUTES e ITEM_EFFECTS (depende de ITEMS)
-- attributes: catálogo de atributos que podem receber bônus (hp, mana, ataque, armadura, critico, etc.)
-- item_effects: bônus/acréscimos de cada item sobre um atributo (base fica em items.dano / items.armadura)
CREATE TABLE IF NOT EXISTS attributes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(30) NOT NULL UNIQUE,
    descricao VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS item_effects (
    id SERIAL PRIMARY KEY,
    item_id INTEGER NOT NULL,
    attribute_id INTEGER NOT NULL,
    valor NUMERIC(10,2) NOT NULL,
    percentual BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (item_id)
        REFERENCES items(id)
        ON DELETE CASCADE,

    FOREIGN KEY (attribute_id)
        REFERENCES attributes(id),

    UNIQUE(item_id, attribute_id)
);

-- LOCATIONS (não depende de nenhuma outra tabela)
CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    dificuldade INTEGER NOT NULL,
    regiao VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS classes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(30) UNIQUE NOT NULL,
    descricao TEXT,
    hp_base INT NOT NULL,
    mana_base INT NOT NULL,
    ataque_base INT NOT NULL,
    armadura_base INT NOT NULL,
    hp_regen_base NUMERIC DEFAULT 0,
    hp_regen_por_nivel NUMERIC DEFAULT 0,
    mana_regen_base NUMERIC DEFAULT 0,
    mana_regen_por_nivel NUMERIC DEFAULT 0
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
    armadura_base INTEGER NOT NULL,
    classe_id INTEGER NOT NULL,

    FOREIGN KEY (classe_id)
        REFERENCES classes(id)
);

CREATE TABLE IF NOT EXISTS player_equipment (
    player_id INTEGER NOT NULL,
    slot VARCHAR(20) NOT NULL,
    item_id INTEGER NOT NULL,
    PRIMARY KEY (player_id, slot),
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (item_id) REFERENCES items(id),
    CONSTRAINT chk_player_equipment_slot
        CHECK (slot IN (
            'arma', 
            'armadura', 
            'Anel', 
            'Colar', 
            'Amuleto', 
            'Brinco'
        ))
);

CREATE TABLE IF NOT EXISTS habilidades (
    id SERIAL PRIMARY KEY,
    classe_id INTEGER NOT NULL,
    nome VARCHAR(50) NOT NULL,
    descricao VARCHAR(150),
    nivel_requerido INTEGER NOT NULL DEFAULT 1,
    custo_mana INTEGER NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    valor INTEGER NOT NULL,
    duracao_turnos INTEGER NOT NULL DEFAULT 0,
    cooldown_turnos INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY (classe_id)
        REFERENCES classes(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_habilidade_tipo
        CHECK (tipo IN ('dano', 'cura', 'buff_ataque', 'buff_armadura'))
);

-- MONSTERS (não guarda mais loot único; drops ficam em MONSTER_DROPS)
CREATE TABLE IF NOT EXISTS monsters (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    hp INTEGER NOT NULL,
    ataque INTEGER NOT NULL,
    xp INTEGER NOT NULL,
    ouro INTEGER NOT NULL
);

-- MONSTER_DROPS (depende de MONSTERS e ITEMS) — múltiplos drops possíveis por monstro
CREATE TABLE IF NOT EXISTS monster_drops (
    id SERIAL PRIMARY KEY,
    monster_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    chance_drop NUMERIC(5,2) NOT NULL,  -- ex: 35.00 = 35% de chance

    FOREIGN KEY (monster_id)
        REFERENCES monsters(id)
        ON DELETE CASCADE,

    FOREIGN KEY (item_id)
        REFERENCES items(id)
        ON DELETE CASCADE,

    UNIQUE(monster_id, item_id),

    CONSTRAINT chk_chance_drop
        CHECK (chance_drop > 0 AND chance_drop <= 100)
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
        ON DELETE CASCADE,

    -- impede duas linhas do mesmo item pro mesmo player; upsert deve incrementar quantidade
    UNIQUE(player_id, item_id)
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

CREATE TABLE IF NOT EXISTS combat_logs(
    id SERIAL PRIMARY KEY,
    player_id INTEGER NOT NULL,
    monster_id INTEGER NOT NULL,
    xp_ganho INTEGER NOT NULL,
    gold_ganho INTEGER NOT NULL,
    vitoria BOOLEAN NOT NULL,
    duracao_ms INTEGER NOT NULL,
    data_hora TIMESTAMP NOT NULL DEFAULT NOW(),

    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (monster_id) REFERENCES monsters(id)
);

-- SHOP_ITEMS (depende de ITEMS)
-- preco_compra fica NULL para itens não-compráveis (Loot); preco_venda existe sempre
CREATE TABLE IF NOT EXISTS shop_items (
    id SERIAL PRIMARY KEY,
    item_id INTEGER NOT NULL,
    preco_compra INTEGER,
    preco_venda INTEGER NOT NULL,
    compravel BOOLEAN NOT NULL DEFAULT TRUE,
    disponivel BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_shop_compravel
        CHECK (
            (compravel = TRUE AND preco_compra IS NOT NULL)
            OR (compravel = FALSE AND preco_compra IS NULL)
        ),

    FOREIGN KEY (item_id)
        REFERENCES items(id)
        ON DELETE CASCADE,

    UNIQUE(item_id)
);

CREATE TABLE IF NOT EXISTS recipes (
 
    id SERIAL PRIMARY KEY,
    item_resultado_id INTEGER NOT NULL,
    quantidade_produzida INTEGER NOT NULL DEFAULT 1,
    nivel_crafting_minimo INTEGER NOT NULL DEFAULT 1,
    tipo_estacao VARCHAR(20) NOT NULL,
 
    CONSTRAINT fk_recipe_item_resultado
        FOREIGN KEY (item_resultado_id) REFERENCES items(id),
 
    CONSTRAINT chk_recipe_tipo_estacao
        CHECK (tipo_estacao IN ('ferraria', 'alquimia', 'arcanismo'))
);

CREATE TABLE IF NOT EXISTS recipe_ingredients (
 
    recipe_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantidade_necessaria INTEGER NOT NULL,
 
    PRIMARY KEY (recipe_id, item_id),
 
    CONSTRAINT fk_ingredient_recipe
        FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
 
    CONSTRAINT fk_ingredient_item
        FOREIGN KEY (item_id) REFERENCES items(id)
);

CREATE TABLE IF NOT EXISTS player_crafting (
 
    player_id INTEGER PRIMARY KEY,
    nivel INTEGER NOT NULL DEFAULT 1,
    xp INTEGER NOT NULL DEFAULT 0,
 
    CONSTRAINT fk_player_crafting_player
        FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS location_stations (
 
    location_id INTEGER NOT NULL,
    tipo_estacao VARCHAR(20) NOT NULL,
 
    PRIMARY KEY (location_id, tipo_estacao),
 
    CONSTRAINT fk_location_station_location
        FOREIGN KEY (location_id) REFERENCES locations(id),
 
    CONSTRAINT chk_location_station_tipo
        CHECK (tipo_estacao IN ('ferraria', 'alquimia', 'arcanismo'))
);

-- CIDADES (não depende de nenhuma outra tabela)
CREATE TABLE IF NOT EXISTS cidades (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    regiao VARCHAR(50) NOT NULL,
    descricao VARCHAR(200)
);
 
-- BANCADAS (depende de CIDADES) — toda cidade tem as 4, criadas automaticamente via trigger
CREATE TABLE IF NOT EXISTS bancadas (
    id SERIAL PRIMARY KEY,
    cidade_id INTEGER NOT NULL,
    tipo VARCHAR(20) NOT NULL,
 
    FOREIGN KEY (cidade_id)
        REFERENCES cidades(id)
        ON DELETE CASCADE,
 
    UNIQUE(cidade_id, tipo),
 
    CONSTRAINT chk_bancada_tipo
        CHECK (tipo IN ('Ferraria', 'Alquimia', 'Joalheria', 'Arcanismo'))
);

-- TRIGGER: toda vez que um item novo é inserido, entra automaticamente na loja.
-- Loot vende por preço cheio e não é comprável; os demais tipos vendem por 50% do valor.
CREATE OR REPLACE FUNCTION fn_shop_items_auto_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO shop_items (item_id, preco_compra, preco_venda, compravel, disponivel)
    VALUES (
        NEW.id,
        CASE WHEN NEW.tipo = 'Loot' THEN NULL ELSE NEW.valor END,
        CASE WHEN NEW.tipo = 'Loot' THEN NEW.valor ELSE ROUND(NEW.valor * 0.5) END,
        CASE WHEN NEW.tipo = 'Loot' THEN FALSE ELSE TRUE END,
        TRUE
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_shop_items_auto_insert ON items;

CREATE TRIGGER trg_shop_items_auto_insert
AFTER INSERT ON items
FOR EACH ROW
EXECUTE FUNCTION fn_shop_items_auto_insert();

-- TRIGGER: toda cidade nova ganha as 4 bancadas automaticamente
CREATE OR REPLACE FUNCTION fn_bancadas_auto_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO bancadas (cidade_id, tipo) VALUES
        (NEW.id, 'Ferraria'),
        (NEW.id, 'Alquimia'),
        (NEW.id, 'Joalheria'),
        (NEW.id, 'Arcanismo');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
 
DROP TRIGGER IF EXISTS trg_bancadas_auto_insert ON cidades;
 
CREATE TRIGGER trg_bancadas_auto_insert
AFTER INSERT ON cidades
FOR EACH ROW
EXECUTE FUNCTION fn_bancadas_auto_insert();

