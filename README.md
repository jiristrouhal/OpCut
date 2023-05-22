# Problem
Select, cut and combine set of stock pieces to create desired set of lengths, with minimum
1. cost of the ordered stock (this is a priority) and
2. the total number of cuts.

From the selected, prefer those options, for which joints are closer to the combined pieces' ends.

# Solution
1. Pick the least expensive combination of stock pieces.
2. Sort both the required lengths and the stock to match each other maximally to prevent unnecessary cuts.
3. Cut and group the produced pieces a) by the length, which they're combined into and b) by the stock, from which they've been cut.



