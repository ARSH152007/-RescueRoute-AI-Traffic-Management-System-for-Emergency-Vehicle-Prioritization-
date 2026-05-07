import traci

class EmergencyController:

    def __init__(self):
        self.active_ambulances = set()
        self.total_detected = set()   # ✅ NEW: total tracking (IMPORTANT)

    # ----------------------------
    # DETECT MULTIPLE AMBULANCES
    # ----------------------------
    def detect_emergency(self):
        vehicles = traci.vehicle.getIDList()

        new_ambulances = []

        for v in vehicles:
            try:
                # ✅ BEST METHOD: check vehicle type
                v_type = traci.vehicle.getTypeID(v)

                if v_type == "emergency" and v not in self.active_ambulances:
                    new_ambulances.append(v)
                    self.active_ambulances.add(v)
                    self.total_detected.add(v)   # ✅ COUNT FIX

            except:
                pass

        return new_ambulances

    # ----------------------------
    # GET ROUTE
    # ----------------------------
    def get_route(self, ambulance_id):
        try:
            return list(traci.vehicle.getRoute(ambulance_id))
        except:
            return []

    # ----------------------------
    # GREEN CORRIDOR
    # ----------------------------
    def activate_green_corridor(self, route):
        tls_list = traci.trafficlight.getIDList()

        for edge in route:
            for tls in tls_list:
                try:
                    lanes = traci.trafficlight.getControlledLanes(tls)

                    if any(edge in lane for lane in lanes):
                        state = traci.trafficlight.getRedYellowGreenState(tls)
                        traci.trafficlight.setRedYellowGreenState(
                            tls, "G" * len(state)
                        )
                        print(f"🟢 CORRIDOR GREEN: {tls}")
                        break
                except:
                    pass

    # ----------------------------
    # CLEANUP
    # ----------------------------
    def cleanup(self):
        vehicles = traci.vehicle.getIDList()

        self.active_ambulances = {
            a for a in self.active_ambulances if a in vehicles
        }

    # ----------------------------
    # ✅ GET TOTAL COUNT (NEW)
    # ----------------------------
    def get_total_ambulances(self):
        return len(self.total_detected)