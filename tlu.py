"""
threshold-logic-unit
A minimal, faithful replication of the McCulloch-Pitts neuron.

Paper:  Warren S. McCulloch & Walter Pitts (1943).
        "A Logical Calculus of the Ideas Immanent in Nervous Activity."
        The Bulletin of Mathematical Biophysics, 5(4):115-133.
        https://doi.org/10.1007/BF02478259

One neuron, four ideas, in the smallest form that stays true to the paper.
Run:  python tlu.py
"""


# -- The neuron ----------------------------------------------------------------
# A 1943 McCulloch-Pitts neuron is "all-or-none": each instant it either fires
# (1) or it doesn't (0). It has NO weights and does NOT learn. It simply COUNTS
# its active excitatory inputs and fires when that count reaches a fixed integer
# threshold -- UNLESS any inhibitory input is active, which absolutely vetoes
# firing (the paper's Assumption 4).
#
#   fire = (count of active excitatory inputs >= threshold) AND (no inhibitor on)
def mp(exc, inh, theta):
    return int(not any(inh) and sum(exc) >= theta)


# -- Part 1: one neuron is a logic gate ----------------------------------------
# Pick the threshold and you pick the gate.
AND = lambda a, b: mp([a, b], [], 2)   # needs BOTH inputs  -> threshold 2
OR  = lambda a, b: mp([a, b], [], 1)   # needs EITHER input -> threshold 1
NOT = lambda a:    mp([], [a], 0)      # fires by default; its input inhibits it


# -- Part 2: a NETWORK of neurons computes ANY logic (e.g. XOR) -----------------
# No single threshold makes one neuron do XOR (it isn't linearly separable).
# But wire a few together and you can build anything (the paper's Theorems I-II):
#     a XOR b = (a OR b) AND NOT(a AND b)
def XOR(a, b):
    return AND(OR(a, b), NOT(AND(a, b)))


# -- Part 3: a LOOP gives memory ("a memory -- or an idea") ---------------------
# Feed a neuron's own output back into itself. Once "set", it keeps re-firing
# (reverberates) and so REMEMBERS it was switched on -- until "reset" inhibits
# it. This is the paper's "net with a circle": the same looping trick the authors
# show can even stand in for learning (Theorem VII).
def memory(events):
    state, timeline = 0, []
    for set_, reset_ in events:                  # each tick: (set?, reset?)
        state = mp([set_, state], [reset_], 1)   # fire if set OR still-on, unless reset
        timeline.append(state)
    return timeline


# -- Show it -------------------------------------------------------------------
if __name__ == "__main__":
    bits = [(0, 0), (0, 1), (1, 0), (1, 1)]

    print("AND (threshold 2: needs both)")
    for a, b in bits:
        print(f"  {a} {b} -> {AND(a, b)}")
    print("\nOR  (threshold 1: needs either)")
    for a, b in bits:
        print(f"  {a} {b} -> {OR(a, b)}")
    print("\nNOT (input inhibits a default-on neuron)")
    for a in (0, 1):
        print(f"  {a} -> {NOT(a)}")
    print("\nXOR (a network: (a OR b) AND NOT(a AND b))")
    for a, b in bits:
        print(f"  {a} {b} -> {XOR(a, b)}")

    print("\nMemory -- a loop that remembers (set@t1, reset@t4)")
    events = [(0, 0), (1, 0), (0, 0), (0, 0), (0, 1), (0, 0)]
    print("  set/reset:", events)
    print("  state:    ", memory(events))

    # the math must match the paper
    assert [AND(a, b) for a, b in bits] == [0, 0, 0, 1]
    assert [OR(a, b) for a, b in bits] == [0, 1, 1, 1]
    assert [NOT(a) for a in (0, 1)] == [1, 0]
    assert [XOR(a, b) for a, b in bits] == [0, 1, 1, 0]
    assert memory(events) == [0, 1, 1, 1, 0, 0]
    print("\nAll checks pass -- one neuron, four ideas, true to 1943.")
