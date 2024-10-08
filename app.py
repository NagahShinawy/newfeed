from http import HTTPStatus
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from config import Config
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)


# MySQL connection configuration
def get_db_connection():
    try:
        return mysql.connector.connect(
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            host=Config.MYSQL_HOST,
            database=Config.MYSQL_DATABASE,
            port=Config.MYSQL_PORT
        )
    except Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None


@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Ok"})


# Endpoint to add a new post
@app.route('/post', methods=['POST'])
def add_post():
    content = request.json.get('content')
    user_id = request.json.get('user_id')

    if not content or not user_id:
        return jsonify({"message": "Content and user_id are required"}), HTTPStatus.BAD_REQUEST

    try:
        # Use a context manager for the database connection
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Check if the user exists
                cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
                if cursor.fetchone() is None:
                    return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND

                # Insert the new post
                query = "INSERT INTO posts (user_id, content) VALUES (%s, %s)"
                cursor.execute(query, (user_id, content))
                conn.commit()

                # Prepare the response
                return jsonify({
                    "message": "Post created",
                    "post_id": cursor.lastrowid,
                    "content": content  # Include the content in the response
                }), HTTPStatus.CREATED

    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return jsonify({"message": "Failed to create post", "error": str(err)}), HTTPStatus.INTERNAL_SERVER_ERROR

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"message": "An unexpected error occurred"}), HTTPStatus.INTERNAL_SERVER_ERROR



@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    content = request.json.get('content')

    if not content:
        return jsonify({"message": "Content is required"}), HTTPStatus.BAD_REQUEST

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the post exists before attempting to update it
        query = "SELECT id, content FROM posts WHERE id = %s"
        cursor.execute(query, (post_id,))
        post = cursor.fetchone()

        if post is None:
            return jsonify({"message": "Post not found"}), HTTPStatus.NOT_FOUND

        # Update the post content
        query = "UPDATE posts SET content = %s WHERE id = %s"
        cursor.execute(query, (content, post_id))
        conn.commit()

        # Check if any row was actually updated
        if cursor.rowcount == 0:
            return jsonify({"message": "No changes made to the post", "post": {"id": post_id, "content": post[1]}})

        # Return the updated fields in the response
        updated_post = {
            "id": post_id,
            "content": content
        }

        return jsonify({"message": "Post updated", "post": updated_post}), HTTPStatus.OK

    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
        return jsonify({"message": "Failed to update post"}), HTTPStatus.INTERNAL_SERVER_ERROR

    finally:
        cursor.close()
        conn.close()




# Endpoint to delete a post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM posts WHERE id = %s"
        cursor.execute(query, (post_id,))
        post = cursor.fetchone()

        if post:
            query = "DELETE FROM posts WHERE id = %s"
            cursor.execute(query, (post_id,))
            conn.commit()
            return '', HTTPStatus.NO_CONTENT
        else:
            return jsonify({"message": "Post not found"}), HTTPStatus.NOT_FOUND

    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
        return jsonify({"message": "Failed to delete post"}), HTTPStatus.INTERNAL_SERVER_ERROR

    finally:
        cursor.close()
        conn.close()


# Endpoint to get a post by id
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM posts WHERE id = %s"
    cursor.execute(query, (post_id,))
    post = cursor.fetchone()

    if post:
        return jsonify(post), HTTPStatus.OK
    else:
        return jsonify({"message": "Post not found"}), HTTPStatus.NOT_FOUND


# Endpoint to list all posts
@app.route('/posts', methods=['GET'])
def list_posts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM posts"
    cursor.execute(query)
    posts = cursor.fetchall()

    return jsonify(posts), HTTPStatus.OK


if __name__ == '__main__':
    app.run(debug=True)
