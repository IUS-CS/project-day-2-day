from calendar_app.data.profile_model import UserProfile

class ProfileService:
    def __init__(self, profile_repo):
        self.profile_repo = profile_repo

    def get_profile(self, user_id):
        return self.profile_repo.get(user_id)

    def update_profile(self, user_id, data):
        profile = self.profile_repo.get(user_id)
        if not profile:
            # If no profile exists yet, create one
            profile = UserProfile(user_id=user_id)
        
        # Update fields dynamically
        for key, value in data.items():
            setattr(profile, key, value)

        # Save/update in repo
        self.profile_repo.save(profile)
        return profile