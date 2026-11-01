# -*- coding: utf-8 -*-
import json, sys

b = json.load(open(r'C:\Users\natan\Desktop\antigravity-explorer\bundle.json', encoding='utf-8'))
items = b['items']
print(f"Total items in bundle: {len(items)}")

fields = ['id', 'n', 'en', 'e', 'c', 'simple', 'desc', 'caps', 'steps', 'prompts', 'when', 'tips', 'tier']
missing = {f: 0 for f in fields}

short_simple = 0
empty_prompts = 0
empty_steps = 0
empty_tips = 0
empty_when = 0

for it in items:
    for f in fields:
        if not it.get(f):
            missing[f] += 1
    if len(it.get('simple', '')) < 10:
        short_simple += 1
    if not it.get('prompts') or len(it['prompts']) == 0:
        empty_prompts += 1
    if not it.get('steps') or len(it['steps']) == 0:
        empty_steps += 1
    if not it.get('tips') or len(it['tips']) == 0:
        empty_tips += 1
    if not it.get('when') or len(it['when']) == 0:
        empty_when += 1

print("Missing count by field:", missing)
print(f"Short simple (<10 chars): {short_simple}")
print(f"Empty prompts: {empty_prompts}")
print(f"Empty steps: {empty_steps}")
print(f"Empty tips: {empty_tips}")
print(f"Empty when: {empty_when}")

# Check wizard items
print("\n--- Wizard Check ---")
for w in b.get('wizard', []):
    rec = w.get('rec', '')
    print(f"Goal: {w.get('goal')[:30]}... | Rec: {rec}")

# Check recipes
print("\n--- Recipes Check ---")
for r in b.get('recipes', []):
    print(f"Recipe: {r.get('title')[:35]}... | Steps: {r.get('steps')}")

# Check onboarding
print(f"\nTotal Onboarding cards: {len(b.get('onboarding', []))}")
