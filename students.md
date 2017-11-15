# Comparing Students

## Questions

1.1. That required parameter represents a comparison function that takes in two pointers to objects in an array and given those parameters a and b, the function is specified to return a negative integer if a is less than b, an integer of zero if they are equal, or a positive integer if b is greater than a. How we define what "greater" entails is specific to the objects that we want to compare.
In the case of students who we wish to sort by name, it would make sense to compare the two names and return an int according to the previous statement.

1.2. They must be typecast to const int * because in the example we are trying to compare two integers, which we retrieve by de-referencing the pointers a and b and asigning them to temporary variables arg1 and arg2.
They must be typecast because C is a statically typed language, so we must specify that while they are initally referenced as const void *, we want them treated as const int *, otherwise the compiler will complain about a type mismatch and fail to compile.

1.3. See `students.c`.

1.4. See `students.py`.

1.5. See `students.js`.

## Debrief

a. I found the Sorting HOW TO by python to be helpful to see how a lambda function works.

b. 20 minutes
