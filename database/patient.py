# Patient class is a standard data container class

PATIENT_PRIORITY_COLORS = {"High": "red", "Medium": "orange", "Low": "green"}

class Patient:
    def __init__(self, first_name, last_name, dob, bay, bed, priority, presence, _id = None):
        self.id = _id # mongoDB _id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.bay = bay
        self.bed = bed
        self.priority = priority
        self.presence = presence

    def __repr__(self):
        return f"Patient: {self.id}"

    # Get color from outlined priority colors
    def get_color(self):
        return PATIENT_PRIORITY_COLORS.get(getattr(self, "priority", "Medium"), "blue")

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dob": self.dob,
            "bay": self.bay,
            "bed": self.bed,
            "priority": self.priority,
            "presence": self.presence
        }

    @classmethod
    def from_document(cls, doc):
        return cls(
            first_name=doc.get("first_name"),
            last_name=doc.get("last_name"),
            dob=doc.get("dob"),
            bay=doc.get("bay"),
            bed=doc.get("bed"),
            priority=doc.get("priority"),
            presence=doc.get("presence"),
            _id=doc.get("_id")  # store mongoDB _id
        )

    # True empty object
    @classmethod
    def empty(cls, bay: int, bed: int):
        return cls(
            first_name="",
            last_name="",
            dob="",
            bay=bay,
            bed=bed,
            priority="",
            presence=False,
            _id=None
        )

    # Empty copy of patient that maintains id field
    def empty_copy(self):
        return Patient(
            first_name="",
            last_name="",
            dob="",
            bay=self.bay,
            bed=self.bed,
            priority="",
            presence=False,
            _id=self.id
        )