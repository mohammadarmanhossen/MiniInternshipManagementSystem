from abc import ABC, abstractmethod

class Notifiable(ABC):
    @abstractmethod
    def notify(self, message):
        pass


class Certifiable(ABC):
    @abstractmethod
    def generate_certificate(self):
        pass


class User(Notifiable, ABC):
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email

    def notify(self, message):
        print(f"[{self.__class__.__name__} -> {self.name}]: {message}")



class Student(User, Certifiable):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.tasks = []

    def apply(self, internship):
        internship.add_applicant(self)
        self.notify(f"Applied for '{internship.title}' internship.")
        internship.mentor.notify(f"{self.name} applied for '{internship.title}'.")
        internship.org.notify(f"New applicant: {self.name}")

    def submit(self, task):
        task.is_completed = True
        task.feedback = "Submitted Successfully"
        self.notify(f"Task #{task.id} submitted.")
        task.mentor.notify(f"Task #{task.id} submitted by {self.name}")

    def check_certificate(self):
        completed = [t for t in self.tasks if t.is_completed]
        if len(completed) >= 3:
            self.generate_certificate()

    def generate_certificate(self):
        print(f"\n Certificate Awarded to {self.name}! Congratulations!\n")


class Mentor(User):
    def assign_task(self, student, task_id, desc):
        task = Task(task_id, desc, self)
        student.tasks.append(task)
        student.notify(f"New task assigned: '{desc}'")
        task.student = student
        return task

    def review(self, task, feedback):
        task.feedback = feedback
        task.student.notify(f"Task #{task.id} reviewed: {feedback}")
        task.student.check_certificate()


class Organization(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.internships = []
        self.students = []
        self.mentors = []

    def add_student(self, student):
        self.students.append(student)
        self.notify(f"New student added: {student.name}")

    def add_mentor(self, mentor):
        self.mentors.append(mentor)
        self.notify(f"New mentor added: {mentor.name}")

    def create_internship(self, title, duration, mentor):
        internship = Internship(title, duration, mentor, self)
        self.internships.append(internship)
        mentor.notify(f"Assigned as mentor for '{title}' internship.")
        self.notify(f"Internship created: {title}")
        return internship

    def show_details(self):
        print(f"\nOrganization: \n - {self.name}")
        print("Mentors:")
        for m in self.mentors:
            print(f" - {m.name}")
        print("Students:")
        for s in self.students:
            print(f" - {s.name}")
        print("Internships:")
        for i in self.internships:
            print(f" - {i.title} ({i.duration} weeks)")



class Internship:
    def __init__(self, title, duration, mentor, org):
        self.title = title
        self.duration = duration
        self.mentor = mentor
        self.org = org
        self.applicants = []

    def add_applicant(self, student):
        self.applicants.append(student)
        print(f" {student.name} applied for {self.title}")

    def show_applicants(self):
        print(f"\nApplicants for {self.title}:")
        for s in self.applicants:
            print(f" - {s.name}")


class Task:
    def __init__(self, task_id, desc, mentor):
        self.id = task_id
        self.desc = desc
        self.mentor = mentor
        self.is_completed = False
        self.feedback = ""
        self.student = None



def main():
    org = Organization(1, "Dapplesoft", "hr@dapplesoft.com")

    mentor = Mentor(2, "Hanif", "hanif@hanif.com")
    student = Student(3, "Arman", "arman@techcorp.com")

    org.add_mentor(mentor)
    org.add_student(student)

    internship = org.create_internship("Python Developer", 8, mentor)
    student.apply(internship)
    internship.show_applicants()


    t1 = mentor.assign_task(student, 1, "Build API")
    t2 = mentor.assign_task(student, 2, "Design Database")
    t3 = mentor.assign_task(student, 3, "Write Unit Tests")

    student.submit(t1)
    student.submit(t2)
    student.submit(t3)

    mentor.review(t1, "Excellent work!")
    mentor.review(t2, "Great job!")
    mentor.review(t3, "Perfect!")

    org.show_details()

    print("\n Internship Completed!\n")


if __name__ == "__main__":
    main()
