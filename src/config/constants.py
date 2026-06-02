"""
Application constants.
"""

# =====================================================
# APP
# =====================================================

APP_NAME = "Multi-Agent Ecommerce Platform"

DEFAULT_CURRENCY = "INR"

GST_PERCENTAGE = 18


# =====================================================
# AGENTS
# =====================================================

CONCIERGE_AGENT = "concierge_agent"

INVENTORY_AGENT = "inventory_agent"

INVOICE_AGENT = "invoice_agent"

MARKET_AGENT = "market_agent"


# =====================================================
# WORKFLOW STATUS
# =====================================================

STATUS_PENDING = "PENDING"

STATUS_RUNNING = "RUNNING"

STATUS_COMPLETED = "COMPLETED"

STATUS_FAILED = "FAILED"


# =====================================================
# INTENTS
# =====================================================

INTENT_INVENTORY = "inventory"

INTENT_INVOICE = "invoice"

INTENT_MARKET = "market"

INTENT_UNKNOWN = "unknown"


# =====================================================
# DATABASE TABLES
# =====================================================

TABLE_PRODUCTS = "products"

TABLE_INVOICES = "invoices"

TABLE_MARKET_INSIGHTS = "market_insights"


# =====================================================
# LOG FILES
# =====================================================

APP_LOG_FILE = "logs/app.log"

ERROR_LOG_FILE = "logs/errors.log"

AGENT_LOG_FILE = "logs/agents.log"


# =====================================================
# MARKET INTELLIGENCE
# =====================================================

DEFAULT_DEMAND_SCORE = 50

DEFAULT_TREND_SCORE = 50

PRICE_INCREASE_FACTOR = 1.05

PRICE_DECREASE_FACTOR = 0.95


# =====================================================
# PAGINATION
# =====================================================

DEFAULT_PAGE_SIZE = 10

MAX_PAGE_SIZE = 100