#!/usr/bin/env python3
"""
Reddit/IndieHackers Post Generator
Generates marketing content for community posts.
"""

def generate_reddit_post(title, description, url):
    """Generate a Reddit post for a product launch."""
    post = f"""
**{title}**

{description}

I built this thing solo in about a day and it's already pulling leads. Happy to answer questions or take feature requests.

{url}

#sidehustle #leadgeneration #automation #SaaS
"""
    return post.strip()

def generate_indiehackers_post(title, description, url):
    """Generate an IndieHackers post."""
    post = f"""
## {title}

{description}

I built this to scratch my own itch. Tired of paying $200+ for lead lists that were outdated. Built a scraper in Python, packaged it as a service, testing pricing at $39 per list.

**What's working:** Direct outreach to agencies and consultants.

**Next moves:** Building a free tool to drive traffic. Considering a SaaS subscription model.

Would love feedback from the IH community on pricing and positioning.

{url}
"""
    return post.strip()

# Generate specific post ideas
if __name__ == "__main__":
    posts = [
        generate_reddit_post(
            "Built a lead scraper that finds 200 targeted business contacts in 24 hours — $39 per list",
            "I've been scraping Google Maps + enriching with web data to build targeted lead lists for niche businesses (dentists, plumbers, SaaS, etc.). Each $39 list includes: up to 200 leads, CSV + VCF format, name, phone, email where available. Currently testing with agencies and solo salespeople.",
            "https://leadgenmini.com"
        ),
        generate_indiehackers_post(
            "Launched a $39 lead scraping service — testing $1k MRR",
            "Bootstrapped a lead generation tool that scrapes niche business leads from Google Maps + enriches with contact info. Currently at $0 MRR but just sent first batch of outreach.",
            "https://leadgenmini.com"
        )
    ]
    
    for i, post in enumerate(posts, 1):
        print(f"\n{'='*60}")
        print(f"POST {i}")
        print(f"{'='*60}")
        print(post)
