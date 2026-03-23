# 90-Day LinkedIn Post Roadmap
## System Design for Dummies — Content Calendar
**Start Date:** March 22, 2026 | **End Date:** June 19, 2026

---

## PHASE 1: API Design (Days 1–20)
*Chapter 1 — 20 concepts, 1 post per concept*

| Day | Date | Topic |
|-----|------|-------|
| 1 | Mar 22 | What is an API? (The concept of Endpoints) |
| 2 | Mar 23 | HTTP Methods — GET, POST, PUT, DELETE, PATCH |
| 3 | Mar 24 | The Request-Response Cycle |
| 4 | Mar 25 | HTTP Status Codes — The secret language of APIs |
| 5 | Mar 26 | Authentication — Who are you? |
| 6 | Mar 27 | Authorization — What can you do? |
| 7 | Mar 28 | Access Tokens — How auth works in practice |
| 8 | Mar 29 | OAuth 2.0 — "Login with Google" demystified |
| 9 | Mar 30 | Rate Limiting — Why APIs need speed limits |
| 10 | Mar 31 | Throttling vs Rate Limiting |
| 11 | Apr 1 | Pagination — Why you can't load 1M results at once |
| 12 | Apr 2 | Caching — The superpower of fast APIs |
| 13 | Apr 3 | Idempotency — The concept that prevents double charges |
| 14 | Apr 4 | Webhooks — Don't call us, we'll call you |
| 15 | Apr 5 | API Versioning — How to evolve without breaking things |
| 16 | Apr 6 | OpenAPI / Swagger — Documenting APIs properly |
| 17 | Apr 7 | REST vs GraphQL — Which should you choose? |
| 18 | Apr 8 | API Gateway — The front door of your backend |
| 19 | Apr 9 | Microservices — Breaking up the monolith |
| 20 | Apr 10 | Error Handling in APIs — Done right |

---

## PHASE 2: Integer Overflow & ID Design (Days 21–25)
*Chapter 2 — Chess.com's crash + Snowflake IDs*

| Day | Date | Topic |
|-----|------|-------|
| 21 | Apr 11 | Chess.com's 2 billionth game crash — What really happened |
| 22 | Apr 12 | What is Integer Overflow? |
| 23 | Apr 13 | 32-bit vs 64-bit integers — The difference that broke production |
| 24 | Apr 14 | Snowflake IDs — Twitter's solution to distributed ID generation |
| 25 | Apr 15 | ID Strategy Comparison — Auto-increment vs UUID vs Snowflake |

---

## PHASE 3: Database Design (Days 26–45)
*Chapter 3 — SQL, NoSQL, Indexing, Sharding, Replication, Consistency*

| Day | Date | Topic |
|-----|------|-------|
| 26 | Apr 16 | Why database design matters (real outage stories) |
| 27 | Apr 17 | SQL fundamentals — When structure is your friend |
| 28 | Apr 18 | NoSQL fundamentals — When flexibility wins |
| 29 | Apr 19 | SQL vs NoSQL — The real question to ask |
| 30 | Apr 20 | Polyglot Persistence — Why most companies use both |
| 31 | Apr 21 | What is Indexing? (Book table of contents analogy) |
| 32 | Apr 22 | How B-tree indexes work under the hood |
| 33 | Apr 23 | Types of indexes — B-tree, Hash, Composite, Full-text |
| 34 | Apr 24 | The index tradeoff — Every index slows every write |
| 35 | Apr 25 | What is Sharding? (The restaurant analogy) |
| 36 | Apr 26 | Hash-based Sharding |
| 37 | Apr 27 | Range-based Sharding |
| 38 | Apr 28 | Consistent Hashing — The elegant sharding solution |
| 39 | Apr 29 | Shard Key Selection — The decision you can't easily undo |
| 40 | Apr 30 | What is Replication? (The photocopy analogy) |
| 41 | May 1 | Synchronous vs Asynchronous Replication |
| 42 | May 2 | Primary-Replica Replication |
| 43 | May 3 | Consistency Models — Strong vs Eventual |
| 44 | May 4 | ACID Properties — The database safety guarantee |
| 45 | May 5 | BASE Properties — The distributed tradeoff |

---

## PHASE 4: CAP Theorem (Days 46–60)
*Chapter 4 — Consistency, Availability, Partition Tolerance*

| Day | Date | Topic |
|-----|------|-------|
| 46 | May 6 | The CAP Theorem — The concert ticket story |
| 47 | May 7 | Consistency in distributed systems |
| 48 | May 8 | Availability in distributed systems |
| 49 | May 9 | Partition Tolerance — The one you always get |
| 50 | May 10 | Why network partitions are inevitable (Google's data) |
| 51 | May 11 | CP Systems — "I'd rather be down than wrong" |
| 52 | May 12 | AP Systems — "I'd rather be wrong than down" |
| 53 | May 13 | CP vs AP — How to make the real choice |
| 54 | May 14 | CAP in real databases — Cassandra, MongoDB, Postgres |
| 55 | May 15 | The "CA" myth — Why it doesn't exist in production |
| 56 | May 16 | Business thinking about CAP (Ticketmaster vs Banks) |
| 57 | May 17 | Consistency is per-operation, not per-database |
| 58 | May 18 | PACELC Theorem — Extending CAP |
| 59 | May 19 | CAP in system design interviews — The golden phrase |
| 60 | May 20 | CAP Theorem Cheatsheet recap |

---

## PHASE 5: Kafka & Message Queues (Days 61–90)
*Chapter 5 — Kafka internals, when to use it, alternatives*

| Day | Date | Topic |
|-----|------|-------|
| 61 | May 21 | The messaging problem — What happens when services need to talk |
| 62 | May 22 | What is Apache Kafka? |
| 63 | May 23 | Kafka Topics |
| 64 | May 24 | Kafka Partitions — The unit of parallelism |
| 65 | May 25 | Kafka Brokers & Clusters |
| 66 | May 26 | Consumer Groups — Kafka's horizontal scaling model |
| 67 | May 27 | Offsets — How consumers track progress |
| 68 | May 28 | Kafka Replication — Brokers, leaders, followers |
| 69 | May 29 | ZooKeeper vs KRaft — Kafka's metadata evolution |
| 70 | May 30 | Producer Acknowledgments (acks=0, 1, all) |
| 71 | May 31 | At-most-once vs At-least-once vs Exactly-once |
| 72 | Jun 1 | Consumer Lag — The #1 Kafka operational metric |
| 73 | Jun 2 | Partition Keys — Why they determine everything |
| 74 | Jun 3 | Schema Registry — Preventing silent breaking changes |
| 75 | Jun 4 | Kafka Connect — Zero-code data pipelines |
| 76 | Jun 5 | Kafka Streams & ksqlDB — Stream processing |
| 77 | Jun 6 | Log Compaction — Kafka as a key-value store |
| 78 | Jun 7 | When Kafka shines: Decoupling services |
| 79 | Jun 8 | When Kafka shines: Event Replay & Auditability |
| 80 | Jun 9 | When Kafka shines: High-throughput ingestion |
| 81 | Jun 10 | When NOT to use Kafka |
| 82 | Jun 11 | Kafka vs RabbitMQ |
| 83 | Jun 12 | Kafka vs AWS SQS |
| 84 | Jun 13 | Kafka vs Redis Streams |
| 85 | Jun 14 | Event-Driven Architecture with Kafka |
| 86 | Jun 15 | CQRS & Event Sourcing |
| 87 | Jun 16 | Real-world Kafka: Uber, Netflix, Instagram |
| 88 | Jun 17 | Kafka in system design interviews — The golden phrase |
| 89 | Jun 18 | System design interview cheatsheet — All 5 chapters |
| 90 | Jun 19 | 90-day wrap-up — What we learned |

---

## Post Format Template

**Hook** (1–2 lines, scroll-stopper)
**Body** (3–5 bullet points or short paragraphs)
**Analogy or Real Example**
**Key Takeaway**
**CTA** (comment, follow, share)
**Hashtags** (5–8)

---

## Posts Written

- [x] Day 1 — What is an API?
- [x] Day 2 — HTTP Methods
- [ ] Day 3 onwards...
