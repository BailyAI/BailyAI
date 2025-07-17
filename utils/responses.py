import random
from typing import Dict, Any

def get_random_greeting() -> str:
    """Get a random greeting message"""
    greetings = [
        "Schön, dich zu sehen! 😊",
        "Hallo! Wie geht's dir denn? 🌟",
        "Hey! Bereit für ein nettes Gespräch? 💫",
        "Hallo! Ich freue mich auf unser Gespräch! 😄",
        "Hi! Was gibt's Neues? 🎉",
        "Servus! Wie läuft dein Tag? ☀️",
        "Hallo! Lass uns quatschen! 💬"
    ]
    return random.choice(greetings)

def get_random_reaction() -> str:
    """Get a random reaction emoji/text"""
    reactions = [
        "😊", "😄", "🤔", "👍", "🎉", "💭", "🌟", "✨", "😇", "🙃"
    ]
    return random.choice(reactions)

def get_help_text() -> str:
    """Get formatted help text"""
    return """
🤖 <b>Baily Bot - Hilfe & Befehle</b>

<b>📋 Grundbefehle:</b>
• /start - Bot starten und begrüßen
• /help - Diese Hilfe anzeigen
• /whoami - Deine Benutzerinformationen anzeigen
• /cancel - Unterhaltung zurücksetzen

<b>🔧 Admin-Befehle:</b>
• /status - System-Status prüfen (nur Admin)
• /admin - Admin-Panel öffnen (nur Admin)
• /broadcast - Nachricht an alle senden (nur Admin)

<b>💬 Chat-Funktionen:</b>
• Schreibe einfach eine Nachricht und ich antworte!
• Ich verstehe verschiedene Themen wie Wetter, Essen, Musik und mehr
• Ich merke mir unsere Unterhaltung und antworte passend
• Ich erkenne Fragen und emotionale Ausdrücke

<b>🎯 Tipps:</b>
• Sprich mich einfach auf Deutsch an
• Stelle Fragen mit "wie", "was", "wo" etc.
• Erzähle mir von deinem Tag oder deinen Interessen
• Nutze /cancel um ein neues Gespräch zu beginnen

<b>🆘 Probleme?</b>
Falls etwas nicht funktioniert, versuche /start oder kontaktiere den Admin.

Viel Spaß beim Chatten! 😊
"""

def get_conversation_response(response_type: str, user_state: Dict[str, Any]) -> str:
    """Get contextual conversation response based on type and user state"""
    
    message_count = user_state.get('message_count', 0)
    
    responses = {
        'question': [
            "Das ist eine interessante Frage! 🤔 Lass mich überlegen...",
            "Hmm, gute Frage! 💭 Was denkst du denn darüber?",
            "Das fragst du mich? 😄 Ich bin gespannt auf deine Meinung dazu!",
            "Interessant! 🌟 Erzähl mir mehr über deine Gedanken dazu.",
            "Das ist eine wichtige Frage! 🎯 Hast du schon eine Idee?"
        ],
        'positive': [
            "Das freut mich total zu hören! 😊 Erzähl mir mehr davon!",
            "Wie schön! 🌟 Ich liebe es, wenn Menschen glücklich sind!",
            "Das ist fantastisch! 🎉 Du strahlst richtig positive Energie aus!",
            "Wunderbar! 😄 Solche Nachrichten machen auch mich glücklich!",
            "Das ist toll! ✨ Ich bin so froh für dich!"
        ],
        'negative': [
            "Oh nein, das tut mir leid zu hören. 😔 Möchtest du darüber reden?",
            "Das klingt nicht so gut... 💙 Ich bin da, wenn du reden willst.",
            "Manchmal läuft es nicht so, wie wir wollen. 🤗 Aber morgen ist ein neuer Tag!",
            "Das ist wirklich schade. 😞 Vielleicht kann ich dir helfen oder einfach zuhören?",
            "Ich verstehe, dass das schwer ist. 💭 Lass uns zusammen eine Lösung finden."
        ],
        'wetter': [
            "Das Wetter ist immer ein Thema! ☀️ Wie ist es denn bei dir gerade?",
            "Ah, das Wetter! 🌤️ Ich hoffe, es ist schön bei dir!",
            "Wetter kann die Stimmung wirklich beeinflussen! 🌈 Magst du den heutigen Tag?",
            "Das deutsche Wetter ist ja immer für Überraschungen gut! 😄",
            "Wetterkapriolen sind typisch für uns! 🌦️ Hauptsache, du bleibst trocken!"
        ],
        'essen': [
            "Mmm, Essen! 🍽️ Ich liebe es, über Kulinarisches zu sprechen!",
            "Essen ist so wichtig! 😋 Was ist denn dein Lieblingsgericht?",
            "Kochen oder bestellen? 👨‍🍳 Beide haben ihre Vorzüge!",
            "Essen verbindet Menschen! 🥘 Hast du schon mal etwas Neues probiert?",
            "Lecker! 🍕 Jetzt bekomme ich auch Hunger!"
        ],
        'musik': [
            "Musik ist Leben! 🎵 Welche Richtung hörst du gerne?",
            "Musik kann so viel bewirken! 🎶 Gibt es einen Song, der dich bewegt?",
            "Ohne Musik wäre das Leben langweilig! 🎸 Spielst du auch ein Instrument?",
            "Musik ist die Sprache der Seele! 🎤 Was läuft gerade bei dir?",
            "Toller Musikgeschmack! 🎧 Lass uns über deine Lieblingskünstler sprechen!"
        ],
        'sport': [
            "Sport ist super! 💪 Welche Sportart machst du gerne?",
            "Bewegung ist so wichtig! 🏃‍♂️ Fühlst du dich fit?",
            "Sport verbindet und macht Spaß! ⚽ Verfolgst du auch Profi-Sport?",
            "Aktiv zu sein ist toll! 🏋️‍♀️ Wie hältst du dich fit?",
            "Sport macht glücklich! 🏆 Hast du schon mal an einem Wettkampf teilgenommen?"
        ],
        'arbeit': [
            "Arbeit kann erfüllend sein! 💼 Wie läuft es bei dir im Job?",
            "Der Beruf nimmt viel Zeit ein! 🏢 Machst du gerne, was du tust?",
            "Work-Life-Balance ist wichtig! ⚖️ Findest du genug Zeit für dich?",
            "Arbeit und Freizeit in Balance! 📊 Wie schaffst du das?",
            "Beruflich unterwegs! 🚀 Erzähl mir von deinen Projekten!"
        ],
        'general': [
            "Interessant! 💭 Erzähl mir mehr davon!",
            "Das klingt spannend! 🌟 Wie siehst du das denn?",
            "Aha! 😊 Ich höre gerne zu - red weiter!",
            "Cool! 👍 Was beschäftigt dich noch so?",
            "Verstehe! 🤔 Hast du noch mehr zu erzählen?",
            "Das ist schön zu hören! 😄 Ich bin ganz Ohr!",
            "Wow! ✨ Du hast immer interessante Geschichten!",
            "Faszinierend! 🎯 Ich lerne gerne neue Dinge von dir!"
        ]
    }
    
    # Add personalization based on message count
    if message_count > 10:
        personal_additions = [
            " Du redest gerne mit mir, das finde ich toll! 😊",
            " Ich merke, wir verstehen uns gut! 💫",
            " Unsere Gespräche sind immer interessant! 🌟"
        ]
        base_response = random.choice(responses.get(response_type, responses['general']))
        if random.random() < 0.3:  # 30% chance
            base_response += random.choice(personal_additions)
        return base_response
    
    return random.choice(responses.get(response_type, responses['general']))
