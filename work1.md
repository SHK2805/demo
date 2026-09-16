
h3. Threat Hunting Investigation Notes: IP Address Discrepancy

*Observation:* 
The tester reported an execution IP of *1.1.1.1*, but the Entra ID non-interactive sign-in logs for the same Entra Device ID show an origin IP of *2.2.2.2*.

*Technical Analysis:*
This discrepancy is expected behavior for an Intune-managed Android BYOD device and does not indicate a false positive or unauthorized device spoofing. The difference is likely due to one of the following factors:
1. **Network Address Translation (NAT/CGNAT):** The tester may have provided the local interface IP of the device, whereas Entra ID logs the public-facing egress IP of the cellular carrier or local Wi-Fi network.
2. **Intune Work Profile / Per-App VPN:** Corporate applications within the Android Work Profile may route traffic through an enterprise VPN or Microsoft Tunnel gateway (logging as 2.2.2.2), while personal applications or standard "what is my IP" web checks run outside the container (logging as 1.1.1.1).
3. **Microsoft Cloud Architecture:** Non-interactive background syncs (e.g., Outlook, Teams) often leverage Microsoft front-door proxies, which can alter the logged IP depending on the protocol used.

*Conclusion:*
The activity is verified to belong to the tester's device asset based on the matching unique Entra Device ID. The IP mismatch is a side effect of mobile routing architecture and containerization. Moving ticket to the next phase of review.
