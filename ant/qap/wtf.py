import numpy as np
from qap import Instance

inst = Instance.from_filename(
    "problem-instances/quadratic-assignment/instances/bur26a.dat"
)

x = [
    (0, np.int64(22)),
    (1, np.int64(7)),
    (2, np.int64(6)),
    (3, np.int64(17)),
    (4, np.int64(4)),
    (5, np.int64(25)),
    (6, np.int64(11)),
    (7, np.int64(0)),
    (8, np.int64(16)),
    (9, np.int64(9)),
    (10, np.int64(3)),
    (11, np.int64(13)),
    (12, np.int64(8)),
    (13, np.int64(1)),
    (14, np.int64(21)),
    (15, np.int64(20)),
    (16, np.int64(12)),
    (17, np.int64(5)),
    (18, np.int64(14)),
    (19, np.int64(24)),
    (20, np.int64(15)),
    (21, np.int64(18)),
    (22, np.int64(19)),
    (23, np.int64(10)),
    (24, np.int64(23)),
    (25, np.int64(2)),
]

y = [
    (0, 25),
    (1, 14),
    (2, 10),
    (3, 6),
    (4, 3),
    (5, 11),
    (6, 12),
    (7, 1),
    (8, 5),
    (9, 17),
    (10, 0),
    (11, 4),
    (12, 8),
    (13, 20),
    (14, 7),
    (15, 13),
    (16, 2),
    (17, 19),
    (18, 18),
    (19, 24),
    (20, 16),
    (21, 9),
    (22, 15),
    (23, 23),
    (24, 22),
    (25, 21),
]

costA = 0
costB = 0
for i in range(26):
    for j in range(26):
        pass
#        print(inst.dists[(i,j)] * inst.flows[(y[i],y[j])])
        costA += inst.dists[(i,j)] * inst.flows[(y[i][1],y[j][1])]
        costB += inst.dists[(i,j)] * inst.flows[(x[i][1],x[j][1])]

print(costA)
print(costB)
