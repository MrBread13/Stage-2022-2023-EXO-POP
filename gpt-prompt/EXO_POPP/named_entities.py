"""
Dictionnaire de correspondance entre les émojis utilisés annotant le début d'une entité nommée et ceux annotant la fin de l'entité nommée.
On a également la signification de l'entité nommée en commentaire.
"""
MATCHING_NAMED_ENTITY_TOKENS = {
    "📖": "📕",  # admin
    "👨": "👦",  # mari
    "👰": "👧",  # epouse
    "🥸": "🧐",  # temoin
    "👴": "🎩",  # père
    "👵": "👒",  # mère
    "👹": "😡",  # ex-epoux
    "🏥": "👶",  # naissance
    "🏠": "🏡",  # residence
    "⌛": "⏳",  # age
    "🔧": "🪛",  # profession
    "💬": "🗯",  # prénom
    "🗨": "💭",  # nom
    "🏳": "🏴",  # pays
    "🗺": "📌",  # departement
    "🌇": "🌉",  # ville
    "🔟": "🔢",  # numéro voie
    "🛣": "🛤",  # type voie
    "🔠": "🔡",  # nom voie
    "🗓": "🎉",  # annee
    "📅": "📆",  # mois
    "🌞": "🌝",  # jour
    "⏰": "⌚",  # heure
    "🕑": "🕘",  # minute
    "🪦": "⚰",  # décès
    "😢": "😭",  # veuf
    "🔎": "🔍",  # disparu
}
