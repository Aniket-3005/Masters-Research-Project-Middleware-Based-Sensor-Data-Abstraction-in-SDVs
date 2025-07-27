#!/bin/bash

cd ~
python3 -m venv kuksa_venv
source ~/kuksa_venv/bin/activate

# Terminal 1 - Start Kuksa Databroker via cargo
gnome-terminal -- bash -c "cd ~/kuksa-databroker; source ~/kuksa_venv/bin/activate; sleep 2; cargo run --bin databroker -- --insecure --metadata ~/kuksa-databroker/data/vss-core/vss_release_4.0.json; exec bash"

# Terminal 2 - Start CLI container
sleep 2
gnome-terminal -- bash -c "source ~/kuksa_venv/bin/activate; sleep 2; docker run -it --rm --network host ghcr.io/eclipse-kuksa/kuksa-databroker-cli:main --server localhost:55555; exec bash"

# Terminal 3 - publisher.py
sleep 2
gnome-terminal -- bash -c "source ~/kuksa_venv/bin/activate; sleep 2; python3 ~/Middleware-abstraction/Laptop/publisher.py; exec bash"

# Terminal 4 - subscriber.py
sleep 2
gnome-terminal -- bash -c "source ~/kuksa_venv/bin/activate; sleep 2; python3 ~/Middleware-abstraction/Laptop/subscriber.py; exec bash"

# Terminal 5 - send_image_to_kuksa.py
sleep 2
gnome-terminal -- bash -c "source ~/kuksa_venv/bin/activate; sleep 2; python3 ~/Middleware-abstraction/Laptop/send_image_to_kuksa.py; exec bash"

# Terminal 6 - detect_from_kuksa.py
sleep 2
gnome-terminal -- bash -c "source ~/kuksa_venv/bin/activate; sleep 2; python3 ~/Middleware-abstraction/Laptop/detect_from_kuksa.py; exec bash"

# Terminal 7 - laptop_sync.py
sleep 2
gnome-terminal -- bash -c "source ~/kuksa_venv/bin/activate; sleep 2; python3 ~/Middleware-abstraction/Laptop/laptop_sync.py; exec bash"

echo "All terminals launched successfully with delays."

