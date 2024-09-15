import numpy as np

"STRUCTURES DE DONNEES"


class Machine:
    def __init__(self, id, capacities, max_wish, location):
        self.id = id
        self.capacities = capacities
        self.max_wish = max_wish
        self.location = location
        self.current_load = [0] * len(capacities)

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




"FONCTIONS AUXILIAIRES"

def test_new_loc(p, s, machines, services, locs, useLoc, capa_res):
    for m in range(len(machines)):
        l = locs[m]
        if not useLoc[l][s] and test_resources(p, m, processes, capa_res):
            return m
    return -1

def test_all(p, s, machines, useMach, capa_res):
    for m in range(len(machines)):
        if not useMach[m][s] and test_resources(p, m, processes, capa_res):
            return m
    return -1

def test_resources(p, m, processes, capa_res):
    for r in range(len(capa_res[m])):
        if capa_res[m][r] < processes[p][1][r]:
            return False
    return True

def update_resources(p, m, processes, capa_res):
    for r in range(len(capa_res[m])):
        capa_res[m][r] -= processes[p][1][r]

def read_sc_from_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    sc = []
    machine_section = False

    for line in lines:
        line = line.strip()
        if line == "*******Machines*******":
            machine_section = True
            continue
        elif line.startswith("*******") and machine_section:
            break
        
        if machine_section and line:
            parts = line.split()
            if len(parts) > 1:
                # The first part is the machine index, we can ignore it
                machine_data = list(map(int, parts[2:]))  # Skip the first two parts (index and location)
                sc.append(machine_data)

    return sc

# def read_input(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     nbLocalisations = int(lines[0].strip().split()[1])
#     nbRessources = int(lines[1].strip().split()[1])
#     nbMachines = int(lines[2].strip().split()[1])
#     nbProcessus = int(lines[3].strip().split()[1])
#     nbServices = int(lines[4].strip().split()[1])
    
#     machines = []
#     for i in range(nbMachines):
#         data = list(map(int, lines[6 + i].strip().split()))
#         location = data[0]
#         capacities = data[1:1+nbRessources]
#         max_wish = data[1+nbRessources:1+2*nbRessources]
#         machines.append(Machine(i, capacities, max_wish, location))
    
#     service_start = 7 + nbMachines
#     services = []
#     for i in range(nbServices):
#         required_locs = int(lines[service_start + i].strip().split()[0])
#         services.append(Service(i, required_locs))

#     process_start = service_start + nbServices + 1
#     processes = []
#     for i in range(nbProcessus):
#         data = list(map(int, lines[process_start + i].strip().split()))
#         service = data[0]
#         resource_needs = data[1:]
#         processes.append(Process(i, service, resource_needs))

#     return processes, machines, services



def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    nbLocalisations = int(lines[0].strip().split()[1])
    nbRessources = int(lines[1].strip().split()[1])
    nbMachines = int(lines[2].strip().split()[1])
    nbProcessus = int(lines[3].strip().split()[1])
    nbServices = int(lines[4].strip().split()[1])
    
    machines = []
    capacities = []
    sc = []

    for i in range(nbMachines):
        data = list(map(int, lines[6 + i].strip().split()))
        location = data[0]
        capacity = data[1:1 + nbRessources]
        max_wish = data[1 + nbRessources:1 + 2 * nbRessources]
        capacities.append(capacity)
        sc.append(max_wish)
        machines.append(Machine(i, capacity, max_wish, location))
    
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

    return processes, machines, services, sc, capacities, nbProcessus


def write_output(file_path, team_name, instance_number, allocation):
    with open(file_path, 'w') as file:
        file.write(f"{team_name}\n")
        file.write(f"INSTANCE {instance_number}\n")
        file.write(' '.join(map(str, allocation)) + '\n')



# Fonction pour calculer les dépassements
def calculate_excess(assigned_processes, processes, sc, capacities):
    excess = np.zeros_like(capacities)
    remaining_capacity = capacities.copy()

    for m in range(len(assigned_processes)):
        for p in assigned_processes[m]:
            for r in range(len(capacities[m])):
                remaining_capacity[m][r] -= processes[p][1][r]
                if remaining_capacity[m][r] < sc[m][r]:
                    excess[m][r] += sc[m][r] - remaining_capacity[m][r]
                    
    return excess, remaining_capacity

# Fonction d'allocation optimisée
def optimized_allocation(processes, machines, services, sc, capacities):
    assignments = [[] for _ in range(len(machines))]
    excess = np.zeros((len(machines), len(capacities[0])))

    processes_sorted = sorted(range(len(processes)), key=lambda p: sum(processes[p].resource_needs), reverse=True)

    for p in processes_sorted:
        best_machine = None
        min_excess = float('inf')

        for m in range(len(machines)):
            valid_assignment = True
            current_excess = 0

            for r in range(len(capacities[m])):
                if capacities[m][r] < processes[p].resource_needs[r]:
                    valid_assignment = False
                    break

            if valid_assignment:
                for r in range(len(capacities[m])):
                    new_usage = capacities[m][r] - processes[p].resource_needs[r]
                    if new_usage > sc[m][r]:
                        current_excess += new_usage - sc[m][r]

                if current_excess < min_excess:
                    min_excess = current_excess
                    best_machine = m

        if best_machine is not None:
            assignments[best_machine].append(p)
            for r in range(len(capacities[best_machine])):
                capacities[best_machine][r] -= processes[p].resource_needs[r]
                if capacities[best_machine][r] < sc[best_machine][r]:
                    excess[best_machine][r] += sc[best_machine][r] - capacities[best_machine][r]
        else:
            print(f"Impossible d'affecter le processus {p}")
            return None, None

    return assignments, excess

"ALGORITME PRINCIPAL"

def allocate_processes_to_machines(processes, machines, services):
    useLoc = [[False] * len(services) for _ in range(len(machines))]
    useMach = [[False] * len(services) for _ in range(len(machines))]
    
    for service in services:
        service.covered_locs.clear()

    allocation = [-1] * len(processes)
    
    for process in processes:
        service = services[process.service]
        new_loc = False

        if len(service.covered_locs) < service.required_locs:
            machine = testNewLoc(process, machines, service, useLoc)
            if machine:
                service.covered_locs.add(machine.location)
                useLoc[machine.location][service.id] = True
                new_loc = True
        if not new_loc:
            machine = testAll(process, machines, service, useMach)
            if not machine:
                return False, allocation
        updateRessources(process, machine)
        useMach[machine.id][service.id] = True
        allocation[process.id] = machine.id

    return True, allocation



def convert_processes_per_machine_to_machine_per_process(processes_per_machine, total_processes):
    machine_per_process = [-1] * total_processes  # Initialiser le tableau avec des valeurs par défaut

    for machine_id, processes in enumerate(processes_per_machine):
        for process_id in processes:
            machine_per_process[process_id] = machine_id

    return machine_per_process





# Exemple d'utilisation

for i in range(1, 16) :
    file_path = f'data{i}.txt'  # Chemin vers le fichier d'entrée
    team_name = 'EQUIPE G&A'
    instance_number = i
    output_file_path = f'res_{instance_number}.txt'

    processes, machines, services, sc, capacities, nbProcessus = read_input(file_path)
    assignments_1 = optimized_allocation(processes, machines, services, sc, capacities)[0]
    print(assignments_1)
    #assignments = convert_processes_per_machine_to_machine_per_process(assignments_1, nbProcessus)
    #print(assignments)
    #write_output(output_file_path, team_name, instance_number, assignments)
