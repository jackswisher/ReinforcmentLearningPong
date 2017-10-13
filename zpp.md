# Z++

## Questions

1.

```
function subtract($x, $y)
{
    return(add($x, -$y))
}
```

2.

```
function multiply($x, $y)
{
    $result <- 0
    while ($y)
    {
        $result <- add($result, $x)
        $y <- subtract($y, 1)
    }
    return($result)
}
```

3.

```
function multiply($x, $y)
{
    if ($y)
    {
        return(add($x, multiply($x, subtract($y, 1))))
    }

    return 0
}

```

## Debrief

1. No resources

2. 15 minutes
