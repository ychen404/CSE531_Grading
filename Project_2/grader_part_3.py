import json

# Read JSON data from a file
with open('all_events.json', 'r') as file:
    events = json.load(file)

def check_condition(event, customer_requests):
    request_id = event["customer-request-id"]

    if request_id not in customer_requests:
        customer_requests[request_id] = {"last_logical_clock": 0, "propagate_events": []}

    customer_request = customer_requests[request_id]
    current_clock = event["logical_clock"]

    # Check if logical clock is incremental within the same request
    if current_clock < customer_request["last_logical_clock"]:
        return False

    customer_request["last_logical_clock"] = current_clock

    if event["interface"].startswith("propogate"):
        # If the event is a propagate event, store it for later comparison
        customer_request["propagate_events"].append(event)
    else:
        # Check if non-propagate events happen before propagate events
        for propagate_event in customer_request["propagate_events"]:
            if current_clock > propagate_event["logical_clock"]:
                return False

    return True

customer_requests = {}
correct_events = 0
total_events = 0
incorrect_events = 0

for event in events:
    total_events += 1
    if (check_condition(event, customer_requests)):
        correct_events += 1
        print(f"customer-request-id: {event['customer-request-id']} - Condition met (OK)")
    else:
        incorrect_events += 1
        print(f"customer-request-id: {event['customer-request-id']} - Condition not met (Error)")


print("\nSummary:")
print(f"\nTotal Events: {total_events}")
print(f"Correct Events: {correct_events}")
print(f"Incorrect Events: {incorrect_events}")
