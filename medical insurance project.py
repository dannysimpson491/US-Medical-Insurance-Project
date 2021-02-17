# import libraries
import csv, numpy as np, matplotlib.pyplot as plt

# load CSV data and get headings
with open("C:/Users/danny/Documents/Work/Data Science/Projects/US medical data project/python-portfolio-project-starter-files/insurance.csv",
          newline="") as data:
    insurance_data = csv.DictReader(data)
    headings = insurance_data.fieldnames
    
    # create empty lists for each column in insurance.csv
    for header in headings:
        globals()["%s" % header] = []
    #print(headings)
    
    # append the data to it's corresponding list
    for row in insurance_data:
        age.append(row["age"])
        sex.append(row["sex"])
        bmi.append(row["bmi"])
        children.append(row["children"])
        smoker.append(row["smoker"])
        region.append(row["region"])
        charges.append(row["charges"])

# create a list of variables to loop through and print each variable and it's length
variables = [age, sex, bmi, children, smoker, region, charges]
for variable in variables:
    #print(variable[:10])
    #print("Length:", len(variable))
    pass

# function to convert the data for analysis
def conversion():
    
    # convert lists of strings to NumPy arrays of integers or floats
    new_variables = [np.array([int(x) for x in age]),
                     np.array([0 if x == "male" else 1 for x in sex]),
                     np.array([float(x) for x in bmi]),
                     np.array([int(x) for x in children]),
                     np.array([0 if x == "no" else 1 for x in smoker]),
                     np.array([0 if x == "northwest" else 1 \
                           if x == "northeast" else 2 \
                           if x == "southwest" else 3 for x in region]),
                     np.array([float(x) for x in charges])]
    
    # store updated variables in a dictionary
    patients_info = dict(age = new_variables[0],
                        sex = new_variables[1],
                        bmi = new_variables[2],
                        children = new_variables[3],
                        smoker = new_variables[4],
                        region = new_variables[5],
                        charges = new_variables[6])
     
    return patients_info
                                    
# function called to update variables and store in a dictionary
patients_info_dict = conversion()
#print(patients_info_dict)

# function to calculate measures of average and spread
def analyse_data(data):
    
    # create a dictionary of the results
    values_dict = dict(mean = np.mean(data),
                       median = np.median(data),
                       stdev = np.std(data),
                       minimum = np.amin(data),
                       maximum = np.amax(data),
                       the_range = np.ptp(data))
        
    return values_dict

# for loop to analyse each variable from patients_info_dict and store the results in a dictionary
stats_dict = {}    
for key,value in patients_info_dict.items():
    stats_dict[key] = analyse_data(value)

#print(stats_dict)

# function to plot the distribution of the data
def plot_distribution(variable_name):
    
    # calculate the number of samples for each recorded value
    count = {}
    for i in patients_info_dict[variable_name]:
        if i in count.keys():
            count[i] += 1
        else:
            count[i] = 1
    
    # plot bar chart for categorical data or histogram for numercial data with the mean
    fig, ax = plt.subplots()
    if variable_name == "sex" or variable_name == "children" or \
       variable_name == "smoker" or variable_name == "region":
        ax.bar(count.keys(), count.values())
    else:
        ax.hist(patients_info_dict[variable_name], bins=20)
        ax.axvline(np.mean(patients_info_dict[variable_name]), color='r',
                   linestyle='--', linewidth=1)
        ax.legend(['Mean'], loc="upper right")
    
    # set the title, grid, axes labels and ticks
    ax.set(xlabel=f"{variable_name.title()}",
           ylabel="Frequency",
           title=f"{variable_name.title()} distribution")
    if variable_name == "sex":
        plt.xticks(np.arange(0, 1, step=0.5))
        plt.xticks(np.arange(2), ('Male', 'Female'))
    elif variable_name == "smoker":
        plt.xticks(np.arange(0, 1, step=0.5))
        plt.xticks(np.arange(2), ('Non-smoker', 'Smoker'))
    elif variable_name == "region":
        plt.xticks(np.arange(0, 4, step=0.25))
        plt.xticks(np.arange(4), ('Northwest', 'Northeast', "Southwest", "Southeast"))
    ax.grid()
    plt.show()

# for loop to input each variable into the function
for variable_name in headings:
    plot_distribution(variable_name)

# function to calculate the average cost per condition   
def analyse_charges(variable_name):
     
    index = 0
    charges_per_condition = {}
    
    for i in patients_info_dict[variable_name]:
        
        # 0 = 18-24, 1 = 25-31, 2 = 32-38, 3 = 39-45, 4 = 46-52, 5 = 53+
        if variable_name == "age":
            if i < 25:
                i = 0
            elif i >= 25 and i < 32:
                i = 1
            elif i >= 32 and i < 39:
                i = 2
            elif i >= 39 and i < 46:
                i = 3
            elif i >= 46 and i < 53:
                i = 4
            else:
                i = 5
        
        # 0 = underweight, 1 = healthy, 2 = overweight, 3 = obese, 4 = morbidly obese
        if variable_name == "bmi":
            if i < 18.5:
                i = 0
            elif i >= 18.5 and i < 25:
                i = 1
            elif i >= 25 and i < 30:
                i = 2
            elif i >= 30 and i < 40:
                i = 3
            else:
                i = 4
        
        # add the condition to the dictionary keys and create a list of the corresponding charges 
        if i in charges_per_condition.keys():
            charges_per_condition[i].append(patients_info_dict["charges"][index])
        else:
            charges_per_condition[i] = [patients_info_dict["charges"][index]]
        index += 1
    
    # add the condition to the dictionary keys and get average of the charges for that condition
    average_per_condition = {}
    for key,value in charges_per_condition.items():
        average_per_condition[key] = analyse_data(value)["mean"]      
    
    # take the most expensive condition and minus the cheapest condition to get the range
    the_range = max(average_per_condition.values()) - min(average_per_condition.values())
    
    # store this information in a dictionary
    analyse_charges = dict(average_per_condition = average_per_condition,
                           the_range = the_range)
        
    return analyse_charges

# for loop to analyse each variable's effect on charges and store the results in a dictionary
analyse_charges_dict = {}
for variable_name in headings[:-1]:
    analyse_charges_dict[variable_name] = analyse_charges(variable_name)
    
#print(analyse_charges_dict)

# plotted all factors against charges in order to see the effect
def plot_effect(variable_name):
    
    count = 0
    x, y = [], []
    
    # append each condition to x and the number of samples in each condition to y
    for i in range(len(analyse_charges_dict[variable_name]["average_per_condition"])):
        x.append(count)
        y.append(analyse_charges_dict[variable_name]["average_per_condition"][count])
        count += 1
    
    # plot the data with the mean
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.axhline(y=np.mean(list(analyse_charges_dict[variable_name]["average_per_condition"].values())),
               color='r', linestyle='--', linewidth=1)
    ax.legend(['Mean'], loc="upper right")
            
    if variable_name == "age":
        plt.xticks(np.arange(0, 6, step=0.2))
        plt.xticks(np.arange(6), ('18-24', '25-31', '32-38', '39-45', '46-52', '53+'))
    elif variable_name == "sex":
        plt.xticks(np.arange(0, 1, step=0.5))
        plt.xticks(np.arange(2), ('Male', 'Female'))
    elif variable_name == "bmi":
        plt.xticks(np.arange(0, 5, step=0.25))
        plt.xticks(np.arange(5), ('Underweight', 'Healthy', 'Overweight', 'Obese', 'Morbidly Obese'))
    elif variable_name == "smoker":
        plt.xticks(np.arange(0, 1, step=0.5))
        plt.xticks(np.arange(2), ('Non-smoker', 'Smoker'))
    elif variable_name == "region":
        plt.xticks(np.arange(0, 4, step=0.25))
        plt.xticks(np.arange(4), ('Northwest', 'Northeast', "Southwest", "Southeast"))
            
    ax.set(xlabel=f"{variable_name.title()}",
           ylabel="Charges ($)",
           title=f"The effect of {variable_name.title()} on Charges")
    ax.grid()
    ax.set_ylim(bottom=0)
    plt.show()

# for loop to input each of the independent variables into the function
for variable_name in headings[:-1]:
    plot_effect(variable_name)

# function to find patients overpaying for insurance
def targetting():
    
    actual = []
    insurance_estimates = []
    targets_dict = {}
    
    for i in range(len(age)):
        
        # formula to predict insurance cost based on health factors (from Codecademy, missing region) 
        estimate = (250*patients_info_dict["age"][i]
                     - 128*patients_info_dict["sex"][i]
                     + 370*patients_info_dict["bmi"][i]
                     + 425*patients_info_dict["children"][i]
                     + 24000*patients_info_dict["smoker"][i]
                     - 12500)
        
        # append actual and estimated charges to their corresponding list
        actual.append(patients_info_dict["charges"][i])
        insurance_estimates.append(estimate)
    
    # find patients overpaying by more than 5% and overpayment amount
    index = 0
    for i,j in zip(actual, insurance_estimates):
        if i > j*1.05:
            targets_dict[index] = i-j
        index += 1
    
    return targets_dict

targets_dict = targetting()
#print(targets_dict)

# class to provide different advice to patients based on their health factors
class Advice:
    
    # initialize the attributes of the class
    def __init__(self, patient_index, variable_names=headings):
        self.patient_index = patient_index
        self.patients_info_dict = patients_info_dict
        self.variable_names = variable_names
        self.targets_dict = targets_dict
    
    # method to return BMI advice and smoking advice
    def health_cost_advice(self):
        
        individual = []
        
        # get the values for each of the variables in patients_info_dict
        for i in self.variable_names:
            individual.append(self.patients_info_dict[i][self.patient_index])
        
        # set bmi_message depending on the patient's BMI category /
        # with the difference between the average charge for this condition and the healthy condition
        if individual[2] < 18.5:
            bmi_message = "BMI advice:\nYour BMI is {BMI} (underweight). To achieve a healthy BMI, you should consider increasing your BMI score by around {healthy}. However, this will not reduce your insurance cost.".format(
                BMI = round(individual[2], 1), 
                healthy = round(21.7 - individual[2], 1))
        elif individual[2] >= 25:
            bmi_message = "BMI advice:\nYour BMI is {BMI} ({category}). To achieve a healthy BMI and reduce your insurance cost by an estimated ${estimate}, you should consider reducing your BMI score by around {healthy}.".format(
                BMI = round(individual[2], 1),
                category = "overweight" if individual[2] < 30 else "obese" if individual[2] < 40 else "morbidly obese",
                estimate = (round(analyse_charges_dict["bmi"]["average_per_condition"][2] - analyse_charges_dict["bmi"]["average_per_condition"][1], 2) if individual[2] < 30
                            else round(analyse_charges_dict["bmi"]["average_per_condition"][3] - analyse_charges_dict["bmi"]["average_per_condition"][1], 2) if individual[2] < 40 
                            else round(analyse_charges_dict["bmi"]["average_per_condition"][4] - analyse_charges_dict["bmi"]["average_per_condition"][1], 2)),
                healthy = abs((round(21.7 - individual[2], 1))))
        else:
            bmi_message = "BMI advice:\nYour BMI is {} (healthy). You should try to maintain this for health reasons and to keep your insurance cost down.".format(
                round(individual[2], 1))
        
        # set smoking_message depending on the patient's smoking status /
        # with the difference between the average charge for smokers and non-smokers
        if individual[4] == 1:
            smoking_message = "Smoking advice:\nTo improve your health and reduce your insurance cost by an estimated ${estimate}, you should stop smoking.".format(
                estimate = round(analyse_charges_dict["smoker"]["average_per_condition"][1] - analyse_charges_dict["smoker"]["average_per_condition"][0], 2))
        else:
            smoking_message = "Smoking advice:\nCongratulations for not smoking. This is having a positive effect on your health and your insurance cost."
    
        return f"{bmi_message}\n\n{smoking_message}\n"
    
    # method to return insurance provder advice
    def provider_advice(self):
        
        # set message depending on if the patient is overpaying and by how much
        if self.patient_index in self.targets_dict.keys():
            message = "Insurance provider advice:\nBased on your age, sex, BMI, number of children, smoking status and region, you are overpaying on your health insurance by an estimated ${}; we recommend you change provider.".format(
                round(self.targets_dict[self.patient_index], 2))
        else:
            message = "Insurance provider advice:\nBased on your age, sex, BMI, number of children, smoking status and region, you are not overpaying for your health insurance; we recommend you stay with your provider."
        
        return message

# for loop to get advice for all patients and append them to the corresponding lists
health_cost_advice = []
provider_advice = []
for i in range(len(age)):
    patient_advice = Advice(i)
    health_cost_advice.append(patient_advice.health_cost_advice())
    provider_advice.append(patient_advice.provider_advice())   

# create an instance of the Advice class for patient_14
patient_14 = Advice(14)
#print(patient_14.health_cost_advice())
#print(patient_14.provider_advice())

# class to store patients health factors in a dictionary and estimate insurance cost
class Patient:
    
    # initialize the attributes of the class
    def __init__(self, age, sex, bmi, children, smoker):
        self.age = age
        self.sex = sex
        self.bmi = bmi
        self.children = children
        self.smoker = smoker
    
    # method to store patients health factors in a dictionary
    def patient_info(self):
        
        patient_dict = dict(age=self.age,
                            sex=self.sex,
                            bmi=self.bmi,
                            children=self.children,
                            smoker=self.smoker)
        
        return patient_dict
    
    # method to estimate patients insurance cost usin formula (from Codecademy, missing region)
    def estimated_cost(self):
        
        estimated_cost = (250*self.age
                          - 128*self.sex
                          + 370*self.bmi
                          + 425*self.children
                          + 24000*self.smoker
                          - 12500)
        
        return f"Based on your age, sex, BMI, number of children and smoking status, your estimated insurance cost is ${int(estimated_cost)}."

# create an instance of the Patient class for myself
danny_simpson = Patient(24, 0, 20.2, 0, 0)
#print(danny_simpson.patient_info(), danny_simpson.estimated_cost(), sep="\n")

# create an instance of the Patient class for my grandad
danny_simpson_grandad = Patient(88, 0, 22.8, 4, 1)
#print(danny_simpson_grandad.patient_info(), danny_simpson_grandad.estimated_cost(), sep="\n")