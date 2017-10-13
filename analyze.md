# Analyze This

## Questions

1a. Yes, because once the second digits are sorted and the second pass begins, by sorting them by first number the cards will be in order. The first card for each 1st number will have a 1 in the second digit and so on.

1b. The algorithm will be O(n^2) assuming that one pass must be made for each number, worst case scenario: Stelios has to go through every card to find the next one to put in the list for each card, thus O(n^2).

2a. Yes, this algorithm will work because it is essentially bubble sort but oscillates between bubbling down and bubbling up with each pass. The algorithm is known as "Cocktail shaker sort" and offers only marginal performance benefits.

2b. The algorithm will be O(n^2) because it still takes a similar number of passes as bubble sort and requires each element to be compared to every other element in the worst case, which is O(n^2).

3a. Yes, this algorithm is essentially linear search, with the added twist of shuffling with each pass.

3b. The algorithm is O(n) because in the worst case it will look through every card until it finds the Queen of Hearts, which is O(n).

## Debrief

1. I found wikipedia helpful in cofirming my suspicions about one of the sorting algorithms.

2. I took about 10 minutes to answer this question.
