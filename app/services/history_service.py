import json

from ..database import get_connection


def save_recommendation(
    user_id,
    planner,
    budget,
    payload,
    result
):

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO recommendations
        (
            user_id,
            planner,
            budget,
            input_json,
            result_json
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            planner,
            budget,
            json.dumps(payload),
            json.dumps(result)
        )
    )

    connection.commit()

    recommendation_id = cursor.lastrowid

    connection.close()

    return recommendation_id


def get_history(user_id):

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            planner,
            budget,
            input_json,
            result_json,
            created_at
        FROM recommendations
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    history = []

    for row in rows:

        history.append(
            {
                "id": row["id"],
                "planner": row["planner"],
                "budget": row["budget"],
                "input": json.loads(
                    row["input_json"]
                ),
                "result": json.loads(
                    row["result_json"]
                ),
                "created_at": row["created_at"]
            }
        )

    return history