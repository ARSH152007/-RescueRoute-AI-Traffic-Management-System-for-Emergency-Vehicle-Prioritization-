import traci

waiting_times = []
step_count = 0

def update_metrics():
    global step_count
    vehicles = traci.vehicle.getIDList()

    total_wait = 0

    for v in vehicles:
        total_wait += traci.vehicle.getWaitingTime(v)

    if len(vehicles) > 0:
        avg = total_wait / len(vehicles)
        waiting_times.append(avg)

    step_count += 1

def get_results():
    if len(waiting_times) == 0:
        return 0
    return sum(waiting_times) / len(waiting_times)

def get_all_data():
    return waiting_times