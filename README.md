# Industrial-Cadets-2021

This is a college project which is part of the Industrial Cadets Program.

## Running the program
1. Clone this repository by running `git clone https://github.com/Ru-Pirie/Industrial-Cadets-2021.git`

2. In order to run the programs contained you will need to have python 3 installed as well as nodejs. They can be downloaded [HERE](https://nodejs.org/en/) and [HERE](https://www.python.org/downloads/)

3. Open 2 terminal windows and navigate to where the the program is located. You will need to in the directory called `/server` run `npm i express multer body-parser` and in the directory `/door` run `pip install requests` before they will run.

4. Once all of the terminals are open you should have the following:
    - One terminal in `/Industrial-Cadets-2021/door`
    - One terminal in `/Industrial-Cadets-2021/server`

5. In the door directory run `python3 alpha.py`. In the server one run `node server.js`. This should start both.

## Testing
With the shells running press enter to upload an image and see the result in `Industrial-Cadets-2021/server/images/alpha/`

This is just an example of how an image can be uploaded from a python program which would be running on a raspberry pi. To a express server running on another machine.