# SCABD: Strategically Connecting Analyzed Business Data
# Copyright (C) 2026 michaeljohnsonscabd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
BottyGuard Security
Specialized defense mechanism against automated threats and bot-driven attacks.
"""

class BottyGuard:
    def __init__(self):
        # Optimization: Use a set for O(1) membership lookups and to prevent duplicates
        self.threat_db = set()
        self.protection_active = True

    def monitor_traffic(self, traffic_data):
        """Monitors and filters incoming traffic for bot patterns."""
        # Optimization: Early return if IP is already in the threat database
        if traffic_data.get("ip") in self.threat_db:
            return False

        if "bot_signature" in traffic_data:
            self.block_threat(traffic_data["ip"])
            return False
        return True

    def block_threat(self, threat_ip):
        """Adds a threat to the blocklist."""
        # Only add and log if not already blocked to avoid redundant operations
        if threat_ip not in self.threat_db:
            print(f"BottyGuard: Blocking suspicious threat from {threat_ip}")
            self.threat_db.add(threat_ip)
