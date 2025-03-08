Goal is to build a text based version of the Regicide card game, then use ML to make an agent that can play the game.

Rules pdf: https://www.regicidegame.com/site_files/33132/upload_files/RegicideRulesA4.pdf?dl=1

```
python -3.13 -m venv ./torch_venv
```

```
pip install torch
pip install matplotlib
```

## Tutorial

Gained many insights from pytorch official reinforcement learning tutorial
https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

## action_space 1st pivot

['yield_', 'ac', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', 'jc', 'qc', 'kc', 'ad', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', 'jd', 'qd', 'kd', 'ah', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', 'jh', 'qh', 'kh', 'as', 
'2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', 'js', 'qs', 'ks', 'ac2c', 'ac3c', 'ac4c', 'ac5c', 'ac6c', 'ac7c', 'ac8c', 'ac9c', 'ac10c', 'acjc', 'acqc', 'ackc', 'acad', 'ac2d', 'ac3d', 'ac4d', 'ac5d', 'ac6d', 'ac7d', 'ac8d', 'ac9d', 'ac10d', 'acjd', 'acqd', 'ackd', 'acah', 'ac2h', 'ac3h', 'ac4h', 'ac5h', 'ac6h', 'ac7h', 'ac8h', 'ac9h', 'ac10h', 'acjh', 'acqh', 'ackh', 'acas', 'ac2s', 'ac3s', 'ac4s', 'ac5s', 'ac6s', 'ac7s', 'ac8s', 'ac9s', 'ac10s', 'acjs', 'acqs', 'acks', 'ad2c', 'ad3c', 'ad4c', 'ad5c', 'ad6c', 'ad7c', 'ad8c', 'ad9c', 'ad10c', 'adjc', 'adqc', 'adkc', 'ad2d', 'ad3d', 'ad4d', 'ad5d', 'ad6d', 'ad7d', 'ad8d', 'ad9d', 'ad10d', 'adjd', 'adqd', 'adkd', 'adah', 'ad2h', 'ad3h', 'ad4h', 'ad5h', 'ad6h', 'ad7h', 'ad8h', 'ad9h', 'ad10h', 'adjh', 'adqh', 'adkh', 'adas', 'ad2s', 'ad3s', 'ad4s', 'ad5s', 'ad6s', 'ad7s', 'ad8s', 'ad9s', 'ad10s', 'adjs', 'adqs', 'adks', 
'ah2c', 'ah3c', 'ah4c', 'ah5c', 'ah6c', 'ah7c', 'ah8c', 'ah9c', 'ah10c', 'ahjc', 'ahqc', 'ahkc', 'ah2d', 'ah3d', 'ah4d', 'ah5d', 'ah6d', 'ah7d', 'ah8d', 'ah9d', 'ah10d', 'ahjd', 'ahqd', 'ahkd', 'ah2h', 'ah3h', 'ah4h', 'ah5h', 'ah6h', 'ah7h', 'ah8h', 'ah9h', 'ah10h', 'ahjh', 'ahqh', 'ahkh', 'ahas', 'ah2s', 'ah3s', 'ah4s', 'ah5s', 'ah6s', 'ah7s', 'ah8s', 'ah9s', 'ah10s', 'ahjs', 'ahqs', 'ahks', 'as2c', 'as3c', 'as4c', 'as5c', 'as6c', 'as7c', 'as8c', 'as9c', 'as10c', 'asjc', 'asqc', 'askc', 'as2d', 'as3d', 'as4d', 'as5d', 'as6d', 'as7d', 'as8d', 'as9d', 'as10d', 'asjd', 'asqd', 'askd', 'as2h', 'as3h', 'as4h', 'as5h', 'as6h', 'as7h', 'as8h', 'as9h', 'as10h', 'asjh', 'asqh', 'askh', 'as2s', 'as3s', 'as4s', 'as5s', 'as6s', 'as7s', 'as8s', 'as9s', 'as10s', 'asjs', 'asqs', 'asks', '2c2d', '2c2h', '2c2s', '2d2h', '2d2s', '2h2s', '2c2d2h', '2c2d2s', '2c2h2s', '2d2h2s', '2c2d2h2s', '3c3d', '3c3h', '3c3s', '3d3h', '3d3s', '3h3s', '3c3d3h', '3c3d3s', '3c3h3s', '3d3h3s', '4c4d', '4c4h', '4c4s', '4d4h', '4d4s', '4h4s', '5c5d', '5c5h', '5c5s', '5d5h', '5d5s', '5h5s']

this does not work on defense. Would need to split the model into attack model and defense model. I'm worried this won't train correctly

going to change the actions space

## 2nd pivot

instead of model predicting card command, the model will predict how many cards to play from the hand

like:
['1','2','3'
'1,2','1,3','2,3' ]

there are 127 combinations of cards that can be played from a 7 card hand. when looking at only 1st card or 1st and 2nd card or only 2nd card ...

## insights

Because you can play multiple cards at once there's not a descrete actions space. If the most favored card can be played, then also check the second most favored action.

Author:
Alex Kumbar