import traci
import json
import os
import sys

from data_logger import log_data
from ai_model import train_model, predict_traffic, get_priority_edge
from metrics import update_metrics, get_results
from rl_agent import TrafficRLAgent
from traffic_manager import TrafficManager
from emergency_controller import EmergencyController

SUMO_CMD = ["sumo-gui", "-c", "sumo/config.sumocfg"]

controller = EmergencyController()
manager = TrafficManager()

# ✅ GET ARGUMENTS FROM UI
STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
MODE = sys.argv[2] if len(sys.argv) > 2 else "AI"


def get_traffic_data():
    return {
        edge: traci.edge.getLastStepVehicleNumber(edge)
        for edge in traci.edge.getIDList()
    }


def apply_green(edge):
    for tls in traci.trafficlight.getIDList():
        try:
            lanes = traci.trafficlight.getControlledLanes(tls)

            if any(edge in lane for lane in lanes):
                state = traci.trafficlight.getRedYellowGreenState(tls)
                traci.trafficlight.setRedYellowGreenState(
                    tls, "G" * len(state)
                )
        except:
            pass


def run():
    traci.start(SUMO_CMD)

    print(f"🚀 Simulation Started | Mode: {MODE} | Steps: {STEPS}")

    model = train_model()
    agent = TrafficRLAgent()

    step = 0
    waiting_times = []
    ambulance_count = 0

    while step < STEPS:
        traci.simulationStep()

        vehicles = traci.vehicle.getIDList()

        update_metrics()

        # =========================
        # 🚑 EMERGENCY SYSTEM
        # =========================
        new_ambulances = controller.detect_emergency()

        if new_ambulances:
            print(f"\n🚑 NEW AMBULANCES: {new_ambulances}")

            for amb in new_ambulances:
                ambulance_count += 1   # ✅ correct counting

                route = controller.get_route(amb)

                print(f"🛣 Route for {amb}: {route}")

                controller.activate_green_corridor(route)

        # cleanup ALWAYS run (important)
        controller.cleanup()

        # =========================
        # 🚫 NORMAL MODE (skip AI)
        # =========================
        if MODE == "NORMAL":
            step += 1
            continue

        # =========================
        # 🤖 AI + RL MODE
        # =========================
        traffic_data = get_traffic_data()
        log_data(traffic_data)

        predicted_data = predict_traffic(model, traffic_data)
        priority_edge = get_priority_edge(predicted_data)

        if priority_edge:
            traffic_count = traffic_data.get(priority_edge, 0)

            state = agent.get_state(traffic_count)
            action = agent.choose_action(state)

            apply_green(priority_edge)

            waiting_time = sum(
                traci.vehicle.getWaitingTime(v) for v in vehicles
            )
            waiting_times.append(waiting_time)

            reward = -waiting_time + (10 - traffic_count)

            next_state = agent.get_state(traffic_count)
            agent.update_q(state, action, reward, next_state)

        step += 1

    # =========================
    # 📊 SAVE RESULTS
    # =========================
    avg_wait = get_results()

    results = {
        "average_waiting_time": float(avg_wait),
        "q_table": agent.q_table.tolist(),
        "waiting_times": waiting_times,
        "ambulances_handled": ambulance_count,
        "mode": MODE,
        "steps": STEPS
    }

    file_path = os.path.join(os.getcwd(), "results.json")

    with open(file_path, "w") as f:
        json.dump(results, f)
        f.flush()

    print(f"✅ Results saved | Ambulances: {ambulance_count}")

    traci.close()


if __name__ == "__main__":
    run()