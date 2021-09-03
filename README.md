# SteNuScanner
Web Vulnerability Scanner

This scanner is inspired by the Ideas found in ZAP Proxy, Wapiti, Watobo and BurpSuite. It is a project for my master thesis and mainly focused on educational purpose.

For installation you just have to copy it to your system, run the install script in the install folder (alternativly install the packages in modules.txt with the command in the installation script) and copy the selenium drivers in a PATH directory (described in install_Driver_README.txt in folder install). 

The scan options can be given via the main menu or via command line arguments (for command line arguments just add the arguments with spaces behind the programm call).

Example: 

python ./scanner.py http://localhost:8000 2 1 1 (call with command line arguments)

python ./scanner.py (main menu)

Good Luck testing and there is always a possibility that bugs are included.

SteNu5
