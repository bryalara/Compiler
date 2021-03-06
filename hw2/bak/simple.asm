Section .data
	flag:	   word
	answer:	word
	alpha:	word
	gamma:	word
	C3P0:	   word
	R2D2:	   word
Section .code
	LVALUE	flag
	PUSH	1
	STO
	LVALUE	alpha
	PUSH	30
	STO
	LVALUE	gamma
	PUSH	18
	STO	
	LVALUE	C3P0
	PUSH	5
	STO
	LVALUE	R2D2
	PUSH	2
	STO	
	LVALUE	answer
	RVALUE	alpha
	PUSH	2
	RVALUE	gamma
	MPY
	RVALUE	C3P0
	RVALUE	R2D2
	SUB
	DIV
	ADD
	STO
	RVALUE	answer
	PRINT
	HALT