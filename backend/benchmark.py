import requests
import time
import statistics

# --- Configuration ---
# Make sure this URL matches your running Flask app's query endpoint
API_URL = "http://127.0.0.1:5000/ask"

# Use a variety of questions to test the API
TEST_QUERIES = [
    "What is the purpose of the 'gs' function in the manage_orders.py file?",
    "Explain the database connection logic.",
    "How are user sessions handled?",
    "Summarize the main functionality of the products_dao.py file.",
    "What external libraries are used for payment processing?"
]
# Increase this number for a more accurate average
NUM_REQUESTS = 50


def run_benchmark():
    """Sends a series of requests to the API and measures response times."""
    response_times = []
    print(f"Sending {NUM_REQUESTS} requests to {API_URL}...")

    for i in range(NUM_REQUESTS):
        # Cycle through the test queries to test cache hits and misses
        query = TEST_QUERIES[i % len(TEST_QUERIES)]

        start_time = time.perf_counter()

        try:
            # Assumes your API expects a POST request with a JSON body like {"question": "..."}
            response = requests.post(API_URL, json={"question": query})
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            continue

        end_time = time.perf_counter()
        duration = end_time - start_time
        response_times.append(duration)

        print(
            f"Request {i+1}/{NUM_REQUESTS} | Status: {response.status_code} | Time: {duration:.4f}s")

    if not response_times:
        print("Benchmark failed. No successful requests were made.")
        return None

    # Calculate and print statistics
    avg_time = statistics.mean(response_times)
    print("\n--- Benchmark Results ---")
    print(f"Average response time: {avg_time:.4f} seconds")
    print("-------------------------\n")

    return avg_time


if __name__ == "__main__":
    # You will need to install the requests library: pip install requests
    # Ensure your Flask server is running before executing this script.
    print("Starting benchmark...")
    run_benchmark()
