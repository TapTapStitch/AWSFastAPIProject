unauthorized_response = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "examples": {
                    "expired_token": {
                        "summary": "Token has expired",
                        "value": {"detail": "Token has expired"},
                    },
                    "invalid_token": {
                        "summary": "Invalid token",
                        "value": {"detail": "Invalid token"},
                    },
                }
            }
        },
    }
}

not_found_response = {
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "examples": {
                    "post_not_found": {
                        "summary": "Post not found",
                        "value": {"detail": "Post not found"},
                    }
                }
            }
        },
    }
}

bad_request_response = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "no_data_provided": {
                        "summary": "No data provided for update",
                        "value": {"detail": "No data provided for update"},
                    }
                }
            }
        },
    },
}
