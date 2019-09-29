import numpy as np
import copy
import random

context_features = ["ownCard","haveCard","colleagueAvailable","at_kitchen","AnnInOffice","havePod","at_office","haveCoffee","at_shop","haveMoney"]


#This is an example of a starting context
context = {
context_features[0] : False,
context_features[1] : False,
context_features[2] : True,
context_features[3] : False,
context_features[4] : True,
context_features[5] : False,
context_features[6] : True,
context_features[7] : False,
context_features[8] : False,
context_features[9] : True
}

locations = {
"kitchen" : np.array([0,0]),
"office" : np.array([1,0]),
"shop" : np.array([0,10])
}

def generate_action_value_features(c,l): #given a context and locations, produce
    action_value_features = {}
    actions = ["getKitchenCoffee","getOfficeCoffee","getShopCoffee"]
    if c["at_kitchen"]: #We're in the kitchen
        action_value_features = {
            "getKitchenCoffee" : ["bad","none",0],
            "getOfficeCoffee" : ["good","none",np.linalg.norm(locations["office"]-locations["kitchen"])],
            "getShopCoffee" : ["veryGood","high",np.linalg.norm(locations["shop"]-locations["kitchen"])],
        }
    elif c["at_office"]: #We're in the office
        action_value_features = {
            "getKitchenCoffee" : ["bad","none",np.linalg.norm(locations["kitchen"]-locations["office"])],
            "getOfficeCoffee" : ["good","none",0],
            "getShopCoffee" : ["veryGood","high",np.linalg.norm(locations["shop"]-locations["office"])],
        }
        pass
    elif c["at_shop"]: #We're in the shop
        action_value_features = {
            "getKitchenCoffee" : ["bad","none",np.linalg.norm(locations["kitchen"]-locations["shop"])],
            "getOfficeCoffee" : ["good","none",np.linalg.norm(locations["office"]-locations["shop"])],
            "getShopCoffee" : ["veryGood","high",0],
        }
    else:
        return "SOMETHING IS MESSED UP!"
    return action_value_features

#print(context)
#print(generate_action_value_features(context,locations)) 


def print_rollout(pv,c,l):
    actions = ["getKitchenCoffee","getOfficeCoffee","getShopCoffee"]
    if c["at_kitchen"]:
        print("Currently in the kitchen")
        cur_place = "kitchen"
    if c["at_office"]:
        print("Currently in the office")
        cur_place = "office"
    if c["at_shop"]:
        print("Currently in the shopn")
        cur_place = "shop"

    for action in pv:
        if action == actions[0]:
            print("K")
            if c["ownCard"]:
                print("Get a staff card I own to access the coffee.")
            elif c["colleagueAvailable"]:
                print("Get colleague to given me a coffee card to access coffe") 
            else :
                continue
            
            cur_dist = np.linalg.norm(l[cur_place]-l["kitchen"]),
            print("Go to the Kitchen that is this far away from the "+str(cur_place+str(cur_dist)))

            print("Get the coffee in the kitchen with the accessed card")
            return
       
        elif action == actions[1]:
            print("O")
            cur_dist = np.linalg.norm(l[cur_place]-l["office"])
            if c["AnnInOffice"]:
                print("Go to the Office that is this far away from the current spot:"+str(cur_place)+" " +str(cur_dist))
                print("Get a Pod in office")
                print("Get coffe in the office")
            else:
                continue
            return
        elif action == actions[2]:
            print("S")
            cur_dist = np.linalg.norm(l[cur_place]-l["shop"])
            print("Go to the Shop that is this far away from the current spot:"+str(cur_place)+" "+str(cur_dist))
            print("Get Cofffe at the shop")
            print("Pay shop the money")
            return
            


def learn_social_norms(c,l): #Learn the best ordering of values for a given context and a specific set of actions.
    #get randomly initialized ordering of actions
    action_values = generate_action_value_features(c,l)
    ordering = action_values.keys()

    training_loops = 1


    pvo = [] #potential value orderings
    for i in range(3):
        random.shuffle(ordering)
        x = copy.copy(ordering)
        pvo.append(x)
    #print(pvo)

    for i in range(training_loops):
        print("training loop: "+str(i))
        print(pvo)
        for pv in pvo:
            print_rollout(pv,c,l)

    #print(c)
    #print(l)

learn_social_norms(context,locations)

