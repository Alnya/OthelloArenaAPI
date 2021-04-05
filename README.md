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
00000000"  https://othello-arena-api.herokuapp.com/post
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
00000000"  https://othello-arena-api.herokuapp.com/get_moves
```

## Execute your action
```
curl -X POST -d "num=
00000000
00000000
00000000
000-11000
0001-1000
00000000
00000000
00000000
&action=19"  https://othello-arena-api.herokuapp.com/player_execute
```
