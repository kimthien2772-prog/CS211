"""Project 1: Appointments
Kim Huynh, 2026-04-04, CS 211
"""

# credits: project 1 file in canvas, https://peps.python.org/pep-0008/.
from datetime import datetime
from appt import Appt 

class Appt:
    """An appointment has a start time, an end time, and a title.
    The start and end times should be on the same day.
    Usage example:
    appt1 = Appt(datetime(2026, 3, 15, 13, 30),
                 datetime(2026, 3, 15, 15, 30), "Nap")
    appt2 = Appt(datetime(2026, 3, 15, 15, 00),
                 datetime(2026, 3, 15, 16, 00), "Coffee")

    if appt2 > appt1:
        print(f"appt1 '{appt1}' was over when appt2 '{appt2}' started")
    elif appt1.overlaps(appt2):
        print("Oh no, a conflict in the schedule!")
        print(appt1.intersect(appt2))

    Should print:
        Oh no, there is a conflict in the schedule!
        2026-03-15 15:00 15:30 | Early afternoon nap and Coffee break
    """

# 2.1 Appt Class Constructor

appt1 = Appt(datetime(2026, 3, 15, 13, 30),
             datetime(2026, 3, 15, 15, 30),
             "Early afternoon nap")

def __init__(self, start: datetime, finish: datetime, desc: str):
    """An appointment from start time to finish time, with
    description desc.
    Start and finish occur on the same day.
    """
    assert finish > start,\
        f"Period finish ({finish}) must be after start ({start})"
    self.start = start
    self.finish = finish
    self.desc = desc

# 2.2 Magic Functions

def __eq__(self, other: 'Appt') -> bool:
      '''Equality means same time period, ignoring description
      '''
      return self.start == other.start and self.finish == other.finish

def __lt__(self, other: 'Appt') -> bool:
      '''Does this appointment finish before or when other starts?
      '''
      return self.finish <= other.start

def __gt__(self, other: 'Appt') -> bool:
      '''Does this appointment start after or when other finishes?
      '''
      return self.start >= other.finish

# 2.3 Overlapping appointments

def overlaps(self, other: 'Appt') -> bool:
      '''Is there a non-zero overlap between these periods?
      '''
      return not (self < other or self > other)

def intersect(self, other: 'Appt') -> 'Appt':
    '''The overlapping portion of two Appt objects
    '''
    assert self.overlaps(other)

    start = max(self.start, other.start)
    finish = min(self.finish, other.finish)
    desc = f"{self.desc}" and {other.desc}

    return Appt(start, finish, desc)

#2.4 Formatting appointments

def __str__(self) -> str:
    '''The textual format of an appointment is
    yyyy-mm-dd hh:mm hh:mm | description
    Note that this is accurate only if the start and finish
    attributes occur on the same day.
    '''
    date_iso = self.start.date().isoformat()
    start_iso = self.start.time().isoformat(timespec='minutes')
    finish_iso = self.finish.time().isoformat(timespec='minutes')
    return f"{date_iso} {start_iso} {finish_iso} | {self.desc}"

def __repr__(self) -> str:
      return f"Appt({repr(self.start)}, {repr(self.finish)}, \
                {repr(self.desc)})"

# 3. The Agenda Class

class Agenda:
    """An Agenda is a collection of appointments,
    similar to a list.

    Usage:
    appt1 = Appt(datetime(2026, 3, 15, 13, 30),
            datetime(2026, 3, 15, 15, 30),
            "Early afternoon nap")
    appt2 = Appt(datetime(2026, 3, 15, 15, 00),
            datetime(2026, 3, 15, 16, 00),
            "Coffee break")
    agenda = Agenda()
    agenda.append(appt1)
    agenda.append(appt2)
    ag_conflicts = agenda.conflicts()
    if len(ag_conflicts) == 0:
        print(f"Agenda has no conflicts")
    else:
        print(f"In agenda:\n{agenda.text()}")
        print(f"Conflicts:\n {ag_conflicts}")
    Expected output:
    In agenda:
    2026-03-15 13:30 15:30 | Early afternoon nap
    2026-03-15 15:00 16:00 | Coffee break
    Conflicts:
    2026-03-15 15:00 15:30 | Early afternoon nap and Coffee break
    """

    # Constructor
    def __init__(self):
        self.elements = [ ]

# 3.1 Delegation Methods (append, __len__, and __eq__)

def append(self, appt: Appt):
    """Add an appointment to the agenda."""
    self.elements.append(appt)

def __len__(self) -> int:
    """Return the number of appointments in the agenda."""
    return len(self.elements)

def __eq__(self, other: 'Agenda') -> bool:
    """Check equality with another Agenda by comparing elements."""
    return self.elements == other.elements

# 3.2 Formatting an Agenda: __str__ and __repr__

def __str__(self):
    """Each Appt on a separate line"""
    lines = [ str(e) for e in self.elements ]
    return "\n".join(str(e) for e in self.elements)

def __repr__(self) -> str:
    """The constructor does not work this way"""
    return f"Agenda({self.elements})"

# 3.3 Conflicts

def conflicts(self) -> 'Agenda':
    """Returns an agenda consisting of the conflicts
    (overlaps) between appointments in this agenda
    """
    self.sort()
    conflicts = Agenda()

    for i in range(len(self.elements)):
        current = self.elements[i]

        for j in range(i + 1, len(self.elements)):
            other = self.elements[j]

            if other.start >= current.finish:
                break

            if current.overlaps(other):
                conflicts.append(current.intersect(other))

    return conflicts

# 3.1 Sort

def start_time(appt: Appt) -> datetime:
     return appt.start

def sort(self):
     '''Sort agenda by appointment start times'''
     self.elements.sort(key=lambda appt: appt.start)

# 3.2 Finding conflicts

def conflicts(self) -> 'Agenda':
    self.sort()
    conflicts = Agenda()

    for i in range(len(self.elements)):
         current = self.elements[i]

         for j in range(i + 1, len(self.elements)):
              other = self.elements[j]

              if other.start >= current.finish:
                   break
              
              if current.overlaps(other):
                   conflicts.append(current.intersect(other))
    return conflicts
    
# i = current appointment ; j = next apppointment 


if __name__ == "__main__":
    print("Running usage examples")

    appt1 = Appt(datetime(2026, 3, 15, 13, 30),
                 datetime(2026, 3, 15, 15, 30),
                 "Early afternoon nap")

    appt2 = Appt(datetime(2026, 3, 15, 15, 0),
                 datetime(2026, 3, 15, 16, 0),
                 "Coffee break")

    if appt2 > appt1:
        print(f"appt1 '{appt1}' was over when appt2 '{appt2}' started")
    elif appt1.overlaps(appt2):
        print("Oh no, a conflict in the schedule!")
        print(appt1.intersect(appt2))

    agenda = Agenda()
    agenda.append(appt1)
    agenda.append(appt2)

    ag_conflicts = agenda.conflicts()

    if len(ag_conflicts) == 0:
        print("Agenda has no conflicts")
    else:
        print(f"In agenda:\n{agenda}")
        print(f"Conflicts:\n{ag_conflicts}")