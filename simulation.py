#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 8 21:59:57 2020
Last updated on Dec 11 16:21:12 2020

@author: kaspertidner
"""
#Importerar bibliotek
import random
import matplotlib.pyplot as plt
import pandas as pd

#Definerar olika färger som variabler
GREY = (0.78, 0.78, 0.78)  # suspectible
RED = (0.96, 0.15, 0.15)   # indeceased
ORANGE = (1, 0.65, 0)
YELLOW = (1, 0.88, 0.21)
GREEN = (0, 0.86, 0.03)    # removed
BLACK = (0, 0, 0)          # dead

#Skapar en dictionary för våra punkter vi animerar
#Varje punkt defineras av formatet: point__: [x, y, state, first day, last day, using_mask, isolated, at_mall, age, severeness, day_suspectible_again]
punkter = {}


"""
*****************************************************************************************************************************
"""
#Ändra på dessa värden för att få olika simuleringar:
population = 5000 #Positivt heltalsvärde, anger populationens storlek, ju större desto längre tid tar simuleringen att beräkna
contact_distance = 0.4 #Positivt tal med en decimal, bör ligga mellan 0.1-0.8, anger radien för vad som räknas som en kontakt
box_size = 39 #Storlek på området simuleringen körs inom, positivt tal 
deceased = 10 #Antalet smittade från början, positivt heltal
contact_probability = 0.2 #Sannolikhet vid smitta, mellan 0 och 1
contact_probability_range = 0.05 #+/- på smittsannolikheten, mellan 0 och contact probability
days = 5 #Simmulera i X dagar efter att smittan är utraotad, positivt heltal
incubation_days = 5 #Dagar från att man får smittan tills man börjar smitta, positivt heltal
days_infected = 8 #Dagar man är sjuk vid homogenitet, positivt heltal
walk_size = 0.5 #Hur långt ett steg är, en decimal

#Sätt på och av olika parametrar
restrict_shopping_mall_org = False #En samlingspunkti mitten som simulerar en stor folksamling, True|False
use_masks_org = False #Om befolkningen rekomenderas använda munskydd, True|False
isolation_org = True #Om man smittspårar och sätter folk i karrantän om de blivit sjuka, True|False

turn_on_parameters = "infected" #När ska parametrarna sättas på, välj mellan "direct": allt sätts på direkt, "infected": sätts på efter x antal sjuka samtidigt, "deaths": sätts på när x människor dött, "days": sätts på efter x dagar
turn_on_parameter_value = 500 # Se ovan, nummret speglar efter hur många dagar/döda/sjuka, som parametern sätts på, beroende på valet över

identity = True #Tilldelar varje punkt en ålder och av där en grad av smittan, så att alla punkter uppträder olika, True|False
special_color = False #Ändrar form och kant färger efter olika identiteter, kan vara användbart vid analys, men annars ser det störande ut, True|False
re_suspectible = False #Gör så att modellen blir SIRS och inte SIR, man kan förlora immunitet och åter bli mottaglig, True|False

#Värden på parametrar
mask_proportion = 0.75 #Andel av befolkningen som använder munskydd, mellan 0 och 1
mask_probability = 0.1 #Risk att smitta om man bär munskydd, mellan 0 och 1
mask_probability_range = 0 #+/- på smittsannolikheten om man bär mask, mellan 0 och mask probability
isolation_after_days = 6 #Isolation börjar efter x dagar, bör vara större än incubation_days, positivt heltal
isolation_days = 8 #Hur många dagar man är isolerad, positivt heltal
isolation_proportion = 0.9 #Andel av befolkningen som issoleras, mellan 0 och 1
chanse_of_going_to_mall = 0.05 #Chansen att en individ väljer att åka till shoppingcentret, mellan 0 och 1
mall_size = 8.8 #Sidolängden för shoppingcentret, en decimal
days_immune = 30



#Ålders indelningar:
age_0_15 = 17.8 #Procent av befolkningen som är yngre än 15 år 
age_16_29 = age_0_15 + 18.4 #Procent av befolkningen som är yngre än 29 år 
age_30_45 = age_16_29 + 19.4 #Procent av befolkningen som är yngre än 45 år 
age_46_69 = age_30_45 + 29.8 #Procent av befolkningen som är yngre än 69 år 
#Resterande är 70+ 

#Allvarlighet per åldersgrupp:
#0_15 - Ska bli lika med 100
mild_0_15 = 86 #Procent som får milda symptom
mild_severe_0_15 = 13 #Procent som får svagt allvarliga symptom
critical_0_15 = 0.9 #Procent som får livshotande symptom
death_0_15 = 0.1 #Procent som dör

#16_29 - Ska bli lika med 100
mild_16_29 = 83 #Procent som får milda symptom
mild_severe_16_29 = 16.2 #Procent som får svagt allvarliga symptom
critical_16_29 = 0.7 #Procent som får livshotande symptom
death_16_29 = 0.1 #Procent som dör

#30_45 - Ska bli lika med 100
mild_30_45 = 78 #Procent som får milda symptom
mild_severe_30_45 = 20.1 #Procent som får svagt allvarliga symptom
critical_30_45 = 1.8 #Procent som får livshotande symptom
death_30_45 = 0.1 #Procent som dör

#46_69 - Ska bli lika med 100
mild_46_69 = 73 #Procent som får milda symptom
mild_severe_46_69 = 24.2 #Procent som får svagt allvarliga symptom
critical_46_69 = 2.6 #Procent som får livshotande symptom
death_46_69 = 0.2 #Procent som dör

#70+ - Ska bli lika med 100
mild_70 = 54 #Procent som får milda symptom
mild_severe_70 = 17 #Procent som får svagt allvarliga symptom
critical_70 = 23 #Procent som får livshotande symptom
death_70 = 6 #Procent som dör

#Sjukindelningar:
mild_length = 4
severe_length = 8
critical_length = 14
death_length = 21
mild_range = 2
severe_range = 3
critical_range = 5 
death_range = 7
"""
*****************************************************************************************************************************
"""
#Sätter första dagen = 0
day = 0

#Skapar fyra listor som uppdateras med information om smittspridningen
suspectible = [population - deceased]
indeceased = [deceased]
removed = [0]
deaths = [0]

#Variabler som håller koll på statistik
max_ind = 0
new_mall = 0
inf_mall = 0
total_inf = []
day_para = 10000

#Tar fram en graf med utslumpade punkter att utgå simuleringen ifrån
def plot_start():
    
    for i in range(population):
        x = round((random.random() * box_size), 1)
        y = round((random.random() * box_size), 1)

        age = asign_age()
        severness = asign_severness(age)
        
        #skapar punkterna och erhåller dem information om hur de ska bete sig, var de är, med mera
        if i < deceased:
            punkter["point{0}".format(i)] = [x, y, "Indeceased", day, day+days_infected, False, False, False, age, severness, 0, False, 0, 0]
        else:
            punkter["point{0}".format(i)] = [x, y, "Suspectible", 0, 0, False, False, False, age, severness, 0, False, 0, 0]

#En funktion som slumpar fram en punkts ålder
def asign_age():
    rand_age = random.random()*100
    if rand_age <= age_0_15:
        age = "0_15"
    elif rand_age <= age_16_29:
        age = "16_29"
    elif rand_age <= age_30_45:
        age = "30_45"
    elif rand_age <= age_46_69:
        age = "46_69"
    else:
        age = "70+"
    return age

#En funktion som tar in en punkts ålder utifrån det slumpar fram hur allvarligt sjuk den kommer bli om den blir smittad
def asign_severness(age):
    rand_severness = random.random()*100
    if age == "0_15":
        if rand_severness <= mild_0_15:
            severness = "mild"
        elif rand_severness <= mild_0_15 + mild_severe_0_15:
            severness = "severe"
        elif rand_severness <= mild_0_15 + mild_severe_0_15 + critical_0_15:
            severness = "critical"
        else:
            severness = "death"
    elif age == "16_29":
        if rand_severness <= mild_16_29:
            severness = "mild"
        elif rand_severness <= mild_16_29 + mild_severe_16_29:
            severness = "severe"
        elif rand_severness <= mild_16_29 + mild_severe_16_29 + critical_16_29:
            severness = "critical"
        else:
            severness = "death"
    elif age == "30_45":
        if rand_severness <= mild_30_45:
            severness = "mild"
        elif rand_severness <= mild_30_45 + mild_severe_30_45:
            severness = "severe"
        elif rand_severness <= mild_30_45 + mild_severe_30_45 + critical_30_45:
            severness = "critical"
        else:
            severness = "death"
    elif age == "46_69":
        if rand_severness <= mild_46_69:
            severness = "mild"
        elif rand_severness <= mild_46_69 + mild_severe_46_69:
            severness = "severe"
        elif rand_severness <= mild_46_69 + mild_severe_46_69 + critical_46_69:
            severness = "critical"
        else:
            severness = "death"
    elif age == "70+":
        if rand_severness <= mild_70:
            severness = "mild"
        elif rand_severness <= mild_70 + mild_severe_70:
            severness = "severe"
        elif rand_severness <= mild_70 + mild_severe_70 + critical_70:
            severness = "critical"
        else:
            severness = "death"
    return severness
        
#En funktion som loopar igenom alla sjuka och ser om de smittar andra eller om de tillfrisknar        
def update_state():
    
    #Loopar igenom alla punkter och hämtar hem information om dem
    for i, v in enumerate(punkter):
        x1 = (punkter[v])[0]
        y1 = (punkter[v])[1]
        state1 = (punkter[v])[2]
        mask = (punkter[v])[5]
        age1 = (punkter[v])[8]
        severness1 = (punkter[v])[9]
        
        #Kollar om punkten är smittad, samt om den smittar
        if (state1 == "Indeceased"  and (severness1 == "mild" or severness1 == "severe") and (punkter[v])[3] <= day and day <= (punkter[v])[4]) or (state1 == "Indeceased" and (severness1 == "death" or severness1 == "critical") and (punkter[v])[3] <= day and day <= ((punkter[v])[3] + 10)):
            
            #Om punkten var sjuk så loopas alla punkter igenom en gång till
            for j, w in enumerate(punkter):
                x2 = (punkter[w])[0]
                y2 = (punkter[w])[1]
                state2 = (punkter[w])[2]
                age2 = (punkter[w])[8]
                severness2 = (punkter[w])[9]
                
                #Avståndet mellan den smittsamma punkten samt den andra punkten räknas ut
                delta_x = abs(x2-x1)
                delta_y = abs(y2-y1)
                distance  = (delta_x**2 + delta_y**2)**0.5
                
                #Tittar igenom punkterna efter de som är inom smittradien, samt är mottagliga för smittan
                if distance <= contact_distance and state2 == "Suspectible":
                    
                    #Om en punkt är inom smittradien och är mottaglig slumpas det om den faktiskt blir infekterad
                    probability = calculate_contact_probability(mask)
                    if random.random() < probability:
                        if identity == True:
                            days_infecteds = period_of_sickness(age2, severness2)
                        else:
                            days_infecteds = days_infected
                            
                        #Deras egenskaper uppdateras nu eftersom de blivit smittade
                        (punkter[w])[2] = "Indeceased"
                        (punkter[w])[3] = day+incubation_days
                        (punkter[w])[4] = day+incubation_days+days_infecteds
                        if use_masks == True and random.random() < mask_proportion:
                            (punkter[w])[5] = True
        
        #Kollar om man står som sjuk, men dagen man ska tillfriskna har passerat
        elif state1 == "Indeceased" and day > (punkter[v])[4]:
            
            #Uppdaterar ens hälsotilstånd och skriver en som frisk
            (punkter[v])[2] = "Removed"
            (punkter[v])[10] = day + days_immune
        
        #Om immuniteten kan försvinna, så checkar den om man återigen är mottaglig och uppdaterar hälsotillståndet efter detefter det
        elif state1 == "Removed" and severness1 != "death" and re_suspectible == True and day > (punkter[v])[10]:
            (punkter[v])[2] = "Suspectible"
            (punkter[v])[9] = asign_severness(age1)

#Räknar ut smittsannolikheten vid kontakt
def calculate_contact_probability(mask):
    if mask == True:
        try:
            probability = random.randrange(int((mask_probability-mask_probability_range)*10000), int((mask_probability+mask_probability_range)*10000), 1)/10000
        except:
            probability = mask_probability
    else:
        probability = random.randrange(int((contact_probability-contact_probability_range)*10000), int((contact_probability+contact_probability_range)*10000), 1)/10000
    return probability

#Räknar ut hur länge en punkt är sjuk beroende på ålder och hur alvarsamma symptom man får
def period_of_sickness(age, severness):
    if severness == "death":
        length = random.randint(death_length-death_range, death_length+death_range)
    elif severness == "critical":
        length = random.randint(critical_length-critical_range, critical_length+critical_range)
    elif severness == "severe":
        length = random.randint(severe_length-severe_range, severe_length+severe_range)
    elif severness == "mild":
        length = random.randint(mild_length-mild_range, mild_length+mild_range)
    
    if age == "0_15":
        length -= 1
    elif age == "16_29":
        length -= 1
    elif age == "30_45":
        pass
    elif age == "46_69":
        length += 1
    elif age == "70+":
        length += 2
        
        
    return length

#Skapar en lokal samlingsplats och tar en del av befolkningen dit
def shopping_mall_travel():
    
    #Tittar om restriktioner folksamlingar är påslaget
    if restrict_shopping_mall == False:
        
        #Loopar igenom punkt för punkt
        for i, v in enumerate(punkter):
            isolated = (punkter[v])[6]
            at_mall = (punkter[v])[7]
            severness = (punkter[v])[9]
            
            #Kollar så att man inte sitter i karantän eller ligger på sjukhus, för då kan man inte åka till folksammlingen
            if isolated == False and at_mall == False and (severness == "mild" or severness == "severe"):
                
                #Slumpar om man åker till mall eller inte denna dagen
                if random.random() <= chanse_of_going_to_mall:
                    min_mall_box = int((box_size/2 - mall_size/2)*100)
                    max_mall_box = int((box_size/2 + mall_size/2)*100)
                    x = round(random.randint(min_mall_box, max_mall_box)/100, 2)
                    y = round(random.randint(min_mall_box, max_mall_box)/100, 2)
                    
                    #Uppdaterar punktens position och att den nu är i en folksamling
                    (punkter[v])[0] = x
                    (punkter[v])[1] = y
                    (punkter[v])[7] = True
                    
            #Är man redan i folksamlingen så slumpas det om man ska stanna
            elif at_mall == True:
                if random.random() <= chanse_of_going_to_mall:
                    pass
                
                #Om man lämnar folksamlingen så slumpas man ut till en plats i boxen
                else:
                    x = round((random.random() * box_size), 1)
                    y = round((random.random() * box_size), 1)
                    (punkter[v])[0] = x
                    (punkter[v])[1] = y
                    (punkter[v])[7] = False
    
    #Om folksamlingar förbjuds, samtidigt som man är i en, så får man lämna genom att slumpas ut till någonstas i boxen
    elif restrict_shopping_mall == True:
        for i, v in enumerate(punkter):
            if (punkter[v])[7] == True:
                x = round((random.random() * box_size), 1)
                y = round((random.random() * box_size), 1)
                (punkter[v])[0] = x
                (punkter[v])[1] = y
                (punkter[v])[7] = False

#Funktionen för statistik på hur många som åker till folksamlingar och hur många som smittas där    
def shopping_mall_count():
    
    global new_mall
    global inf_mall
    
    for i, v in enumerate(punkter):
            x = (punkter[v])[0]
            y = (punkter[v])[1]
            state = (punkter[v])[2]
            reel_mall = (punkter[v])[11]
            entry_mall = (punkter[v])[12]
            min_mall_box = round((box_size/2 - mall_size/2), 1)
            max_mall_box = round((box_size/2 + mall_size/2), 1)
            if reel_mall == False:
                if x <= max_mall_box and x >= min_mall_box and y <= max_mall_box and y >= min_mall_box:
                    (punkter[v])[12] = state
                    (punkter[v])[11] = True
            elif reel_mall == True:
                if x <= max_mall_box and x >= min_mall_box and y <= max_mall_box and y >= min_mall_box:
                   pass
                else:
                    (punkter[v])[13] = state
                    (punkter[v])[11] = False
            if reel_mall == True and (punkter[v])[11] == False:
                if entry_mall == "Suspectible":
                    new_mall += 1
                if entry_mall == "Suspectible" and (punkter[v])[13] == "Indeceased":
                    inf_mall += 1
                
    return new_mall, inf_mall
    
#Letar igenom befolkningen efter sjuka, och sätter dem i karrantän
def check_for_infected():
    
    #Körs endast om åtgärden att sätta folk i isolering är påslagen
    if isolation == True:
        for i, v in enumerate(punkter):
             state = (punkter[v])[2]
             start_day = ((punkter[v])[3])-incubation_days+isolation_after_days
             recover_day = (punkter[v])[4] + 1
             isolated = (punkter[v])[6]
             if state == "Indeceased" and day >= start_day and day <= recover_day and isolated == False:
                 
                 #Letar efter sjuka personer, och det finns en viss chans(isolated_proportion) chans att de hittas
                 if random.random() < isolation_proportion:
                     (punkter[v])[6] = True
                     (punkter[v])[0] = box_size + contact_distance + 0.1
                     (punkter[v])[1] = round((random.random() * box_size), 1)
                 else:
                     (punkter[v])[6] = "Failed"
             elif day > recover_day and isolated == True:
                 isolated == False
                 (punkter[v])[0] = round((random.random() * box_size), 1)
                 (punkter[v])[1] = round((random.random() * box_size), 1)

#Färglägger alla punkter efter deras state(SIR), körs endast om animationer är påslagna
def color_plot():
    plt.figure()
    ax = plt.axes(xlim=(0, box_size + contact_distance + 0.3), ylim=(0, box_size))
    
    for i, v in enumerate(punkter):
        x = (punkter[v])[0]
        y = (punkter[v])[1]
        state = (punkter[v])[2]
        severness = (punkter[v])[9]
        mask = (punkter[v])[5]
        if special_color == True:
            if state == "Suspectible":
                ax.scatter(x, y, color=GREY)
            elif state == "Indeceased" and mask == True:
                ax.scatter(x, y, color=RED, marker="p")
            elif state == "Indeceased" and severness == "mild":
                ax.scatter(x, y, color=RED, edgecolors=GREEN)
            elif state == "Indeceased" and severness == "severe":
                ax.scatter(x, y, color=RED, edgecolors=YELLOW)
            elif state == "Indeceased" and severness == "critical":
                ax.scatter(x, y, color=RED, edgecolors=ORANGE)
            elif state == "Indeceased" and severness == "death":
                ax.scatter(x, y, color=RED, edgecolors=BLACK)
            elif state == "Indeceased":
                ax.scatter(x, y, color=RED)
            elif state == "Removed" and severness == "death":
                ax.scatter(x, y, color=BLACK)
            elif state == "Removed":
                ax.scatter(x, y, color=GREEN)
        else:
            if state == "Suspectible":
                ax.scatter(x, y, color=GREY)
            elif state == "Indeceased":
                ax.scatter(x, y, color=RED)
            elif state == "Removed" and severness == "death":
                ax.scatter(x, y, color=BLACK)
            elif state == "Removed":
                ax.scatter(x, y, color=GREEN)
            
    plt.plot([box_size + 0.1, box_size + 0.1], [0, box_size], 'k-', lw=2)
    rubrik = "Dag: " + str(day) + " - (S: " + str(suspectible[-1]) + " / I: " + str(indeceased[-1]) + " / R: " + str(removed[-1]) + " / D: " + str(deaths[-1]) + ")"
    plt.title(rubrik, fontsize="10")
    plt.show()

#Gör så alla punkter tar ett steg(motsvarar en dag)
def take_a_step():
    global day
    for i, v in enumerate(punkter):
        x = (punkter[v])[0]
        y = (punkter[v])[1]
        isolated = (punkter[v])[6]
        at_mall = (punkter[v])[7]
        age = (punkter[v])[8]
        severness = (punkter[v])[9]
        walk_length = walk_size
        if isolated == True or at_mall == True or severness == "death" or severness=="critical":
            pass
        else:
            if severness == "death" or severness == "critical":
                 walk_length = 0
            elif age == "0_15":
                walk_length += 0.2
            elif age == "16_29":
                walk_length += 0.2
            elif age == "30_45":
                walk_length += 0.1
            elif age == "46_69":
                pass
            elif age == "70+":
                walk_length -= 0.1
            else:
                pass
            
            
            (dx, dy) = random.choice([(0, walk_length), (0, -(walk_length)), (walk_length, 0), (-(walk_length), 0)])
            x += dx
            y += dy
            if x > box_size:
                x = box_size-0.1
            elif x < 0:
                x = 0.1
            if y > box_size:
                y = box_size-0.1
            elif y < 0:
                y = 0.1
            x = round(x, 1)
            y = round(y, 1)
            (punkter[v])[0] = x
            (punkter[v])[1] = y
    day +=1
    
#Uppdaterar SIR listorna med aktuella värden på hur många som är sjuka, återhämtat sig, mottagliga
def update_sir():
    global max_ind
    sus = 0
    ind = 0
    rem = 0
    dea = 0
    for i, v in enumerate(punkter):
        state = (punkter[v])[2] 
        severness = (punkter[v])[9]
        if state == "Suspectible":
            sus +=1
        elif state == "Indeceased":
            ind += 1
        elif state == "Removed":
            rem += 1
        if state == "Removed" and severness == "death":
            dea +=1
        
    suspectible.append(sus)
    indeceased.append(ind)
    removed.append(rem)
    deaths.append(dea)
    if indeceased[-1] > max_ind:
        max_ind = indeceased[-1]

#Ritar en SIR graf över simulationen
def make_sir_graph(range_days):
    data = pd.DataFrame({  'suspectible_list':suspectible, 'infectious_list':indeceased, 'recovered_list':removed }, index=range(range_days))
    data_perc = data.divide(data.sum(axis=1), axis=0)
    plt.stackplot(range(range_days),  data_perc["infectious_list"],  data_perc["recovered_list"],  data_perc["suspectible_list"], labels=['i(t)','r(t)','s(t)'])
    plt.legend(loc='upper left')
    plt.margins(0,0)
    rubrik = "Dag: " + str(day) + " - (S: " + str(suspectible[-1]) + " / I: " + str(indeceased[-1]) + " / R: " + str(removed[-1]) + " / D: " + str(deaths[-1]) + ")"
    plt.title(rubrik, fontsize="10")
    plt.show()

def turn_on_restrictions():
    global restrict_shopping_mall
    global use_masks
    global isolation
    global day_para
    
    if turn_on_parameters == "direct" or turn_on_parameters == "days" and day >= turn_on_parameter_value or turn_on_parameters == "infected" and indeceased[-1] >= turn_on_parameter_value or turn_on_parameters == "deaths" and  deaths[-1] >= turn_on_parameter_value:
        restrict_shopping_mall = restrict_shopping_mall_org 
        use_masks = use_masks_org 
        isolation = isolation_org 
        if day < day_para:
            day_para = day
    else:
        restrict_shopping_mall = False
        use_masks = False
        isolation = False
    
    
#Kör funktionerna för att skapa animeringen
def main():
    turn_on_restrictions()
    plot_start()
    update_sir()
    n_days = 0
    #Simulera tills smittan är borta
    while indeceased[-1] > 0:
        n_days+=1
        update_state()
        check_for_infected()
        shopping_mall_travel()
        if restrict_shopping_mall == False:
            new_mall, inf_mall = shopping_mall_count()
        take_a_step()
        update_sir()
        turn_on_restrictions()
        print(day)

    #Simulera i ytterigare X dagar efter det
    for i in range (days):
        update_state()
        check_for_infected()
        shopping_mall_travel()
        take_a_step()
        update_sir()
        turn_on_restrictions()
        
    make_sir_graph(n_days + days + 2)
    print("Döda procent = " + str(round(deaths[-1]/removed[-1]*100, 1)) + "%, Total andel smittade: " + str(round(removed[-1]/population*100, 1)) + "%, max antalet sjuka samtidigt var: " + str(max_ind))
    if turn_on_parameters != "direct":
        print("Mall var öppet i: " + str(day_para)+ " dagar")
        print("Andelen av de mottagliga som blev smittade i mall var: " + str(round(inf_mall/new_mall*100, 1)) + "%, antalet besök i folksamling var totalt: " + str(round(new_mall/day_para, 1)))
    else:
        if restrict_shopping_mall_org == False:
            print("Andelen av de mottagliga som blev smittade i mall var: " + str(round(inf_mall/new_mall*100, 1)) + "%, antalet besök i folksamling per dag var på genomsnitt: " + str(round(new_mall/day, 1)))
main()
