from flask import Flask, render_template, request, url_for, flash, redirect, session
import random, time
from threading import Thread

app = Flask(__name__)

## College work

@app.route('/')
def home():
    return render_template("homepage.html", the_title="WELCOME TO THE WORD GAME",
                           game_url=url_for("game"), score_url=url_for("highscoretable"))

@app.route('/game')
def game():
    
    # Get source word
    source = ""
    words = [ line.strip() for line in open('/etc/dictionaries-common/words') ]
    source = random.choice(words)

    # If source contains an "'" or has less than 7 letters
    a = "'"
    while (len(source) < 7) or (a in source):
        source = random.choice(words)

    # Make lower case
    source = source.lower()
    
    # Get timestamp
    ts = time.time()
    
    return render_template("game.html", the_title="WORD GAME",
                           the_source = source,submit_url=url_for('checkwords'),
                           the_time = ts)
    
        
@app.route('/checkwords', methods =["POST"])
def checkwords():

    canContinue = True
    wordsEntered = True

    # Check that you entered seven words
    if request.form["word1"] == '' or request.form["word2"] == '' or request.form["word3"] == '' or request.form["word4"] == '' or request.form["word5"] == '' or request.form["word6"] == '' or request.form["word7"] == '':
        flash("You must enter seven words!!! Start again!")
        wordsEntered = False
        canContinue = False
    
    # Record timestamp at end
    ts2 = time.time()

    # Gets dictionary
    words = [line.strip() for line in open('/etc/dictionaries-common/words')]

    source = request.form["source"]
    ts1 = request.form["time1"]
    ts1 = float(ts1)

    # Calculate time taken
    timeTaken = ts2-ts1

    # Get words
    word1 = request.form["word1"]
    word2 = request.form["word2"]
    word3 = request.form["word3"]
    word4 = request.form["word4"]
    word5 = request.form["word5"]
    word6 = request.form["word6"]
    word7 = request.form["word7"]

    # Make lower case so case isn't an issue
    word1 = word1.lower()
    word2 = word2.lower()
    word3 = word3.lower()
    word4 = word4.lower()
    word5 = word5.lower()
    word6 = word6.lower()
    word7 = word7.lower()

    # Put words in list
    wordList = [word1.strip(), word2.strip(), word3.strip(),
                word4.strip(), word5.strip(), word6.strip(), word7.strip()] 

    #####################################################################
    # CONDITIONS

    if wordsEntered == True:
        # 1)
        # 1a) Check each word is made up from letters contained in the source word
        for word in wordList:
            for c in word:
                if c not in source:
                    flash("'" + word + "'" + " contains letters not in the source word")
                    canContinue = False

        # 1b) Check that the number of each letter in the source word hasn't been exceeded
        for word in wordList:
            for c in source:
                for c2 in word:
                    if c == c2:
                        if source.count(c) < word.count(c2):
                            flash("'" + word + "'" + " has too many letters of type " + "'" + c2 + "'")
                            canContinue = False
                            break

        # 2) Each word exits within the dictionary
        for word in wordList:
            if word not in words:
                flash("'" + word + "'" + " not in dictionary")
                canContinue = False

        # 3) Checks for more than three letters
        for word in wordList:
            if len(word) <= 2:
                flash("'" + word + "'" + " has too few letters")
                canContinue = False

        # 4) Check for duplicates
        w = wordList
        w2 = set(w)# This will remove any duplicate strings for w2
        if len(w) != len(w2):
            flash("No duplicates allowed!")
            canContinue = False

        # 5) If any of the words = the source word
        for word in wordList:
            if(word == source):
                flash("'" + word + "'" + " is the same as the source word")
                canContinue = False

        if canContinue == False:
            flash("INVALID WORDS ENTERED, START AGAIN!!")

            
    # END CONDITIONS
    #####################################################################

    if canContinue == True:
        return render_template("name.html", the_title="FINISHED!!", the_time=timeTaken,
                               submit_url2=url_for('result'))
    else:
        return redirect(url_for("game"))


@app.route('/result', methods=["POST"])
def result():
    newDict = {}
    nameEntered = True

    # Get name and time
    name = request.form["user_name"]
    time = request.form["time2"]

    # If no name entered
    if name == "":
        nameEntered = False

    if nameEntered == True:
        t = Thread(target=update_score, args=(name, time))
        t.start()
            
        return render_template("result.html", the_title="CHEERS!!", the_name=name,score_url=url_for("highscoretable"))
    else:
        return redirect(url_for("game"))


@app.route('/highscoretable')
def highscoretable():

    # We load the high score table here
        newDict = {}
        with open('score.log', 'r') as f:
            for line in f:
                splitLine = line.split()
                newDict[splitLine[0]] = ",".join(splitLine[1:])

        sorted_dict = sorted(newDict.items(), key=lambda x: float(x[1])) # List of dictionaries

        while(len(sorted_dict) > 10):
            sorted_dict.pop()

        lines = sorted_dict[::-1]

        return render_template("highscore.html", the_title="HIGH SCORE TABLE", data=lines,
                               home_url=url_for("home"))


def update_score(name, score):
	with open("score.log", "a") as log:
		print(name, score, file=log)

app.config["SECRET_KEY"] = 'secretkey'
app.run(debug=True)









