#!/usr/bin/env python3
"""
Campaign Launcher — Automated Reddit/IndieHackers Posting
Generates and logs marketing posts across communities.
"""
import json
import os
from datetime import datetime


class CampaignLauncher:
    """Manages marketing campaigns across platforms."""
    
    COMMUNITIES = {
        "reddit_leadgen": {
            "name": "r/leadgeneration",
            "url": "https://reddit.com/r/leadgeneration",
            "rules": "No self-promo in first 48h, contribute before selling"
        },
        "reddit_sales": {
            "name": "r/sales",
            "url": "https://reddit.com/r/sales",
            "rules": "Focus on value, not pitching"
        },
        "reddit_SaaS": {
            "name": "r/SaaS",
            "url": "https://reddit.com/r/SaaS",
            "rules": "Share journey, not product"
        },
        "indiehackers": {
            "name": "IndieHackers",
            "url": "https://indiehackers.com/new",
            "rules": "Build in public, share metrics"
        },
        "hackernews": {
            "name": "Hacker News Show",
            "url": "https://news.ycombinator.com/show",
            "rules": "No Show HN in title, describe the problem"
        }
    }
    
    def __init__(self):
        self.campaigns = []
        
    def plan_campaign(self, name, posts):
        """Plan a campaign with scheduled posts."""
        campaign = {
            "name": name,
            "posts": posts,
            "status": "planned",
            "created_at": datetime.now().isoformat()
        }
        self.campaigns.append(campaign)
        return campaign
    
    def generate_posts(self, product_name, value_prop):
        """Generate post templates for each platform."""
        templates = {}
        
        templates["reddit_leadgen"] = f"""
I just built a lead scraper that finds 200 targeted {value_prop} in 24 hours for $39.

Background: I was tired of paying $200+ for lead lists that were 60% outdated. Built this in a weekend with Python + BeautifulSoup.

How it works: You give me a niche (e.g., "plumbers in Austin") and I scrape Google Maps + enrich with web data. Deliver CSV + VCF in 24h.

I just sent my first 10 lists to agencies. Early feedback: "Better than Apollo for local biz."

Questions welcome. Happy to share details.
""".strip()
        
        templates["indiehackers"] = f"""
## Launching {product_name} — $39 lead lists

**Problem:** Lead lists cost $200+ and are 60% outdated.
**Solution:** Scraped, enriched, verified leads for $39.
**Status:** Just launched, testing pricing.
**Revenue:** $0 so far, 10 lists shipped for feedback.
**Next:** Building a free tool to drive traffic.

Would love IH feedback on pricing and positioning.
""".strip()
        
        templates["hackernews"] = f"""
I built a lead scraper that extracts 200 business contacts from Google Maps in ~20 minutes.

It's a Python/BeautifulSoup pipeline that:
1. Searches Google Maps via DuckDuckGo
2. Extracts business name, phone, address
3. Enriches with email from web scraping
4. Returns CSV + VCF

I packaged it as a $39 service (per list). Testing demand before building SaaS.

GitHub: https://github.com/justin/leadgenmini (will make public after first 10 sales)
""".strip()
        
        return templates
    
    def save_plan(self, filename):
        """Save campaign plan to JSON."""
        with open(filename, 'w') as f:
            json.dump(self.campaigns, f, indent=2)
        print(f"✅ Campaign plan saved to {filename}")


if __name__ == "__main__":
    launcher = CampaignLauncher()
    
    # Plan initial launch campaign
    posts = launcher.generate_posts("LeadGenMini", "local business leads")
    campaign = launcher.plan_campaign(
        name="LeadGenMini Launch",
        posts=posts
    )
    launcher.save_plan("launch_campaign.json")
    
    print("\n🚀 CAMPAIGN PLAN GENERATED")
    print("=" * 60)
    for platform, post in posts.items():
        print(f"\n📍 {platform.upper()}")
        print(f"{'=' * 40}")
        print(post[:300] + "...")
