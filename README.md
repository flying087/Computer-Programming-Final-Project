# Computer-Programing-Final-Project

My final project is  a shoot-'em-up “bullet hell” game using PyGame. In this game, the objective is to defeat the boss enemy by shooting at it while avoiding the bullets that it fires. The catch is that the boss enemy fires hundreds of bullets at a time, so the player is required to move precisely to dodge the bullets.

## How to play

### Basics
The game plays like any other bullet hell. You have 3 lives, and if you get hit by a bullet you loose a life. Loose all 3 lives and you die. You get a short period of invincibility after losing a life, signaled by your ship rapidly blinking for a few seconds. To win, you need to reduce the boss' health points (HP) to zero. 

### Controls
You can damage the boss by shooting at it. To shoot, hold the **[Z]** key. You'll fire three bullets, one of which will automatically target the boss while the other two will travel in a straight line. When dodging the boss' attacks, you may need to be more prescise in your movements or wish to see your hitbox. You can do this by holding the **[X]** key, which slows your ship down and displays your hitbox as a red square. 

### Hitbox
You only loose a life when your hitbox is hit, not your entire ship. Since your hitbox is a lot smaller than your actual ship, you can maneuver through gaps that may not seem wide enough at first.