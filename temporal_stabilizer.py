from collections import defaultdict
from typing import Any, Callable


class TemporalStabilizer:
    def __init__(self,
                 weight_config=None,
                 prefer_rule: Callable[[dict, dict, int], Any] = None,
                 verbose=False):
        self.weight_config = weight_config or {
            'confidence': 0.5,
            'duration': 0.3,
            'stability': 0.2
        }
        self.objects = defaultdict(lambda: {'detections': []})
        self.verbose = verbose
        self.prefer_rule = prefer_rule

    def update(self, obj_id, class_id, confidence, duration):
        self.objects[obj_id]['detections'].append({
            'class': class_id,
            'confidence': confidence,
            'duration': duration
        })

    def lock_class(self, obj_id):
        history = self.objects[obj_id]['detections']
        if not history:
            return None

        class_data = defaultdict(lambda: {'confidences': [], 'total_duration': 0, 'count': 0})
        total_duration = 0

        for det in history:
            cls = det['class']
            class_data[cls]['confidences'].append(det['confidence'])
            class_data[cls]['total_duration'] += det['duration']
            class_data[cls]['count'] += 1
            total_duration += det['duration']

        class_weights = {}
        total_detections = len(history)

        for cls, data in class_data.items():
            conf_avg = sum(data['confidences']) / len(data['confidences'])
            duration = data['total_duration']
            freq = data['count'] / total_detections

            weight = (
                conf_avg * self.weight_config['confidence'] +
                duration * self.weight_config['duration'] +
                freq * self.weight_config['stability']
            )
            class_weights[cls] = weight

        if self.prefer_rule:
            preferred = self.prefer_rule(class_data, class_weights, total_detections)
            if preferred is not None:
                if self.verbose:
                    print(f"[PreferRule] Overriding with: {preferred}")
                return preferred

        return max(class_weights, key=class_weights.get)

    def get_history(self, obj_id):
        return self.objects.get(obj_id, None)

    def clear(self, obj_id):
        if obj_id in self.objects:
            del self.objects[obj_id]

    def reset_all(self):
        self.objects.clear()

    def track_summary(self):
        return {
            obj_id: self.lock_class(obj_id)
            for obj_id in self.objects
        }