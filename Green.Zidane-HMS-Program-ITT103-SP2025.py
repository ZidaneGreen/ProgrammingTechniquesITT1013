# HOSPITAL MANAGEMENT SYSTEM | # Course - ITT103  - Programming techniques
# ========================================================================

# Importing the necessary libraries
# ---------------------------------------------------------------------------------------------------------------------

import random
import string
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console = Console()
# -------------------------------------------------------
# CLASS: Person (Parent Class)
# Represents a generic person with name, age and gender
# ----------------------------------------------------------------------------------------------------------------

class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def display(self):
        print("name:", self.name)
        print("age:", self.age)
        print("gender:", self.gender)


# CLASS Patient (inherit from parent class)
# -------------------------------------------------------------------------------------------------------------------

class Patient(Person):
    def __init__(self, name, age, gender, patient_id):
        super().__init__(name, age, gender)
        self.patient_id = patient_id
        self.appointment_list = []

    def view_profile(self):
        print("=====Patient Profile=====")
        print("name:", self.name)
        print("age:", self.age)
        print("gender:", self.gender)
        print("patient_id:", self.patient_id)
        print("appointments:")
        if self.appointment_list:
            for appt in self.appointment_list:
                print("  -", appt)
        else:
            print("  No appointments found.")

    # Randomly generate patient ID
    # ----------------------------------------------------------------------------------------------------------------

    def generate_patient_id(self):
        letters = string.ascii_uppercase
        digits = string.digits
        random_part = ''.join(random.choices(letters + digits, k=4))
        return "P" + random_part


# CLASS Doctor (Inherit from parent class)
# -----------------------------------------------------------------------------------------------------------------

class Doctor(Person):
    def __init__(self, name, age, gender, doctor_id, speciality, schedule):
        super().__init__(name, age, gender)
        self.doctor_id = doctor_id
        self.speciality = speciality
        self.schedule = schedule

    def is_available(self, time):
        return time in self.schedule

    def view_profile(self):
        print("=====Doctor Profile=====")
        print("name:", self.name)
        print("doctor_id:", self.doctor_id)
        print("speciality:", self.speciality)
        print("available times:", ", ".join(self.schedule))


    # Adding patients to the Hospital System
    # ------------------------------------------------------------------------------------------------------------------

    def generate_doctor_id(self):
        letters = string.ascii_uppercase
        digits = string.digits
        random_part = ''.join(random.choices(letters + digits, k=4))
        return "D" + random_part


# CLASS Appointment
# -----------------------------------------------------------------------------------------------------------------

class Appointment:
    def __init__(self, appointment_id, patient, doctor, date, time):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.status = "Scheduled"

    def confirm(self):
        self.status = "confirmed"

    def cancel(self):
        self.status = "cancelled"

    def __str__(self):
        return f"[{self.appointment_id}] Dr. {self.doctor.name} on {self.date} at {self.time} - {self.status}"

    def view_profile(self):
        print("=====Appointment Profile=====")
        print("appointment_id:", self.appointment_id)
        print("patient name:", self.patient.name)
        print("doctor name:", self.doctor.name)
        print("date:", self.date)
        print("time:", self.time)
        print("status:", self.status)

SPECIALTIES = [
            "General Practitioner",
            "Pediatrician",
            "Cardiologist",
            "Dermatologist",
            "Neurologist",
            "Gynecologist",
            "Surgeon"
        ]


# CLASS Hospital System (Main Controller)
# -----------------------------------------------------------------------------------------------------------------

class HospitalSystem:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.appointments = []
        self.patient_counter = 1
        self.doctor_counter = 1
        self.appointment_counter = 1

# Adding patient to the system
# ----------------------------------------------------------------------------------------------------------------------

    def add_patient(self):
        print("\n***** Add new Patient *****")
        name = input("Enter Patient Name: ")
        try:
            age = int(input("Enter Patient Age: "))
        except ValueError:
            print("Invalid age. Must be a number.")
            return

        while True:
            gender = input("Enter Patient Gender (male/female): ").strip().lower()
            if gender in ['male', 'female']:
                break
            else:
                print("Invalid input. Please enter 'male' or 'female'.")

        patient = Patient(name, age, gender, Patient.generate_patient_id(self))

        self.patients[patient.patient_id] = patient

        print(f"Patient {name} added with ID {patient.patient_id}.")

# View patients profile
# ----------------------------------------------------------------------------------------------------------------------

    def view_patient_profile(self):
        console.print("\n[bold cyan]--- View Patient Profile ---[/bold cyan]")
        patient_id = input("Enter Patient ID: ")

        if patient_id in self.patients:
            patient = self.patients[patient_id]
            patient.view_profile()
        else:
            console.print("[bold red]Patient ID not found.[/bold red]")


# Adding Doctors to the Hospital system
# -----------------------------------------------------------------------------------------------------------------

    def add_doctor(self):
        print("\n***** Add new Doctor *****")
        name = input("Enter Doctor Name: ")
        try:
            age = int(input("Enter Doctor Age: "))
        except ValueError:
            print("Invalid age. Must be a number.")
# Using a while loop to ensure that the gender selected is one of what is required

        while True:
            gender = input("Enter Doctor Gender (male/female): ").strip().lower()
            if gender in ['male', 'female']:
                break
            else:
                print("Invalid input. Please enter 'male' or 'female'.")

#Display list of specialities
        print("\nSelect Doctor Speciality:")
        for index, spec in enumerate(SPECIALTIES, start=1):
            print(f"{index}. {spec}")

#Allows user to pick from the list by number
        while True:
            try:
                selection = int(input("Enter number of the specialty: "))
                if 1 <= selection <= len(SPECIALTIES):
                    speciality = SPECIALTIES[selection - 1]
                    break
                else:
                    print("Please choose a valid number from 1 to", len(SPECIALTIES))
            except ValueError:
                print("Invalid input. Please enter a number.")

        week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        schedule = []

        print("\nEnter doctor's availability:")

        for day in week_days:
            available = input(f"Are you available on {day}? (yes/no): ").strip().lower()
            if available == "yes":
                try:
                    num_times = int(input(f"How many time slots on {day}? "))
                except ValueError:
                    print("Invalid number. Skipping this day.")
                    continue

                for i in range(num_times):
                    time = input(f"  Enter time slot {i + 1} on {day} (e.g., 10:00 AM): ").strip()
                    schedule.append(f"{day} {time}")

        doctor = Doctor(name, age, gender, Doctor.generate_doctor_id(self), speciality, schedule)
        self.doctors[doctor.doctor_id] = doctor

        print(f"Doctor {name} added with ID {doctor.doctor_id}.")

# Viewing Doctor's Profile
# ----------------------------------------------------------------------------------------------------------------------

    def view_doctor_schedule(self):
        console.print("\n[bold cyan]--- View Doctor's Schedule ---[/bold cyan]")
        doctor_id = input("Enter Doctor's ID: ")

        if doctor_id in self.doctors:
            doctor = self.doctors[doctor_id]

# Doctor Profile Panel
            panel_content = (
                f"[bold]Doctor ID:[/bold] {doctor.doctor_id}\n"
                f"[bold]Name:[/bold] Dr. {doctor.name}\n"
                f"[bold]Speciality:[/bold] {doctor.speciality}"
            )
            console.print(Panel(panel_content, title="DOCTOR PROFILE", expand=False, border_style="magenta"))

# Doctor's Schedule Table
            if doctor.schedule:
                table = Table(title="Available Time Slots: ", border_style="green")
                table.add_column("No.", justify="center", style="cyan", no_wrap=True)
                table.add_column("Time Slot", justify="left", style="white")

                for i, slot in enumerate(doctor.schedule, start=1):
                    table.add_row(str(i), slot)

                console.print(table)
            else:
                console.print(Panel("[red]No available time slots.[/red]", border_style="red"))
        else:
            console.print("[bold red]Doctor ID not found.[/bold red]")

    # Booking Appointment in the System
# ----------------------------------------------------------------------------------------------------------------------

    def book_appointment(self):
        print("\n--- Book Appointment ---")
        patient_id = input("Enter patient ID: ")
        doctor_id = input("Enter doctor ID: ")

        if patient_id not in self.patients:
            print("Patient not found.")
            return
        if doctor_id not in self.doctors:
            print("Doctor not found.")
            return

        doctor = self.doctors[doctor_id]
        if not doctor.schedule:
            print("Doctor has no available time slots.")
            return

        print("\nDoctor's Available Time Slots:")
        for i, slot in enumerate(doctor.schedule, start=1):
            print(f"{i}. {slot}")

        while True:
            try:
                selection = int(input("Select a time slot by number: "))
                if 1 <= selection <= len(doctor.schedule):
                    selected_slot = doctor.schedule[selection - 1]
                    break
                else:
                    print("Please select a valid slot number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        date, time = selected_slot.split(" ", 1)

        appointment_id = f"A{self.appointment_counter:03}"
        self.appointment_counter += 1

        appointment = Appointment(appointment_id, self.patients[patient_id], doctor, date, time)
        appointment.confirm()
        self.appointments.append(appointment)

        self.patients[patient_id].appointment_list.append(appointment)
        doctor.schedule.remove(selected_slot)

        print(f"Appointment booked successfully. ID: {appointment_id}")


    # Cancel Appointment already made in the system
    # ----------------------------------------------------------------------------------------------------------------

    def cancel_appointment(self):
        print("\n--- Cancel Appointment ---")
        appointment_id = input("Enter appointment ID: ")
        found = False

        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                appointment.cancel()
                appointment.doctor.schedule.append(appointment.time)  # Free the time slot
                print(f"Appointment {appointment_id} cancelled.")
                found = True
                break

        if not found:
            print("Appointment ID not found.")

    # Reschedule Appointment
    # -----------------------------------------------------------------------------------------------------------------
    def reschedule_appointment(self):
        print("\n--- Reschedule Appointment ---")
        appointment_id = input("Enter appointment ID: ")
        found = False

        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                found = True
                doctor = appointment.doctor

                print(f"\nCurrent appointment details:")
                appointment.view_profile()

                if not doctor.schedule:
                    print("Doctor has no other available time slots.")
                    return

                print("\nAvailable new time slots:")
                for i, slot in enumerate(doctor.schedule, start=1):
                    print(f"{i}. {slot}")

                while True:
                    try:
                        new_selection = int(input("Select new time slot by number: "))
                        if 1 <= new_selection <= len(doctor.schedule):
                            new_slot = doctor.schedule[new_selection - 1]
                            break
                        else:
                            print("Please select a valid slot number.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")

                new_date, new_time = new_slot.split(" ", 1)

                # Free up old slot
                doctor.schedule.append(f"{appointment.date} {appointment.time}")
                doctor.schedule.remove(new_slot)

                # Update appointment
                appointment.date = new_date
                appointment.time = new_time

                print(f"Appointment {appointment_id} rescheduled successfully.")
                appointment.view_profile()
                return

            if not found:
                print("Appointment not found.")
    # Generate Bill to patient
    # ----------------------------------------------------------------------------------------------------------------



    def generate_bill(self):
        console.print("\n[bold cyan]--- Generate Bill ---[/bold cyan]")
        appointment_id = input("Enter appointment ID: ")

        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                # Header panel
                console.print(Panel.fit(
                    "🧾 [bold underline]BILL RECEIPT[/bold underline]\nProgramming Techniques General Hospital",
                    border_style="blue",
                    title="Hospital"
                ))

                # Billing table
                bill_table = Table(title="Billing Summary", show_header=False, box=None)
                bill_table.add_column("Item", style="bold", justify="right")
                bill_table.add_column("Details", style="white")

                # Standard details
                bill_table.add_row("Patient:", appointment.patient.name)
                bill_table.add_row("Doctor:", f"Dr. {appointment.doctor.name}")
                bill_table.add_row("Date:", appointment.date)
                bill_table.add_row("Time:", appointment.time)
                bill_table.add_row("Consultation Fee:", "JMD 3000")

                # Extra fees
                try:
                    extra_fees = float(input("Enter extra service fees (tests, meds): JMD "))
                except ValueError:
                    console.print("[bold red]Invalid input. Bill not generated.[/bold red]")
                    return

                total = 3000 + extra_fees
                bill_table.add_row("Extra Services:", f"JMD {extra_fees:,.2f}")
                bill_table.add_row("[bold green]Total:[/bold green]", f"[bold green]JMD {total:,.2f}[/bold green]")

                console.print(bill_table)
                console.print(
                    Panel.fit("[bold green]✅ Payment complete. Thank you![/bold green]", border_style="green"))
                return

        console.print("[bold red]Appointment not found.[/bold red]")

    # Hospital System Menu
    # -----------------------------------------------------------------------------------------------------------------

    def menu(self):
        while True:
            print("\n***** HOSPITAL MANAGEMENT SYSTEM *****")
            print("1. Add Patient")
            print("2. View Patient's profile")
            print("3. Add Doctor")
            print("4. View Doctor's Schedule")
            print("5. Book Appointment")
            print("6. Reschedule Appointment")
            print("7. Cancel Appointment")
            print("8. Generate Bill")
            print("9. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                self.add_patient()
            elif choice == "2":
                self.view_patient_profile()
            elif choice == "3":
                self.add_doctor()
            elif choice == "4":
                self.view_doctor_schedule()
            elif choice == "5":
                self.book_appointment()
            elif choice == "6":
                self.reschedule_appointment()
            elif choice == "7":
                self.cancel_appointment()
            elif choice == "8":
                self.generate_bill()
            elif choice == "9":
                print("Thank you for using our Hospital's system, Goodbye.")
                break
            else:
                print("Invalid choice. Try again.")

# Running the program
# -----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    system = HospitalSystem()
    system.menu()
