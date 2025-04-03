from difflib import SequenceMatcher
from accessflow.models.pid import PID
from accessflow.models.request import Request

class FuzzyMatchRequestToPIDs:
    def __init__(self, logger, session):
        self.logger = logger
        self.session = session

    def run(self, request_id, name, nonprod_pid = None, prod_pid = None):
        request = Request.query.filter(Request.id == request_id).first()
        if not request:
            self.logger.error(f"Could not find request with ID '{request_id}'!")
            raise Exception("Invalid request ID.")

        matches = {
            "nonprod": {
                "pid": None,
                "confidence": 0,
                "alternatives": []
            },
            "prod": {
                "pid": None,
                "confidence": 0,
                "alternatives": []
            }
        }

        # Fetch all PIDs from database
        all_pids = PID.query.all()

        # Step 1: Best PID comment match for request name
        best_comment_match = max(
            all_pids,
            key = lambda pid: self.get_similarity(name, pid.comment),
            default = None
        )

        # Step 2: Match per environment
        for environment_type, input_pid in [("nonprod", nonprod_pid), ("prod", prod_pid)]:
            if not input_pid:
                continue

            candidates = []
            for pid in all_pids:
                if pid.environment_type.value == environment_type:
                    name_score = self.get_similarity(input_pid, pid.name)
                    comment_score = self.get_similarity(name, pid.comment)
                    cross_comment_score = self.get_similarity(pid.comment, best_comment_match.comment) if best_comment_match else 0

                    combined_score = int((name_score * 0.5) + (comment_score * 0.3) + (cross_comment_score * 0.2))
                    candidates.append((pid, combined_score))

            # Sort by best score
            candidates.sort(key = lambda tup: tup[1], reverse = True)

            if candidates:
                best_pid, best_score = candidates[0]
                matches[environment_type]["pid"] = best_pid
                matches[environment_type]["confidence"] = best_score

                # If confidence is below 90%, add alternative PID matches
                if best_score < 90:
                    matches[environment_type]["alternatives"] = [
                        {"pid": alt[0], "confidence": alt[1]}
                        for alt in candidates[1:3]
                    ]

        self.logger.info(matches)

        # Step 3: Add matches to database
        if matches["nonprod"]["pid"]:
            request.add_pid(matches["nonprod"]["pid"].id, matches["nonprod"]["confidence"])
            if "alternatives" in matches["nonprod"] and len(matches["nonprod"]["alternatives"]) > 0:
                for alternative in matches["nonprod"]["alternatives"]:
                    request.add_pid(alternative["pid"].id, alternative["confidence"])

        if matches["prod"]["pid"]:
            request.add_pid(matches["prod"]["pid"].id, matches["prod"]["confidence"])
            if "alternatives" in matches["prod"] and len(matches["prod"]["alternatives"]) > 0:
                for alternative in matches["prod"]["alternatives"]:
                    request.add_pid(alternative["pid"].id, alternative["confidence"])

        self.logger.info(matches)

    # Thank you ChatGPT for this one...
    def get_similarity(self, a, b):
        return int(SequenceMatcher(None, a.strip().lower(), b.strip().lower()).ratio() * 100)