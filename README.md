
# Admiral Arithmetic

Project for EnlighteNUS, a hackathon organized by NUS-IEEE on 23rd-24th February, 2019. 

With the theme being Education, we decided to make a teaching tool to help kids learn basic arithmetic: A modified real-time spinoff of the common two-player board game _Battleships_ where opportunities are created when a player successsfully solves simple, randomly generated math problems.

Code:
 - client.py (client code for RPi)
 - server.py (server code for another RPi)
 
 Setup:
 - connect to server
 - initialize variables
 - get question list from server
 - get user input for ship positions
 - submit confirmation 
 - wait for both players confirmation 

Loop:
- display qn no., current qn,
- wait for user input; thread with death/win
- if wrong, say wrong and go back to user input
- else, wait for user input on attack vector & start 5-second timer
- while timer<=5 || invalid/no input, wait for user input, else, send random attack vector

Interrupts:
- Attack interrupt (software interrupt when attack is made) (uses threading)
	- update P1 array after receiving data of P2 attack
- Hardware interrupt (button to change LED display to opponents)
