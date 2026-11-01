# -*- coding: utf-8 -*-
import json, os

bundle_path = r'C:\Users\natan\Desktop\antigravity-explorer\bundle.json'
with open(bundle_path, 'r', encoding='utf-8') as f:
    bundle = json.load(f)

items = bundle['items']
print(f"Loaded {len(items)} items from bundle.json")

everyday_cats = {'slash', 'core', 'workspace', 'agents', 'dev', 'extra'}
# Special items in cloud that are useful for everyone
everyday_extra_ids = {'bigquery-sql', 'google-cloud-storage-basics', 'building-data-apps'}

updated_everyday = 0
updated_niche = 0

for it in items:
    cat = it.get('c', '')
    if cat in everyday_cats or it.get('id') in everyday_extra_ids:
        it['tier'] = 'everyday'
        updated_everyday += 1
    else:
        it['tier'] = 'niche'
        updated_niche += 1

print(f"Assigned tiers: {updated_everyday} everyday, {updated_niche} niche")

# Ensure wizard has rich recommendations
wiz_recs = {
    "🌐 לבנות אתר, אפליקציה או כלי אינטראקטיבי": [
        {"id": "grill-me", "n": "חידוד רעיונות (/grill-me)"},
        {"id": "plan", "n": "תכנון חכם (/plan)"},
        {"id": "goal", "n": "טייס אוטומטי (/goal)"},
        {"id": "generative_ui", "n": "ממשקים חיים (/generative_ui)"},
        {"id": "browser", "n": "בדיקה בדפדפן (/browser)"}
    ],
    "📅 לנהל יומן, מסמכים, אקסלים ומצגות בגוגל": [
        {"id": "gcalendar", "n": "יומן גוגל (gcalendar)"},
        {"id": "gdrive", "n": "גוגל דרייב (gdrive)"},
        {"id": "gdocs", "n": "גוגל דוקס (gdocs)"},
        {"id": "gsheets", "n": "גוגל שיטס (gsheets)"},
        {"id": "gslides", "n": "גוגל מצגות (gslides)"}
    ],
    "🐛 לתקן תקלה מעצבנת או לשפר קוד קיים": [
        {"id": "boost", "n": "מועצת מומחים (/boost)"},
        {"id": "browser", "n": "דפדפן חי (/browser)"},
        {"id": "diff", "n": "השוואת שינויים (/diff)"},
        {"id": "rewind", "n": "חזרה בזמן (/rewind)"},
        {"id": "learn", "n": "שמירת לקחים (/learn)"}
    ],
    "👥 להריץ פרויקט ענק במהירות שיא עם כמה סוכנים": [
        {"id": "teamwork", "n": "צוות סוכנים (/teamwork)"},
        {"id": "run-workflow", "n": "הרצת תהליכים (/run-workflow)"},
        {"id": "remote-control", "n": "שליטה מהטלפון (/remote-control)"}
    ],
    "📱 לפתח לאנדרואיד או לשלב יכולות AI של Gemini": [
        {"id": "android-device-hub", "n": "אמולטור אנדרואיד חי"},
        {"id": "compose-preview", "n": "תצוגת Compose"},
        {"id": "gemini-api-dev", "n": "Gemini API"},
        {"id": "gemini-live-api-dev", "n": "Gemini Live קול ווידאו"}
    ],
    "☁️ לנתח דאטה, BigQuery או מחקר מדעי": [
        {"id": "building-data-apps", "n": "דשבורד נתונים חי"},
        {"id": "bigquery-sql", "n": "שאילתות BigQuery"},
        {"id": "literature-search-arxiv", "n": "חיפוש מאמרים ב-arXiv"},
        {"id": "pubmed-database", "n": "מאגר רפואי PubMed"}
    ]
}

for w in bundle.get('wizard', []):
    goal = w.get('goal', '')
    for k, v in wiz_recs.items():
        if k in goal or goal in k:
            w['recList'] = v
            break

with open(bundle_path, 'w', encoding='utf-8') as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)

print(f"Successfully saved updated bundle.json ({os.path.getsize(bundle_path)} bytes)")
