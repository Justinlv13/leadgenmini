#!/usr/bin/env python3
"""
Cold Email Engine — Automated Outreach for Lead Gen Services
Sends personalized cold emails at scale using templates.
"""
import csv
import random
import time
import os
from datetime import datetime


class ColdEmailEngine:
    """Send cold emails with personalization and tracking."""
    
    TEMPLATES = {
        "leadgen_service": """Subject: {company_name} — Quick lead list question

Hi {first_name},

I help {niche} businesses find more customers — fast.

I built a tool that scrapes targeted leads from Google Maps and delivers them in 24 hours.

For example, I could pull up to 200 {niche} leads in {city} with full contact details for $39.

Worth a quick look? Reply and I'll send a free sample of 5 leads, no strings attached.

Best,
Justin
P.S. — I can also do custom niches; just give me the keywords.
""",
        "free_tool": """Subject: Free tool: Validate your email lists instantly

Hi {first_name},

I built a free email validation tool that checks format + domain reachability.

No signup needed. Paste your list, get results in seconds.

Try it here: {tool_url}

If you need bulk validation (1000+ emails), my Pro plan handles that too — $19/month.

Cheers,
Justin
"""
    }
    
    def __init__(self):
        self.sent_emails = []
        
    def personalize(self, template_name, **kwargs):
        """Fill in template with kwargs."""
        template = self.TEMPLATES.get(template_name, template_name)
        return template.format(**kwargs)
    
    def generate_batch(self, prospects, template_name="leadgen_service"):
        """Generate personalized emails for a batch of prospects."""
        emails = []
        for prospect in prospects:
            email = self.personalize(template_name, **prospect)
            emails.append({
                "to": prospect.get("email", ""),
                "subject": email.split("\n")[0].replace("Subject: ", ""),
                "body": email,
                "prospect_name": prospect.get("first_name", ""),
                "company": prospect.get("company_name", ""),
                "status": "draft"
            })
        return emails
    
    def export_csv(self, emails, filename):
        """Export emails to CSV for manual sending or mail merge."""
        if not emails:
            return
        keys = emails[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            import csv as csv_module
            writer = csv_module.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(emails)
        print(f"✅ Exported {len(emails)} emails to {filename}")


if __name__ == "__main__":
    engine = ColdEmailEngine()
    
    # Demo: Generate sample emails
    sample_prospects = [
        {"first_name": "John", "company_name": "Acme Plumbing", "niche": "plumbing", "city": "Austin"},
        {"first_name": "Sarah", "company_name": "Bright Dental", "niche": "dentistry", "city": "Miami"},
    ]
    
    emails = engine.generate_batch(sample_prospects, "leadgen_service")
    engine.export_csv(emails, "outreach_campaign_1.csv")
    print("\n🎯 Cold email engine ready. Load real prospects and export for your mailer.")
