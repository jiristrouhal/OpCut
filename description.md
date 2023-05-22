# Best Cut


## Task
Deliver a program, that takes set of lengths and set of available stock pieces, with a specified quantity assigned to each of them (e.g. the unit price). The program then produces the best cut in terms of a minimal sum of the quantity's values over all the used stock pieces. The cutted pieces are grouped and assigned to each of the required lengths to be covered.

### Example
You have to use stock consisting of 1 m and 2 m long pieces and you want to cover three lengths, being 8 m, 1.5 m and 0.9 m. Find a way to use a specified number of stock and to cut them so the total length of the used stock is minimum.

### Trivial example
You can use 1 m stock lengh and you have to cover 8 m lenght. This should result in the optimal cut being one group of eight 1 m long pieces.

### Prioritize the cut with less cutted pieces
If you could use also 2 m stock length, the program should instead produce a single group of four 2 m long pieces.

## Structure of the program
The program should consist of the following parts:
1. the user input for the required lengths and the stock along with the optinal specification of variable;
2. part generating all possible variants, that can be combined to the lengths specified;
3. part choosing a certain number of the best variants;
4. the output, presenting the selected variants

### Generation of variants
To avoid problems with not enough memory to store all the generated variants, every variant is tested to be better than the currently found optimum, immediatelly after it is generated and it is stored only as the optimum, if it's better than the previously found optimum variant. 

The structure is thus modified into the following:
1. the user input for the required lengths and the stock along with the optinal specification of variable;
2. generation of the next untested variant;
3. comparison of the new variant and if it is found better, storing it as the optimum variant;
4. checking, if all the possible variants have been tested;
5. showing the output = list of *n* best variants.

