import numpy as np

class Machine:
    def __init__(self, id, capacities, max_wish, location):
        self.id = id
        self.capacities = capacities
        self.max_wish = max_wish
        self.location = location
        self.current_load = [0] * len(capacities)

    def copy(self):
        return Machine(self.id, self.capacities[:], self.max_wish[:], self.location)

class Process:
    def __init__(self, id, service, resource_needs):
        self.id = id
        self.service = service
        self.resource_needs = resource_needs

class Service:
    def __init__(self, id, required_locs):
        self.id = id
        self.required_locs = required_locs
        self.covered_locs = set()

class Allocation:
    def __init__(self, processes, machines, services):
        self.processes = processes
        self.machines = machines
        self.services = services
        self.machine_allocations = [-1] * len(processes)

def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    nbLocalisations = int(lines[0].strip().split()[1])
    nbRessources = int(lines[1].strip().split()[1])
    nbMachines = int(lines[2].strip().split()[1])
    nbProcessus = int(lines[3].strip().split()[1])
    nbServices = int(lines[4].strip().split()[1])
    
    machines = []
    for i in range(nbMachines):
        data = list(map(int, lines[6 + i].strip().split()))
        location = data[0]
        capacities = data[1:1+nbRessources]
        max_wish = data[1+nbRessources:1+2*nbRessources]
        machines.append(Machine(i, capacities, max_wish, location))
    
    service_start = 7 + nbMachines
    services = []
    for i in range(nbServices):
        required_locs = int(lines[service_start + i].strip().split()[0])
        services.append(Service(i, required_locs))

    process_start = service_start + nbServices + 1
    processes = []
    for i in range(nbProcessus):
        data = list(map(int, lines[process_start + i].strip().split()))
        service = data[0]
        resource_needs = data[1:]
        processes.append(Process(i, service, resource_needs))
    
    return nbLocalisations, nbRessources, nbMachines, nbProcessus, nbServices, machines, services, processes

def write_result(file_path, team_name, instance_number, assignments, score):
    with open(file_path, 'w') as file:
        file.write(f"{team_name}\n")
        file.write(f"INSTANCE {instance_number}\n")
        file.write(" ".join(map(str, assignments)) + "\n")
        file.write(f"Score: {score}\n")

def calculate_score(machines):
    score = 0
    for machine in machines:
        for r in range(len(machine.capacities)):
            usage = machine.current_load[r]
            max_usage = machine.max_wish[r]
            score += max(0, usage - max_usage)
    return score

def assign_processus(nbLocalisations, nbRessources, nbMachines, nbProcessus, nbServices, machines, services, processus):
    assignments = [-1] * nbProcessus
    service_locations = {s.id: set() for s in services}

    for p in processus:
        best_machine = None
        best_score = float('inf')

        for m in machines:
            if any(m.current_load[r] + p.resource_needs[r] > m.capacities[r] for r in range(nbRessources)):
                continue

            if p.service in service_locations and m.location in service_locations[p.service]:
                continue
            
            temp_machines = [m.copy() for m in machines]
            for r in range(nbRessources):
                temp_machines[m.id].current_load[r] += p.resource_needs[r]
            
            temp_score = calculate_score(temp_machines)
            if temp_score < best_score:
                best_score = temp_score
                best_machine = m

        if best_machine is not None:
            assignments[p.id] = best_machine.id
            for r in range(nbRessources):
                best_machine.current_load[r] += p.resource_needs[r]
            service_locations[p.service].add(best_machine.location)

    return assignments, calculate_score(machines)

def main():
    for numero in range(1, 16):
        data_file = f'data{numero}.txt'
        result_file = f'res_{numero}.txt'
        team_name = 'EQUIPE G&A'
        instance_number = numero

        nbLocalisations, nbRessources, nbMachines, nbProcessus, nbServices, machines, services, processus = read_input(data_file)
        assignments, score = assign_processus(nbLocalisations, nbRessources, nbMachines, nbProcessus, nbServices, machines, services, processus)
        write_result(result_file, team_name, instance_number, assignments, score)



main()
