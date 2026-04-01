# 9 Biased
### See All Sides. Know the Facts.

AI powered daily newsletter that maps political bias, analytical depth, and shared facts across news sources, helping readers cut through spin and understand what's actually happening.

---

## What It Does

Every day, 9Biased automatically:

1. **Fetches** articles from 20+ news outlets spanning left, center, and right-leaning sources
2. **Clusters** them into the top 3 stories of the day using the Claude API
3. **Analyzes** each story — scoring every article on a 0–1 scale from pure opinion to pure analysis, extracting shared facts, and writing a neutral framing contrast
4. **Renders** a polished HTML newsletter with a 6-cell coverage map
5. **Sends** it to subscribers via Gmail SMTP

---

## Newsletter Components

| Section | What It Shows |
|---|---|
| **Header & Legend** | Date, color key (Blue = Left, Gray = Center, Red = Right), border key (Solid = Analytical, Dashed = Opinion) |
| **Coverage Map** | 6-cell grid: Left / Center / Right × Analytical / Opinion — see bias at a glance |
| **Source Breakdown** | Per-source bias tag, analytical score (%), and one-sentence reasoning |
| **Shared Factual Core** | 3–5 bullet points every source agrees on regardless of framing |
| **Framing Contrast** | Two neutral sentences on how left vs. right outlets frame the story differently |

---

## Project Structure

```
├── run.py              # Main entry point — orchestrates the full pipeline
├── fetcher.py          # Pulls articles from NewsAPI (4 targeted calls)
├── classifier.py       # Claude API: clustering, scoring, fact extraction
├── renderer.py         # Builds the HTML newsletter (coverage map, story blocks)
├── sender.py           # Gmail SMTP delivery
├── sources.py          # Master list of outlets with bias classifications
├── .env.example        # Environment variable template
└── requirements.txt    # Python dependencies
```

---

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/your-username/9-nein-biased.git
cd 9-nein-biased
pip3 install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in:

```env
ANTHROPIC_API_KEY=sk-ant-api03-...       # console.anthropic.com → API Keys
NEWS_API_KEY=your_newsapi_key            # newsapi.org/register (free tier)
GMAIL_USER=yourname@gmail.com            # Your Gmail address
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx  # Google App Password (see below)
RECIPIENTS=email1@example.com,email2@example.com
```

### 3. Gmail App Password

Gmail requires an App Password (not your regular password) for SMTP:

1. Enable 2-Factor Authentication on your Google account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Generate a new App Password and paste it into `.env`

> **Note:** Google Workspace / school accounts may not support App Passwords. Use a personal `@gmail.com` account.

---

## Usage

```bash
# Generate newsletter + send to all recipients
python3 run.py

# Generate HTML file only (no email sent) — good for testing
python3 run.py --save-only

# Generate and open in browser
python3 run.py --preview
```

### Schedule daily sends (cron)

```bash
# Send every day at 7:00 AM
0 7 * * * cd /path/to/9-nein-biased && python3 run.py
```

---

## API Keys & Costs

| Service | Free Tier | Est. Daily Cost |
|---|---|---|
| [Anthropic API](https://console.anthropic.com) | $5 minimum top-up | ~$0.03–0.05/run |
| [NewsAPI](https://newsapi.org/register) | 100 req/day free | Free |
| Gmail SMTP | Free | Free |

> **Note:** Claude Pro (claude.ai) and the Anthropic API are **separate products** with separate billing. You need API credits from [console.anthropic.com](https://console.anthropic.com), not a Claude Pro subscription.

---

## Source Bias Classifications

Sources are pre-classified in `sources.py`:

| Bias | Example Outlets |
|---|---|
| **Left** | The Atlantic, Mother Jones, HuffPost, MSNBC, Jacobin |
| **Center** | Reuters, Associated Press, NPR, The Hill, Axios, BBC News |
| **Right** | Fox News, Breitbart, Newsmax, The Washington Times, National Review |

Classifications are based on [AllSides](https://www.allsides.com/media-bias/ratings) and [Ad Fontes Media](https://adfontesmedia.com/) research.

---

## How the AI Classification Works

The pipeline makes two Claude API calls per story:

**Call 1 — Story Clustering**
> Given all articles, identify the top 3 stories covered across multiple sources. Group articles by story and generate a neutral headline for each.

**Call 2 — Story Analysis**
> For each story: score every article 0.0 (pure opinion) to 1.0 (pure analysis), explain the score in one sentence, extract 3–5 shared facts, and write a 2-sentence neutral framing contrast.

---

## Ethical Design Principles

- **No new bias introduced** — Claude is explicitly prompted to write neutral headlines and framing contrasts. The system flags its own classifications rather than hiding them.
- **Transparent scoring** — Every analytical score includes a plain-English explanation visible to the reader.
- **Licensed data only** — All articles sourced via NewsAPI's licensed feed. No scraping.
- **No user data stored** — Recipient emails live only in `.env` and are never logged or retained.

---

## Requirements

```
feedparser==6.0.11
requests==2.31.0
python-dotenv==1.0.0
```

Python 3.8+ required.

---

## Troubleshooting

| Error | Fix |
|---|---|
| `401 Unauthorized` (Anthropic) | Check `ANTHROPIC_API_KEY` in `.env` — must match the key at console.anthropic.com |
| `Credit balance too low` | Add credits at console.anthropic.com → Plans & Billing |
| `Total articles fetched: 0` | Check `NEWS_API_KEY` in `.env` — register free at newsapi.org |
| `Gmail auth failed` | Use an App Password, not your Gmail password. Workspace accounts may not support this. |
| `No sources` in coverage map | The new `fetcher.py` makes 4 targeted API calls — make sure you're using the latest version |

---

## License

MIT License — free to use, modify, and distribute.

---

*Built as a capstone project. 9 Biased is not affiliated with any news organization. Bias classifications reflect independent media research and AI analysis*

<img width="1185" height="571" alt="Screenshot 2026-04-01 at 4 18 12 PM" src="https://github.com/user-attachments/assets/5f514dda-f277-466b-a14e-0176992bbd60" />
<img width="627" height="568" alt="Screenshot 2026-04-01 at 4 18 41 PM" src="https://github.com/user-attachments/assets/45d92085-0ea9-4b77-b89c-a949592adfa1" />
<img width="566" height="567" alt="Screenshot 2026-04-01 at 4 18 49 PM" src="https://github.com/user-attachments/assets/9d29947d-60cb-4507-aff0-726bc8d2bb00" />
<img width="577" height="478" alt="Screenshot 2026-04-01 at 4 18 56 PM" src="https://github.com/user-attachments/assets/fa1bf90c-5805-454f-a53c-39eed2af4c2e" />

