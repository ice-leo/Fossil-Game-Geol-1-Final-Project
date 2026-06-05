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
        'dialogue_idle': "Hello, Sir Leo! Please complete my task three times >:)\nTask: Click on soil blocks to excavate fossils.\nPoints: 2 for each fossil, plus 1 for each leftover attempts!",
        'dialogue_done': "You've excavated all three sites. Proceed to Prof. Stratum for the quiz!",
        'speed'        : 0,
        'health'       : 100,
        'graphic'      : 'graphics/monsters/bamboo/idle', # <-- UPDATED PATH
    },
    'quiz_npc': {
        'name'         : 'Prof. Stratum',
        'dialogue_idle': "Hello, Sir Leo! Study the Fossildex then come take my quiz!\nPoints: 2 for each correct answer!",
        'dialogue_locked': "Complete all excavation levels first!",
        'dialogue_done': "You've already completed the game. Congratulations!",
        'speed'        : 0,
        'health'       : 100,
        'graphic'      : 'graphics/monsters/squid/idle', # <-- UPDATED PATH
    }
}
# ── Excavation Grid ──────────────────────────────────────────────────────────
EXC_COLS        = 12      # grid columns
EXC_ROWS        = 9       # grid rows
EXC_CELL_SIZE   = 56      # pixels per cell
EXC_MAX_ATTEMPTS = 60

# ── Fossil Data ───────────────────────────────────────────────────────────────

# ── Quiz ──────────────────────────────────────────────────────────────────────
QUIZ_POINTS_PER_CORRECT = 2

QUIZ_QUESTIONS = [
    {
        'question': 'Where did the trilobites live?',
        'options' : ['Forests', 'Deserts', 'Oceans', 'Mountains'],
        'answer'  : 2,
    },
    {
        'question': 'What body feature did trilobites have?',
        'options' : ['Feather', 'Three-lobed Exoskeleton', 'Fur', 'Wings'],
        'answer'  : 1,
    },
    {
        'question': 'What type of animal was the ammonite?',
        'options' : ['Marine mollusc', 'Dinosaur', 'Bird', 'Insect'],
        'answer'  : 0,
    },
    {
        'question': 'What are ammonites known for?',
        'options' : ['Their feathers', 'Their tightly coiled shells', 'Their long legs', 'Their sharp teeth'],
        'answer'  : 1,
    },
    {
        'question': 'What rare metal found in clay layer helps scientists date the extinction of the T. Rex?',
        'options' : ['Gold', 'Iridium', 'Iron', 'Copper'],
        'answer'  : 1,
    },
    {
        'question': 'Which modern animals are the closest surviving relatives of the Tyrannosaurus?',
        'options' : ['Lizards', 'Crocodiles', 'Birds', 'Snakes'],
        'answer'  : 2,
    },
    {
        'question': 'Where did the last isolated population of mammoths survive until 1650 B.C.?',
        'options' : ['China', 'Greenland', 'Alaska', 'Wrangel Island'],
        'answer'  : 3,
    },
    {
        'question': 'What is the name of the theory that claims humans hunted mammoths to extinction?',
        'options' : ['The Climate Theory', 'The Overkill Hypothesis', 'The Ice Age Theory', 'The Bottleneck Hypothesis'],
        'answer'  : 1,
    },
    {
        'question': 'Why is amber important to scientists?',
        'options' : ['It creates electricity', 'It preserves ancient organisms', 'It produces oxygen'],
        'answer'  : 1,
    },
    {
        'question': 'What do scientists conclude from archaeopteryx fossils?',
        'options' : ['Birds evolved from reptiles', 'Reptiles evolved from fish', 'Mammals evolved from birds', 'Dinosaurs never existed'],
        'answer'  : 0,
    },
    {
        'question': 'Why is archaeopteryx important?',
        'options' : ['It is the largest dinosaur discovered', 'It links reptiles and birds', 'It lived underwater', 'It had no feathers'],
        'answer'  : 1,
    },
    {
        'question': 'What sometimes became trapped inside fresh resin?',
        'options' : ['Large dinosaurs', 'Primates', 'Intact DNA', 'Small organisms'],
        'answer'  : 3,
    }
]

# ── Scoring / Trophies ────────────────────────────────────────────────────────
FOSSIL_FOUND_POINTS      = 2   # per fossil successfully excavated
REMAINING_ATTEMPT_POINTS = 1   # per leftover attempt when BOTH fossils found

GOLD_THRESHOLD   = 140
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
