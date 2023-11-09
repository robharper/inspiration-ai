# Set env vars from cloud-functions .env.yaml file
export $(yq e 'to_entries | map(.key + "=" + .value) | join(" ")' .env.yaml)

# Run the util
python regenerate.py "$1" "$2"