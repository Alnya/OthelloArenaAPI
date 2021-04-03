# OthelloArenaAPI
This is Othello Arena API by Alnya.

## Get Alnya's action and executed board
```
curl -X POST -d "num=
00000000
00000000
00000000
000-11000
0001-1000
00000000
00000000
00000000"  http://127.0.0.1:5000/post
```
```
curl -X POST -d "num=
00000000
00000000
00000000
000-11000
0001-1000
00000000
00000000
00000000"  https://othello-arena-api.herokuapp.com/get
```

## Get your moves
```
curl -X POST -d "num=
00000000
00000000
00000000
000-11000
0001-1000
00000000
00000000
00000000"  http://127.0.0.1:5000/get_moves
```
```
curl -X POST -d "num=
00000000
00000000
00000000
000-11000
0001-1000
00000000
00000000
00000000"  https://othello-arena-api.herokuapp.com/get_moves
```