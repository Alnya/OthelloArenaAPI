# OthelloArenaAPI
This is Othello Arena API by Alnya.

## Introduction
This API is deployed on Heroku.<br>
The base program is [here](https://github.com/Alnya/PBL_Othello/blob/master/OthelloAction-strong.py).<br>
Front-end program is [here](https://github.com/Alnya/Alnya.github.io).<br>
Playing-Othello page is [here](https://alnya.github.io/othello-alnya/).<br>

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
