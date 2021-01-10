# password-memorizer
Programm to help you memorize complex passwords.

## Disclaimer
Never enter your passwords into programs, that you don't trust. Take responsibility for your own security and examine the code.

## How it works
This program will repeatedly ask you to enter your password. After you entered it, it will tell you, if your input was correct or wrong and show you some statistics. It checkes the validity of your password using hashes. The salted hash is calculated, when you first add your password. This way your actual password is never stored on the disk.

The hashes are stored in a csv file. The programm also allows you to remove entrys from that file. 
