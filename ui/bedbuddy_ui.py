# BedBuddy class generates, displays, and updates UI
# Database class called within it for MongoDB CRUD operations

import tkinter as tk
from tkinter import ttk, messagebox

from database.patient import Patient
from config.db_config import get_db
from database.db_operation import Database

# ---------- Get MongoDB ----------
database = Database(get_db())

# ---------- Fixed Data ----------
MAX_BAYS = 3
MAX_BEDS_PER_BAY = 6

# ---------- Fixed Sizes ----------
BED_WIDTH = 80
BED_HEIGHT = 110
BAY_WIDTH = 330
BAY_HEIGHT = 270
BEDS_PER_ROW = 3

class BedBuddy:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hospital Dashboard")
        self.root.geometry("1700x500")

        # ---------------- Data ---------------- #
        self.bay_beds: dict[int, list[Patient]] = {}
        self.load_db_bays()

        # ---------------- State ---------------- #
        self.selected_bed = None
        self.current_bay = 1  # Bay 1 is default

        # ---------------- UI Setup ---------------- #
        self.setup_sidebar()
        self.setup_patient_view()
        self.setup_bay_view()
        self.show_bay(1)

    # ---------------- Initial Data Loading ---------------- #
    def load_db_bays(self):
        bays = [
            int(bay)
            for bay in database.db.list_collection_names()
            if bay.isdigit() and 1 <= int(bay) <= 6
        ]

        # Create "1" bay collection if none
        if not bays:
            database.create_bay(1)
            bays = [1]

        # Get patients in each bay
        for bay in bays:
            patients = database.get_bay_patients(bay)
            # If no patients, load 1 empty
            if not patients:
                empty_patient = Patient.empty(bay, 1)
                patients = [empty_patient]
                # Create empty bed document in database
                database.insert_patient(empty_patient)
            self.bay_beds[bay] = patients

    # ---------------- Sidebar ---------------- #
    def setup_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg="lightgray", width=150)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="ED Space", bg="lightgray", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))

        self.bay_buttons_frame = tk.Frame(self.sidebar, bg="lightgray")
        self.bay_buttons_frame.pack(anchor="w", padx=10, pady=10, fill="x")

        self.bay_buttons = {}  # Store buttons for highlighting
        for i in range(1, len(self.bay_beds) + 1):
            btn = tk.Button(self.bay_buttons_frame, text=f"- Bay {i}", bg="lightgray", relief="flat",
                            command=lambda num=i: self.show_bay(num))
            btn.pack(anchor="w", padx=5)
            self.bay_buttons[i] = btn

        self.patients_btn = tk.Button(
            self.sidebar,
            text="- Show All Patients",
            bg="lightgray",
            relief="flat",
            command=self.show_all_bays
        )
        self.patients_btn.pack(anchor="w", padx=5, pady=(5, 0))

        self.bay_control_frame = tk.Frame(self.sidebar, bd=1, relief="groove", bg="lightgray", padx=5, pady=5)
        self.bay_control_frame.pack(side="bottom", fill="x", pady=5)

        self.add_bay_btn = tk.Button(self.bay_control_frame, text="+ Add Bay", bg="lightblue", relief="raised",
                                     command=self.add_bay)
        self.remove_bay_btn = tk.Button(self.bay_control_frame, text="- Remove Bottom Bay", bg="red", fg="white",
                                        relief="raised", command=self.remove_bay)
        self.add_bay_btn.pack(fill="x", pady=(0, 5))
        self.remove_bay_btn.pack(fill="x", pady=(5, 0))

        self.bed_control_frame = tk.Frame(self.sidebar, bd=1, relief="groove", bg="lightgray", padx=5, pady=5)
        self.add_bed_btn = tk.Button(self.bed_control_frame, text="+ Add Bed", bg="lightgreen", relief="raised",
                                     command=self.add_bed)
        self.remove_bed_btn = tk.Button(self.bed_control_frame, text="- Remove Bed", bg="salmon", relief="raised",
                                        command=self.remove_bed)
        self.add_bed_btn.pack(fill="x", pady=(0, 2))
        self.remove_bed_btn.pack(fill="x", pady=(2, 0))

        # Highlight default tab: Bay 1
        self.highlight_tab(1)

    # ---------------- Highlighting Method ---------------- #
    def highlight_tab(self, bay_number):
        # Reset all buttons
        for num, btn in self.bay_buttons.items():
            btn.config(bg="lightgray", fg="black")
        self.patients_btn.config(bg="lightgray", fg="black")

        # Highlight the current tab
        if bay_number is None:
            self.patients_btn.config(bg="lightblue", fg="white")
        else:
            if bay_number in self.bay_buttons:
                self.bay_buttons[bay_number].config(bg="lightblue", fg="white")

    # ---------------- Patient Treeview ---------------- #
    def setup_patient_view(self):
        self.patient_frame = tk.Frame(self.root, bd=1, relief="solid")
        self.patient_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(self.patient_frame, text="Patient View", font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)

        columns = ("Name", "DOB", "Location", "Priority")
        self.tree = ttk.Treeview(self.patient_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    # ---------------- Bay View ---------------- #
    def setup_bay_view(self):
        self.bay_frame = tk.Frame(self.root, bd=1, relief="solid")
        self.bay_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(self.bay_frame, text="Bay View", font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)

        self.beds_frame = tk.Frame(self.bay_frame, bg="lightgray")
        self.beds_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.beds_frame.pack_propagate(False)

    # ---------------- Core Methods ---------------- #
    def refresh_tree(self, bay_filter=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        bays_to_show = [bay_filter] if bay_filter else self.bay_beds.keys()

        for bay_num in bays_to_show:
            for patient in self.bay_beds[bay_num]:
                if patient.presence:
                    patient_name = f"{patient.first_name} {patient.last_name}"
                    patient_dob = patient.dob
                    patient_location = f"Bay {patient.bay} / Bed {patient.bed}"
                    self.tree.insert("", "end", values=(patient_name, patient_dob, patient_location, patient.priority))

    def update_bed_info(self, curr_patient):
        for i, patient in enumerate(self.bay_beds[curr_patient.bay]):
            if patient.bed == curr_patient.bed:
                self.bay_beds[curr_patient.bay][i] = curr_patient
                break

    # ---------------- Patient Dialogs ---------------- #
    def add_patient_dialog(self, bay, bed):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add Patient to Bay {bay} Bed {bed}")
        dialog.geometry("300x300")
        dialog.grab_set()

        tk.Label(dialog, text="First Name").pack(pady=2)
        first_name_entry = tk.Entry(dialog)
        first_name_entry.pack(pady=2)

        tk.Label(dialog, text="Last Name").pack(pady=2)
        last_name_entry = tk.Entry(dialog)
        last_name_entry.pack(pady=2)

        tk.Label(dialog, text="DOB (YYYY-MM-DD)").pack(pady=2)
        dob_entry = tk.Entry(dialog)
        dob_entry.pack(pady=2)

        tk.Label(dialog, text="Priority").pack(pady=2)
        priority_var = tk.StringVar(dialog)
        priority_var.set("Medium")
        tk.OptionMenu(dialog, priority_var, "High", "Medium", "Low").pack(pady=2)

        def submit():
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            dob = dob_entry.get().strip()
            priority = priority_var.get()

            if not first_name or not last_name or not dob:
                messagebox.showwarning("Missing Info", "Please fill in all fields")
                return

            # Get existing bed document id
            existing_id = database.find_create_patient(bay, bed)
            # New patient with bed id loaded
            new_patient = Patient(
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                bay=bay,
                bed=bed,
                priority=priority,
                presence=True,
                _id=existing_id.id
            )
            self.update_bed_info(new_patient)
            # MONGODB - update bed with patient
            database.update_patient(new_patient)

            # Refresh current view without switching tabs
            if self.current_bay is None:
                self.show_all_bays()
            else:
                self.show_bay(self.current_bay)
            self.refresh_tree(self.current_bay)
            dialog.destroy()

        tk.Button(dialog, text="Add Patient", command=submit).pack(pady=5)

    def edit_patient_dialog(self, patient: Patient):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Patient in Bay {patient.bay} Bed {patient.bed}")
        dialog.geometry("300x350")
        dialog.grab_set()

        tk.Label(dialog, text="First Name").pack(pady=2)
        first_name_entry = tk.Entry(dialog)
        first_name_entry.insert(0, patient.first_name)
        first_name_entry.pack(pady=2)

        tk.Label(dialog, text="Last Name").pack(pady=2)
        last_name_entry = tk.Entry(dialog)
        last_name_entry.insert(0, patient.last_name)
        last_name_entry.pack(pady=2)

        tk.Label(dialog, text="DOB (YYYY-MM-DD)").pack(pady=2)
        dob_entry = tk.Entry(dialog)
        dob_entry.insert(0, patient.dob)
        dob_entry.pack(pady=2)

        tk.Label(dialog, text="Priority").pack(pady=2)
        priority_var = tk.StringVar(dialog)
        priority_var.set(patient.priority)
        tk.OptionMenu(dialog, priority_var, "High", "Medium", "Low").pack(pady=2)

        def save_changes():
            patient.first_name = first_name_entry.get().strip()
            patient.last_name = last_name_entry.get().strip()
            patient.dob = dob_entry.get().strip()
            patient.priority = priority_var.get()

            self.update_bed_info(patient)
            # MONGODB - update patient data
            database.update_patient(patient)

            # Refresh current view without switching tabs
            if self.current_bay is None:
                self.show_all_bays()
            else:
                self.show_bay(self.current_bay)

            self.refresh_tree(self.current_bay)
            dialog.destroy()

        def remove_patient():
            confirm = messagebox.askyesno("Remove Patient",
                                          f"Remove {patient.first_name} {patient.last_name} from Bed {patient.bed}?")
            if confirm:
                # Create empty patient
                empty_patient = patient.empty_copy()
                self.update_bed_info(empty_patient)
                # MONGODB - Clear existing document
                database.update_patient(empty_patient)

                if self.current_bay is None:
                    self.show_all_bays()
                else:
                    self.show_bay(self.current_bay)
                self.refresh_tree(self.current_bay)
                dialog.destroy()

        tk.Button(dialog, text="Save Changes", command=save_changes, bg="lightblue").pack(pady=5)
        tk.Button(dialog, text="Remove Patient", command=remove_patient, bg="salmon", fg="white").pack(pady=5)

    # ---------------- Bed Methods ---------------- #
    def create_bed(self, frame, patient):
        f = tk.Frame(frame, width=BED_WIDTH, height=BED_HEIGHT, bg="white", bd=1, relief="solid")
        f.pack_propagate(False)

        # Patient icon if present
        icon_lbl = None
        if patient.presence:
            patient_color = patient.get_color()
            icon_lbl = tk.Label(f, text="👤", fg=patient_color, bg="darkgray", font=("Arial", 25))
            icon_lbl.pack(side="top", pady=5)

        # Patient name or empty
        patient_name = f"{patient.first_name} {patient.last_name}" if patient.presence else ""
        name_lbl = tk.Label(f, text=patient_name, bg="white", font=("Arial", 8), wraplength=BED_WIDTH)
        name_lbl.pack(side="top")

        # Bed number at bottom
        label = tk.Label(f, text=f"Bed {patient.bed}", bg="white", font=("Arial", 10))
        label.pack(side="bottom", pady=5)

        def on_click(event):
            if self.selected_bed:
                self.selected_bed.config(bd=1, relief="solid", highlightthickness=0)
            f.config(bd=3, relief="solid", highlightbackground="red", highlightcolor="red", highlightthickness=3)
            self.selected_bed = f

            curr_patient = next(
                (p for p in self.bay_beds.get(patient.bay, []) if p.bed == patient.bed),
                None
            )

            if curr_patient.presence:
                self.edit_patient_dialog(curr_patient)
            else:
                self.add_patient_dialog(curr_patient.bay, curr_patient.bed)

        f.bind("<Button-1>", on_click)
        label.bind("<Button-1>", on_click)
        name_lbl.bind("<Button-1>", on_click)
        if icon_lbl:
            icon_lbl.bind("<Button-1>", on_click)

        return f

    # ---------------- Show Bay ---------------- #
    def show_bay(self, bay_number):
        self.current_bay = bay_number if bay_number else 1
        self.highlight_tab(bay_number)

        if self.selected_bed:
            self.selected_bed.config(bd=1, relief="solid", highlightthickness=0)
            self.selected_bed = None

        self.bed_control_frame.pack(side="bottom", fill="x", pady=5)

        for widget in self.beds_frame.winfo_children():
            widget.destroy()

        if hasattr(self, "current_view_label"):
            self.current_view_label.destroy()
        self.current_view_label = tk.Label(self.bay_frame, text=f"Current View: Bay {self.current_bay}",
                                           font=("Arial", 12, "bold"))
        self.current_view_label.pack(anchor="w", padx=5, pady=5)

        bay_container = tk.Frame(self.beds_frame, width=BAY_WIDTH, height=BAY_HEIGHT, bg="lightgray", bd=1, relief="solid")
        bay_container.pack(padx=10, pady=10)
        bay_container.pack_propagate(False)

        row, col = 0, 0
        for patient in self.bay_beds[self.current_bay]:
            bed = self.create_bed(bay_container, patient)
            bed.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col >= BEDS_PER_ROW:
                col = 0
                row += 1

        self.refresh_tree(self.current_bay)

    # ---------------- Show All Bays ---------------- #
    def show_all_bays(self):
        self.current_bay = None
        self.highlight_tab(None)

        if self.selected_bed:
            self.selected_bed.config(bd=1, relief="solid", highlightthickness=0)
            self.selected_bed = None

        self.bed_control_frame.pack_forget()

        for widget in self.beds_frame.winfo_children():
            widget.destroy()

        if hasattr(self, "current_view_label"):
            self.current_view_label.destroy()
        self.current_view_label = tk.Label(self.bay_frame, text=f"Current View: All Patients",
                                           font=("Arial", 12, "bold"))
        self.current_view_label.pack(anchor="w", padx=5, pady=5)

        sorted_bays = sorted(self.bay_beds.items())
        for idx, (bay_num, beds) in enumerate(sorted_bays):
            row = (idx // 3) * 2
            col = idx % 3

            bay_container = tk.Frame(self.beds_frame, width=BAY_WIDTH, height=BAY_HEIGHT, bd=1, relief="solid", bg="lightgray")
            bay_container.grid(row=row, column=col, padx=10, pady=10)
            bay_container.pack_propagate(False)

            for j, patient in enumerate(beds):
                bed_row, bed_col = divmod(j, BEDS_PER_ROW)
                bed = self.create_bed(bay_container, patient)
                bed.grid(row=bed_row, column=bed_col, padx=5, pady=5)

        self.refresh_tree(None)

    # ---------------- Add/Remove Bay & Bed ---------------- #
    def add_bay(self):
        total_bays = len(self.bay_beds)
        if total_bays >= MAX_BAYS:
            messagebox.showwarning("Limit Reached", f"Maximum of {MAX_BAYS} bays reached!")
            return

        bay_num = total_bays + 1
        self.bay_beds[bay_num] = []

        # MONGODB - create bay collection
        database.create_bay(bay_num)

        # Create button for new bay
        new_btn = tk.Button(self.bay_buttons_frame, text=f"- Bay {bay_num}", bg="lightgray", relief="flat",
                            command=lambda num=bay_num: self.show_bay(num))
        new_btn.pack(anchor="w", padx=5)
        self.bay_buttons[bay_num] = new_btn

        # Switch view to new bay and highlight it
        self.show_bay(bay_num)

        messagebox.showinfo("Success", f"Bay {bay_num} added successfully!")

    def remove_bay(self):
        if len(self.bay_beds) <= 1:
            messagebox.showwarning("Cannot Remove", "There must be at least 1 bay!")
            return

        last_bay = max(self.bay_beds.keys())
        confirm = messagebox.askyesno("Remove Bay", f"Remove Bay {last_bay}?")
        if confirm:
            del self.bay_beds[last_bay]
            # MONGODB - drop bay collection
            database.delete_bay(last_bay)

            if last_bay in self.bay_buttons:
                self.bay_buttons[last_bay].destroy()
                del self.bay_buttons[last_bay]

            if self.bay_beds:
                self.show_bay(max(self.bay_beds.keys()))

    def add_bed(self):
        if self.current_bay is None:
            messagebox.showwarning("No Bay Selected", "Please select a specific bay to add a bed.")
            return

        beds_in_bay = self.bay_beds[self.current_bay]
        if len(beds_in_bay) >= MAX_BEDS_PER_BAY:
            messagebox.showwarning("Limit Reached", f"Bay {self.current_bay} can only have {MAX_BEDS_PER_BAY} beds.")
            return

        new_bed_num = len(beds_in_bay) + 1

        empty_patient = Patient.empty(self.current_bay, new_bed_num)
        beds_in_bay.append(empty_patient)

        # MONGODB - create empty patient document
        database.insert_patient(empty_patient)

        self.show_bay(self.current_bay)

    def remove_bed(self):
        if self.current_bay is None:
            messagebox.showwarning("No Bay Selected", "Select a bay first!")
            return

        beds_in_bay = self.bay_beds[self.current_bay]
        if len(beds_in_bay) <= 1:
            messagebox.showwarning("Cannot Remove", "Each bay must have at least 1 bed!")
            return

        bed_to_remove = beds_in_bay[-1]
        confirm = messagebox.askyesno("Remove Bed", f"Remove Bed {bed_to_remove.bed} from Bay {self.current_bay}?")
        if confirm:
            beds_in_bay.pop()

            #MONGODB - remove patient document
            if bed_to_remove.id:
                string = database.delete_patient(bed_to_remove)

            self.show_bay(self.current_bay)

    # ---------------- Run ---------------- #
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = BedBuddy()
    app.run()
