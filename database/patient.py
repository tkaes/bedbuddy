from bson import ObjectId

class Patient:
    def __init__(self, first_name, last_name, dob, bay, bed, priority, presence, color, _id = None):
        self.id = _id # mongoDB _id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.bay = bay
        self.bed = bed
        self.priority = priority
        self.color = color
        self.presence = presence

    def __repr__(self):
        return f"Patient: {self.id}"

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dob": self.dob,
            "bay": self.bay,
            "bed": self.bed,
            "priority": self.priority,
            "color": self.color,
            "presence": self.presence
        }

    @classmethod
    def from_document(cls, doc):
        priority = doc.get("priority", "")
        # assign color based on priority
        if priority.lower() == "high":
            color = "red2"
        elif priority.lower() == "medium":
            color = "yellow"
        elif priority.lower() == "low":
            color = "green"
        else:
            color = "azure"  # fallback

        return cls(
            first_name=doc.get("first_name"),
            last_name=doc.get("last_name"),
            dob=doc.get("dob"),
            bay=doc.get("bay"),
            bed=doc.get("bed"),
            priority=priority,
            color=color,
            presence=doc.get("presence"),
            _id=doc.get("_id")  # store mongoDB _id
        )

    @classmethod
    def empty(cls, bay: int, bed: str):
        return cls(
            first_name="",
            last_name="",
            dob="",
            bay=bay,
            bed=bed,
            priority="",
            color="",
            presence=False,
            _id=None
        )