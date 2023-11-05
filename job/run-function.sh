# Fix OSX threading issues
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# export DRY_RUN=true
# export DATE_OVERRIDE="2023-11-04"

# Set env vars from cloud-functions .env.yaml file
export $(yq e 'to_entries | map(.key + "=" + .value) | join(" ")' .env.yaml)
# Run the function locally
functions-framework --target=generate_inspiration