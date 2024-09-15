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

def testRessources(process, machine):
    for r in range(len(machine.capacities)):
        if machine.current_load[r] + process.resource_needs[r] > machine.capacities[r]:
            return False
    return True


def updateRessources(process, machine):
    for r in range(len(machine.capacities)):
        machine.current_load[r] += process.resource_needs[r]



def testNewLoc(process, machines, service, useLoc):
    for machine in machines:
        if not useLoc[machine.location][service.id] and testRessources(process, machine):
            return machine
    return None



def testAll(process, machines, service, useMach):
    for machine in machines:
        if not useMach[machine.id][service.id] and testRessources(process, machine):
            return machine
    return None



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

    return processes, machines, services




def write_output(file_path, team_name, instance_number, allocation):
    with open(file_path, 'w') as file:
        file.write(f"{team_name}\n")
        file.write(f"INSTANCE {instance_number}\n")
        file.write(' '.join(map(str, allocation)) + '\n')


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

# Exemple d'utilisation

for i in range(1, 16) :
    file_path = f'data{i}.txt'  # Chemin vers le fichier d'entrée
    team_name = 'EQUIPE G&A'
    instance_number = i
    output_file_path = f'res_{instance_number}.txt'

    processes, machines, services = read_input(file_path)
    success, allocation = allocate_processes_to_machines(processes, machines, services)
    if success:
        write_output(output_file_path, team_name, instance_number, allocation)
        print("Allocation réussie et fichier de sortie généré")
    else:
        print("Échec de l'allocation")