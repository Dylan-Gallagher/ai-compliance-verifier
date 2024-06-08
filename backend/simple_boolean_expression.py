# Why don't I simplify it using basic python

# User Params - pretend they entered these
user_params = {
    "over_1b_params": True,
    "is_open_source":False,
}

# Pretend the boolean expression gets generated by an LLM iteratively
def verify_compliance(user_params_dict):
    return not user_params_dict["over_1b_params"] or user_params_dict["is_open_source"]

first_result = verify_compliance(user_params)
print(f"{first_result=}")   # Outputs False because the user is not compliant

# Pretend the user patterns up and fixes their issues
user_params["is_open_source"] = True

print("Trying again...")
second_result = verify_compliance(user_params)
print(f"{second_result=}")  # Outputs True now

ai_act_section = "Article 12 does not apply to "
