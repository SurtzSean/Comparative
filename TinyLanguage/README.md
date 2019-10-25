# Tiny Language using top down recursion
interpreter which uses the top-down recursive descent method and inhereted/synthesized attributes to parse and evaluate a simple programming language based on the following grammar:
```
<prog> 		::= <let-in-end> { <let-in-end> }
<let-in-end> 	:: = let <decl-list> in <type> ( <expr> ) end ;
<decl>			::= id : <type> = <expr> ;
<type>			::= int | real
<expr>			::= <term> { + <term> | - <term> } | if <cond> then <expr> else <expr>
<term>			::= <factor> { * <factor> | / <factor> }
<factor>		::= ( <expr> ) | id | number | <type>(id)
<cond>			::= <oprnd> < <oprnd> | <oprnd> <= <oprnd> | <oprnd> > <oprnd> | <oprnd> >= <oprnd> | <oprnd> == <oprnd> | <oprnd> <> <oprnd>
<oprnd>			:= id | intnum
```
# Sample Run
#### Input
```
let x : int = 5 ;
in
        int ( x + 3 * x )
end ;
let r : real = 10.0 ;
        pi : real = 3.1416 ;
in
        real ( pi * r * r )
end ;
let a : int = 3 ;
b : real = 0.5 ;
c : real = b * b ;
in
        real ( if a > 5 then b + 1.1 else c )
end ;
let x : int = 7 ;
y : real = 3.0 ;
in
        real ( ( real ( x ) + y ) * ( real ( x ) - y ) )
end ;

let x : int = 7 ;
        y : real = 3.0 ;
        z : int = 2 ;
in
        int ( if y <> 3.0 then z * int ( y ) else x + z )
end ;
let x : int = 1 ;
	in
		int ( int ( x ) )
end ;
let x = 8 ; in ( x + y ) end ;
```

#### Output
```
~/Desktop/CIS424% ./let.py test.tiny
20
314.16
0.25
40.0
9
1
```
