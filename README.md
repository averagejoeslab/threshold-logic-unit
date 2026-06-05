# threshold-logic-unit

A tiny, faithful replication of the paper that **invented the artificial neuron**:

> Warren S. McCulloch & Walter Pitts (1943). *A Logical Calculus of the Ideas Immanent in Nervous Activity.* Bulletin of Mathematical Biophysics 5:115–133. [doi:10.1007/BF02478259](https://doi.org/10.1007/BF02478259)

The whole idea fits in **one neuron and ~30 lines of Python** ([`tlu.py`](./tlu.py)). This README walks the paper's arc in plain language — the math included.

---

## The big idea

A real neuron is **all-or-none**: in any instant it either *fires* or it *doesn't*. Nothing in between.

McCulloch & Pitts noticed that "this neuron fired" is therefore just a **true / false** statement. And if neurons are little true/false elements, then a **network of neurons is a circuit that computes logic** — AND, OR, NOT, and anything built from them.

That's the entire paper in one sentence. Everything below unpacks it.

## The neuron (the only math you need)

Their neuron is gloriously simple. It has:

- some **excitatory** inputs (they push it *toward* firing),
- some **inhibitory** inputs (they *veto* firing),
- a fixed whole-number **threshold** `θ`.

The rule:

> **Fire** if the number of active excitatory inputs is **at least `θ`** — **and** no inhibitory input is active.

```
fire = (count of active excitatory inputs ≥ θ)  AND  (no inhibitor active)
```

Two things surprise modern readers:

1. **No weights.** It just *counts* inputs. (Weighted inputs arrive 15 years later, with Rosenblatt's perceptron.)
2. **No learning.** You wire it by hand, and inhibition is **absolute** — a single active inhibitor stops the neuron cold, no matter how many excitatory inputs are on.

In code, that is a single line:

```python
mp = lambda exc, inh, theta: int(not any(inh) and sum(exc) >= theta)
```

## Part 1 — one neuron *is* a logic gate

Choose the threshold and the same neuron becomes a different gate:

| Gate | How it works | Threshold |
|------|--------------|-----------|
| **AND** | needs *both* inputs | `θ = 2` |
| **OR**  | needs *either* input | `θ = 1` |
| **NOT** | a default-on neuron that its input *inhibits* | `θ = 0`, 1 inhibitor |

## Part 2 — a network computes *anything*

One neuron has a famous limit: it **cannot** compute **XOR** ("one or the other, but not both"). XOR isn't *linearly separable* — no single threshold splits its true cases from its false ones.

The fix is the paper's first big result: **wire neurons together and you can build any logic at all.** For XOR:

```
a XOR b  =  (a OR b)  AND  NOT(a AND b)
```

Three gates, one little network. (McCulloch & Pitts prove this works for *every* logical expression — Theorems I & II.)

## Part 3 — a loop gives memory

So far everything flows forward. Now **feed a neuron's output back into itself.**

Once you "set" it, it keeps re-triggering itself — it **reverberates** — so it *remembers* that it was switched on, until something "resets" (inhibits) it. The authors call such a firing "a memory — or an idea."

This is the paper's second half ("nets with circles"), and it is how the network gains **state**. (They even show this looping trick can stand in for *learning* — Theorem VII.)

## The punchline

Put it together and a network of these neurons is exactly a **finite-state machine** — logic plus memory. The authors close with the famous result:

> a net "furnished with a tape, scanners… and suitable efferents… can compute only such numbers as can a Turing machine."

In other words: **network + an external memory tape = a universal computer.** This paper is the bridge from *brains* to *computers* — written in 1943, before either modern neuroscience or the digital computer existed.

## Why it still matters

This is the **ancestor of every neural network.** The next step in the story is [Rosenblatt's perceptron (1958)](https://doi.org/10.1037/h0042519): take this neuron, **add tunable weights and a learning rule**, and it can now *learn from data* instead of being wired by hand. That one change starts machine learning.

## Run it

```bash
python tlu.py
```

No dependencies. It prints the truth tables for AND / OR / NOT / XOR and a memory timeline, and checks every result against what the paper says.

---

*Educational reconstruction by [Average Joes Lab](https://averagejoeslab.com). All credit for the ideas to McCulloch & Pitts (1943).*
