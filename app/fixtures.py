FIXTURES = {
    "authentic": {
        "report_id": "mock-authentic-001",
        "clip_id": "mock-clip-001",
        "job_status": "done",
        "verdict": "authentic",
        "authenticity_score": 96,
        "certainty": "high",
        "segments": [],
        "modules": {
            "source": None,
            "audio": None,
            "vision": None,
        },
        "reasons": [
            "No significant manipulation indicators detected."
        ],
        "recommendations": [
            "Verify the original source before publication."
        ],
        "model_version": "mock-v1",
        "error": None,
    },

    "suspicious": {
        "report_id": "mock-suspicious-001",
        "clip_id": "mock-clip-002",
        "job_status": "done",
        "verdict": "suspicious",
        "authenticity_score": 48,
        "certainty": "medium",
        "segments": [
            {
                "start_sec": 5.0,
                "end_sec": 9.5,
                "media_type": "audio",
                "reason": "Mock indicator: unusual audio transition."
            }
        ],
        "modules": {
            "source": None,
            "audio": None,
            "vision": None,
        },
        "reasons": [
            "A potentially unusual audio transition requires review."
        ],
        "recommendations": [
            "Review the flagged segment.",
            "Seek independent source verification."
        ],
        "model_version": "mock-v1",
        "error": None,
    },

    "inconclusive": {
        "report_id": "mock-inconclusive-001",
        "clip_id": "mock-clip-003",
        "job_status": "done",
        "verdict": "inconclusive",
        "authenticity_score": None,
        "certainty": "low",
        "segments": [],
        "modules": {
            "source": None,
            "audio": None,
            "vision": None,
        },
        "reasons": [
            "Insufficient evidence for a reliable assessment."
        ],
        "recommendations": [
            "Obtain a higher-quality copy.",
            "Do not treat this result as a final judgment."
        ],
        "model_version": "mock-v1",
        "error": None,
    },

    "failed": {
        "report_id": "mock-failed-001",
        "clip_id": "mock-clip-004",
        "job_status": "failed",
        "verdict": None,
        "authenticity_score": None,
        "certainty": None,
        "segments": [],
        "modules": {
            "source": None,
            "audio": None,
            "vision": None,
        },
        "reasons": [],
        "recommendations": [],
        "model_version": "mock-v1",
        "error": "Mock processing failure.",
    },
}
