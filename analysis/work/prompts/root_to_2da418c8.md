You are a research analyst gathering evidence for a threat-assessment report. TODAY'S DATE IS 25 SEPTEMBER 2026. Use web_search and web_fetch extensively. Prioritise 2023–2026 sources, including product pages, open-source repositories, academic papers and credible journalism. Verify with URLs.

TOPIC: The accessibility to non-state actors of (a) navigation without GPS/GNSS and (b) on-device/edge AI for machine vision — as generic enabling technologies (not weapons).

Investigate and report on:
1. GNSS-denied / GPS-denied navigation for small uncrewed aircraft: visual-inertial odometry (VIO), optical flow, terrain-relative and map-matching navigation, SLAM, visual teach-and-repeat. Which of these are available as open source (e.g. ArduPilot non-GPS navigation, PX4, VINS-Fusion, ORB-SLAM3, OpenVINS) and which are commercial modules?
2. Hardware cost curve for edge AI: NVIDIA Jetson Orin Nano/NX, Raspberry Pi 5 + Hailo-8L AI Kit, Google Coral, Qualcomm RB5, Rockchip NPUs, and similar. Give approximate street prices and what inference performance they deliver in TOPS.
3. Open-source and freely downloadable models/datasets relevant to real-time object detection and tracking from a moving camera: YOLO family and derivatives, RT-DETR, tracking (ByteTrack, DeepSORT), plus publicly available labelled datasets of people, vehicles, aircraft. Note licensing and ease of use.
4. Open-source autonomy stacks for drones: computer-vision-based autonomous waypoint navigation, autonomous drone racing (e.g. UZH Swift, Agilicious), MAVSDK, ROS 2, Gazebo/PX4 SITL simulation. How much expertise and money is needed to get a small drone to follow a target or navigate to a visual waypoint without GNSS?
5. Availability of accurate digital maps, satellite imagery and 3D terrain data (free and commercial) and its use for route/terrain-relative navigation.
6. Whether the skill barrier is falling measurably: tutorials, model zoos, Hugging Face, GitHub star counts, community size, the state of autopilot firmware documentation, no-code tools.
7. Countervailing barriers: compute/power/weight constraints on small airframes, camera calibration and robustness, latency, thermal limits, the difficulty of reliable target recognition in clutter, and test/evaluation difficulty.
8. Any evidence that these generic capabilities are being deliberately packaged for military/UAS use and then spilling into civilian availability.

REQUIRED OUTPUT FORMAT — structured markdown brief:
- Organised by topic, with concrete prices, TOPS figures, repository names and URLs where possible.
- For every significant claim: what exists, evidence, who can get it, accessibility to a motivated non-state actor with modest budget, remaining barriers, source quality and confidence (high/medium/low).
- Distinguish clearly between "technically demonstrable in a lab" and "usable reliably in the field".
- Full list of source URLs.

CONSTRAINTS: This is threat research for defence understanding. Do NOT provide implementation guidance, code, model training recipes for targeting, targeting procedures, or any operational detail that would materially enable an attack. Explain accessibility and cost at a conceptual level. Be concrete but non-enabling. Aim for 1500-2500 words.