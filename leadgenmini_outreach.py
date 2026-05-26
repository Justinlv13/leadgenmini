#!/usr/bin/env python3
"""
LeadGenMini — Daily Cold Email Outreach
Sends 20 emails/day to leads that haven't been contacted.
Uses same SMTP infrastructure as QuickBookedAI (Zoho via OUTBOUND_PASS).
"""

import os
import sys
import csv
import time
import random
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# ── Load env from QuickBookedAI backend ─────────────────────────
env_path = '/home/justin/projects/backend/.env'
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()

# Also load Supabase URL from backend .env if available
supabase_url = os.environ.get('SUPABASE_URL', '')
supabase_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '')

# ── CONFIG ──────────────────────────────────────────────────────
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.environ.get("OUTBOUND_USER", "justin@getquickbookedai.com")
SMTP_PASS = os.environ.get("OUTBOUND_PASS", "")
FROM_NAME = "Justin | LeadGenMini"
FROM_EMAIL = "justin@getquickbookedai.com"
DAILY_MAX = 20
DELAY_BETWEEN_EMAILS = (90, 180)  # random seconds

LOG_FILE = f"/home/justin/workspace/leadgenmini_outreach_{datetime.now().strftime('%Y%m%d')}.csv"
SENT_LOG = "/home/justin/workspace/leadgenmini_sent_log.csv"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if not SMTP_PASS:
    logger.error("❌ OUTBOUND_PASS not set. Check backend .env")
    sys.exit(1)


# ── EMAIL TEMPLATES ─────────────────────────────────────────────
def get_email_sequence(business_name, niche, city, email_num):
    niche_display = niche.replace('_', ' ').title()

    sequences = {
        1: {
            "subject": f"{business_name} — quick question about your lead gen",
            "body": f"""Hi there,

I help {niche_display} businesses find more customers without paying $500+/month for agencies.

I built a tool that scrapes targeted local business leads from Google Maps and delivers them as a CSV within 24 hours.

For example, I could pull 100 {niche_display} leads in {city} with full contact details — name, phone, email, website — for $39 flat.

Worth a quick look? Reply and I'll send a free sample of 5 leads from your area.

Best,
Justin
LeadGenMini
https://bootstrapleadgen.netlify.app/"""
        },
        2: {
            "subject": f"Re: {business_name} — quick question about your lead gen",
            "body": f"""Hi there,

Just circling back on my last email.

If a free sample of local {niche_display} leads would be helpful, just reply "SEND" and I'll drop 5 leads from {city} in your inbox.

No commitment. No spam. Just data.

Best,
Justin
LeadGenMini"""
        },
        3: {
            "subject": f"How a {niche_display} in {city} got 12 new leads for $39",
            "body": f"""Hi there,

Quick case study:

A {niche_display} in {city} bought a targeted lead list for $39. They sent a simple 3-email sequence to 100 leads.

Result: 12 qualified leads, 3 conversions in the first month.

If you want to try it, reply "SEND" and I'll send 5 free leads from your area.

Best,
Justin
LeadGenMini
https://bootstrapleadgen.netlify.app/"""
        },
        4: {
            "subject": f"Last email — free leads for {business_name}",
            "body": f"""Hi there,

This is my last email. I don't want to clutter your inbox.

If you ever need targeted local leads, here's the short version:

- You pick a niche + city
- I deliver 50-100 verified leads with contact details
- $39 flat, no subscriptions
- Delivered within 24 hours

Get a free 5-lead sample: https://bootstrapleadgen.netlify.app/

If you're not interested, no worries — just reply "stop" and I'll remove you.

Best,
Justin
LeadGenMini"""
        },
    }
    return sequences.get(email_num, sequences[1])


# ── SMTP FUNCTIONS ──────────────────────────────────────────────
def create_smtp_connection():
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        logger.info("✅ SMTP connection established")
        return server
    except Exception as e:
        logger.error(f"❌ SMTP connection failed: {e}")
        raise


def send_email(smtp_server, to_email, subject, body):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = Header(subject, 'utf-8')
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        smtp_server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        logger.info(f"✅ Sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send to {to_email}: {e}")
        return False


def log_sent(email, business_name, email_num, status, error_msg=''):
    file_exists = os.path.exists(SENT_LOG)
    with open(SENT_LOG, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'email', 'business_name', 'email_num', 'status', 'error'])
        writer.writerow([datetime.now().isoformat(), email, business_name, email_num, status, error_msg])


# ── LOAD LEADS ──────────────────────────────────────────────────
def load_leads():
    """Load leads from Supabase that have emails and haven't been contacted."""
    try:
        import requests
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}',
        }

        # Get leads with emails
        resp = requests.get(
            f"{supabase_url}/rest/v1/leadgenmini_leads?select=id,business_name,email,niche,city&not=email.is.null&neq=email=&limit=500",
            headers=headers, timeout=10
        )
        all_leads = resp.json()

        # Get already-contacted leads from sent log
        sent_emails = set()
        if os.path.exists(SENT_LOG):
            with open(SENT_LOG, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('status') == 'sent':
                        sent_emails.add(row['email'])

        # Filter to new leads only
        new_leads = [l for l in all_leads if l.get('email') and l['email'] not in sent_emails]
        return new_leads

    except Exception as e:
        logger.error(f"Error loading leads: {e}")
        return []


# ── MAIN ────────────────────────────────────────────────────────
def main():
    logger.info("🚀 LeadGenMini Outreach Engine starting...")

    leads = load_leads()
    if not leads:
        logger.info("✅ No new leads to email. All caught up.")
        return

    logger.info(f"📊 {len(leads)} leads ready for outreach")

    smtp = create_smtp_connection()
    sent_today = 0

    for lead in leads[:DAILY_MAX]:
        email = lead['email']
        name = lead['business_name']
        niche = lead.get('niche', 'service')
        city = lead.get('city', 'South Africa')

        subject, body = get_email_sequence(name, niche, city, 1)
        success = send_email(smtp, email, subject, body)

        if success:
            log_sent(email, name, 1, 'sent')
            sent_today += 1
        else:
            log_sent(email, name, 1, 'failed', 'send failed')

        delay = random.randint(*DELAY_BETWEEN_EMAILS)
        logger.info(f"⏳ Waiting {delay}s before next send...")
        time.sleep(delay)

    smtp.quit()
    logger.info(f"✅ Outreach complete. {sent_today} emails sent today.")


if __name__ == "__main__":
    main()
