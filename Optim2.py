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

def testRessources(process, machine):
    for r in range(len(machine.capacities)):
        if machine.current_load[r] + process.resource_needs[r] > machine.capacities[r]:
            return False
    return True

def updateRessources(process, machine, revert=False):
    multiplier = -1 if revert else 1
    for r in range(len(machine.capacities)):
        machine.current_load[r] += multiplier * process.resource_needs[r]

def calculate_score(machines):
    score = 0
    for machine in machines:
        for r in range(len(machine.capacities)):
            excess = max(0, machine.current_load[r] - machine.max_wish[r])
            score += excess
    return score

def calculate_potential_increase(machine, process):
    potential_increase = 0
    for r in range(len(machine.capacities)):
        new_load = machine.current_load[r] + process.resource_needs[r]
        if new_load > machine.max_wish[r]:
            potential_increase += new_load - machine.max_wish[r]
    return potential_increase

def testNewLoc(process, machines, service, useLoc):
    best_machine = None
    best_increase = float('inf')
    for machine in machines:
        if not useLoc[machine.location][service.id] and testRessources(process, machine):
            current_increase = calculate_potential_increase(machine, process)
            if current_increase < best_increase:
                best_machine = machine
                best_increase = current_increase
    return best_machine

def testAll(process, machines, service, useMach):
    best_machine = None
    best_increase = float('inf')
    for machine in machines:
        if not useMach[machine.id][service.id] and testRessources(process, machine):
            current_increase = calculate_potential_increase(machine, process)
            if current_increase < best_increase:
                best_machine = machine
                best_increase = current_increase
    return best_machine

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
        required_locs = int(lines[service_start + i ].strip())
        services.append(Service(i, required_locs))

    process_start = service_start + nbServices
    processes = []
    for i in range(nbProcessus):
        data = list(map(int, lines[process_start + i + 1].strip().split()))
        service = data[0]
        resource_needs = data[1:]
        processes.append(Process(i, service, resource_needs))

    return processes, machines, services

def write_output(file_path, team_name, instance_number, allocation, score):
    with open(file_path, 'w') as file:
        file.write(f"{team_name}\n")
        file.write(f"{instance_number}\n")
        file.write(f"{score}\n")
        file.write(' '.join(map(str, allocation)) + '\n')

# Exemple d'utilisation
file_path = 'data1.txt'  # Chemin vers le fichier d'entrée
team_name = 'EQUIPE G&A'
instance_number = 1
output_file_path = f'res_{instance_number}.txt'

processes, machines, services = read_input(file_path)
success, allocation = allocate_processes_to_machines(processes, machines, services)
if success:
    score = calculate_score(machines)
    write_output(output_file_path, team_name, instance_number, allocation, score)
    print(f"Allocation réussie et fichier de sortie généré avec un score de {score}")
else:
    print("Échec de l'allocation")






# class Machine:
#     def __init__(self, id, capacities, max_wish, location):
#         self.id = id
#         self.capacities = capacities
#         self.max_wish = max_wish
#         self.location = location
#         self.current_load = [0] * len(capacities)

# class Process:
#     def __init__(self, id, service, resource_needs):
#         self.id = id
#         self.service = service
#         self.resource_needs = resource_needs

# class Service:
#     def __init__(self, id, required_locs):
#         self.id = id
#         self.required_locs = required_locs
#         self.covered_locs = set()

# def testRessources(process, machine):
#     for r in range(len(machine.capacities)):
#         if machine.current_load[r] + process.resource_needs[r] > machine.capacities[r]:
#             return False
#     return True

# def updateRessources(process, machine, revert=False):
#     multiplier = -1 if revert else 1
#     for r in range(len(machine.capacities)):
#         machine.current_load[r] += multiplier * process.resource_needs[r]

# def calculate_score(machines):
#     score = 0
#     for machine in machines:
#         for r in range(len(machine.capacities)):
#             excess = max(0, machine.current_load[r] - machine.max_wish[r])
#             score += excess
#     return score

# def testNewLoc(process, machines, service, useLoc):
#     best_machine = None
#     best_increase = float('inf')
#     for machine in machines:
#         if not useLoc[machine.location][service.id] and testRessources(process, machine):
#             current_increase = calculate_potential_increase(machine, process)
#             if current_increase < best_increase:
#                 best_machine = machine
#                 best_increase = current_increase
#     return best_machine

# def testAll(process, machines, service, useMach):
#     best_machine = None
#     best_increase = float('inf')
#     for machine in machines:
#         if not useMach[machine.id][service.id] and testRessources(process, machine):
#             current_increase = calculate_potential_increase(machine, process)
#             if current_increase < best_increase:
#                 best_machine = machine
#                 best_increase = current_increase
#     return best_machine

# def calculate_potential_increase(machine, process):
#     potential_increase = 0
#     for r in range(len(machine.capacities)):
#         new_load = machine.current_load[r] + process.resource_needs[r]
#         if new_load > machine.max_wish[r]:
#             potential_increase += new_load - machine.max_wish[r]
#     return potential_increase

# def allocate_processes_to_machines(processes, machines, services):
#     useLoc = [[False] * len(services) for _ in range(len(machines))]
#     useMach = [[False] * len(services) for _ in range(len(machines))]
    
#     for service in services:
#         service.covered_locs.clear()

#     allocation = [-1] * len(processes)
    
#     for process in processes:
#         service = services[process.service]
#         new_loc = False

#         if len(service.covered_locs) < service.required_locs:
#             machine = testNewLoc(process, machines, service, useLoc)
#             if machine:
#                 service.covered_locs.add(machine.location)
#                 useLoc[machine.location][service.id] = True
#                 new_loc = True
#         if not new_loc:
#             machine = testAll(process, machines, service, useMach)
#             if not machine:
#                 return False, allocation
#         updateRessources(process, machine)
#         useMach[machine.id][service.id] = True
#         allocation[process.id] = machine.id
#     return True, allocation

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

#     process_start = service_start + nbServices
#     processes = []
#     for i in range(nbProcessus):
#         data = list(map(int, lines[process_start + i + 1].strip().split()))
#         service = data[0]
#         resource_needs = data[1:]
#         processes.append(Process(i, service, resource_needs))

#     return processes, machines, services

# def write_output(file_path, team_name, instance_number, allocation):
#     with open(file_path, 'w') as file:
#         file.write(f"{team_name}\n")
#         file.write(f"{instance_number}\n")
#         file.write(' '.join(map(str, allocation)) + '\n')

# # Exemple d'utilisation
# file_path = 'data1.txt'  # Chemin vers le fichier d'entrée
# team_name = 'EQUIPE G&A'
# instance_number = 1
# output_file_path = f'res_{instance_number}.txt'

# processes, machines, services = read_input(file_path)
# success, allocation = allocate_processes_to_machines(processes, machines, services)
# if success:
#     score = calculate_score(machines)
#     write_output(output_file_path, team_name, instance_number, allocation)
#     print("Allocation réussie et fichier de sortie généré")
# else:
#     print("Échec de l'allocation")
