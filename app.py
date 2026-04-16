from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Define keyword categories with regex patterns
KEYWORDS = {
    "THREAT / ASSAULT": [
        r"\bkill\b", r"\bmurder\b", r"\bdie\b", r"\bdeath\b", r"\bassault\b",
        r"\battack\b", r"\bshoot\b", r"\bstab\b", r"\bsuicide\b", r"\bhang\b",
        r"\bhit\b", r"\bbeat\b", r"\bdestroy\b", r"\bhurt\b", r"\bpain\b",
        r"\bslaughter\b", r"\btorture\b"
    ],
    "VULGAR / OBSCENE": [
        r"\bfuck\b", r"\bshit\b", r"\bcrap\b", r"\bdamn\b", r"\bbitch\b",
        r"\bbastard\b", r"\bwhore\b", r"\bslut\b", r"\bdick\b", r"\bpussy\b",
        r"\bcunt\b", r"\basshole\b", r"\bfag\b", r"\bfaggot\b", r"\bprick\b"
    ],
    "INSULT": [
        r"\bstupid\b", r"\bidiot\b", r"\bdumb\b", r"\bmoron\b", r"\bfool\b",
        r"\bretard\b", r"\bloser\b", r"\bugly\b", r"\bfat\b", r"\bdumbass\b",
        r"\bimbecile\b", r"\bignorant\b", r"\bassface\b"
    ],
    "HATE SPEECH": [
        r"\bhate\b", r"\bhates\b", r"\bhated\b", r"\bhateful\b", r"\bracist\b",
        r"\bsexist\b", r"\bhomophobic\b", r"\bnazi\b", r"\bterrorist\b",
        r"\bwhite power\b", r"\bblack lives don't\b", r"\bkill all \b",
        r"\b(?:muslim|christian|jew|gay|lesbian|trans|black|white|asian)s? should\b"
    ]
}

# Also add single-word offensive list (for partial matching, but careful)
SINGLE_WORD_OFFENSIVE = [
    "fuck", "shit", "cunt", "bitch", "asshole", "bastard", "whore", "slut",
    "pussy", "dick", "cock", "tits", "damn", "hell", "piss", "crap", "assface"
]

def detect_toxicity(text):
    text_lower = text.lower()
    detected_categories = []
    max_score = 0
    primary_category = "CLEAN"
    
    # Check each category
    for category, patterns in KEYWORDS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                score = 0.95  # high confidence for matched keywords
                detected_categories.append({"category": category, "score": score})
                if score > max_score:
                    max_score = score
                    primary_category = category
                break  # once a pattern matches in this category, no need to check others in same category
    
    # Also check single word offensive list (for words like "fuck" not caught by word boundaries)
    for word in SINGLE_WORD_OFFENSIVE:
        if word in text_lower.split():  # exact word match
            score = 0.90
            # Determine which category it belongs to
            if word in ["fuck", "shit", "cunt", "bitch", "asshole", "bastard", "whore", "slut", "pussy", "dick", "cock", "tits", "damn", "hell", "piss", "crap"]:
                cat = "VULGAR / OBSCENE"
            else:
                cat = "OFFENSIVE"
            detected_categories.append({"category": cat, "score": score})
            if score > max_score:
                max_score = score
                primary_category = cat
    
    # Remove duplicates (keep highest score per category)
    unique = {}
    for item in detected_categories:
        cat = item["category"]
        if cat not in unique or item["score"] > unique[cat]["score"]:
            unique[cat] = item
    detected_categories = list(unique.values())
    
    if not detected_categories:
        return "CLEAN", 1.0, []
    else:
        return primary_category, max_score, detected_categories

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing "text" field'}), 400
        
        tweet_text = data['text']
        prediction, confidence, categories = detect_toxicity(tweet_text)
        
        return jsonify({
            'text': tweet_text,
            'prediction': prediction,
            'confidence': confidence,
            'categories': categories
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)