# Selune

RPG de texto em Python, com sistema de combate, evolução de personagem e persistência de dados em PostgreSQL.

Projeto desenvolvido como estudo prático de Programação Orientada a Objetos, modelagem de banco de dados relacional e integração Python + PostgreSQL, evoluindo depois para práticas de Engenharia de Dados.

## Tecnologias

- **Python 3** — lógica do jogo (POO: herança, composição, polimorfismo)
- **PostgreSQL** — persistência de dados (players, monstros, itens, localizações, inventário)
- **psycopg2** — driver de conexão Python ↔ PostgreSQL
- **python-dotenv** — gerenciamento seguro de credenciais via variáveis de ambiente
- **Docker** — containerização da aplicação e do banco

## Estrutura do projeto

Selune/
├── main.py                  # ponto de entrada do jogo (menu, loop principal)
├── postgre.sql              # script de criação das tabelas do banco
├── requirements.txt         # dependências Python
├── .env.example             # modelo de variáveis de ambiente (sem valores reais)
│
├── Entities/                # classes de domínio do jogo
│   ├── player.py            # Player (composição: Inventory, Equipment)
│   ├── monster.py           # Monstro
│   ├── item.py              # Item + subclasses (Weapon, Armadura, Consumivel, Loot, Acessorio)
│   ├── inventory.py         # Inventory (lista de itens do player)
│   └── equipment.py         # Equipment (slots de arma/armadura/acessório)
│
├── Systems/
│   └── combat.py            # Combat — orquestra turnos, XP, gold e loot
│
├── World/
│   └── location.py          # Localização (regiões do jogo)
│
└── Database/                # camada de acesso a dados (Repository Pattern)
    ├── connection.py            # conexão com PostgreSQL via .env
    ├── player_repository.py     # CRUD de players
    ├── monster_repository.py    # CRUD de monstros + relação com localizações
    ├── item_repository.py       # CRUD de itens
    ├── location_repository.py   # CRUD de localizações
    ├── inventory_repository.py  # inventário persistido (upsert de quantidade)
    └── seed.py                  # popula o banco com dados iniciais

## Modelo de dados

- **players** — dados do personagem (status, atributos, progressão)
- **items** — itens do jogo, com herança em tabela única (armas, armaduras, consumíveis, loot, acessórios)
- **monsters** — monstros, cada um com um possível item de loot (`loot_item_id`, opcional)
- **locations** — regiões do mundo
- **monster_locations** — relação muitos-para-muitos entre monstros e regiões
- **inventory** — relação muitos-para-muitos entre players e items, com quantidade

## Como executar

### Pré-requisitos

- Python 3.10+
- PostgreSQL instalado e rodando

### 1. Clone o repositório

git clone https://github.com/willian-andrade-dev/Selune.git
cd Selune

### 2. Crie um ambiente virtual e instale as dependências

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt

### 3. Configure as variáveis de ambiente

Copie o modelo e preencha com suas credenciais reais do PostgreSQL:

cp .env.example .env

Edite o .env com seu editor de preferência:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=rpg_database
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui


### 4. Crie o banco de dados

CREATE DATABASE rpg_database;

### 5. Crie as tabelas

Rode o script `postgre.sql` no banco `rpg_database` (via extensão do VSCode, DBeaver, ou terminal `psql`).

### 6. Popule os dados iniciais (itens, monstros, localizações)

python -m Database.seed

### 7. Rode o jogo

python main.py

## Funcionalidades

- Criação e login de personagem (progresso salvo no banco)
- Sistema de combate por turnos
- Ganho de XP, ouro e itens ao derrotar monstros
- Sistema de level up (aumenta ataque e HP máximo)
- Inventário persistente
- Sistema de equipamento (arma, armadura, acessório)
- Uso de itens (cura, equipar) com efeitos distintos por tipo (polimorfismo)
- Monstros distribuídos por região (relação muitos-para-muitos)

## Prints

### Menu Principal
![Menu principal do jogo](Menu_principal.png)
### Combate
![Tela de combate](Combate.png)
### Inventário
![Inventário do jogador](Inventario.png)


## Roadmap

Projeto em desenvolvimento contínuo. Próximos passos incluem:
- Sistema de loja, NPCs e crafting
- Logs de combate para análise de dados (Spark, Airflow, dbt)