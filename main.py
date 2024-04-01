import tkinter as tk
from tkinter import messagebox

class TaskManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")
        self.master.geometry("400x420")
        self.master.config(bg="#f0f0f0")      
        self.tasks = []        
        self.task_label = tk.Label(self.master, text="Aggiungi attività:", bg="#f0f0f0", font=("Helvetica", 12))
        self.task_label.pack(pady=5)       
        self.task_entry = tk.Entry(self.master, width=30, font=("Helvetica", 12))
        self.task_entry.pack(pady=5)        
        self.status_options = ["Completo", "In corso", "Abbandonato"]       
        self.status_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.status_frame.pack(pady=5)        
        self.status_label = tk.Label(self.status_frame, text="Seleziona lo stato:", bg="#f0f0f0")
        self.status_label.grid(row=0, column=0, padx=5, pady=5) 
        self.status_var = tk.StringVar(self.master)
        self.status_var.set(self.status_options[0])  
        self.status_menu = tk.OptionMenu(self.status_frame, self.status_var, *self.status_options)
        self.status_menu.config(font=("Helvetica", 10))
        self.status_menu.grid(row=0, column=1, padx=5, pady=5)     
        self.add_button = tk.Button(self.master, text="Aggiungi attività", command=self.add_task, bg="#4caf50", fg="white", relief=tk.FLAT, font=("Helvetica", 10))
        self.add_button.pack(pady=5)  
        self.task_list = tk.Listbox(self.master, width=40, font=("Helvetica", 12), selectbackground="#a5d8ff")
        self.task_list.pack(pady=10)    
        self.button_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.button_frame.pack(pady=5)   
        self.complete_button = tk.Button(self.button_frame, text="Aggiorna stato", command=self.update_status, bg="#ffc107", fg="black", relief=tk.FLAT, font=("Helvetica", 10))
        self.complete_button.grid(row=0, column=0, padx=5, pady=5)  
        self.delete_button = tk.Button(self.button_frame, text="Elimina", command=self.delete_task, bg="#ff0000", fg="white", relief=tk.FLAT, font=("Helvetica", 10))
        self.delete_button.grid(row=0, column=1, padx=5, pady=5)   
        self.load_tasks()
        self.task_list.bind("<Button-3>", self.update_status_rightclick)
        self.task_list.bind("<Button-1>", self.deselect_item)
        
    def add_task(self):
        task = self.task_entry.get()
        if task:
            status = self.status_var.get()
            self.tasks.append((task, status))
            self.task_list.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Attenzione", "Inserire un'attività!")
    
    def update_status(self):
        try:
            selected_task_index = self.task_list.curselection()[0]
            status = self.status_var.get()
            self.tasks[selected_task_index] = (self.tasks[selected_task_index][0], status)
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Attenzione", "Selezionare un'attività da aggiornare!")

    def delete_task(self):
        try:
            selected_task_index = self.task_list.curselection()[0]
            self.task_list.delete(selected_task_index)
            del self.tasks[selected_task_index]
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Attenzione", "Selezionare un'attività da eliminare!")
    
    def update_status_rightclick(self, event):
        try:
            index = self.task_list.nearest(event.y)
            current_status = self.tasks[index][1]
            new_status = self.status_var.get()
            if current_status != new_status:
                self.tasks[index] = (self.tasks[index][0], new_status)
                self.update_task_list()
                self.save_tasks()
        except IndexError:
            pass
            
    def deselect_item(self, event):
        self.task_list.selection_clear(0, tk.END)
    
    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task, status in self.tasks:
            if status == "Completo":
                bg_color = "light green"
            elif status == "In corso":
                bg_color = "yellow"
            elif status == "Abbandonato":
                bg_color = "light gray"
            self.task_list.insert(tk.END, task)
            self.task_list.itemconfig(tk.END, {'bg': bg_color})
    
    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task, status in self.tasks:
                file.write(f"{task},{status}\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) == 2:
                        task, status = data
                        self.tasks.append((task, status))
            self.update_task_list()
        except FileNotFoundError:
            pass

def main():
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()