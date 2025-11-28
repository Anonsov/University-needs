from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

AUDIT_LOG: List[str] = []


class AuditMixin:
    def log(self, message: str) -> None:
        AUDIT_LOG.append(message)


@dataclass
class StudentProfile:
    name: str
    group: str
    _gpa: float = 0.0
    _grades: List[int] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)

    def get_grades(self) -> List[int]:
        return self._grades

    def set_gpa(self, value: float) -> None:
        if value < 0 or value > 4.0:
            raise ValueError("GPA out of range")
        self._gpa = value

    @property
    def gpa(self) -> float:
        return self._gpa

    @gpa.setter
    def gpa(self, value: float) -> None:
        self.set_gpa(value)

    def attach_metadata(self, key: str, value: Any) -> None:
        self.meta[key] = value


class GradeBook(AuditMixin):
    _students: Dict[str, StudentProfile] = {}

    def __init__(self, semester: str):
        self.semester = semester
        self.current_student: Optional[StudentProfile] = None

    def get_or_create_student(self, name: str, group: str) -> StudentProfile:
        if name not in self._students:
            self._students[name] = StudentProfile(name=name, group=group)
            self.log(f"[GradeBook] Created student profile for {name}")
        self.current_student = self._students[name]
        return self.current_student

    def add_grade(self, grade: int) -> None:
        if not self.current_student:
            raise RuntimeError("No active student selected")
        self.current_student._grades.append(grade)
        self.log(f"[GradeBook] Added grade {grade} for {self.current_student.name}")

    def get_all_students(self) -> Dict[str, StudentProfile]:
        return self._students

    def override_gpa(self, name: str, new_gpa: float) -> None:
        student = self._students.get(name)
        if not student:
            raise KeyError(name)
        student._gpa = new_gpa
        self.log(f"[GradeBook] GPA for {name} forcefully set to {new_gpa}")

    def get_student_profile(self, name: str) -> Optional[StudentProfile]:
        return self._students.get(name)


class AccessControlledGradeBook(GradeBook):
    def __init__(self, semester: str, access_level: str):
        super().__init__(semester)
        self.access_level = access_level

    def add_grade(self, grade: int) -> None:
        if self.access_level not in ("admin", "teacher"):
            self.log(f"[AccessControlledGradeBook] Denied adding grade {grade}")
            return
        super().add_grade(grade)

    def override_gpa(self, name: str, new_gpa: float) -> None:
        if self.access_level != "admin":
            self.log(f"[AccessControlledGradeBook] Unauthorized GPA override attempt for {name}")
            return
        super().override_gpa(name, new_gpa)

    def print_report(self) -> None:
        for name, student in self._students.items():
            print(f"{name} ({student.group}) -> GPA: {student._gpa}, grades: {student._grades}")


def demo_script():
    gb = AccessControlledGradeBook(semester="Fall 2025", access_level="teacher")

    s1 = gb.get_or_create_student("Ali", "CS-202")
    s2 = gb.get_or_create_student("Laylo", "CS-202")

    gb.current_student = s1
    gb.add_grade(5)
    gb.add_grade(4)

    gb.current_student = s2
    gb.add_grade(3)
    gb.add_grade(5)

    s1._grades.append(1)
    s1._gpa = -10
    s2._grades.clear()

    students = gb.get_all_students()
    students["Ali"] = StudentProfile(name="Hacked", group="XXX")

    gb.print_report()

    print("AUDIT LOG:", AUDIT_LOG)


if __name__ == "__main__":
    demo_script()
