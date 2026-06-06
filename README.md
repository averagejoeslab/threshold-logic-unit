# threshold-logic-unit

A tiny, faithful replication of the paper that **invented the artificial neuron**:

> Warren S. McCulloch & Walter Pitts (1943). *A Logical Calculus of the Ideas Immanent in Nervous Activity.* Bulletin of Mathematical Biophysics 5:115–133. [doi:10.1007/BF02478259](https://doi.org/10.1007/BF02478259)

The whole idea fits in **one neuron**, built up **one idea at a time** in a runnable notebook ([`tlu.ipynb`](./tlu.ipynb)) whose outputs are saved so you can read it like a story. This README walks the same arc in plain language — the math included.

---

## The big idea

A real neuron is **all-or-none**: in any instant it either *fires* or it *doesn't*. Nothing in between.

McCulloch & Pitts noticed that "this neuron fired" is therefore just a **true / false** statement. And if neurons are little true/false elements, then a **network of neurons is a circuit that computes logic** — AND, OR, NOT, and anything built from them.

That's the entire paper in one sentence. Everything below unpacks it — one step at a time.

## 1. The simplest possible neuron

Start with the least a neuron could do: **add up its inputs, and fire if the total is big enough.** That cutoff is the **threshold**. No weights, no learning — just counting.

```python
def neuron(inputs, threshold):
    total = sum(inputs)                     # count the inputs that are ON (the 1s)
    return 1 if total >= threshold else 0   # fire if the total reaches the threshold
```

## 2. Pick a threshold, get a logic gate

The first surprise: **the threshold alone turns this neuron into different gates.**

| Gate | How it works | Threshold |
|------|--------------|-----------|
| **AND** | needs *both* inputs | `2` |
| **OR**  | needs *either* input | `1` |

```python
def AND(a, b): return neuron([a, b], threshold=2)   # fires only if BOTH are on
def OR(a, b):  return neuron([a, b], threshold=1)   # fires if EITHER is on
```

## 3. We hit a wall: NOT

Try to build **NOT** — "fire when the input is *off*." You can't: adding inputs only ever pushes a neuron *toward* firing, never away from it.

So the model adds a second kind of input — an **inhibitory** one. In 1943 it's *absolute*: **a single inhibitory signal vetoes firing entirely**, no matter the total. That's the one piece we add:

```python
def neuron(inputs, threshold, inhibited=False):
    if inhibited:                           # one inhibitory signal stops it cold
        return 0
    total = sum(inputs)
    return 1 if total >= threshold else 0
```

Now **NOT** is a neuron that's *on by default* (threshold `0`, no excitatory inputs) which its input simply switches off:

```python
def NOT(a): return neuron([], threshold=0, inhibited=bool(a))
```

Two things surprise modern readers: **no weights** (it just *counts* — weighted inputs arrive 15 years later, with the perceptron) and **no learning** (you wire it by hand).

## 4. Wire gates into a network → *any* logic (XOR)

One neuron has a famous limit: it **cannot** compute **XOR** ("one or the other, but not both"). XOR isn't *linearly separable* — no single threshold splits its true cases from its false ones.

The paper's first big result fixes this: **wire neurons together and you can build any logic at all.**

```
a XOR b  =  (a OR b)  AND  NOT(a AND b)
```

Three gates we already built, wired into one little network. (McCulloch & Pitts prove this works for *every* logical expression — Theorems I & II.)

## 5. Loop it → memory

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

Open the notebook and run the cells top to bottom:

```bash
pip install jupyter
jupyter notebook tlu.ipynb
```

The outputs are already saved in the notebook, so you can also just **read it rendered on GitHub** — every cell shows its result. It builds the neuron up step by step (AND / OR / NOT / XOR and a memory loop) and self-checks every result against the paper. Only the Python standard library is used in the cells.

## Original paper

Everything in this repo is a reconstruction of:

> Warren S. McCulloch & Walter Pitts (1943). *A Logical Calculus of the Ideas Immanent in Nervous Activity.* The Bulletin of Mathematical Biophysics **5**(4):115–133. <https://doi.org/10.1007/BF02478259>

<details>
<summary>BibTeX</summary>

```bibtex
@article{mcculloch1943logical,
  title   = {A logical calculus of the ideas immanent in nervous activity},
  author  = {McCulloch, Warren S. and Pitts, Walter},
  journal = {The Bulletin of Mathematical Biophysics},
  volume  = {5},
  number  = {4},
  pages   = {115--133},
  year    = {1943},
  doi     = {10.1007/BF02478259}
}
```
</details>

---

*Educational reconstruction by [Average Joes Lab](https://averagejoeslab.com). All credit for the ideas to McCulloch & Pitts (1943).*
