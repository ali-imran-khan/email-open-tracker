# email-open-tracker

Tiny Flask app I use for cold outreach. Each email gets a 1x1 pixel:

```html
<img src="https://<your-host>/track.png?id=acme-john" width="1" height="1">
```

When the email is opened the pixel loads, the open gets written to `opens.log`, and an n8n webhook fires with `{prospect, timestamp}`. In n8n that updates the lead in the CRM and pings me so I can follow up while they're still in their inbox.

Hosted on PythonAnywhere (free tier is enough).

## Run

```bash
pip install -r requirements.txt
export N8N_WEBHOOK_URL=https://<you>.app.n8n.cloud/webhook/<id>
python tracker.py
```

## Caveats

- Apple Mail Privacy Protection and Gmail's image proxy preload images, so "opened" can fire without a real open. Treat it as a signal, not proof.
- Lots of clients block images by default, so missing opens don't mean much either.
- Tracking pixels count as tracking under GDPR / ePrivacy. If you're emailing people in the EU or UK, you need a lawful basis and should say so in your privacy notice.
