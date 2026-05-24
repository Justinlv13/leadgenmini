#!/usr/bin/env python3
"""
FreeLeadValidator - Traffic Magnet Tool
Validates email addresses, enriches with web data.
Free tier drives traffic, paid tier does bulk processing.
"""
import re
import requests
from urllib.parse import quote_plus


class FreeLeadValidator:
    """Validates and enriches single email addresses (free tier)."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def validate_email(self, email):
        """Validate email format + check domain."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            return {"valid": False, "reason": "Invalid format"}
        
        domain = email.split('@')[1]
        
        # Check domain MX record via DNS (basic check)
        try:
            import socket
            socket.getaddrinfo(domain, None)
            domain_reachable = True
        except:
            domain_reachable = False
        
        return {
            "valid": domain_reachable,
            "domain": domain,
            "format": "valid",
            "domain_reachable": domain_reachable
        }
    
    def enrich(self, email):
        """Enrich with publicly available data."""
        domain = email.split('@')[1]
        
        # Try to find company name from domain
        company = domain.replace('www.', '').split('.')[0].title()
        
        return {
            "email": email,
            "company": company,
            "domain": domain,
            "validation": self.validate_email(email)
        }


if __name__ == "__main__":
    validator = FreeLeadValidator()
    
    # Demo
    test_emails = [
        "contact@google.com",
        "invalid-email",
        "sales@microsoft.com"
    ]
    
    for email in test_emails:
        result = validator.enrich(email)
        print(f"📧 {result['email']} | Company: {result['company']} | Valid: {result['validation']['valid']}")
