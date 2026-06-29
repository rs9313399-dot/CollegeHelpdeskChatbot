# College Helpdesk Chatbot

College Helpdesk Chatbot is a Flask-based web chatbot that answers common college-related questions from a local JSON knowledge base.

It supports topics such as admission, fees, courses, hostel, placements, library, sports, faculty, events, and contact information.

## Highlights

- Flask web app with a responsive chat interface.
- Local JSON knowledge base for easy FAQ updates.
- Exact and fuzzy matching for user questions.
- Quick buttons for common topics.
- Small-talk handling for greetings, thanks, and farewells.
- Admin link in the interface for FAQ editing workflow.
- Glass-style frontend UI with static CSS and JavaScript.

## Tech Stack

| Area | Tools |
| --- | --- |
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Data | JSON knowledge base |
| Matching | Python `difflib.SequenceMatcher` |

## Project Structure

```text
CollegeHelpdeskChatbot/
├── app.py                 # Flask routes and chatbot logic
├── data.json              # FAQ and response data
├── templates/
│   ├── index.html         # Chat page
│   └── admin.html         # Admin page
└── static/
    ├── chat.js            # Chat frontend behavior
    └── style.css          # UI styling
```

## Getting Started

### Prerequisites

- Python 3.9+

### Installation

```bash
git clone https://github.com/rs9313399-dot/CollegeHelpdeskChatbot.git
cd CollegeHelpdeskChatbot
python -m venv .venv
.venv\Scripts\activate
pip install flask
```

For macOS/Linux:

```bash
source .venv/bin/activate
```

### Run

```bash
python app.py
```

Open the Flask URL printed in the terminal, usually:

```text
http://127.0.0.1:5000
```

## Main Routes

| Route | Purpose |
| --- | --- |
| `/` | Chat interface |
| `/chat` | JSON endpoint for chatbot replies |
| `/admin` | FAQ management page, if enabled in the app |

## Updating Answers

Edit `data.json` to add or update topics:

```json
{
  "admission": "Admission process starts in July. Visit college website.",
  "fees": "Fees depend on course. B.Tech approx 45000 per year."
}
```

Restart the app after making changes.

## Author

Built by [Ratnesh Singh](https://github.com/rs9313399-dot).

