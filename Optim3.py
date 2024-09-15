# ALGO1_modified.py

def testRessources(processus, machine, capa_res):
    for r in range(len(capa_res[0])):
        if capa_res[machine][r] < processus['resources'][r]:
            return False
    return True

def updateRessources(processus, machine, capa_res):
    for r in range(len(capa_res[0])):
        capa_res[machine][r] -= processus['resources'][r]

def calculate_score(machine_resources, sc):
    score = 0
    for m in range(len(machine_resources)):
        for r in range(len(machine_resources[m])):
            excess = max(0, machine_resources[m][r] - sc[m][r])
            score += excess
    return score

def allocate_process(processes, machines, capacities, sc):
    machine_resources = [[0] * len(capacities[0]) for _ in range(len(machines))]
    allocation = [-1] * len(processes)
    capa_res = [cap.copy() for cap in capacities]

    for p in range(len(processes)):
        service = processes[p]['service']
        new_loc = False
        
        # Try to allocate to a new location first
        for m in range(len(machines)):
            if testRessources(processes[p], m, capa_res):
                allocation[p] = m
                updateRessources(processes[p], m, capa_res)
                new_loc = True
                break
        
        if not new_loc:
            for m in range(len(machines)):
                if testRessources(processes[p], m, capa_res):
                    allocation[p] = m
                    updateRessources(processes[p], m, capa_res)
                    break
            else:
                return False, float('inf')  # No valid allocation

    for m in range(len(machines)):
        for r in range(len(machine_resources[m])):
            machine_resources[m][r] = capacities[m][r] - capa_res[m][r]

    return allocation, calculate_score(machine_resources, sc)

def load_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    nbLocalisations = int(lines[0].split()[1])
    nbRessources = int(lines[1].split()[1])
    nbMachines = int(lines[2].split()[1])
    nbProcessus = int(lines[3].split()[1])
    nbServices = int(lines[4].split()[1])
    
    # Skipping to machine data
    machine_start = 6
    capacities = []
    sc = []
    for i in range(nbMachines):
        parts = list(map(int, lines[machine_start + i].split()))
        capacities.append(parts[1:1+nbRessources])
        sc.append(parts[1+nbRessources:1+2*nbRessources])
    
    # Skipping to service data
    service_start = machine_start + nbMachines + 1
    services = []
    for i in range(nbServices):
        services.append(int(lines[service_start + i]))

    # Skipping to process data
    process_start = service_start + nbServices + 1
    processes = []
    for i in range(nbProcessus):
        parts = list(map(int, lines[process_start + i].split()))
        processes.append({'service': parts[0], 'resources': parts[1:]})

    return processes, capacities, sc, services

# Main function to run the allocation and score calculation
def main():
    numero = 8
    filename = f'data{numero}.txt'  # Replace with actual filename if necessary
    processes, capacities, sc, services = load_data(filename)
    machines = list(range(len(capacities)))  # Create a list of machine indices

    allocation, score = allocate_process(processes, machines, capacities, sc)
    
    print("Allocation:", allocation)
    print("Score:", score)

    # Save the results to a file
    with open(f'res_{numero}.txt', 'w') as file:
        file.write("EQUIPE G&A\n")
        file.write(f"INSTANCE {numero}\n")
        file.write(' '.join(map(str, allocation)) + '\n')
        file.write("Score: " + str(score) + '\n')



main()
