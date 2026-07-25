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
    armadura_base INT NOT NULL
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

