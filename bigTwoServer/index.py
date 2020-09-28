import json
from flask import Flask, request, render_template, jsonify
from datetime import timedelta
import random
import time
import threading
from threading import Timer
cardOld = [0,0,0,0,0,0,0,0] #one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight   
userCard = {}
userWin = 0
userPass = [0,0,0,0]
userCount = []
userTemp = 0
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
@app.route("/", methods=['GET', 'POST'])

def index():
    global userCard
    global userWin
    global userPass
    global userCount
    global userTemp
    global cardOld
    if request.method == "POST":
        event = request.form["event"]
        name = request.form["name"]
        if(len(userCard) < 4):
            if (name in userCard):
                return "register success"
            else:
                userCard[name] = []
                userCount.append(name)
                if(len(userCard) == 4):#發牌
                    temp = deal()
                    print(temp)
                    count = 0
                    for i in userCard:
                        userCard[i] = temp[count*13:count*13+13]
                        count+=1
                    return "all player ready"

                return "wait another user"
        print("event="+event)
        if(event == "update"):
            temp = {}
            temp['userCard'] = userCard[name]
            temp['cardOld'] = cardOld
            temp['userTurn'] = userCount[userTemp]
            #print("userCard=",userCard)
            return (json.dumps(temp))
        if(event == "sendCard"):
            if(userCount[userTemp] == name):
                card = request.form["card"]
                card = json.loads(card)
                count1 = 0
                for i in card:
                    count1 = 0
                    for j in range(0,len(userCard[name])):
                        if(userCard[name][j] == i):
                            count1 = 1
                            break
                    if(count1 == 0):
                        return "loss or error card"

                print("name=",name)
                print("card=",card)
                #比較大小
                if(len(card) == 0):
                    userPass[userTemp] = 1
                    nextPlayer()
                    return "pass"
                if(function(card,len(card),cardOld) == 1):
                    userWin = userTemp
                    for i in card:
                        for j in userCard[name]:
                            if(j == i):
                                userCard[name].remove(j)
                                break
                    if(len(userCard[name]) == 0):
                        userCount.remove(name)
                    nextPlayer()
                    return "success"
                else:
                    return "error"
            else:
                return "not your turn"

    return render_template("index.html")
def nextPlayer():
    global userTemp
    global cardOld
    global userPass
    global userWin
    userTemp+=1
    userTemp%=4
    count1 = 0
    temp = 0
    for i in userPass:
        if i == 1:
            count1+=1
        else:
            temp = count1
    if(count1 >= 3):
        userTemp = temp
        cardOld = [0,0,0,0,0,0,0,0]
        userPass = [0,0,0,0]
    return

def deal():
    card = list(range(0,52))
    print(card)
    for i in range(10000):
        a = random.randint(0,51)
        b = random.randint(0,51)
        temp = card[a]
        card[a] = card[b]
        card[b] = temp
    return card
def endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld):
    cardOld[0] = one_max_color
    cardOld[1] = one_max_card
    cardOld[2] = two_max_color
    cardOld[3] = two_max_card 
    cardOld[4] = flush_straight_card        #同花順   
    cardOld[5] = Four_of_a_Kind          #鐵支    
    cardOld[6] = Full_house              #葫蘆  
    cardOld[7] = straight                #順子 
def function(card,num,cardOld):
    one_max_color = cardOld[0]
    one_max_card =cardOld[1]
    two_max_color =cardOld[2]
    two_max_card =cardOld[3]  
    flush_straight_card=cardOld[4]          #同花順   
    Four_of_a_Kind=cardOld[5]           #鐵支    
    Full_house = cardOld[6]             #葫蘆  
    straight =cardOld[7]                #順子  
    card = card
    num = num
    card2 = [0 for x in range(5)]
    for i in range(0,num):
        card2[i]= (card[i])%13

    card = sorted(card)
    card2= sorted(card2)
    print(card2)
           
    if num == 5:            #可能為同花順,鐵支,葫蘆,順子
        if (((card2[0]+card2[4])//2)==card2[2] and ((card2[1]+card2[3])//2)==card2[2]):
            if(((card[0]+card[4])//2)==card[2] and ((card[1]+card[3])//2)==card[2]):                #同花順
                if(card2[0]>flush_straight_card):
                    flush_straight_card = card[0]%13
                    one_max_color = 0
                    one_max_card = 0
                    two_max_color = 0
                    two_max_card = 0
                    Four_of_a_Kind = 0
                    Full_house = 0
                    straight = 0
                    print('桐花順')
                    endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld)
                    return 1 
                elif(card2[0]==flush_straight_card):
                    if (card[0]//13>flush_straight_card//13):
                        flush_straight_card = card[0]%13
                        one_max_color = 0
                        one_max_card = 0
                        two_max_color = 0
                        two_max_card = 0
                        Four_of_a_Kind = 0
                        Full_house = 0
                        straight = 0
                        print('桐花順')
                        endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld)
                        return 1
                    else:
                        print('錯誤')
                        return 0
                else:
                    print('此同花不夠大')
                    return 0
            else:
                if(flush_straight_card==0 or Four_of_a_Kind==0 or two_max_card==0 or one_max_card==0 or Full_house==0):
                    if(card2[0]+1>straight):
                        straight = card2[0]
                        endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld)
                        return 1 
                    else:
                        print('順子不夠大')
                        return 0 
                else:
                    print('錯誤的順子')
                    return 0
        elif (card2[0]==card2[1] and card2[1]==card2[2] and card2[2]==card2[3] ) or (card2[1]==card2[2] and card2[2]==card2[3] and card2[3]==card2[4]):   #鐵支
            if (flush_straight_card!=0):
                print('鐵支沒有桐花大下去')
                return 0
            else:
                if (card2[2]+1>Four_of_a_Kind) :
                    Four_of_a_Kind=card2[2]
                    one_max_color = 0
                    one_max_card = 0
                    two_max_color = 0
                    two_max_card = 0
                    flush_straight_card = 0
                    Full_house = 0
                    straight = 0
                    print('鐵支')
                    endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld)
                    return 1 
                else:
                    print('此鐵支不夠大')
                    return 0              
        elif ((card2[0]==card2[1] and card2[1]==card2[2] and card2[3]==card2[4]) or (card2[2]==card2[3] and card2[3]==card2[4] and card2[0]==card2[1])):
            if (flush_straight_card!=0 or Four_of_a_Kind!=0 or two_max_card!=0 or one_max_card!=0 or straight!=0):
                print('葫蘆不夠大')    #葫蘆
                return 0 
            else:
                if (card2[2]+1>Full_house) :
                    Full_house=card[2]
                    print('葫蘆')
                    endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld)
                    return 1
                else:
                    print('此葫蘆不夠大')
                    return 0 
        else:
            print('亂出')
            return 0 
    elif num == 2:       #對子
        if  ((flush_straight_card!=0) or Four_of_a_Kind!=0 or Full_house!=0 or straight!=0 or one_max_card!=0):
            print('對子不可出')
            return 0 
        else: 
            if (card2[0]!=card2[1]):
                print('出牌錯誤')
                return 0 
            elif (card2[0] < two_max_card):
                print('出牌錯誤')
                return 0 
            elif (card2[0]==two_max_card):
                if (card[0]//13+1  > two_max_color):
                    if (card[0]//13 > card[1]//13):
                        two_max_color = card[0]//13;
                        print('對子前面那張牌花色較大')
                        endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld)
                        return 1 
                    else:
                        two_max_color = card[1]//13;
                        print('對子前面那張牌花色較小')
                        endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld)
                        return 1 
                elif (card[1]//13+1 >two_max_color):
                    two_max_color = card[1]//13;
                    print('對子只有後面那張花色比原始大')
                    endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld)
                    return 1 
                else:
                    print('花色不夠大')
                    return 0 
            else:
                if (card[0]//13>card[1]//13):
                    two_max_color = card[0]//13;
                    two_max_card = card2[0];
                    print('對子前面花色大點數比原始大')
                    endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld)
                    return 1
                else:
                    two_max_color = card[1]//13;
                    two_max_card = card2[1];
                print('對子前面花色小點數比原始大')
                endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld)
                return 1
    elif num == 1:  
        print(card2[4])        #單張
        if  (flush_straight_card!=0 or Four_of_a_Kind!=0 or Full_house!=0 or straight!=0 or two_max_card!=0) :
            print('單張不可出')
            return 0
        else:
            if (card2[4]<one_max_card):
                print('不夠大')
                return 0
            elif (card2[4] == one_max_card):
                if (card[0]//13<one_max_color):
                    print('花色不夠大')
                    return 0
                else:
                    one_max_color =card[0]//13;
                    print('單張花色較大')
                    endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld)
                    return 1 
            else:
                one_max_color = card[0]//13;
                one_max_card = card2[4];
                print('單張')
                endFcuntion(one_max_color,one_max_card,two_max_color,two_max_card,flush_straight_card,Four_of_a_Kind,Full_house,straight, cardOld)
                return 1

    elif num == 0:           # pass
        print('pass')
        return 1
    else:
        print( 'bug' )    # 条件均不成立时输出
        return 0
if __name__ == "__main__":
    #app.run(
    #    host = '0.0.0.0',
    #    port = 7777,  
    #    debug = True 
    #)
    app.run()
