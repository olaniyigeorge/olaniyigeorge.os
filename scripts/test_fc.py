#!/usr/bin/env python3
"""Firecrawl connectivity probe — remove if not using Firecrawl."""
import sys
sys.path.insert(0, "C:/nvm4w/nodejs/node_modules/firecrawl")
try:
    import dist.index as fc
    print("firecrawl loaded:", hasattr(fc, "Murk") or hasattr(fc, "default"))
except Exception as e:
    print("firecrawl probe failed:", e)
    sys.exit(1)
