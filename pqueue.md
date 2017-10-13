# Now Boarding

## Questions

1.

```c
typedef struct
{
    passenger current;
    pqueue *next;
}
pqueue;
```

2. while new passenger's group > temp.current.group check pqueue.next
    if null, set next to a malloc'd pqueue with new passenger as the current passenger and next as NULL, set bool addedPassenger to true
    otherwise set temp to temp.next
  Out of the loop, if addedPassenger then do nothing, otherwise create a new pqueue with current as the new passenger and next as temp.next

3. This alogrithm will be O(n) because in the worst case scenario it will have to check every passenger and then add the new passenger to the back. It will be a linear search.

4. call the current pqueue temp, store passenger temp.current, if temp.next != NULL then set temp = temp.next, return the stored passenger (Will return null if the pqueue is empty)

5. This algorithm will be O(1) because it just has to return the first element in the linked list in every case. Thus O(1).

## Debrief

1. None

2. 15 minutes
