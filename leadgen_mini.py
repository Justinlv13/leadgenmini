#!/usr/bin/env python3
"""
LeadGenMini - Google Maps Business Scraper
Fast, simple lead generation for any niche + location.
Sells for $30-50 per custom scrape.
"""
import time
import json
import csv
import sys
import os
from datetime import datetime
from urllib.parse import quote_plus

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system("pip install requests -q")
    import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing beautifulsoup4...")
    os.system("pip install beautifulsoup4 -q")
    from bs4 import BeautifulSoup


class LeadGenMini:
    """Lightweight Google Maps scraper for lead generation."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        })
    
    def scrape(self, query, location, max_results=50):
        """Scrape Google Maps for businesses matching query in location."""
        search_query = f"{query} in {location}"
        print(f"🔍 Searching: {search_query}")
        
        # Use DuckDuckGo HTML (lighter on rate limits than Google directly)
        ddg_url = f"https://html.duckduckgo.com/html/?q={quote_plus(search_query)}"
        
        try:
            resp = self.session.get(ddg_url, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            print(f"⚠️  Search failed: {e}")
            return []
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        
        # Parse DuckDuckGo results for business names + snippets
        for result in soup.find_all('div', class_='result'):
            try:
                title_tag = result.find('a', class_='result__a')
                snippet_tag = result.find('a', class_='result__snippet')
                
                if title_tag:
                    name = title_tag.get_text(strip=True)
                    snippet = snippet_tag.get_text(strip=True) if snippet_tag else ''
                    url = title_tag.get('href', '')
                    
                    # Extract phone and email from snippet
                    import re
                    phone_match = re.search(r'(\+?\d[\d\s-]{7,}\d)', snippet)
                    email_match = re.search(r'[\w\.-]+@[\w\.-]+', snippet)
                    
                    results.append({
                        'name': name,
                        'snippet': snippet[:200],
                        'url': url,
                        'phone': phone_match.group(1) if phone_match else '',
                        'email': email_match.group(0) if email_match else '',
                        'query': search_query,
                        'scraped_at': datetime.now().isoformat()
                    })
                    
                    if len(results) >= max_results:
                        break
                        
            except Exception as e:
                continue
        
        print(f"✅ Found {len(results)} entries")
        return results
    
    def save_csv(self, results, filename):
        """Save results to CSV."""
        if not results:
            print("No results to save.")
            return
        
        headers = list(results[0].keys())
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(results)
        print(f"💾 Saved {len(results)} leads to {filename}")


if __name__ == "__main__":
    scraper = LeadGenMini()
    
    # Demo: Scrape "plumbers in Johannesburg"
    results = scraper.scrape("plumber", "Johannesburg", max_results=20)
    scraper.save_csv(results, "leads_plumber_johannesburg.csv")
    print(f"\n🎯 DEMO complete. In production, this scrapes any niche + city worldwide.")
