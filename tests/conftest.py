import os

from hypothesis import settings

settings.register_profile("easy", max_examples=10)
settings.register_profile("mild", max_examples=100)
settings.register_profile("hard", max_examples=1000)

settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "default"))
