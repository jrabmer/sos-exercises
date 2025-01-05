import numpy as np
from pathlib import Path


def print_matrix(m):
    for i in m:
        print("".join([f"{j:<8} " for j in i]))


class Instance(object):
    def __init__(self, size, dists, flows):
        self.size = size
        self.dists = np.array(dists)
        self.flows = np.array(flows)

    @classmethod
    def from_filename(cls, path):
        p = Path(path)
        data = [i for i in p.read_text().splitlines() if i != ""]
        size = int(data[0])
        dists = [i.split(" ") for i in data[1 : size + 1]]
        dists = [[float(i) for i in x] for x in dists]

        flow = [i.split(" ") for i in data[size + 1 :]]
        flow = [[float(i) for i in x if i != ""] for x in flow]

        return cls(size, dists, flow)


"""     def print(self):
        print(f"size: {self.size}")
        print("dists:")
        print_matrix(self.dists)
        print("flows:")
        print_matrix(self.flows)
 """


class AntColonyQAP(object):

    def __init__(self, distances, flows, n_ants, n_best, n_iterations, decay, alpha=1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances.
            flows (2D numpy.array): Square matrix of flows.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
        """

        # calculate initial heuristic
        d_vec = [sum(i) for i in distances]
        f_vec = [sum(i) for i in flows]
        self.cost = np.array([[i * j for j in f_vec] for i in d_vec])

        self.size = len(distances)
        self.distances = distances
        self.flows = flows
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        #        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha

    def run(self):
        all_time_best_assignment = ("placeholder", np.inf)

        for i in range(self.n_iterations):
            # let all ants find their path
            assignments = self.gen_assignments()

            # spread pheronomes
            self.spread_pheronome(assignments)

            # find the shortest path taken by an ant
            best_assignment = min(assignments, key=lambda x: x[1])
            print(best_assignment[1])

            if best_assignment[1] < all_time_best_assignment[1]:
                all_time_best_assignment = best_assignment

        return all_time_best_assignment

    def spread_pheronome(self, assignments, q=1):
        # decay all traces
        self.pheromone *= self.decay

        # add traces based on chosen assignments
        for ass in assignments:
            for pairing in ass[0]:
                self.pheromone[pairing] += q / ass[1]

    def calc_ass_cost(self, assignment):
        total_cost = 0

        for i in range(self.size):
            for j in range(self.size):
                total_cost += inst.dists[(i,j)] * inst.flows[(assignment[i][1],assignment[j][1])]
#        for pairing in assignment:
#            total_cost += self.distances[pairing] * self.flows[pairing]
        return total_cost

    def gen_assignments(self):
        assignments = []
        for i in range(self.n_ants):
            assignment = self.ant_walk(0)
            assignments.append((assignment, self.calc_ass_cost(assignment)))
        return assignments

    def ant_walk(self, start_location):
        # list of facilities; first element was assigned to first location, etc.
        assignment = []

        # set of facilities that were already chosen
        chosen_facilities = set()
        chosen_facilities

        # go through all locations, assign every location a facility
        for location in range(self.size):
            facility = self.choose_facility(
                self.pheromone[location], self.cost[location], chosen_facilities
            )

            assignment.append((location, facility))
            chosen_facilities.add(facility)

        return assignment

    def choose_facility(self, pheromone, cost, chosen_facilities):
        pheromone = np.copy(pheromone)

        # calculate probabilites of picking facilities
        probabilities = self.alpha * pheromone + (1 - self.alpha) * cost

        # set probability of picking an already assigned facility to 0
        probabilities[list(chosen_facilities)] = 0

        # normalize probabilities
        probabilities = probabilities / probabilities.sum()

        facility = np.random.choice(range(self.size), p=probabilities)
        return facility




if __name__ == '__main__':
    inst = Instance.from_filename(
    "problem-instances/quadratic-assignment/instances/bur26a.dat"
    )
# inst = Instance(
#    4,
#    [[0, 1, 2, 3], [1, 0, 4, 5], [2, 4, 0, 6], [3, 5, 6, 0]],
#    [[0, 60, 50, 10], [60, 0, 30, 20], [50, 30, 0, 50], [10, 20, 50, 0]],
# )
# inst.print()

    ac = AntColonyQAP(inst.dists, inst.flows, 1, 1, 50, 0.95)
    print(ac.run())