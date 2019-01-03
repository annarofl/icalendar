class Student:
    all_students = []

    def __init__(self, name, year, form, form_tutor):
        self.name = name
        self.year = year
        self.form = form
        self.form_tutor = form_tutor
        self.all_students.append(self)

    def __str__(self):
        """
        Return the student data in pre-defined format
        """
        return (
            f"{self.name:8s}: ({self.year},{self.form},{self.form_tutor})"
        )

    def display_info(self):
        for k, v in self.__dict__.items():
            print("{}: {}".format(str(k).title().replace("_", " "), str(v).title()))
        print()


Student("Raheem", 11, "11L", "Mrs Halai")
Student("Phin", 11, "11K", "Mrs Power")
Student("Oliver", 11, "11B", "Mr Rugooba")
Student("Hasnat", 11, "11K", "Mrs Power")

for s in Student.all_students:
    #s.display_info()
    print(s)
