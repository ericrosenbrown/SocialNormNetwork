import numpy as np
from operator import itemgetter
import copy
import random

context_features = ["ownCard","haveCard","colleagueAvailable","at_kitchen","AnnInOffice","havePod","at_office","haveCoffee","at_shop","haveMoney"]


#This is an example of a starting context
context = {
context_features[0] : True,
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
def specific_action_value_features(c,l,place): #given a context and locations, produce
    action_value_features = {}
    actions = ["getKitchenCoffee","getOfficeCoffee","getShopCoffee"]
    if place=="at_kitchen": #We're in the kitchen
        action_value_features = {
            "getKitchenCoffee" : ["bad","none",0],
            "getOfficeCoffee" : ["good","none",np.linalg.norm(locations["office"]-locations["kitchen"])],
            "getShopCoffee" : ["veryGood","high",np.linalg.norm(locations["shop"]-locations["kitchen"])],
        }
    elif place=="at_office": #We're in the office
        action_value_features = {
            "getKitchenCoffee" : ["bad","none",np.linalg.norm(locations["kitchen"]-locations["office"])],
            "getOfficeCoffee" : ["good","none",0],
            "getShopCoffee" : ["veryGood","high",np.linalg.norm(locations["shop"]-locations["office"])],
        }
        pass
    elif place=="at_shop": #We're in the shop
        action_value_features = {
            "getKitchenCoffee" : ["bad","none",np.linalg.norm(locations["kitchen"]-locations["shop"])],
            "getOfficeCoffee" : ["good","none",np.linalg.norm(locations["office"]-locations["shop"])],
            "getShopCoffee" : ["veryGood","high",0],
        }
    else:
        return "SOMETHING IS MESSED UP!"
    return action_value_features

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
    real_avf = generate_action_value_features(c,l)


    best_pv_action = ""
    counter = 0
    print("PRINTING PV")
    print(pv)
    for pv_el in pv: #for each value tuple
        print(pv_el)
        if real_avf["getKitchenCoffee"] == pv_el:
            best_pv_action = "getKitchenCoffee"
            print(counter)
            break
        elif  real_avf["getOfficeCoffee"] == pv_el:
            best_pv_action = "getOfficeCoffee"
            print(counter)
            break
        elif real_avf["getShopCoffee"] == pv_el:
            best_pv_action = "getShopCoffee"
            print(counter)
            break
        counter += 1
    print(best_pv_action)
        

    av = generate_action_value_features(c,l)
    if c["at_kitchen"]:
        print("Currently in the kitchen")
        cur_place = "kitchen"
    if c["at_office"]:
        print("Currently in the office")
        cur_place = "office"
    if c["at_shop"]:
        print("Currently in the shop")
        cur_place = "shop"

    if best_pv_action in actions:
        if best_pv_action == actions[0]:
            if c["ownCard"]:
                print("Get a staff card I own to access the coffee.")
            elif c["colleagueAvailable"]:
                print("Get colleague to given me a coffee card to access coffe") 
            else :
                return
            
            print("Go to the Kitchen that is this far away from the "+str(cur_place+str(av["getKitchenCoffee"][2])))

            print("Get the coffee in the kitchen with the accessed card")
            return
       
        elif best_pv_action == actions[1]:
            if c["AnnInOffice"]:
                print("Go to the Office that is this far away from the current spot:"+str(cur_place)+" " +str(av["getOfficeCoffee"][2]))
                print("Get a Pod in office")
                print("Get coffe in the office")
            else:
                return
            return
        elif best_pv_action == actions[2]:
            print("Go to the Shop that is this far away from the current spot:"+str(cur_place)+" "+str(av["getShopCoffee"][2]))
            print("Get Cofffe at the shop")
            print("Pay shop the money")
            return
            


def learn_social_norms(c,l): #Learn the best ordering of values for a given context and a specific set of actions.
    #get randomly initialized ordering of actions
    real_action_values = generate_action_value_features(c,l)

    set_of_context_features = []
    set_of_context_features.append(specific_action_value_features(c,l,"at_kitchen").values())
    set_of_context_features.append(specific_action_value_features(c,l,"at_office").values())
    set_of_context_features.append(specific_action_value_features(c,l,"at_shop").values())
    flat_cf = [item for sublist in set_of_context_features for item in sublist]
    print(flat_cf)
    #print(set_of_context_features)

    for f in flat_cf:
        print(f)

    training_loops = 5
    num_pv = 10
    num_top = 5
    num_new = num_pv-num_top


    pvo = [] #potential value orderings
    for i in range(num_pv):
        random.shuffle(flat_cf)
        x = copy.copy(flat_cf)
        pvo.append(x)

    for i in range(training_loops):
        community_feedback = []
        print("training loop: "+str(i))
        counter = 0
        for pv in pvo:
            print("CONTEXT 1: IN OFFICE")
            c["at_shop"] = False
            c["at_office"] = True
            print_rollout(pv,c,l)

            print("CONTEXT 2: IN KITCHEN")
            c["at_office"] = False
            c["at_kitchen"] = True
            print_rollout(pv,c,l)

            print("CONTEXT 3: IN SHOP")
            c["at_kitchen"] = False
            c["at_shop"] = True
            print_rollout(pv,c,l)
            feedback = raw_input("How much did you like this behavior?")
            community_feedback.append((float(feedback),counter))
            counter += 1

        print(community_feedback)

        #change the pvo list to be better based on community feedback
        sorted_cf = sorted(community_feedback, key=itemgetter(0))
        sorted_cf.reverse()
        print(sorted_cf)

        new_pvo = []
        for top in range(num_top):
            new_pvo.append(pvo[sorted_cf[top][1]]) 

        for i in range(num_new):
            random.shuffle(flat_cf)
            x = copy.copy(flat_cf)
            new_pvo.append(x)
        pvo=new_pvo
        
        

    #print(c)
    #print(l)

learn_social_norms(context,locations)

