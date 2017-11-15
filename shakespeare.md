# To be or not to be

## ~~That is the question~~ These are the questions

4.1. 1000 DNA objects

4.2. The method update_fitness calculates the average of how close the two strings are to each other. To do this it adds one to a total if the characters at the same index in the target string and the string we are testing match and then divides by the length of the phrase to get the average.

4.3. 1 letter matches so update_fitness would compute 1 / 18 as a float which is 0.05555555555555555 as a float (according to the python repl).

4.4. If we made fitness equal to one minus the edit distance divided by the length of the string, we could get a similarly functional fitness function. The fitness would be one when the two strings were identical and the closer the two strings are to each other the greater the fitness.

4.5. This is part of the idea behind genetic algorithms as a way to "mimic" evolution, without it we could not solve the problem using a genetic algorithm. In this case, it introduces new letters into the gene pool. Otherwise we might not ever have the right character in the right location unless one of the children has that character in the right location.

## Debrief

a. The given link and the python repl

b. 20 minutes
