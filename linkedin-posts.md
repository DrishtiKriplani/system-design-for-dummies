# LinkedIn Posts — System Design for Dummies

---

## CONSISTENT HASHING — FINAL

---

Interviewer: "You have 3 servers handling your cache. You add a 4th. What happens?"

❌ Rejected:
"The new server joins and traffic gets balanced across all 4."

✅ Selected:
"When you add a server, the hashing changes. Almost all your cached data suddenly points to the wrong server. Your cache becomes useless overnight. Every request hits the database directly — at full traffic."

"To avoid this, I'd use consistent hashing. Think of servers arranged in a circle. Each piece of data goes to the nearest server on that circle. Add a new server — it only takes data from its one neighbor. Everything else stays exactly where it was."

---

The first candidate knew how to add a server.

The second candidate knew what breaks when you do.

That's the difference between a good answer and a great one.

Consistent hashing is used by Cassandra, DynamoDB, and Akamai for exactly this reason — scaling without surprises.

But consistent hashing alone isn't enough.

Even with a ring, one server can silently end up handling 3x more data than another — just due to how positions fall on the ring.

That's where virtual nodes come in.
Each physical server gets multiple spots on the ring — not just one.
Load spreads evenly. No hot servers. No surprises.

We've covered consistent hashing, virtual nodes, and how real systems use them — in detail — in the System Design for Dummies PDF.

Link in the comments.

#SystemDesign #ConsistentHashing #BackendEngineering #StaffEngineer #TechInterview #DistributedSystems

---
---
**90-Day Content Calendar | Starting March 22, 2026**

---

## DAY 1 — March 22, 2026
**Topic: What is an API?**

---

Every app you love is secretly talking to dozens of others behind the scenes.

That conversation? It happens through APIs.

When you open Swiggy and see your order status — Swiggy's app is calling an API to fetch that data.
When you pay via UPI — an API sends your bank a message and waits for a yes or no.
When you "Login with Google" — an API hands Google your request and brings back your identity.

**So what exactly is an API?**

API stands for Application Programming Interface.
Think of it as a waiter in a restaurant.

You (the client) don't walk into the kitchen and grab your food.
You tell the waiter (the API) what you want.
The waiter goes to the kitchen (the server), gets it, and brings it back.

The kitchen doesn't need to know who you are.
You don't need to know how the kitchen works.
The waiter handles everything in between.

**The most important concept in an API: the Endpoint.**

An endpoint is a specific URL where a request can be sent.

```
GET https://api.swiggy.com/orders/12345
```

This is an endpoint that says:
→ "Give me the details of order #12345"

Every feature in an app maps to an endpoint.
- Get my profile → endpoint
- Place an order → endpoint
- Cancel a ride → endpoint

**The takeaway:**

APIs are the contracts between systems.
They define what you can ask for, how to ask it, and what you'll get back.

You don't need to know the internals.
You just need to know the contract.

That's the entire premise of modern software.

---

I'm breaking down system design — one concept at a time, for 90 days.
Follow along if you want to actually understand how large-scale systems work.

Day 2 tomorrow: HTTP Methods — GET, POST, PUT, DELETE and when to use each.

#SystemDesign #SoftwareEngineering #APIs #BackendDevelopment #TechLearning #Programming #100DaysOfCode #SystemDesignForDummies

---
---

## KAFKA POST
**Topic: What is Apache Kafka? (Staff Engineer Level)**

---

Most engineers add Kafka to their architecture diagrams before they can explain why.

Interviewers notice. Senior engineers notice. Your on-call rotation will notice at 3 AM.

Here's what Kafka actually is — and the mental model that makes the "when not to use it" decision obvious.

**Kafka is not a message queue.**

This is the most common misconception.

RabbitMQ, SQS — those are queues. Message goes in. Consumer reads it. Message is gone.

Kafka is an append-only, distributed commit log.

Messages are written to disk, replicated across brokers, and retained based on a policy — not deleted on consumption. A consumer reading a message doesn't affect any other consumer. A new service can join tomorrow and replay events from 7 days ago.

That single architectural decision — retention after consumption — is what makes Kafka a fundamentally different primitive.

**The abstraction that unlocks the design:**

Producer writes to a topic. Topic is split into partitions. Each partition is an ordered, immutable sequence of records. Consumers pull at their own pace and track their position via an offset.

No consumer is coupled to any producer. No producer knows or cares how many consumers exist.

This is why Zomato can add a new analytics consumer to `order.placed` without touching the order service. The producer has zero knowledge of its downstream dependencies.

**What most Kafka posts skip:**

The hard part isn't writing to a topic. It's your partition key.

Messages within a partition are strictly ordered. Across partitions — no ordering guarantee.

Use the wrong key and you get hot partitions: one partition handling 60% of traffic while others sit idle. Uber routes all events for the same rider to the same partition by keying on `user_id`. That's not a Kafka feature — it's a deliberate design decision.

**The throughput question engineers always ask:**

4M+ messages/second per broker. Zero-copy transfer (disk → network socket, no userspace copy). This is why Kafka wins at high-throughput ingestion where SQS (~3K/sec FIFO) or RabbitMQ (~50K/sec) simply can't compete.

But throughput is rarely the real reason to choose Kafka.

**The real reasons:**

→ Multiple independent consumers on the same event stream — consumer groups
→ Replay: replay 7 days of `payment-events` to fix a billing bug without touching the source system
→ Decoupling: your order service shouldn't know that 6 downstream services depend on it
→ Ordering guarantees per entity — impossible with a standard queue

**When Kafka is the wrong tool:**

One producer, one consumer, no replay? Use SQS. You're paying for operational complexity you don't need.

Request-response workflow? Kafka adds 10–100ms poll latency plus batching overhead. gRPC round-trips in 1–5ms. Don't use Kafka to solve a latency problem.

Low-scale async jobs? PostgreSQL with `SELECT ... FOR UPDATE SKIP LOCKED` handles hundreds of concurrent workers with zero infrastructure.

The engineers who impress in system design interviews aren't the ones who add Kafka everywhere.

They're the ones who say: "I'd use Kafka here specifically because we need multiple consumer groups and event replay. If it were a single consumer with no replay requirement, SQS is the right call."

That sentence signals you understand tradeoffs — not just tools.

---

What's the most painful Kafka misconfiguration you've debugged in production?

#Kafka #SystemDesign #DistributedSystems #BackendEngineering #SoftwareArchitecture #StaffEngineer

---
---

## CONSISTENT HASHING POST
**Topic: Consistent Hashing (Final v2)**

---

3 AM. Pagerduty fires.

Database CPU: 100%.
Cache hit rate: 4%.
On-call engineer: confused.

The cache wasn't down. It was full.
Full of keys no one was asking for anymore.

Someone had added a node to the cluster at midnight.

```
node = hash(key) % N
```

Change N by 1 → 91% of keys silently reroute.
A warm cache becomes a useless one. Instantly.

This is the modulo trap.
It's not a bug. It's the math working exactly as designed.

---

Consistent hashing exists for one reason:
make topology changes boring.

Instead of modulo, you place nodes on a ring.
Each key belongs to the nearest node clockwise.
Add a node → 1 neighbor loses some keys. That's it.
The rest of the cluster doesn't notice.

1/N keys move instead of N/N.

Cassandra, DynamoDB, Akamai, Discord all use this.
Not because it's elegant.
Because 3 AM should be boring.

---

One gotcha: a naive ring still creates uneven load.
One node can own 3× the keyspace of another.
Virtual nodes fix it — 150 positions per server, load variance ~10%.
Cassandra calls them tokens.

---

The ring solves reshuffling.
It doesn't solve hotspots — that's a different problem for a different post.

Scale without chaos. That's the job.

#SystemDesign #DistributedSystems #ConsistentHashing #BackendEngineering #StaffEngineer

---
---

## DAY 2 — March 23, 2026
**Topic: HTTP Methods — GET, POST, PUT, DELETE, PATCH**

---

Every time your app talks to a server, it uses one of 5 words.

Just 5.
And most developers use them wrong.

These are HTTP Methods — and they tell the server *what you want to do*, not just *where you want to go*.

Think of it like verbs in a sentence.
The URL is the noun. The method is the verb.

```
GET    /users/42        → Read user #42
POST   /users           → Create a new user
PUT    /users/42        → Replace user #42 entirely
PATCH  /users/42        → Update just one field of user #42
DELETE /users/42        → Delete user #42
```

**Here's how to remember them:**

🔵 **GET** — "Just looking." No changes. Safe to call 10 times, same result.
→ Load your Twitter feed. Fetch your bank balance. Search Google.

🟢 **POST** — "Create something new." Sends data in the request body.
→ Submit a form. Place an order. Register an account.

🟡 **PUT** — "Replace entirely." Send the full updated object.
→ Like overwriting a file. If you miss a field, it disappears.

🟠 **PATCH** — "Update just this one thing." Partial update.
→ Change your username without touching your email or profile pic.

🔴 **DELETE** — "Remove it."
→ Delete a tweet. Cancel a subscription. Remove a cart item.

**The most common mistake I see:**

Using POST for everything.

POST /updateUser — wrong.
POST /deleteUser — wrong.
POST /getOrders — please no.

This is called "tunnel vision" on POST. It ignores the semantics HTTP gives you for free.

When you use the right method:
✅ Caches know what to cache (GET responses are cacheable, POST aren't)
✅ Browsers know what's safe to retry
✅ Your API becomes self-documenting
✅ Load balancers and proxies behave correctly

**The real insight:**

HTTP methods aren't just syntax.
They're a contract about *what happens* when this request is made.

Breaking that contract means your API behaves unpredictably — for clients, caches, and your own team.

---

This is Day 2 of my 90-day system design series.
Yesterday: What is an API?
Tomorrow: The Request-Response Cycle — what actually happens between "send" and "receive."

Drop a comment if you've seen POST-for-everything in the wild. (We've all been there.)

#SystemDesign #APIs #HTTP #BackendDevelopment #SoftwareEngineering #WebDevelopment #TechLearning #SystemDesignForDummies
