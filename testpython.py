import os
import csv

def read_class_schedule(path, filename):
    """
    Reads a file and returns a list of the classes

    [{"Subject": "Python", "Teacher": "Me", ...}, ...]
    """
    class_schedule = []
    with open(path + filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            class_schedule.append(row)
    return class_schedule


link = "sdjfdsgfsdugsdjf"
class_day = "Saturday"
class_name = "2nd English"
teacher = "Raj T"
start_time = "6:00 PM"
end_time = "6:45 PM"

# Create a string re`pre`sentation of the class name and time
strclass_name_n_time = (class_name, class_day, start_time.upper(), end_time.upper(), teacher.title())

#Converts into list
class_name_n_time = list(strclass_name_n_time)



# Define the path to the class schedules directory
path = 'class_schedules/'
files = os.listdir(path)

# Iterate over each file in the class schedules directory
for file in files:
    # Read the class schedule from the file
    class_schedule = read_class_schedule(path, file)
    
    # Iterate over each class info in the class schedule
    for class_info in class_schedule:
        
        class_info = list(class_info.values())
        
        # Check if the class info matches the provided class name, time, etc
        if class_info[0] == class_name_n_time[0] and class_info[1] == class_name_n_time[1] and class_info[2] == class_name_n_time[2] and class_info[3] == class_name_n_time[3] and class_info[4] == class_name_n_time[4]:

            # Respond with a confirmation message
            print(f"Meeting link ({link}) for {class_name} on {class_day} at {start_time} to {end_time} with {teacher} has been added.")
            
            memeclass_info.insert(8, link)

            with open('schedule.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(class_info)
                print("=========================================================")
                print(f"MEETING LINK ADDED: File Updated to: ```{class_info[0:5]} {class_info[8]}```")
                break
