# Example

```
 + - - +
 0 + - -
 - 0 + -
 - + + 0
```

```python
z0 = x0 - x1 - x2 + x3
z1 = x1 - x2 - x3
z2 = -x0 + x2 - x3
z3 = -x0 + x1 + x2

```

```python
nx3 = -x3;
t0 = x0 - x2;
t1 = x1 + nx3;
z0 = t0 - t1;
z1 = t1 - x2;
z2 = nx3 - t0;
z3 = x1 - t0;
```
