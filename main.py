import json
import datetime
import tkinter as tk
import tkinter.messagebox as messagebox

# DEnna delen är för att hantera filen assignments.json. Den läser in och sparar data i JSON-format.

def load_assignments(filename="assignments.json"):
    with open(filename, 'r') as f:
        return json.load(f)
    
def save_assignments(assignments, filename="assignments.json"):
    with open(filename, "w") as f:
        json.dump(assignments, f, indent=4)

#Funktionerna nedan är för att hantera ämnen och uppgifter. De lägger till ämnen och uppgifter, validerar datumformat och räknar dagar kvar till förfallodatum.

def add_subject(subject):
    assignments = load_assignments()
    if subject in assignments:
        return subject + " already exists." # Om ämnet redan finns, returnera ett meddelande
    else:
        assignments[subject] = {}
        save_assignments(assignments)


def add_assignment(subject, assignment, info, due_date):
    if not validate_date_format(due_date):
        messagebox.showerror("Invalid Date", "Please enter the due date in YYYY-MM-DD format.")
    else:
        assignments = load_assignments()

        if subject not in assignments:
            assignments[subject] = {}

        assignments[subject][assignment] ={
            "info": info,
            "due_date": due_date,
        } # Lägger till uppgiften i det valda ämnet

        save_assignments(assignments)

def validate_date_format(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d") # Kontrollerar om datumet är i formatet YYYY-MM-DD
        return True
    except:
        return False


def days_til_due(subject, assignment):
    assignments = load_assignments("assignments.json")
    due_date_str = assignments[subject][assignment]["due_date"]

    # Konverterar due_date_str till ett datetime-objekt
    due_date_obj = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()

    # Räkna ut skillnaden i dagar mellan idag och förfallodatumet
    today = datetime.date.today()
    days_left = (due_date_obj - today).days

    return f"{days_left}"

def remove_assignment(subject, assignment):
    assignments = load_assignments()
    if subject in assignments and assignment in assignments[subject]:
        del assignments[subject][assignment]
        save_assignments(assignments)
        refresh_subjects()

def remove_subject(subject):    
    assignments = load_assignments()
    if subject in assignments:
        del assignments[subject]
        save_assignments(assignments)
        refresh_subjects()

# Gui delen av koden

def new_window(windowType):
    global new_win
    if new_win is None or not new_win.winfo_exists(): #Förhindrar att flera fönster öppnas samtidigt
        if windowType == "new_subject":
            new_win = tk.Toplevel(root)
            new_win.title("New Subject")
            new_win.geometry("200x400")
            new_win.resizable(False, False)
            new_win.configure(bg="lightblue")
            new_win.focus_force()
            subject_label = tk.Label(new_win, text="Subject:", bg="lightblue")
            subject_label.pack(pady=10)
            subject_entry = tk.Entry(new_win, bg="lightyellow")
            subject_entry.pack(pady=10)
            subject_button = tk.Button(new_win, text="Add Subject", bg="lightyellow", command=lambda: [add_subject(subject_entry.get()), refresh_subjects(), new_win.destroy()]) #Lägger till ämnet i listan
            subject_button.pack(pady=10)

        elif windowType == "new_assignment":
            new_win = tk.Toplevel(root)
            new_win.title("New Assignment")
            new_win.geometry("200x400")
            new_win.resizable(False, False)
            new_win.configure(bg="lightblue")
            new_win.focus_force()
            subject_label = tk.Label(new_win, text="Subject name:", bg="lightblue")
            subject_label.pack(pady=10)
            subject_entry = tk.Entry(new_win, bg="lightyellow")
            subject_entry.pack(pady=10)

            assignment_label = tk.Label(new_win, text="Assignment name:", bg="lightblue")
            assignment_label.pack(pady=10)
            assignment_entry = tk.Entry(new_win, bg="lightyellow")
            assignment_entry.pack(pady=10)

            info_label = tk.Label(new_win, text="Info:", bg="lightblue")
            info_label.pack(pady=10)
            info_entry = tk.Entry(new_win, bg="lightyellow")
            info_entry.pack(pady=10)

            due_date_label = tk.Label(new_win, text="Due Date (YYYY-MM-DD):", bg="lightblue")
            due_date_label.pack(pady=10)

            due_date_entry = tk.Entry(new_win, bg="lightyellow")
            due_date_entry.pack(pady=10)

            assignment_button = tk.Button(new_win, text="Add Assignment", bg="lightyellow", command=lambda: [add_assignment(subject_entry.get(), assignment_entry.get(), info_entry.get(), due_date_entry.get()), refresh_subjects(), new_win.destroy()])
            assignment_button.pack(pady=10)

        else:
            new_win.lift()  # Bring to front if it's already open

def assignment_in_subject(subject):
    new_win = tk.Toplevel(root)
    new_win.title("New Assignment")
    new_win.geometry("200x400")
    new_win.resizable(False, False)
    new_win.configure(bg="lightblue")
    new_win.focus_force()

    assignment_label = tk.Label(new_win, text="Assignment name:", bg="lightblue")
    assignment_label.pack(pady=10)
    assignment_entry = tk.Entry(new_win, bg="lightyellow")
    assignment_entry.pack(pady=10)

    info_label = tk.Label(new_win, text="Info:", bg="lightblue")
    info_label.pack(pady=10)
    info_entry = tk.Entry(new_win, bg="lightyellow")
    info_entry.pack(pady=10)

    due_date_label = tk.Label(new_win, text="Due Date (YYYY-MM-DD):", bg="lightblue")
    due_date_label.pack(pady=10)

    due_date_entry = tk.Entry(new_win, bg="lightyellow")
    due_date_entry.pack(pady=10)

    assignment_button = tk.Button(new_win, text="Add Assignment", bg="lightyellow", command=lambda: [add_assignment(subject, assignment_entry.get(), info_entry.get(), due_date_entry.get()), refresh_subjects(), new_win.destroy()])
    assignment_button.pack(pady=10)
def check_assignments(subject):
    global new_win
    assignments = load_assignments()
    
    if new_win is None or not new_win.winfo_exists(): #Förhindrar att flera fönster öppnas samtidigt
        new_win = tk.Toplevel(root)
        new_win.title(f"Assignments: {subject}")
        new_win.geometry("420x400")
        new_win.configure(bg="lightblue")
        new_win.resizable(False, False)

        # Create a canvas and scrollbar
        canvas = tk.Canvas(new_win, bg="lightblue", highlightthickness=0) #Skapar en canvas för att visa uppgifterna
        scrollbar = tk.Scrollbar(new_win, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="lightblue")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        ) # Binder scroll_frame till canvas så att den kan scrollas

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw") # Skapar ett fönster i canvas där scroll_frame kommer att visas
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for j in assignments[subject]: # Loopar igenom alla uppgifter i det valda ämnet och visar dem i scroll_frame
            tk.Label(scroll_frame, text=f"Assignment: {j}", bg="lightblue").pack(anchor="w", padx=10)
            tk.Label(scroll_frame, text=f"Info: {assignments[subject][j]['info']}", bg="lightblue").pack(anchor="w", padx=10)
            tk.Label(scroll_frame, text=f"Due date: {assignments[subject][j]['due_date']}", bg="lightblue").pack(anchor="w", padx=10)
            tk.Label(scroll_frame, text=f"Days left: {days_til_due(subject, j)}", bg="lightblue").pack(anchor="w", padx=10)
            tk.Label(scroll_frame, text="-----------------------------------", bg="lightblue").pack(anchor="w", padx=10, pady=5)

        # Knapp för att ta bort och lägga till uppgifter
        remove_button = tk.Button(scroll_frame, text="Remove Assignment", bg="lightyellow", command=lambda: remove_window(subject))
        remove_button.pack(pady=10)
        add_assignment_button = tk.Button(scroll_frame, text="Add Assignment", bg="lightyellow", command=lambda: [new_win.destroy(), assignment_in_subject(subject)])
        add_assignment_button.pack(pady=10)


def refresh_subjects():
    assignments = load_assignments()
    subject_list.delete(0, tk.END)
    for i in assignments:
        subject_list.insert(tk.END, i)

def get_selection(mylistbox): # Hämtar det valda ämnet från listboxen
    selection = mylistbox.curselection()
    if selection:
        index = selection[0]
        value = mylistbox.get(index)
        return value
    

def confirm_and_remove_assignment(subject, assignment):
    if messagebox.askyesno("Confirm Delete", f"Delete '{assignment}' from {subject}?"):
        remove_assignment(subject, assignment)

def confirm_and_remove_subject(subject):
    if messagebox.askyesno("Confirm Delete", f"Delete {subject}?"):
        remove_subject(subject)


def remove_window(subject):
    assignments = load_assignments()
    if subject not in assignments or not assignments[subject]:
        return  # No assignments to remove

    remove_window = tk.Toplevel(new_win)
    remove_window.title("Remove Assignment")
    remove_window.geometry("300x200")
    remove_window.configure(bg="lightblue")
    remove_window.resizable(False, False)
    remove_window.focus_force()

    tk.Label(remove_window, text="Select assignment to remove:", bg="lightblue").pack(pady=10)

    # Create a StringVar and OptionMenu for assignments
    selected_assignment = tk.StringVar(remove_window)
    assignment_names = list(assignments[subject].keys())
    selected_assignment.set(assignment_names[0])  # default value

    dropdown = tk.OptionMenu(remove_window, selected_assignment, *assignment_names)
    dropdown.configure(bg="lightyellow")
    dropdown.pack(pady=10)

    # Remove button that deletes selected assignment
    remove_button = tk.Button(
        remove_window,
        text="Remove",
        bg="lightyellow",
        command=lambda: [confirm_and_remove_assignment(subject, selected_assignment.get()), remove_window.destroy()]
    )
    remove_button.pack(pady=10)


# Själva GUI-koden börjar här

new_win = None  # Reference for the new window
root = tk.Tk()
root.resizable(False, False)
root.title("Assignment Tracker")
root.geometry("400x400")
root.configure(bg="lightblue")



subject_list = tk.Listbox(root, width=50, height=10, bg="lightyellow", font=("Times new roman", 14))
assignments = load_assignments()
for i in assignments:
    subject_list.insert(tk.END, i)
subject_list.pack(pady=20)

new_subject_button = tk.Button(root, text="New Subject", bg="lightyellow", command=lambda: new_window("new_subject"))
new_subject_button.pack()

new_assignment_button = tk.Button(root, text="New Assignment", bg="lightyellow", command=lambda: new_window("new_assignment"))
new_assignment_button.pack()

remove_subject_button = tk.Button(root, text="Remove Subject", bg="lightyellow", command=lambda: [confirm_and_remove_subject(get_selection(subject_list)), refresh_subjects()])
remove_subject_button.pack()

check_assignments_button = tk.Button(root, text="Check Assignments", bg="lightyellow", command=lambda: check_assignments(get_selection(subject_list)))
check_assignments_button.pack()



root.mainloop()