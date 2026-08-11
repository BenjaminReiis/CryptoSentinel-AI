<p align="center">
  <img src="assets/banner.png" alt="CryptoSentinel AI" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-Backend-ffd23f?style=for-the-badge&logo=python&logoColor=black" />
  <img src="https://img.shields.io/badge/FastAPI-API-ff9f4f?style=for-the-badge&logo=fastapi&logoColor=black" />
  <img src="https://img.shields.io/badge/Next.js-Dashboard-7ae0ff?style=for-the-badge&logo=next.js&logoColor=black" />
  <img src="https://img.shields.io/badge/TimescaleDB-PostgreSQL-00ffc3?style=for-the-badge&logo=postgresql&logoColor=black" />
  <img src="https://img.shields.io/badge/Kafka-Redpanda-8f7bff?style=for-the-badge&logo=apachekafka&logoColor=black" />
  <img src="https://img.shields.io/badge/status-arquitetura%2Fdesign-ff5f8a?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-MIT-3a8fff?style=for-the-badge" />
</p>

<h1 align="center">🛰️ CryptoSentinel AI</h1>

<p align="center">
  <b>🇺🇸 <a href="#-english">English</a> &nbsp;|&nbsp; 🇧🇷 <a href="#-português">Português</a></b>
</p>

---

## 🇺🇸 English

### 📌 Goal

**CryptoSentinel AI** monitors cryptocurrencies, prices, wallets, blocks
and transactions in real time, turning raw data into **analytical
signals**.

### 🧠 Architecture

<p align="center">
  <img src="assets/architecture.png" alt="System architecture" width="70%">
</p>

```
Market Data · Blockchain Data · External Data
                    ↓
            Event Streaming (Kafka / Redpanda)
                    ↓
            Data Processing (Python / Rust)
                    ↓
      TimescaleDB (time series)  +  PostgreSQL (metadata)
                    ↓
              AI / Analytics (ML + LLM)
                    ↓
              API / WebSocket (FastAPI)
                    ↓
              Web Dashboard (Next.js)
```

Three independent ingestion sources — **market data**, **blockchain
data** and **external data** (news, sentiment, macro) — converge into a
single event stream, get processed, persisted, analyzed and finally
surfaced through the API and dashboard.

For historical transfer data, an **indexed API** avoids scanning and
indexing the entire blockchain for every address. For more structured
queries, **subgraphs** turn blockchain data into queryable GraphQL APIs —
**The Graph** is particularly useful here, since it lets you build custom
APIs over blockchain data with standardized schemas that help normalize
metrics across protocols. **Alchemy** currently offers price, transfer,
webhook and WebSocket APIs, plus Chain APIs for multiple networks — a good
fit as one ingestion layer, not the system's only data source.

### 📁 Repository structure

A monorepo layout:

```
cryptosentinel-ai/
│
├── apps/
│   ├── web/
│   │   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── lib/
│   │
│   └── api/
│       ├── app/
│       │   ├── main.py
│       │   ├── routes/
│       │   ├── services/
│       │   ├── models/
│       │   └── websocket/
│       └── tests/
│
├── services/
│   ├── blockchain-ingestor/
│   │   ├── adapters/
│   │   │   ├── ethereum.py
│   │   │   ├── bitcoin.py
│   │   │   ├── solana.py
│   │   │   └── base.py
│   │   └── worker.py
│   │
│   ├── market-ingestor/
│   │   ├── exchanges/
│   │   ├── prices/
│   │   └── worker.py
│   │
│   ├── transaction-analyzer/
│   │   ├── detectors/
│   │   ├── scoring/
│   │   └── worker.py
│   │
│   └── ai-engine/
│       ├── models/
│       ├── features/
│       ├── signals/
│       └── inference.py
│
├── packages/
│   ├── schemas/
│   ├── database/
│   ├── blockchain/
│   ├── analytics/
│   └── config/
│
├── infrastructure/
│   ├── docker/
│   ├── postgres/
│   ├── redis/
│   ├── kafka/
│   └── monitoring/
│
├── scripts/
├── tests/
├── docker-compose.yml
├── .env.example
├── pyproject.toml
├── package.json
└── README.md
```

### 🔥 Core modules

**1. Market monitor** — tracks price, 1m/5m/15m/1h/4h/24h change, volume,
market cap, liquidity, volatility, dominance, spreads, order books, and
cross-asset correlation.

**2. Blockchain intelligence** — one adapter per chain behind a common
interface, so adding a new chain doesn't require rewriting the system:

```python
from abc import ABC, abstractmethod


class BlockchainAdapter(ABC):

    @abstractmethod
    async def get_latest_block(self):
        pass

    @abstractmethod
    async def get_transaction(self, tx_hash: str):
        pass

    @abstractmethod
    async def get_balance(self, address: str):
        pass

    @abstractmethod
    async def subscribe_transactions(self):
        pass
```

```
BlockchainAdapter
       │
       ├── EthereumAdapter
       ├── BitcoinAdapter
       ├── SolanaAdapter
       ├── BSCAdapter
       ├── PolygonAdapter
       ├── ArbitrumAdapter
       ├── BaseAdapter
       ├── AvalancheAdapter
       └── ...
```

### ⚡ Real-time monitoring

Raw chain events...

```json
{
    "chain": "ethereum",
    "block": 23194821,
    "tx_hash": "0x...",
    "from": "0x...",
    "to": "0x...",
    "token": "USDT",
    "amount": 1250000,
    "timestamp": 1786380000
}
```

...become analytical events:

```json
{
    "event": "WHALE_TRANSFER",
    "severity": "HIGH",
    "chain": "ethereum",
    "asset": "USDT",
    "amount_usd": 1250000,
    "confidence": 0.94
}
```

WebSockets are especially useful for following new blocks, pending
transactions, logs, and account/program updates on supported networks —
the dashboard receives events without polling.

### 🧠 AI engine

The AI doesn't just say "buy" or "sell" — it produces a **Risk & Trend
Score**:

```
TREND SCORE
────────────────────────
Momentum             +82
Volume                +71
Whale Activity        +89
Liquidity              +64
On-chain Flow          +77
Social Sentiment       +58
Volatility              -21
────────────────────────
TOTAL                  74/100
```

```json
{
  "asset": "BTC",
  "trend": "BULLISH",
  "score": 74,
  "confidence": 0.87,
  "signals": [
    "Volume increase",
    "Net inflow into large wallets",
    "Positive momentum",
    "Increased on-chain activity"
  ]
}
```

**Anomaly detection** watches for: 🐋 whale movement, 🚨 volume anomaly,
⚠️ liquidity drop, 🔄 exchange inflow/outflow spikes, 🔥 token transfer
spikes, 📈/📉 unusual accumulation/distribution, 🧠 smart-money movement,
⚡ gas spikes, 💧 DeFi liquidity movement.

### 🗄️ Database

- **PostgreSQL** — entities and relationships
- **TimescaleDB** — time series: `prices`, `market_metrics`, `volume`,
  `transactions`, `gas`, `whale_movements`, `wallet_activity`, `signals`,
  `sentiment`
- **Redis** — cache and real-time state
- **Kafka/Redpanda** — decouples blockchain ingestion, processing and
  analysis

### 🌐 API (FastAPI example)

```python
from fastapi import FastAPI

app = FastAPI(title="CryptoSentinel AI", version="1.0.0")


@app.get("/api/v1/market/{symbol}")
async def market(symbol: str):
    return {"symbol": symbol.upper(), "status": "monitoring"}


@app.get("/api/v1/transactions/{chain}")
async def transactions(chain: str):
    return {"chain": chain, "status": "streaming"}


@app.get("/api/v1/signals/{symbol}")
async def signals(symbol: str):
    return {"symbol": symbol.upper(), "signals": []}
```

### 📡 WebSocket

```python
from fastapi import WebSocket


@app.websocket("/ws/market")
async def market_stream(websocket: WebSocket):
    await websocket.accept()
    while True:
        event = await get_next_market_event()
        await websocket.send_json(event)
```

### 🖥️ Dashboard

```
┌────────────────────────────────────────────────────────────┐
│ CRYPTOSENTINEL AI                           ● LIVE          │
├────────────────────────────────────────────────────────────┤
│ BTC       $XX,XXX     +2.41%     🟢 BULLISH                │
│ ETH       $X,XXX      +1.83%     🟢 BULLISH                │
│ SOL       $XXX        -0.42%     🟡 NEUTRAL                │
├────────────────────────────────────────────────────────────┤
│                    MARKET OVERVIEW                          │
│              📈 market chart                                │
├───────────────────────────┬────────────────────────────────┤
│ WHALE ACTIVITY             │ AI SIGNALS                    │
│ 🐋 BTC  +$84M              │ BTC  82/100 🟢                 │
│ 🐋 ETH  +$31M              │ ETH  74/100 🟢                 │
│ 🐋 USDT +$18M              │ SOL  51/100 🟡                 │
├───────────────────────────┴────────────────────────────────┤
│ RECENT ON-CHAIN EVENTS                                      │
│ Ethereum │ Whale Transfer │ $12.4M │ 16:11:03               │
│ Bitcoin  │ Large Tx       │ $8.7M  │ 16:10:58               │
│ Solana   │ Token Spike    │ $3.2M  │ 16:10:51               │
└────────────────────────────────────────────────────────────┘
```

### 🔐 Security

Since this touches financial/on-chain data, **monitoring is fully
separated from any fund-moving capability**. The initial system is
**read-only**:

```
Blockchain → READ ONLY → Indexer → Analytics → AI → Dashboard
```

No private keys or seed phrases are ever stored in the backend.

### 📊 Advanced metrics

Price Momentum · Volume Momentum · Volatility · Liquidity · Whale Score ·
Exchange Flow · Net Flow · Wallet Concentration · Token Velocity · Gas
Activity · Smart Money Score · Accumulation Score · Distribution Score ·
Market Regime · Anomaly Score · Trend Score · Risk Score

### 🧩 Stack

| Layer | Technologies |
|---|---|
| 🌐 **Frontend** | Next.js · TypeScript · Tailwind · TradingView Lightweight Charts |
| ⚙️ **Backend** | Python · FastAPI · Pydantic · WebSockets |
| 🗄️ **Data** | PostgreSQL · TimescaleDB · Redis |
| 📡 **Streaming** | Kafka / Redpanda |
| ⛓️ **Blockchain** | Alchemy · The Graph · own RPC/WebSockets when needed |
| 🤖 **AI** | Python · scikit-learn · PyTorch · LLMs for interpretation |
| 🐳 **DevOps** | Docker · GitHub Actions · Prometheus · Grafana |

### 🚀 Suggested MVP roadmap

```
PHASE 1
├── Bitcoin, Ethereum, BNB Chain, Solana
├── Prices, blocks, transactions
└── Dashboard

PHASE 2
├── Whale detection
├── Wallet tracking
├── Exchange flows
├── Alerts
└── Real-time WebSocket

PHASE 3
├── AI Trend Engine
├── Anomaly detection
├── Smart-money detection
├── Sentiment
└── Risk scoring

PHASE 4
├── More blockchains
├── DeFi / DEX
├── Token intelligence
├── Backtesting
└── Predictive models
```

### 📄 License

MIT — see `LICENSE` for details.

---

## 🇧🇷 Português

### 📌 Objetivo

O **CryptoSentinel AI** monitora criptomoedas, preços, carteiras, blocos e
transações em tempo real, transformando os dados em **sinais
analíticos**.

### 🧠 Arquitetura

<p align="center">
  <img src="assets/architecture.png" alt="Arquitetura do sistema" width="70%">
</p>

```
Market Data · Blockchain Data · External Data
                    ↓
            Event Streaming (Kafka / Redpanda)
                    ↓
            Data Processing (Python / Rust)
                    ↓
      TimescaleDB (séries temporais)  +  PostgreSQL (metadados)
                    ↓
              AI / Analytics (ML + LLM)
                    ↓
              API / WebSocket (FastAPI)
                    ↓
              Web Dashboard (Next.js)
```

Três fontes de ingestão independentes — **dados de mercado**, **dados de
blockchain** e **dados externos** (notícias, sentimento, macro) —
convergem para um único stream de eventos, são processados, persistidos,
analisados e finalmente expostos via API e dashboard.

Para dados de transferências históricas, uma **API indexada** evita ter
que varrer e indexar toda a blockchain para cada endereço. Para consultas
mais estruturadas, **subgraphs** transformam dados de blockchain em APIs
GraphQL consultáveis — o **The Graph** é particularmente interessante aqui,
pois permite criar APIs customizadas sobre dados de blockchain com schemas
padronizados que ajudam a normalizar métricas entre protocolos. A
**Alchemy** atualmente oferece APIs de preços, transferências, webhooks e
WebSockets, além de Chain APIs para várias redes — um bom encaixe como uma
das camadas de ingestão, não como fonte única do sistema.

### 📁 Estrutura dos repositórios

Um monorepo:

```
cryptosentinel-ai/
│
├── apps/
│   ├── web/
│   │   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── lib/
│   │
│   └── api/
│       ├── app/
│       │   ├── main.py
│       │   ├── routes/
│       │   ├── services/
│       │   ├── models/
│       │   └── websocket/
│       └── tests/
│
├── services/
│   ├── blockchain-ingestor/
│   │   ├── adapters/
│   │   │   ├── ethereum.py
│   │   │   ├── bitcoin.py
│   │   │   ├── solana.py
│   │   │   └── base.py
│   │   └── worker.py
│   │
│   ├── market-ingestor/
│   │   ├── exchanges/
│   │   ├── prices/
│   │   └── worker.py
│   │
│   ├── transaction-analyzer/
│   │   ├── detectors/
│   │   ├── scoring/
│   │   └── worker.py
│   │
│   └── ai-engine/
│       ├── models/
│       ├── features/
│       ├── signals/
│       └── inference.py
│
├── packages/
│   ├── schemas/
│   ├── database/
│   ├── blockchain/
│   ├── analytics/
│   └── config/
│
├── infrastructure/
│   ├── docker/
│   ├── postgres/
│   ├── redis/
│   ├── kafka/
│   └── monitoring/
│
├── scripts/
├── tests/
├── docker-compose.yml
├── .env.example
├── pyproject.toml
├── package.json
└── README.md
```

### 🔥 Módulos principais

**1. Monitor de mercado** — acompanha preço, variação 1m/5m/15m/1h/4h/24h,
volume, market cap, liquidez, volatilidade, dominância, spreads, order
books e correlação entre ativos.

**2. Blockchain Intelligence** — um adapter por blockchain atrás de uma
interface comum, permitindo adicionar uma nova chain sem reescrever o
sistema:

```python
from abc import ABC, abstractmethod


class BlockchainAdapter(ABC):

    @abstractmethod
    async def get_latest_block(self):
        pass

    @abstractmethod
    async def get_transaction(self, tx_hash: str):
        pass

    @abstractmethod
    async def get_balance(self, address: str):
        pass

    @abstractmethod
    async def subscribe_transactions(self):
        pass
```

```
BlockchainAdapter
       │
       ├── EthereumAdapter
       ├── BitcoinAdapter
       ├── SolanaAdapter
       ├── BSCAdapter
       ├── PolygonAdapter
       ├── ArbitrumAdapter
       ├── BaseAdapter
       ├── AvalancheAdapter
       └── ...
```

### ⚡ Monitoramento em tempo real

Eventos brutos da chain...

```json
{
    "chain": "ethereum",
    "block": 23194821,
    "tx_hash": "0x...",
    "from": "0x...",
    "to": "0x...",
    "token": "USDT",
    "amount": 1250000,
    "timestamp": 1786380000
}
```

...viram eventos analíticos:

```json
{
    "event": "WHALE_TRANSFER",
    "severity": "HIGH",
    "chain": "ethereum",
    "asset": "USDT",
    "amount_usd": 1250000,
    "confidence": 0.94
}
```

WebSockets são especialmente úteis para acompanhar novos blocos,
transações pendentes, logs e atualizações de contas/programas em redes
suportadas — o dashboard recebe os eventos sem precisar fazer polling.

### 🧠 Motor de IA

A IA não deve simplesmente dizer "compre" ou "venda" — o ideal é gerar um
**Risk & Trend Score**:

```
TREND SCORE
────────────────────────
Momentum             +82
Volume                +71
Whale Activity        +89
Liquidez               +64
On-chain Flow          +77
Social Sentiment       +58
Volatilidade            -21
────────────────────────
TOTAL                  74/100
```

```json
{
  "asset": "BTC",
  "trend": "BULLISH",
  "score": 74,
  "confidence": 0.87,
  "signals": [
    "Aumento de volume",
    "Entrada líquida em grandes carteiras",
    "Momentum positivo",
    "Aumento de atividade on-chain"
  ]
}
```

**Detecção de anomalias**: 🐋 whale movement, 🚨 volume anomaly, ⚠️
liquidity drop, 🔄 exchange inflow/outflow spike, 🔥 token transfer
spike, 📈/📉 unusual accumulation/distribution, 🧠 smart-money movement,
⚡ gas spike, 💧 DeFi liquidity movement.

### 🗄️ Banco de dados

- **PostgreSQL** — entidades e relacionamentos
- **TimescaleDB** — séries temporais: `prices`, `market_metrics`,
  `volume`, `transactions`, `gas`, `whale_movements`, `wallet_activity`,
  `signals`, `sentiment`
- **Redis** — cache e estado de tempo real
- **Kafka/Redpanda** — separa ingestão de blockchain, processamento e
  análise

### 🌐 API (exemplo com FastAPI)

```python
from fastapi import FastAPI

app = FastAPI(title="CryptoSentinel AI", version="1.0.0")


@app.get("/api/v1/market/{symbol}")
async def market(symbol: str):
    return {"symbol": symbol.upper(), "status": "monitoring"}


@app.get("/api/v1/transactions/{chain}")
async def transactions(chain: str):
    return {"chain": chain, "status": "streaming"}


@app.get("/api/v1/signals/{symbol}")
async def signals(symbol: str):
    return {"symbol": symbol.upper(), "signals": []}
```

### 📡 WebSocket

```python
from fastapi import WebSocket


@app.websocket("/ws/market")
async def market_stream(websocket: WebSocket):
    await websocket.accept()
    while True:
        event = await get_next_market_event()
        await websocket.send_json(event)
```

### 🖥️ Dashboard

```
┌────────────────────────────────────────────────────────────┐
│ CRYPTOSENTINEL AI                           ● LIVE          │
├────────────────────────────────────────────────────────────┤
│ BTC       $XX,XXX     +2.41%     🟢 BULLISH                │
│ ETH       $X,XXX      +1.83%     🟢 BULLISH                │
│ SOL       $XXX        -0.42%     🟡 NEUTRAL                │
├────────────────────────────────────────────────────────────┤
│                    MARKET OVERVIEW                          │
│              📈 gráfico de mercado                          │
├───────────────────────────┬────────────────────────────────┤
│ WHALE ACTIVITY             │ AI SIGNALS                    │
│ 🐋 BTC  +$84M              │ BTC  82/100 🟢                 │
│ 🐋 ETH  +$31M              │ ETH  74/100 🟢                 │
│ 🐋 USDT +$18M              │ SOL  51/100 🟡                 │
├───────────────────────────┴────────────────────────────────┤
│ RECENT ON-CHAIN EVENTS                                      │
│ Ethereum │ Whale Transfer │ $12.4M │ 16:11:03               │
│ Bitcoin  │ Large Tx       │ $8.7M  │ 16:10:58               │
│ Solana   │ Token Spike    │ $3.2M  │ 16:10:51               │
└────────────────────────────────────────────────────────────┘
```

### 🔐 Segurança

Por se tratar de um sistema financeiro/on-chain, **monitoramento fica
totalmente separado de qualquer capacidade de movimentar fundos**. O
sistema inicial é **read-only**:

```
Blockchain → READ ONLY → Indexer → Analytics → AI → Dashboard
```

Nenhuma private key ou seed phrase é armazenada no backend.

### 📊 Métricas avançadas

Price Momentum · Volume Momentum · Volatility · Liquidity · Whale Score ·
Exchange Flow · Net Flow · Wallet Concentration · Token Velocity · Gas
Activity · Smart Money Score · Accumulation Score · Distribution Score ·
Market Regime · Anomaly Score · Trend Score · Risk Score

### 🧩 Stack

| Camada | Tecnologias |
|---|---|
| 🌐 **Frontend** | Next.js · TypeScript · Tailwind · TradingView Lightweight Charts |
| ⚙️ **Backend** | Python · FastAPI · Pydantic · WebSockets |
| 🗄️ **Dados** | PostgreSQL · TimescaleDB · Redis |
| 📡 **Streaming** | Kafka / Redpanda |
| ⛓️ **Blockchain** | Alchemy · The Graph · RPC/WebSockets próprios quando necessário |
| 🤖 **IA** | Python · scikit-learn · PyTorch · LLMs para interpretação |
| 🐳 **DevOps** | Docker · GitHub Actions · Prometheus · Grafana |

### 🚀 Roadmap sugerido para o MVP

```
FASE 1
├── Bitcoin, Ethereum, BNB Chain, Solana
├── Preços, blocos, transações
└── Dashboard

FASE 2
├── Whale detection
├── Wallet tracking
├── Exchange flows
├── Alertas
└── WebSocket em tempo real

FASE 3
├── AI Trend Engine
├── Anomaly detection
├── Smart-money detection
├── Sentiment
└── Risk scoring

FASE 4
├── Mais blockchains
├── DeFi / DEX
├── Token intelligence
├── Backtesting
└── Modelos preditivos
```

### 📄 Licença

MIT — veja `LICENSE` para mais detalhes.

---

<p align="center">
  <sub>Kafka/Redpanda 📡 · TimescaleDB + PostgreSQL 🗄️ · FastAPI ⚡ · Next.js 🌐 · ML + LLM 🤖</sub>
</p>
