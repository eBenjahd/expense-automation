AI Expense Automation

Backend automation system for expense tracking, AI-powered transaction processing, and automated notifications.

The project allows users to interact with their finances through Telegram. Incoming messages are processed by an n8n workflow, classified by an AI agent, and converted into structured financial operations that are handled by a Django REST API.

Architecture

Telegram
   │
   ▼
n8n Workflow
   │
   ├── Authenticate user
   ├── Check Telegram profile
   ├── Redis conversation memory
   │
   ▼
AI Intent Router
   │
   ├── create_transaction
   ├── list_transactions
   ├── update_transaction
   ├── delete_transaction
   ├── create_budget
   ├── list_budgets
   ├── update_budget
   └── delete_budget
   │
   ▼
Specialized AI Workflow
   │
   ▼
Django REST API
   │
   ├── Transactions
   ├── Budgets
   ├── Accounts
   └── Categories
   │
   ▼
PostgreSQL

Features

* Telegram-based financial assistant
* AI-powered intent classification
* Automatic expense and income extraction
* Transaction management
* Budget management
* User identification through Telegram
* Redis-based conversational memory
* Automatic default account handling
* Automated notifications
* API authentication for n8n
* Request throttling
* Django REST Framework permissions
* PostgreSQL database
* Docker-based infrastructure

Technology Stack

Backend

* Python
* Django
* Django REST Framework
* PostgreSQL
* Redis

Automation

* n8n
* Telegram Bot API
* AI/LLM integration

Infrastructure

* Docker
* Docker Compose
* Nginx
* Gunicorn

Finance API

Transactions

GET    /api/finance/transactions/
POST   /api/finance/transactions/
GET    /api/finance/transactions/<id>/
PUT    /api/finance/transactions/<id>/
PATCH  /api/finance/transactions/<id>/
DELETE /api/finance/transactions/<id>/

Transactions support:

* Account
* Category
* Transaction type
* Amount
* Currency
* Description
* Source
* Original Telegram message
* Occurrence date

Budgets

GET    /api/finance/budgets/
POST   /api/finance/budgets/
GET    /api/finance/budgets/<id>/
PUT    /api/finance/budgets/<id>/
PATCH  /api/finance/budgets/<id>/
DELETE /api/finance/budgets/<id>/

AI Intent System

The main AI agent does not directly manipulate financial data.

Instead, it acts as an intent router.

For example:

"Hoy gasté 45 soles en comida"

is classified as:

{
  "intent": "create_transaction"
}

The workflow then routes the request to a specialized transaction-processing agent.

This separation keeps the main agent focused on understanding the user’s intention while allowing each operation to have its own validation and processing logic.

Transaction Processing

A transaction can be created from a natural-language message.

For example:

"Hoy gasté 45 soles en comida"

can be converted into structured information such as:

{
  "category": {
    "name": "comida",
    "kind": "expense"
  },
  "kind": "expense",
  "amount": "45.00",
  "currency": "PEN"
}

If the user does not specify an account, the backend automatically uses the user’s default efectivo account.

The backend remains responsible for validating and creating the final transaction.

User Authentication

Requests coming from n8n are protected using an API key.

The backend validates:

X-API-Key

before allowing n8n to access protected endpoints.

Telegram users are identified through:

X-Telegram-Chat-ID

This allows the backend to associate incoming Telegram messages with the corresponding Django user.

Redis Memory

Redis is used for short-term conversational memory.

A user’s conversation can be stored under a key such as:

user:<telegram_chat_id>:chat_memory

The system uses a limited context window and expiration time so that the AI does not receive an unnecessarily large conversation history.

Example Redis structure:

user:1249654480:chat_memory
        │
        └── LIST
             ├── Human message
             ├── AI response
             ├── Human message
             └── AI response

Request Protection

The Django API uses:

* Custom permissions
* API key authentication
* Telegram user validation
* DRF throttling

Example throttling configuration:

5 requests / second
100 requests / minute

This prevents a single Telegram user or integration from generating an excessive number of requests.

Local Development

Clone the repository:

git clone <repository-url>
cd expense-automation

Create a virtual environment:

python -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create your environment variables:

DJANGO_SECRET_KEY=
DEBUG=
DATABASE_URL=
N8N_API_KEY=

Run migrations:

python manage.py migrate

Start the development server:

python manage.py runserver

Docker

The production infrastructure uses Docker Compose for services such as:

Django
PostgreSQL
Redis
n8n
Nginx

Each service is isolated and communicates through Docker networks.

Project Goals

The main goal of the project is to build a practical financial automation system where users can manage expenses and budgets through natural language without interacting directly with a traditional REST API.

The architecture is intentionally separated into:

User interaction
        ↓
Automation
        ↓
AI interpretation
        ↓
Backend validation
        ↓
Database

This keeps AI responsible for interpreting natural language while the backend remains responsible for business rules, validation, authentication, and persistence.

Future Improvements

* Financial reports
* Spending alerts
* Budget notifications
* Recurring transactions
* Advanced transaction filtering
* Financial analytics
* Improved category management
* Long-term semantic memory
* RAG experimentation
* Automated monthly reports
* Additional Telegram commands