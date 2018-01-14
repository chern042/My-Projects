'''This program is a fully functional, simple avoidance game. You play as a spaceship, with only two controls.
You can move up, and you can move down to avoid an ensemble of meteors in deep space heading towards you.
Each meteor you're lucky enough to avoid gets counted as a point, and when you do inevitably get hit, you can immortalize your score.
That is, provided it's good enough to go against the previous 5 highest scores. At the beginning of the program you can choose to see the top 5 high scores, or begin the game.
If you do begin the game, you can start avoiding those meteors! Once you lose, an entry box will require you to enter your name.
Provided you keep it less than 8 characters long, you can press enter and your name and score will be added to a file, and maybe the high scores menu.
It all starts over again.'''

#Culminating Project
#Carlos and Jaimison
#January 25, 2015

from tkinter import *
import random
import time
from operator import itemgetter


'''The shipPos function positions the ship and tracks its coordinates.'''
def shipPos(height):
    global shipVar
    global shipCoords
    shipVar = mainScreen.create_image(32,height,image=spaceShip,tag="spaceship") #Positions ship sprite in canvas.
    shipCoords = mainScreen.coords(shipVar) #Grabs ship's current coordinates.


'''The shipUp function moves the ship 30 pixels up.'''
def shipUp(event):
    global shipMove
    global shipCoords
    if shipMove >= -130: #If the ship hasn't moved past the top boundaries.
        shipMove -= 30 #Track ship's movement for canvas boundaries.
        mainScreen.move('spaceship',0,-30) #Move ship 30 pixels up.
    shipCoords = mainScreen.coords(shipVar) #Grabs ship's current coordinates after movement.


'''The shipDown function moves the ship 30 pixels down.'''
def shipDown(event):
    global shipMove
    global shipCoords
    if shipMove <= 190: #If the ship hasn't moved past the bottom boundaries.
        shipMove += 30 #Track ship's movement for canvas boundaries.
        mainScreen.move('spaceship',0,30) #Move ship 30 pixels down.
    shipCoords = mainScreen.coords(shipVar) #Grabs ship's current coordinates after movement.

'''The setHighScore function writes the current high score data to the high score file, then resets the instructions for the main screen again.'''
def setHighScore():
    mainScreen.delete(scoreText) #Delete the score text from canvas.
    highScore = meteorScore #Set the highscore to the same value as meteorScore.
    nameInput.destroy() #Destroy the nameInput entry box.
    mainScreen.delete("loseTitle1") #Delete first lose title.
    mainScreen.delete("loseTitle2") #Delete second lose title.
    scoreFile=open("highScores.txt","a") #Open the high scores file for appending.
    scoreFile.write(highName+"\n") #Writes the current player's name to the file.
    scoreFile.write(str(highScore)+"\n") #Writes the player's score to the file.
    buttonFrame.grid(row=0) #Places the frame with the buttons again on row 0.
    mainScreen.create_text(4,460,text="Instructions:",fill="red",font=('fixedsys',10),tag="instructions1",anchor="w") #Places instructions 1 again.
    mainScreen.create_text(4,475,text="Move Up: UP ARROW",fill="red",font=('fixedsys',10),tag="instructions2",anchor="w") #Places instructions 2 again.
    mainScreen.create_text(4,490,text="Move Down: DOWN ARROW",fill="red",font=('fixedsys',10),tag="instructions3",anchor="w") #Places instructions 3 again.
    scoreFile.close() #Closes high scores file.

'''The loseScreen function creates the highscore name entry box, and allows the user to interact with the game after losing, before being sent to the function which writes it to file.
For an added bonus, you are not allowed to enter a high score name longer than 8 characters, so it does not glitch up the high scores menu.'''
def loseScreen():
    global nameInput
    mainScreen.create_text(250,220,text="Enter Name:",fill="red",font=('fixedsys',20),tag="loseTitle1") #Enter name prompt text.
    mainScreen.create_text(250,280,text="(Press Enter To Confirm)",fill="red",font=('fixedsys',10),tag="loseTitle2") #Instruction on how to finalize entry.
    nameInput = Entry(root,font=('fixedsys',20),fg="red",width=12) #Actual entry box for high score name.
    nameInput.grid(row=0) #Places the entry box on row 0.
    def getName(event): #Nested function for name entry.
        global highName
        highName = nameInput.get() #Gets the data from the entry box.
        if len(highName) > 8: #If the data from the entry box is greater than 8 characters.
            nameInput.destroy() #Destroy The box.
            mainScreen.delete("loseTitle1") #Destroy the first lose title.
            mainScreen.delete("loseTitle2") #Destroy second lose title.
            loseScreen() #Recalls the loseScreen function.
        else: #If its less than 8 characters.
            setHighScore() #Call the setHighScore function.
    root.bind('<Return>',getName) #Bind the enter key to the getName nested function.

'''The very early named obstacles function is the main bulk of the game. It sets all the important variables and lists the program needs to keep track of in order to function properly.
The function creates randomly placed meteors, and moves them towards the spaceship. It keeps track of all the meteors on screen by giving each one its own custom tag, and number.
Each meteor tag is added to a list, which helps figure out which meteors need to be moved, removed, and kept track of in case of collision.'''
def obstacles():
    global shipMove
    global scoreText
    global meteorScore
    shipMove = 0 #Set shipMove variable to 0.
    meteorWait = 0 #Set meteorWait variable to 0.
    meteorDifWait = 0 #Set meteorDifWait variable to 0.
    meteorSpeed = -0.3 #Set meteorSpeed variable to -0.3.
    meteorFreq = 50000 #Set meteorFreq variable to 50000
    buttonFrame.grid_forget() #Temporarily remove the frame with the start menu buttons.
    mainScreen.delete("instructions1") #Remove instruction part 1.
    mainScreen.delete("instructions2") #Remove instruction part 2.
    mainScreen.delete("instructions3") #Remove instruction part 3.
    shipPos(250) #Call the shipPos function to draw the ship at a y coordinate of 250.
    root.bind_all('<Up>',shipUp) #Bind the up arrow key to the shipUp function.
    root.bind_all('<Down>',shipDown) #Bind the down arrow key to the shipDown function.
    meteorList= [] #Creates a list called meteorList.
    meteorNum = 0 #Set meteorNum variable to 0.
    meteorScore = 0 #Set meteorScore variable to 0.
    try:
        mainScreen.delete(scoreText) #Try deleting score text if possible.
    except:
        pass #Otherwise, nothing happens.
    scoreText = mainScreen.create_text(380,100,text="Score:"+str(meteorScore),fill="red",font=('fixedsys',20)) #Creates the score tracker text.
    endGame = False #Sets endGame boolean variable to false.
    while True:
        if endGame == True: #If the game has ended, by the endGame variable being true.
            mainScreen.delete('spaceship') #Delete spaceship.
            for i in meteorList: #For every element in the meteorList list.
                mainScreen.delete(i) #Delete the element.
            loseScreen() #Call loseScreen function.
            break #Break infinite loop.
        meteorWait += 100 #Add 100 to meteorWait
        meteorDifWait += 100 #Add 100 to meteorDifWait
        if meteorDifWait == 500000: #If meteorDifWait hits 50000.
            meteorSpeed += meteorSpeed*0.2 #Incrementally increase the meteor speed.
            meteorFreq -= meteorFreq*0.2 #Incrementally increase the meteor frequency.
            meteorDifWait = 0 #Reset meteorDifWait counter to 0.
        meteorPos = random.randint(100,500) #Give a random integer value to meteorPos between 100 and 500.
        if meteorWait >= meteorFreq: #If the meteorWait variable has surpassed the current meteorFreq value which increases over time.
            meteorNum += 1 #Add 1 to meteorNum variable.
            meteorVar = mainScreen.create_image(550,meteorPos,image=meteor,tag="meteorObs" + str(meteorNum) ) #Create a new meteor at a random position decided by the meteorPos variable.
            meteorList.append("meteorObs" + str(meteorNum)) #Appends the newest created meteor's tag to the meteorList.
            meteorWait = 0 #Resets meteorWait to 0.
        time.sleep(0.001) #Hold the program for 0.001 seconds.
        mainScreen.update() #Update the mainScreen canvas.
        for i in meteorList: #For every element in the meteorList.
            mainScreen.move(i,meteorSpeed,0) #Move the currently selected meteor a value of meteorSpeed left.
            meteorCoords = mainScreen.coords(i) #Passes the current meteor's coordinate to the meteorCoords variable.
            try:
                if mainScreen.find_overlapping(shipCoords[0]-7,shipCoords[1]+7,shipCoords[0]+5,shipCoords[1]-7)[1] > 1: #Tries to see if there are overlapping sprites within a 'hitbox' of the spaceship's coordinates.
                    endGame = True #If there is, set endGame to true.
            except:
                pass #Otherwise, nothing happens.
            try:
                if int(meteorCoords[0]) < -45: #Try checking if the meteor's position is past the screen.
                    meteorScore +=1 #If it is, add 1 to score.
                    try:
                        mainScreen.delete(scoreText) #Try to delete previous score.
                    except:
                        pass #If it cant, do nothing.
                    scoreText = mainScreen.create_text(380,100,text="Score:"+str(meteorScore),fill="red",font=('fixedsys',20)) #Adds the score text again with the updated score value.
                    mainScreen.delete(i) #Delete the current meteor thats outside the screen.
                    meteorList.remove(i)  #Remove the meteor's position in the list.
            except IndexError:
                pass #If it can't, do nothing.


'''Creates a highscore menu'''
def scoreMenu():
    global scores
    try:
        scores.destroy() #Trys to destroy a high score window.
    except :
        pass #If no window can be destroyed the program does not crash.
    scoreFile=open("highScores.txt","r") #Opens the highsore file.
    scores=Tk() #Creates the window.
    scores.wm_title("High Scores") #Assigns the title to the window.
    scoreScreen = Canvas (scores,width=300, height=300,bg="black") #Creates the canvas.
    scoreScreenTitle=scoreScreen.create_text(150,25,text="High Scores",fill="red",font=('fixedsys',25)) #Makes the highscore title.
    scoresList=[] #Creates a list for the scores from the file.
    while True:
        scoreDictionary={} #Creates a dictionary to later be added to the list.
        scoreDictionary["name"]=str.strip(scoreFile.readline()) #Takes the player name from the scorefile.
        if scoreDictionary["name"]=="":
            break #Breaks the loop if no more names are found.
        scoreDictionary["points"]=int(str.strip(scoreFile.readline())) #Takes the amount of points from the scorefile.
        scoresList.append(scoreDictionary) #Adds the dictionary to the list.
    sortedList=sorted(scoresList,key=itemgetter("points"),reverse=True) #Sorts the list of dictionary and makes it a new list.
    counter= 0 #Creates a counter variable.
    for index in sortedList:
        scoreNames=scoreScreen.create_text(10,45*counter+90,anchor="w",text=index["name"],fill="red",font=('fixedsys',25)) #Puts the names on the canvas.
        counter+= 1 #Adds one to counter.
        if counter==5:
            break #Breaks when counter gets up to 5 to prevent putting more than 5 names on the canvas.
    counter=0 #Assigns counter to 0.
    for index in sortedList:
        scoreAmount=scoreScreen.create_text(220,45*counter+90,anchor="w",text=index["points"],fill="red",font=('fixedsys',25))#Puts the points on the canvas
        counter+= 1
        if counter==5:
            break #Breaks when counter gets up to 5 to prevent putting more than 5 names on the canvas.
    scoreScreen.pack() #Packs the canvas.
    scoreFile.close() #Closes the high score file.


'''The beginning of the program. Sets up the main Tkinter canvas, text, and buttom frames. Also contains the very important Tkinter mainloop, which without nothing is possible.'''
root = Tk() #Creates main window.
root.wm_title("Space Game") #Sets the window title to 'Space Game'.

mainScreen = Canvas (width=500, height=500,bg="black") #Creates a canvas called 'mainScreen'.
topText = mainScreen.create_text(250,50,text="Space Game",fill="red",font=('fixedsys',50)) #Creates text as a title for the canvas.
mainScreen.create_text(4,460,text="Instructions:",fill="red",font=('fixedsys',10),tag="instructions1",anchor="w") #Instructions title.
mainScreen.create_text(4,475,text="Move Up: UP ARROW",fill="red",font=('fixedsys',10),tag="instructions2",anchor="w") #Up arrow instruction.
mainScreen.create_text(4,490,text="Move Down: DOWN ARROW",fill="red",font=('fixedsys',10),tag="instructions3",anchor="w") #Down arrow instruction.

spaceShip = PhotoImage(file="spaceship.gif") #Imports spaceship sprite.
meteor = PhotoImage(file="meteor.gif") #Imports meteor sprite.
mainScreen.grid() #Places mainScreen canvas on window using the grid geometry handler.


buttonFrame = Frame (root,height=300,width=300,bg="black") #Creates a frame called 'buttonFrame' for the mainscreen buttons.
buttonFrame.grid(row=0) #Places the frame in row 0 on the window.

startGame = Button(buttonFrame,text="Start",font=('fixedsys',20),command = lambda:obstacles(),activebackground="red") #Creates startGame button within the buttonFrame. When pressed it calls obstacles function.
startGame.grid() #Places button.

showScores = Button(buttonFrame,text="High Scores",font=('fixedsys',20),command = lambda:scoreMenu(),activebackground="red") #Creates showScores button within the buttonFrame. When pressed it calls the scoreMeu function.
showScores.grid(pady=30) #Places button with a 30 pixel padding on the y axis.



root.mainloop() #Makes all the Tkinter objects visible.



