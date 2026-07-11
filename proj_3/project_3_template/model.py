"""Project 3: Contagion
Kim Huynh, 2026-04-18, CS 211
"""

# credits: MVC pattern slides from class, model.py template, 
# canvas announcement regarding class Wanderer

import mvc  # for Listenable
import enum
import random
import config

from typing import List, Tuple

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.WARN)


class Health(enum.Enum):
    """Each individual is one discrete state of health"""
    vulnerable = enum.auto()
    asymptomatic = enum.auto()
    symptomatic = enum.auto()
    recovered = enum.auto()
    dead = enum.auto()

    def __str__(self) -> str:
        return self.name


class Individual(mvc.Listenable):
    """An individual in the population,
    e.g., a person who might get and spread a disease.
    The 'state' instance variable is public read-only, e.g.,
    listeners can check it.
    """

    def __init__(self, kind: str,
                 region: "Population", row: int, col: int):
        
        super().__init__() # initialize Listenable
        self.kind = kind
        self.region = region
        self.row = row
        self.col = col

        # track how long the individual has been in a state
        self._time_in_state = 0
        self.state = Health.vulnerable
        self.next_state = Health.vulnerable

        self.T_Incubate = config.get_int(kind, "T_Incubate")
        self.P_Transmit = config.get_float(kind, "P_Transmit")
        self.T_Recover = config.get_int(kind, "T_Recover")
        self.P_Death = config.get_float(kind, "P_Death")
        self.P_Greet = config.get_float(kind, "P_Greet")
        self.N_Neighbors = config.get_int(kind, "N_Neighbors")
        self.P_Visit = config.get_float(kind, "P_Visit")
        self.Visit_Dist = config.get_int(kind, "Visit_Dist")

        # precompute neighbors for efficiency
        self.neighbors = region.neighbors(
            num=self.N_Neighbors,
            row=row,
            col=col,
            dist=self.Visit_Dist
        )

    def step(self):
        """Next state"""
        if self.state == Health.asymptomatic:
            if self._time_in_state > self.T_Incubate:
                self.next_state = Health.symptomatic

        if self.state == Health.symptomatic:
            if self._time_in_state > self.T_Recover:
                self.next_state = Health.recovered
            elif random.random() < self.P_Death:
                self.next_state = Health.dead

        # interaction happens every step
        self.social_behavior()

    def social_behavior(self):
        raise NotImplementedError("Social behavior should be implemented in subclasses")

    def tick(self):
        """Time passes"""
        self._time_in_state += 1
        if self.state != self.next_state:
            self.state = self.next_state
            self.notify_all("newstate")   # notify UI / listeners
            self._time_in_state = 0

    def infect(self):
        """Called by another individual spreading germs.
        May also be called on "patient 0" to start simulation.
        """
        if self.state == Health.vulnerable:
            self.next_state = Health.asymptomatic

    def meet(self, other: "Individual"):
        """Two individuals meet.  Either may infect
        the other.
        """
        self.maybe_transmit(other)
        other.maybe_transmit(self)

    def maybe_transmit(self, other: "Individual"):
        # only transmit if contagious and other is vulnerable
        if not self._is_contagious():
            return
        if other.state != Health.vulnerable:
            return
        if random.random() < self.P_Transmit:
            other.infect()

    def _is_contagious(self) -> bool:
        """SARS COVID 19 apparently spreads before
        the individual is symptomatic.
        """
        # infection can spread before symptoms appear
        return (self.state == Health.symptomatic
                or self.state == Health.asymptomatic)

    def hello(self, visitor: "Individual") -> bool:
        """True means 'welcome' and False means 'go away'"""
        raise NotImplementedError("Each class must implement 'hello'")


class Typical(Individual):
    """Typical individual. May visit different neighbors
    each day.
    """
    def __init__(self, region: "Population", row: int, col: int):
        # Much of the constructor has been "factored out" into
        # the abstract base class
        super().__init__("Typical", region, row, col)

    def social_behavior(self):
        """A typical individual visits neighbors at random"""
        # randomly visit one neighbor
        if random.random() < self.P_Visit:
            addr = random.choice(self.neighbors)
            neighbor = self.region.visit(addr)
            if neighbor.hello(self):
                neighbor.meet(self)

    def hello(self, visitor: Individual) -> bool:
        """True means 'welcome' and False means 'go away'"""
        # always accepts visitors
        return True


class Wanderer(Individual):
    """Typical individual. May visit different neighbors
    each day.
    """
    def __init__(self, region: "Population", row: int, col: int):
        # Much of the constructor has been "factored out" into
        # the abstract base class
        super().__init__("Wanderer", region, row, col)

    def social_behavior(self):
        """A typical individual visits neighbors at random"""
        # picks a completely random location in the grid
        if random.random() < self.P_Visit:
            rand_row = random.randint(0, self.region.nrows - 1)
            rand_col = random.randint(0, self.region.ncols - 1)
            neighbor = self.region.visit((rand_row, rand_col))
            if neighbor != self and neighbor.hello(self):
                neighbor.meet(self)

    def hello(self, visitor: Individual) -> bool:
        """True means 'welcome' and False means 'go away'"""
        return True


class AtRisk(Individual):
    """Immunocompromised or elderly.
    Vulnerable and cautious.
    """
    def __init__(self, region: "Population", row: int, col: int):
        # Much of the constructor has been "factored out" into
        # the abstract base class
        super().__init__("AtRisk", region, row, col)
        self.prior_visit = None     # keeps track of repeat visits

    def social_behavior(self):
        """The way an AtRisk individual interacts with neighbors"""
        # visits less frequently
        if random.random() >= self.P_Visit:
            return

        # prefers visiting the same person twice
        if self.prior_visit is None:
            addr = random.choice(self.neighbors)
            neighbor = self.region.visit(addr)
            self.prior_visit = neighbor
        else:
            neighbor = self.prior_visit
            self.prior_visit = None

        if neighbor.hello(self):
            neighbor.meet(self)

    def hello(self, visitor: Individual) -> bool:
        """Accept visits only from the same neighbors I visit"""
        # only accept visits from known neighbors
        visitor_addr = (visitor.row, visitor.col)
        return visitor_addr in self.neighbors


class Population(mvc.Listenable):
    """Simple grid organization of individuals"""

    def __init__(self, rows: int, cols: int):
        super().__init__()
        self.cells = []
        self.nrows = rows
        self.ncols = cols

        # build grid of individuals
        for row_i in range(rows):
            row = []
            for col_i in range(cols):
                row.append(self._random_individual(row_i, col_i))
            self.cells.append(row)

    def _random_individual(self, row: int, col: int) -> "Individual":
        # choose type based on config proportions
        classes = [
            (AtRisk, config.get_float("Grid", "Proportion_AtRisk")),
            (Typical, config.get_float("Grid", "Proportion_Typical")),
            (Wanderer, config.get_float("Grid", "Proportion_Wanderer"))
        ]

        while True:
            for the_class, proportion in classes:
                dice = random.random()
                if dice < proportion:
                    return the_class(self, row, col)

    def seed(self):
        """Patient zero"""
        row = random.randint(0, self.nrows - 1)
        col = random.randint(0, self.ncols - 1)
        self.cells[row][col].infect()
        self.cells[row][col].tick()

    def step(self):
        """Determine next states"""
        # compute next states
        for row in self.cells:
            for cell in row:
                cell.step()

        # apply updates
        for row in self.cells:
            for cell in row:
                cell.tick()

        self.notify_all("timestep")

    def count_in_state(self, state: Health) -> int:
        """How many individuals are currently in state?"""
        # count how many individuals are in a given state
        count = 0
        for row in self.cells:
            for cell in row:
                if cell.state == state:
                    count += 1
        return count

    def neighbors(self, num: int, row: int, col: int, dist: int) -> List[Tuple[int, int]]:
        """Give me addresses of up to num neighbors
        up to dist away from here(Manhattan distance)
        """
        result = []
        count = 0
        attempts = 0

        while count < num:
            attempts += 1
            assert attempts < 1000, f"Can't find {num} neighbors at distance {dist}"

            row_step = random.randint(0 - dist, dist)
            col_step = random.randint(0 - dist, dist)

            row_addr = row + row_step
            col_addr = col + col_step

            # keep within grid bounds
            if row_addr < 0 or row_addr >= self.nrows:
                continue
            if col_addr < 0 or col_addr >= self.ncols:
                continue
            # avoid self and duplicates
            if row_addr == row and col_addr == col:
                continue
            if (row_addr, col_addr) in result:
                continue

            result.append((row_addr, col_addr))
            count += 1

        return result

    def visit(self, address: Tuple[int, int]) -> Individual:
        """Return individual at a given location"""
        row_num, col_num = address
        return self.cells[row_num][col_num]