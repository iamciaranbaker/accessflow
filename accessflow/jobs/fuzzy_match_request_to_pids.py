from difflib import SequenceMatcher
from accessflow.models.pid import PID, PIDEnvironmentType

class FuzzyMatchRequestToPIDs:
    def __init__(self, logger, session):
        self.logger = logger
        self.session = session

    def run(self, request_id, name, nonprod_pid = None, prod_pid = None):
        matches = {
            "nonprod": {
                "pid": None,
                "confidence": 0
            },
            "prod": {
                "pid": None,
                "confidence": 0
            }
        }

        # Fetch all PIDs
        all_pids = PID.query.all()

        # Step 1: Best PID comment match for the request name
        best_comment_match = None
        best_comment_score = 0
        for pid in all_pids:
            score = self.get_similarity(name, pid.comment)
            if score > best_comment_score:
                best_comment_score = score
                best_comment_match = pid

        # Step 2: Best nonprod PID match
        if nonprod_pid:
            best_np_match = None
            best_np_score = 0
            for pid in all_pids:
                if pid.environment_type == PIDEnvironmentType.NONPROD:
                    name_score = self.get_similarity(nonprod_pid, pid.name)
                    comment_score = self.get_similarity(name, pid.comment)
                    cross_comment_score = self.get_similarity(pid.comment, best_comment_match.comment) if best_comment_match else 0

                    # Weighted confidence
                    combined_score = int((name_score * 0.5) + (comment_score * 0.3) + (cross_comment_score * 0.2))

                    if combined_score > best_np_score:
                        best_np_score = combined_score
                        best_np_match = pid

            if best_np_match:
                matches["nonprod"]["pid"] = best_np_match
                matches["nonprod"]["confidence"] = best_np_score

        # Step 3: Best prod PID match
        if prod_pid:
            best_p_match = None
            best_p_score = 0
            for pid in all_pids:
                if pid.environment_type == PIDEnvironmentType.PROD:
                    name_score = self.get_similarity(prod_pid, pid.name)
                    comment_score = self.get_similarity(name, pid.comment)
                    cross_comment_score = self.get_similarity(pid.comment, best_comment_match.comment) if best_comment_match else 0

                    combined_score = int((name_score * 0.5) + (comment_score * 0.3) + (cross_comment_score * 0.2))

                    if combined_score > best_p_score:
                        best_p_score = combined_score
                        best_p_match = pid

            if best_p_match:
                matches["prod"]["pid"] = best_p_match
                matches["prod"]["confidence"] = best_p_score

        self.logger.info(matches)
    
    # Thank you ChatGPT for this one...
    def get_similarity(self, a, b):
        return int(SequenceMatcher(None, a.strip().lower(), b.strip().lower()).ratio() * 100)