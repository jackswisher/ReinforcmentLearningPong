# Fair and Balanced

## Questions

1. Yes because it is an array with an odd number of elements we calculate the left side and the right side while ignoring the middle element. LHS = 16 + 26 = 42, RHS = 3 + 39 = 42. Therefore LHS = RHS, so the array is balanced.

2. Yes, odd number of elements, LHS = 0 + 0 = 0, RHS = 0 + 0 = 0. Therefore the array is balanced.

3.

```c
bool balanced(int array[], int n)
{
    int leftSum = 0;
    int rightSum = 0;
    int middlePos = n / 2;
    if (n % 2 == 0)
    {

        for (int i = 0; i < n; i++)
        {
            if (i < middlePos)
            {
                leftSum += array[i];
            }
            else
            {
                rightSum += array[i];
            }
        }
    }
    else
    {
        for (int i = 0; i < n; i++)
        {
            if (i < middlePos)
            {
                leftSum += array[i];
            }
            else if (i > middlePos)
            {
                rightSum += array[i];
            }
        }
    }

    return leftSum == rightSum;
}
```

## Debrief

1. No resources used.

2. 10 minutes.
