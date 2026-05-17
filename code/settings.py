"""
settings.py  –  Global constants for Fossil Excavation & Quiz Game
"""

# ── Screen ──────────────────────────────────────────────────────────────────
WIDTH        = 1280
HEIGHT       = 720
FPS          = 60
TITLE        = "Fossil Excavation & Quiz Game"

# ── Tile / Map ───────────────────────────────────────────────────────────────
TILESIZE     = 64
HITBOX_OFFSET = {
    'player': -26,
    'npc'   : -26,
    'object': -40,
    'grass' : -10,
    'invisible': 0,
}

# ── Player ───────────────────────────────────────────────────────────────────
PLAYER_SPEED = 5

# ── NPC types ────────────────────────────────────────────────────────────────
NPC_DATA = {
    'excavation_npc': {
        'name'         : 'Dr. Pebble',
        'dialogue_idle': "Hello, young explorer! Want to try your hand at fossil excavation?",
        'dialogue_done': "You've excavated all three sites. Well done!",
        'speed'        : 0,
        'health'       : 100,
        'graphic'      : 'graphics/monsters/bamboo/idle', # <-- UPDATED PATH
    },
    'quiz_npc': {
        'name'         : 'Prof. Stratum',
        'dialogue_idle': "Think you know your fossils? Come take my quiz!",
        'dialogue_locked': "Complete all excavation levels first!",
        'dialogue_done': "You've already completed the quiz!",
        'speed'        : 0,
        'health'       : 100,
        'graphic'      : 'graphics/monsters/squid/idle', # <-- UPDATED PATH
    }
}
# ── Excavation Grid ──────────────────────────────────────────────────────────
EXC_COLS        = 12      # grid columns
EXC_ROWS        = 9       # grid rows
EXC_CELL_SIZE   = 56      # pixels per cell
EXC_MAX_ATTEMPTS = 5


# ── Fossil Data ───────────────────────────────────────────────────────────────

# ── Quiz ──────────────────────────────────────────────────────────────────────
QUIZ_POINTS_PER_CORRECT = 2

QUIZ_QUESTIONS = [
    {
        'question': 'Which era did trilobites first appear?',
        'options' : ['Cambrian', 'Jurassic', 'Carboniferous', 'Cretaceous'],
        'answer'  : 0,
    },
    {
        'question': 'Ammonites are most closely related to which living animal?',
        'options' : ['Clams', 'Nautilus', 'Starfish', 'Sea urchins'],
        'answer'  : 1,
    },
    {
        'question': 'Fossil fern leaves are commonly found in which type of rock?',
        'options' : ['Granite', 'Basalt', 'Coal measures / shale', 'Quartzite'],
        'answer'  : 2,
    },
    {
        'question': 'Brachiopods superficially resemble which other organism?',
        'options' : ['Snails', 'Crabs', 'Clams', 'Corals'],
        'answer'  : 2,
    },
    {
        'question': 'What geological period did T. rex live in?',
        'options' : ['Triassic', 'Jurassic', 'Permian', 'Late Cretaceous'],
        'answer'  : 3,
    },
    {
        'question': 'Nautiloids are ancestors of which modern animal?',
        'options' : ['Octopus', 'Nautilus', 'Lobster', 'Jellyfish'],
        'answer'  : 1,
    },
    {
        'question': 'Which of these fossils is used as a KEY INDEX FOSSIL for dating Paleozoic rocks?',
        'options' : ['T. rex Tooth', 'Fern Leaf', 'Trilobite', 'Brachiopod'],
        'answer'  : 2,
    },
    {
        'question': 'What property allowed trilobites to fossilize so well?',
        'options' : ['Soft body', 'Hard calcite exoskeleton', 'Large size', 'Deep-sea habitat'],
        'answer'  : 1,
    },
    {
        'question': 'Carboniferous coal seams are made from compressed:',
        'options' : ['Dinosaur bones', 'Marine shells', 'Ancient plant matter', 'River sediments'],
        'answer'  : 2,
    },
    {
        'question': 'Which fossil type has survived virtually UNCHANGED for ~500 million years?',
        'options' : ['Ammonite', 'Trilobite', 'T. rex Tooth', 'Nautiloid'],
        'answer'  : 3,
    },
    {
        'question': 'Which era did trilobites first appear?',
        'options' : ['Cambrian', 'Jurassic', 'Carboniferous', 'Cretaceous'],
        'answer'  : 0,
    },
    {
        'question': 'Ammonites are most closely related to which living animal?',
        'options' : ['Clams', 'Nautilus', 'Starfish', 'Sea urchins'],
        'answer'  : 1,
    }
]

# ── Scoring / Trophies ────────────────────────────────────────────────────────
FOSSIL_FOUND_POINTS      = 2   # per fossil successfully excavated
REMAINING_ATTEMPT_POINTS = 1   # per leftover attempt when BOTH fossils found

GOLD_THRESHOLD   = 150
SILVER_THRESHOLD = 100
BRONZE_THRESHOLD = 90

TROPHY_DATA = {
    'gold'  : {'label': 'Fossil Master',     'color': (255, 215,   0)},
    'silver': {'label': 'Fossil Expert',     'color': (192, 192, 192)},
    'bronze': {'label': 'Fossil Apprentice', 'color': (205, 127,  50)},
    'none'  : {'label': 'Try again next time :<',   'color': (150, 150, 150)},
}

# ── Colours ──────────────────────────────────────────────────────────────────
UI_BG_COLOR      = '#222222'
UI_BORDER_COLOR  = '#111111'
TEXT_COLOR       = '#EEEEEE'
BAR_COLOR        = '#1e1e1e'
HEALTH_COLOR     = 'green'
ENERGY_COLOR     = 'blue'
UI_ITEM_BG_COLOR = '#1a1a1a'
UPGRADE_BG_COLOR = '#1a1a1a'
