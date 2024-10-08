import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "http://127.0.0.1:5000"

# Function to pretty print JSON response
def log_response(response):
    logging.info(f"Status Code: {response.status_code}")
    try:
        logging.info("Response Body:")
        logging.info(json.dumps(response.json(), indent=4))
    except ValueError:
        logging.warning("No JSON response")

# Test: Create a new post
def test_create_post():
    url = f"{BASE_URL}/post"
    data = {
        "content": "This is a test post",
        "user_id": 2
    }
    response = requests.post(url, json=data)
    logging.info("Create Post:")
    log_response(response)
    return response.json().get('post_id')

# Test: Get a post by ID
def test_get_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.get(url)
    logging.info(f"Get Post (ID: {post_id}):")
    log_response(response)

# Test: Update a post by ID
def test_update_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    data = {
        "content": "This is an updated post"
    }
    response = requests.put(url, json=data)
    logging.info(f"Update Post (ID: {post_id}):")
    log_response(response)

# Test: Delete a post by ID
def test_delete_post(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.delete(url)
    logging.info(f"Delete Post (ID: {post_id}):")
    log_response(response)

def main():
    # Step 1: Test creating a post
    post_id = test_create_post()

    # Step 2: Test getting the post
    if post_id:
        test_get_post(post_id)

    # Step 3: Test updating the post
    if post_id:
        test_update_post(post_id)

    # Step 4: Test deleting the post
    if post_id:
        test_delete_post(post_id)

if __name__ == "__main__":
    main()



# Endpoint to add a new post
