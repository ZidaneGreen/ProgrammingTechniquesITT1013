# HOSPITAL MANAGEMENT SYSTEM | # Course - ITT103  - Programming techniques
# ========================================================================

# Importing the necessary libraries
# ---------------------------------------------------------------------------------------------------------------------

import random
import string

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
        print("appointments:", self.appointment_list)

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


    def add_patient(self):
        print("\n***** Add new Patient *****")
        name = input("Enter Patient Name: ")
        try:
            age = int(input("Enter Patient Age: "))
        except ValueError:
            print("Invalid age. Must be a number.")
            return

#Using a while loop to ensure that the gender selected is one of what is required

        while True:
            gender = input("Enter Patient Gender (male/female): ").strip().lower()
            if gender in ['male', 'female']:
                break
            else:
                print("Invalid input. Please enter 'male' or 'female'.")

        patient = Patient(name, age, gender, Patient.generate_patient_id(self))

        self.patients[patient.patient_id] = patient

        print(f"Patient {name} added with ID {patient.patient_id}.")

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

    # Booking Appointment in the System
    # -----------------------------------------------------------------------------------------------------------------

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

        date = input("Enter date (YYYY-MM-DD): ")
        time = input("Enter time (e.g., 10:00 AM): ")

        doctor = self.doctors[doctor_id]
        if not doctor.is_available(time):
            print("Doctor is not available at this time.")
            return

        appointment_id = f"A{self.appointment_counter:03}"
        self.appointment_counter += 1

        appointment = Appointment(appointment_id, self.patients[patient_id], doctor, date, time)
        appointment.confirm()
        self.appointments.append(appointment)

        self.patients[patient_id].appointment_list.append(appointment)
        doctor.schedule.remove(time)

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

    # Generate Bill to patient
    # ----------------------------------------------------------------------------------------------------------------

    def generate_bill(self):
        print("\n--- Generate Bill ---")
        appointment_id = input("Enter appointment ID: ")
        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                print("\n***** BILL RECEIPT *****")
                print("Programming Techniques General Hospital")
                print("--------------------------")
                print("Patient:", appointment.patient.name)
                print("Doctor:", appointment.doctor.name)
                print("Date:", appointment.date)
                print("Time:", appointment.time)
                print("--------------------------")
                print("Consultation Fee: JMD 3000")

                try:
                    extra_fees = float(input("Enter extra service fees (tests, meds): JMD "))
                except ValueError:
                    print("Invalid input. Bill not generated.")
                    return

                total = 3000 + extra_fees
                print("Total: JMD", total)
                print("==========================")
                return

        print("Appointment not found.")

    # Hospital System Menu
    # -----------------------------------------------------------------------------------------------------------------

    def menu(self):
        while True:
            print("\n***** HOSPITAL MANAGEMENT SYSTEM *****")
            print("1. Add Patient")
            print("2. Add Doctor")
            print("3. Book Appointment")
            print("4. Cancel Appointment")
            print("5. Generate Bill")
            print("6. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                self.add_patient()
            elif choice == "2":
                self.add_doctor()
            elif choice == "3":
                self.book_appointment()
            elif choice == "4":
                self.cancel_appointment()
            elif choice == "5":
                self.generate_bill()
            elif choice == "6":
                print("Thank you for using our Hospital's system, Goodbye.")
                break
            else:
                print("Invalid choice. Try again.")

# Running the program
# -----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    system = HospitalSystem()
    system.menu()
