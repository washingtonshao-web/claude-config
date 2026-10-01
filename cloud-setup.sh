#!/bin/bash
# Entry point for the cloud environment's setup script:
#   curl -fsSL https://raw.githubusercontent.com/washingtonshao-web/claude-config/main/cloud-setup.sh | bash || true
rm -rf /opt/claude-config
git clone -q --depth 1 https://github.com/washingtonshao-web/claude-config /opt/claude-config && bash /opt/claude-config/cloud/install.sh full
exit 0
