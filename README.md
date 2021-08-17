# OthelloArenaAPI
This is Othello Arena API by Alnya.

---

## Introductions
This API is deployed on Heroku.<br>
[The base program](https://github.com/Alnya/PBL_Othello/blob/master/OthelloAction-strong.py).<br>
[Front-end program](https://github.com/Alnya/Alnya.github.io).<br>
[Back-end program(this program)](https://github.com/Alnya/OthelloArenaAPI).<br>
[Playing-Othello page](https://alnya.github.io/othello-alnya/).<br>

---

## How to use this program

### Get Alnya's action and executed board
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

### Get your moves
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

### Execute your action
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

---

## Authors
[OthelloLogic.py](OthelloLogic.py) by Tokyo Denki University's Data Science & Machine Learning Lab.<br>

***All others*** by Alnya.
