# Time Prioritizer CLI

A command-line tool that prioritizes activities based on available time slots. This tool helps users efficiently schedule their tasks while considering priority levels.

## Features
- **Command-Line Interface (CLI)**: Uses `argparse` for flexibility.
- **JSON Input**: Activities and availability are stored in JSON files for easy customization.
- **Priority-Based Scheduling**: Sorts activities based on High, Medium, and Low priority.
- **Time Slot Parsing**: Handles AM/PM formats and durations accurately.
- **Error Handling**: Detects invalid JSON formats and missing files.

## Installation
Clone this repository and ensure you have Python installed.

```sh
$ git clone https://github.com/your-username/time-prioritizer.git
$ cd time-prioritizer
```

## Usage

1. **Prepare JSON Files**

Create two JSON files for activities and availability.

### Example `activities.json`
```json
[
    {"name": "Complete Record Keeping", "duration": 2, "priority": "High"},
    {"name": "Go to Gym", "duration": 1.5, "priority": "Medium"},
    {"name": "Relax and Unwind", "duration": 1, "priority": "Low"}
]
```

### Example `availability.json`
```json
{
    "Monday": ["7 PM - 9 PM"],
    "Tuesday": ["6 PM - 8:30 PM", "9 PM - 10 PM"],
    "Wednesday": ["7 PM - 9 PM"]
}
```

2. **Run the Script**

```sh
$ python time_prioritizer.py --activities-file activities.json --availability-file availability.json
```

## Output Example
```
📅 Suggested Schedule:
Monday:
  ✅ Suggestion: Complete Record Keeping (2 hrs)
Tuesday:
  ✅ Suggestion: Go to Gym (1.5 hrs)
Wednesday:
  ✅ Suggestion: Relax and Unwind (1 hr)
```

## Contributing
Feel free to fork this repository, make improvements, and submit pull requests.

## License
This project is licensed under the GNU Affero General Public License (GNU AGPL).

