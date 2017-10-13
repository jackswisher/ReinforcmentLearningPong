# #functions

## Questions

1. This inplementation would be slow because there would be many collisions, because it is storing them by their first letter. This means that if any two strings have the same first letter then there will be a collision. The more collisions there are the slower the hash table.

2. In theory this may be a "perfect" hash function, however the size of the necessary hash for there to be a unique bucket for every possibility. In the given example a simple 3 letter string would require an array of length 4276803 to store it uniquely, otherwise the modulus function would need to be used. So in practice we do not have enough storage space for this to be a perfect hash function.

3. It takes much less space to store 50 strings rather than 50 JPEGs and it is also much faster to check because rather than having to check every pixel, the hash function can be applied to the image and if the hashes don't match then the files are not the same.

4. A trie uniquely stores a string and that string can be navigated to in 0(1), however in the worst case the hash fucntion could store every element in one bucket which would be the same as linear searching, which is O(n).

## Debrief

1. No resources.

2. 10 minutes.
