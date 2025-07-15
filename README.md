# TemporalStabilizer

**TemporalStabilizer** is a lightweight Python library designed to stabilize classification decisions over time using weighted temporal logic. It is useful in video analytics, object tracking, or any context where per-frame classification may fluctuate and you want a robust final decision.

## 🧠 Features

- **Temporal memory** per tracked object
- **Weighted fusion** of confidence, duration, and frequency
- **Custom override rules** for domain-specific logic
- **Lightweight and dependency-free** (just standard Python)

## 🚀 Installation

```bash
pip install temporal-stabilizer  # (coming soon)
```
Or clone it:

```bash
git clone https://github.com/your-repo/temporal-stabilizer.git
```

## 📦 Usage Example

```python
from temporal_stabilizer import TemporalStabilizer

stabilizer = TemporalStabilizer(verbose=True)

stabilizer.update(obj_id=101, class_id='cat', confidence=0.75, duration=0.2)
stabilizer.update(obj_id=101, class_id='dog', confidence=0.85, duration=0.4)
stabilizer.update(obj_id=101, class_id='dog', confidence=0.90, duration=0.4)

final = stabilizer.lock_class(101)
print(f"Final class: {final}")

stabilizer.clear(101)
```

## 🔧 Custom Rules (Optional)

```python
def prefer_vehicle_classes(class_data, weights, total):
    if 4 in weights and 3 in weights:
        if class_data[4]['total_duration'] > class_data[3]['total_duration']:
            return 4
        else:
            return 3
    return None

stabilizer = TemporalStabilizer(prefer_rule=prefer_vehicle_classes)
```

## ⚙️ Configuration

You can customize the weights:

```python
TemporalStabilizer(weight_config={
    'confidence': 0.6,
    'duration': 0.3,
    'stability': 0.1
})
```

## 📜 License

MIT License. Free for academic and commercial use.

## 👨‍💻 Author

Developed by Ali A Yehya. Contributions welcome!
