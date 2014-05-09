input: n
output: list of primes
eratos(n)
  a[1] := 0                          
  for i := 2 to n do a[i] := 1
  p := 2
  while p2  <  n do
    j := p2
    while j  <  n do
      a[j] := 0
      j := j+p
    repeat p := p+1 until a[p] = 1   
  return a