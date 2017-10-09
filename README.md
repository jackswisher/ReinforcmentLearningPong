# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

According to the Oxford English dictionary, it means "an invented long word said to mean a lung disease caused by inhaling very fine ash and sand dust."

Source: https://en.oxforddictionaries.com/definition/pneumonoultramicroscopicsilicovolcanoconiosis

## According to its man page, what does `getrusage` do?

From the man page I see that 'getrusage' returns a data type rusage defined by a struct that contains the cpu runtime, memory used, along with other statistics about resource usage.

## Per that same man page, how many members are in a variable of type `struct rusage`?

There are 16 variables of type long in the struct rusage.

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

If we passed them directly rather than by reference, then a new copy would be made of each instance rather than just a pointer. This would take up unnecessary memory and slow the program down.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

The for loop functions similar to a while loop in that it keeps reading through a file while the character does not denote the end of the file.
Each iteration through the character is checked to see if it is alphabetical or an apostrophe not as the first character of a word.
If the word is longer than the max length then all the characters are disregarded and the loop prepares for a new word. If the letter is a digit then the word is disregarded.
In the case that the current character is not alphabetical or a digit and the index is greater than 0, then the null character is appended and the word is checked and the benchmark is updated.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

We use fgetc because we only want to accept alphabetical characters and apostrophes, which requires us to check each and every character.
If we used fscanf then we would have no control over whether a character is appended to the array, and we do not know whether they are all alphabetical.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

This way the original word could not be modified because it is a constant. This ensures that the letters are not changed while the word is being checked. Otherwise, the word could be modified.
