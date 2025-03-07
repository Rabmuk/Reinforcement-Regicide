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

## insights

Because you can play multiple cards at once there's not a descrete actions space. If the most favored card can be played, then also check the second most favored action.

Author:
Alex Kumbar