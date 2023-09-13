import os
from discord.ext import commands
from dotenv import load_dotenv
from main import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# bot = commands.Bot(intents=discord.Intents.all())
bot = commands.Bot()

path = 'class_schedules/'
# path = 'test/'
files = os.listdir(path)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guilds:')
    bot_guilds = [g for g in [o.name for o in bot.guilds]]
    print(*bot_guilds, sep='\n')


@bot.slash_command(name='hello', description='Greets You!')
async def hello(ctx):
    await ctx.respond(f'Hello {ctx.author.display_name}!')


@bot.slash_command(name='send_reminders', description='Send Reminders to Students that have a class today.')
@commands.has_role('VP')
async def send_reminders(ctx):
    await ctx.respond("# Sending Reminders!")
    messages = main()

    for subject, student in messages.items():
        await ctx.send('## ' + subject.split('.')[0])
        for s in student:
            await ctx.send(s)
        await ctx.send('================================================================')


@bot.slash_command(name='list_students', description='List the students in a class OR a teacher OR both.')
async def list_students(ctx, class_name: str = None, teacher: str = None):
    
    # If only class name is provided
    if class_name and not teacher:
        for file in files:
            class_schedule = read_class_schedule(path, file)
            to_return = {}
            students = []
            current_teacher = ""
            flag = False
            for c in class_schedule:
                if c['Subject'].lower() != class_name.lower(): continue
                
                flag = True
                if current_teacher != c['Teacher']: students = []
                current_teacher = c['Teacher']

                d = {'Day': c['Day'], 'Time': c['Start Time'] + " - " + c['End Time'], 'Students': students}
                students.append(c['Student First Name'] + " " + c["Student Last Name"])
                to_return[c['Teacher']] = d

            if flag: break
            
        await ctx.respond("# " + class_name)
        for teacher_name, contents in to_return.items():
            await ctx.send("## " + teacher_name + " (" + contents['Day'] + " " + contents['Time'] + ")")
            for student in contents['Students']:
                await ctx.send("- " + student)
            
    # If only teacher name is provided
    elif teacher and not class_name:
        to_return = {}
        
        for file in files:
            class_schedule = read_class_schedule(path, file)
            current_subject = ""
            students = []
            for c in class_schedule:
                if c['Teacher'].lower() != teacher.lower(): continue

                if current_subject != c['Subject']: students = []
                current_subject = c['Subject']
                
                students.append(c['Student First Name'] + " " + c["Student Last Name"])
                d = {"Day": c['Day'], 'Time': c['Start Time'] + " - " + c['End Time'], 'Students': students}
                to_return[c['Subject']] = d

        await ctx.respond("# " + teacher)
        for subject, contents in to_return.items():
            await ctx.send("## " + subject + " (" + contents['Day'] + " " + contents['Time'] + ")")
            for student in contents['Students']:
                await ctx.send("- " + student)

    # If both class and teacher is provided
    elif class_name and teacher:
        for file in files:
            class_schedule = read_class_schedule(path, file)
            to_return = {}
            students = []
            flag = False

            for c in class_schedule:
                if c['Subject'].lower() != class_name.lower() or c['Teacher'].lower() != teacher.lower(): continue

                flag = True

                to_return['Day'] = c['Day']
                to_return['Time'] = c['Start Time'] + " - " + c['End Time']

                students.append(c['Student First Name'] + " " + c["Student Last Name"])
                to_return['Students'] = students

            if flag: break

        await ctx.respond("# " + class_name + " by " + teacher)
        await ctx.send("## Day: " + to_return['Day'])
        await ctx.send("## Time: " + to_return['Time'])
        for student in to_return['Students']:
            await ctx.send("- " + student)

    # If none
    else:
        ctx.respond("Provide a class name or a teacher's name or both.")


@bot.slash_command(name='send_reminder_to', description='Send Reminder to a specific student.')
@commands.has_role('VP')
async def send_reminder_to(ctx, fname, lname):
    student_name = (fname.strip() + ' ' + lname.strip()).title()

    for file in files:
        class_schedule = read_class_schedule(path, file)
        sender_address = "academicempowermentproject@gmail.com"

        for student in class_schedule:
            current_name = student['Student First Name'].title() + ' ' + student['Student Last Name'].title()
            current_name = current_name.title()
            if student_name == current_name:
                await ctx.respond(send_class_reminders(student, sender_address))

@bot.slash_command(name='add_meeting_time', description='Insert your Google Meet link so that an email can be sent including the meeting link')
async def add_meeting_time(ctx, link, class_day, class_name, teacher, start_time, end_time):
   

    # Create a string re`pre`sentation of the class name and time
    strclass_name_n_time = (class_name.strip() + ' ' + class_day.strip() + " " + start_time.strip().upper() + ' ' + end_time.strip().upper() + ' ' + teacher.strip().title())
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
                await ctx.respond(f"Meeting link ({link}) for {class_name} on {class_day} at {start_time} to {end_time} with {teacher} has been added.")
                
                class_info.insert(8, link)

                with open('schedule.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(class_info)
                    await ctx.respond("=========================================================")
                    await ctx.respond(f"MEETING LINK ADDED: File Updated to: ```{class_info[0:4] + {class_info[8]}}```")
                    break


bot.run(TOKEN)