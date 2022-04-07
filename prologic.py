import sat_interface

"""
Liars and Truth-tellers I

Amy says, "Bob is a liar." // A⇔¬B
Bob says, "Cal is a liar." // B⇔¬C
Cal says, "Amy and Bob are liars." // C⇔(¬A∧¬B)

¬A∨¬B
B∨A
¬B∨¬C
C∨B
¬C∨¬A
¬C∨¬B
A∨B∨C
"""
los_tt1 = ["~A ~B", "B A", "~B ~C", "C B", "~C ~A", "~C ~B", "A B C"]
players_tt1 = ["A", "~A", "B", "~B", "C", "~C"]

def tt1(los, players):
    sat = sat_interface.KB(los)
    satcheck = sat.is_satisfiable()
    liars = []
    truthers = []

    for player in players:
        if sat.test_literal(player):
            truthers.append(player)
        else:
            liars.append(player)

    return satcheck, truthers, liars


a, b, c = tt1(los_tt1, players_tt1)
print("TT1")
print("SAT CHECK: " + str(a))
print("True: " + str(b))
print("False: " + str(c))
print('\n')

"""
Liars and Truth-tellers II

Amy says, "Cal and I are truthful." // A⇔C∧A
Bob says, "Cal is a liar." // B⇔¬C
Cal says, "Bob speaks the truth or Amy lies." // C⇔(B∨¬A)

A∧C // ~A v A ∧ ~A v ~C v A

¬B∨¬C
C∨B

~CvBv~A
~BvC
AvC

"""
los_tt2 = ["~A A", "~A ~C A", "~B ~C", "C B", "~C B ~A", "~B C", "A C"]
players_tt2 = ["A", "~A", "B", "~B", "C", "~C"]


def tt2(los, players):
    sat = sat_interface.KB(los)
    satcheck = sat.is_satisfiable()
    liars = []
    truthers = []

    for player in players:
        if sat.test_literal(player):
            truthers.append(player)
        else:
            liars.append(player)

    return satcheck, truthers, liars


a, b, c = tt2(los_tt2, players_tt2)
print("TT2")
print("SAT CHECK: " + str(a))
print("True: " + str(b))
print("False: " + str(c))
print('\n')
"""
Liars and Truth-tellers III

Amy says, "Cal is not honest." // A⇔¬C
Bob says, "Amy and Cal never lie." // B⇔A∧C
Cal says, "Bob is correct." // C⇔B

¬A∨¬C
C∨A

~B v A
~A v ~C v B

~C v B
~B v C

"""
los_tt3 = ["~A ~C", "~B A", "~A ~C B", "~C B", "~B C"]
players_tt3 = ["A", "~A", "B", "~B", "C", "~C"]

def tt3(los, players):
    sat = sat_interface.KB(los)
    satcheck = sat.is_satisfiable()
    liars = []
    truthers = []

    for player in players:
        if sat.test_literal(player):
            truthers.append(player)
        else:
            liars.append(player)

    return satcheck, truthers, liars


a, b, c = tt2(los_tt2, players_tt2)
print("TT3")
print("SAT CHECK: " + str(a))
print("True: " + str(b))
print("False: " + str(c))
print('\n')

"""
Robbery and a Salt
The salt has been stolen! Well, it was found that the culprit was either the Caterpillar, 
Bill the Lizard or the Cheshire Cat. The three were tried and made the following statements in court:

CATERPILLAR: Bill the Lizard ate the salt.
BILL THE LIZARD: That is true!
CHESHIRE CAT: I never ate the salt.

As it happened, at least one of them lied and at least one told the truth. Who ate the salt?

¬C ⇔ B // C B . ~B ~C
B ⇔ B // ~B B
CC ⇔ ¬CC // ~CC ~CC . CC CC 

C ⇔ B // ~C B . ~B C
¬B ⇔ B // B B . [~B B]
CC ⇔ ¬CC // [~CC ~ CC] . [CC CC] 

C ⇔ B // [~C B] . [~B C]
B ⇔ B // [~B B]
¬CC ⇔ ¬CC // CC ~CC

C ⇔ B // [~C B] . [~B C]
¬B ⇔ B // [B B] . [~B B]
¬CC ⇔ ¬CC // [CC ~CC]

¬C ⇔ B // [C B] . [~B ~C]
B ⇔ B // [~B B]
¬CC ⇔ ¬CC // [CC ~CC]

¬C ⇔ B // [C B] . [~B ~C]
¬B ⇔ B // [B B] . [~B B]
CC ⇔ ¬CC // [~CC ~CC] . [CC CC] 
"""

los_salt = ["C B", "~B ~C", "~B B", "~A ~A", "A A", "~C B", "~B C", "B B", "A ~A"]
players_salt = ["A", "~A", "B", "~B", "C", "~C"]

def salt(los, players):
    sat = sat_interface.KB(los)
    satcheck = sat.is_satisfiable()
    liars = []
    truthers = []

    for player in players:
        if sat.test_literal(player):
            truthers.append(player)
        else:
            liars.append(player)

    return satcheck, truthers, liars


a, b, c = salt(los_tt2, players_tt2)
print("Salt")
print("SAT CHECK: " + str(a))
print("True: " + str(b))
print("False: " + str(c))
print("Note: C = Caterpillar, A = Cat, B = Lizard, so Caterpillar ate the salt")
print('\n')


"""
An honest name
Three golfers named Tom, Dick, and Harry are walking to the clubhouse.
The first man in line says, "The guy in the middle is Harry."
The man in the middle says, "I’m Dick."
The last man says, "The guy in the middle is Tom."
Tom, the best golfer of the three, always tells the truth.
Dick sometimes tells the truth, while Harry, the worst golfer, never does.

T ⇔ H       // ~T H . ~H T
D ⇔ H v ¬H  // ~D H ~H . ~H D . H D
H ⇔ T v D   // ~H T D . ~T H . ~D H
-----
D ⇔ D v ¬D  // ~D D ~D . ~D D . D D <--- empty clause, problem!
H ⇔ ¬D      // ~H ~D . D H
-----
D ⇔ T v ¬T  // ~D T ~T . ~T D . T D
H ⇔ ¬T      // ~H ~T . T H


===
WRONG: 
T ⇔ H // ~T H . ~H T
D ⇔ H // ~D H . ~H D
T ⇔ ¬H // ~T ~H . H T
H ⇔ ¬H // ~H ~H . H H 
-----
D ⇔ D // ~D D 
D ⇔ ¬D // ~D ~D. D D 
H ⇔ ¬D // H ~D . D H
-----
D ⇔ T // ~D T . ~T D
D ⇔ ¬T // ~D ~T . T D
H ⇔ ¬T // [~H T] . T H
"""

los_golf = ["~T H", "~H T", "~D H ~H", "~H D", "H D", "~H T D", "~T H", "~D H", "~D D ~D", "~D D", "D D", "~H ~D",
            "D H", "~D T ~T", "~T D", "D T", "~H ~T", "T H"]
players_golf = ["T", "~T", "D", "~D", "H", "~H"]

def golf(los, players):
    sat = sat_interface.KB(los)
    satcheck = sat.is_satisfiable()
    liars = []
    truthers = []

    for player in players:
        if sat.test_literal(player):
            truthers.append(player)
        else:
            liars.append(player)

    return satcheck, truthers, liars


a, b, c = golf(los_golf, players_golf)
print("Golf")
print("SAT CHECK: " + str(a))
print("True: " + str(b))
print("False: " + str(c))
print('\n')