from temporal_stabilizer import TemporalStabilizer

def strict_rule(class_data, class_weights, total_detections):
    if "dog" in class_weights and "cat" in class_weights:
        if class_data["dog"]["total_duration"] > class_data["cat"]["total_duration"]:
            return "dog"
        else:
            return "cat"
    return None

stabilizer = TemporalStabilizer(
    weight_config={"confidence": 0.6, "duration": 0.3, "stability": 0.1},
    prefer_rule=strict_rule,
    verbose=True
)

stabilizer.update(obj_id=1, class_id="dog", confidence=0.8, duration=0.3)
stabilizer.update(obj_id=1, class_id="cat", confidence=0.6, duration=0.2)
stabilizer.update(obj_id=1, class_id="dog", confidence=0.9, duration=0.4)

final = stabilizer.lock_class(1)
print("Final class decision:", final)

stabilizer.reset_all()