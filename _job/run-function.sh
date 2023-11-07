# Fix OSX threading issues
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# Set env vars from cloud-functions .env.yaml file
export $(yq e 'to_entries | map(.key + "=" + .value) | join(" ")' .env.yaml)
# Run the function locally
functions-framework --target=generate_inspiration