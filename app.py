import json
import os
from datetime import datetime
from flask import Flask, render_template_string, redirect, url_for, request, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import plotly
import plotly.graph_objects as go
from werkzeug.security import generate_password_hash, check_password_hash
import plotly.express as px
from flask import Flask, render_template_string, request, jsonify
import pandas as pd
import plotly.utils

app = Flask(__name__, static_folder="static")
os.makedirs("static", exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ocean.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)

# Load pollution data
df = pd.read_csv("ocean_pollution_data.csv")
oceans = df["Ocean"].tolist()
plastic_pollution = df["Plastic Pollution"].tolist()
chemical_pollution = df["Chemical Pollution"].tolist()
metal_pollution = df["Metal Pollution"].tolist()

# Total Pollution Calculation
total_pollution = [
    plastic_pollution[i] + chemical_pollution[i] + metal_pollution[i]
    for i in range(len(oceans))
]

# Coordinates for Oceans
ocean_coords = {
    "Pacific Ocean": (-140, 0),
    "Atlantic Ocean": (-30, 10),
    "Indian Ocean": (80, -10),
    "Southern Ocean": (0, -65),
    "Arctic Ocean": (0, 80)
}

# Ocean Details (unchanged)
ocean_details = {
    "Pacific Ocean": {
        "description": "The Pacific Ocean is the largest and deepest ocean, covering more area than all landmasses combined.",
        "details": '''
        <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px;">
        <h1 style="text-align: center; color: #1a73e8;">Pacific Ocean</h1>

        <h2 style="color: #1a73e8;">Pacific Ocean Overview</h2>
        <p>The Pacific Ocean is the largest and deepest ocean on Earth, covering about 63 million square miles (165 million square kilometers) — nearly 30% of the Earth's surface. It stretches from the Arctic Ocean in the north to the Southern Ocean in the south and is bordered by Asia and Australia to the west and the Americas to the east.</p>

        <h3 style="color: #1a73e8;">Key Facts and Figures</h3>
        <ul>
            <li><strong>Size:</strong> ~63 million square miles (~165 million km²)</li>
            <li><strong>Depth:</strong> Average depth ~12,080 ft (3,682 m); Maximum depth at Challenger Deep in the Mariana Trench (~36,070 ft or ~10,994 m)</li>
            <li><strong>Volume:</strong> ~710 million cubic kilometers</li>
            <li><strong>Temperature:</strong> Ranges from -1.4°C (29.5°F) near the poles to over 30°C (86°F) in tropical regions</li>
        </ul>

        <h2 style="color: #1a73e8;">Unique Features</h2>
        <ul>
            <li><strong>Mariana Trench</strong> – Deepest part of the ocean (10,994 m)</li>
            <li><strong>Ring of Fire</strong> – Home to over 75% of the world's active volcanoes and frequent earthquakes</li>
            <li><strong>Great Barrier Reef</strong> – Largest coral reef system located off the coast of Australia</li>
            <li><strong>Pacific Garbage Patch</strong> – Massive floating collection of plastic debris between Hawaii and California</li>
        </ul>

        <h2 style="color: #1a73e8;">Ocean's Rarest Gems: Mysterious and Rarest Creatures of Marine Life</h2>

        <!-- Giant Squid: Text on the left, image on the right -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #006400;">🦑Giant Squid (Architeuthis dux)</h3>
                <ul>
                    <li><strong>Size:</strong> Can grow up to 43 feet (13 meters)</li>
                    <li><strong>Depth:</strong> Found at depths of 300–1,000 meters</li>
                    <li><strong>Notable Fact:</strong> Extremely rare and elusive; only a few live specimens have been observed in the wild.</li>
                </ul>
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='giant_squid.jpg') }}" alt="Giant Squid" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
        </div>

        <!-- Megamouth Shark: Text on the right, image on the left -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='megamouth_shark.jpg') }}" alt="Megamouth Shark" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
            <div style="flex: 1;">
                <h3 style="color: #006400;">🦈Megamouth Shark (Megachasma pelagios)</h3>
                <ul>
                    <li><strong>Size:</strong> Up to 18 feet (5.5 meters)</li>
                    <li><strong>Depth:</strong> Typically found at depths of 120–1,500 meters</li>
                    <li><strong>Notable Fact:</strong> Only about 100 confirmed sightings since its discovery in 1976</li>
                </ul>
            </div>
        </div>

        <h2 style="color: #1a73e8;">Extinct Beneath the Waves: How Pollution Erased Marine Species</h2>

        <!-- Megalodon: Text on the left, image on the right -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #006400;">🦈Megalodon (Otodus megalodon)</h3>
                <ul>
                    <li><strong>Time Period:</strong> Lived from ~23 million to 3.6 million years ago (Miocene to Pliocene)</li>
                    <li><strong>Size:</strong> Estimated to grow up to 60 feet (18 meters)</li>
                    <li><strong>Diet:</strong> Fed on whales, large fish, and marine mammals</li>
                    <li><strong>Cause of Extinction:</strong>
                        <ul>
                            <li>Cooling ocean temperatures</li>
                            <li>Decline in prey population</li>
                            <li>Competition with modern great white sharks</li>
                        </ul>
                    </li>
                </ul>
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='megalodon.jpg') }}" alt="Megalodon" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
        </div>

        <!-- Archelon: Text on the right, image on the left -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='archelon.jpg') }}" alt="Archelon" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
            <div style="flex: 1;">
                <h3 style="color: #006400;">🐢Archelon – Giant Sea Turtle</h3>
                <ul>
                    <li><strong>Time Period:</strong> Lived during the Late Cretaceous (~80–66 million years ago)</li>
                    <li><strong>Size:</strong> Shell length up to 13 feet (4 meters)</li>
                    <li><strong>Habitat:</strong> Coastal waters of the Pacific</li>
                    <li><strong>Cause of Extinction:</strong>
                        <ul>
                            <li>Cretaceous–Paleogene extinction event (~66 million years ago)</li>
                            <li>Loss of nesting grounds and food sources</li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>

        <h2 style="color: #1a73e8;">Tides of Destruction: The Worst Ocean Pollution Disasters in History</h2>

        <!-- MV Wakashio Oil Spill: Text on the left, image on the right -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #FF0000;">🚢MV Wakashio Oil Spill (2020)</h3>
                <ul>
                    <li><strong>Location:</strong> Off the coast of Mauritius (Indian Ocean but affected Pacific currents)</li>
                    <li><strong>Magnitude:</strong>
                        <ul>
                            <li>Over 1,000 tons of heavy fuel oil spilled</li>
                        </ul>
                    </li>
                    <li><strong>Cause:</strong>
                        <ul>
                            <li>Japanese bulk carrier MV Wakashio ran aground on a coral reef</li>
                        </ul>
                    </li>
                    <li><strong>Impact:</strong>
                        <ul>
                            <li>Destruction of coral reefs and marine habitats</li>
                            <li>Oil-coated beaches and mangroves</li>
                            <li>Long-term harm to local fishing and tourism industries</li>
                        </ul>
                    </li>
                </ul>
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='wakashio_spill.jpg') }}" alt="MV Wakashio Oil Spill" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
        </div>

        <h2 style="color: #FF0000;">🌍Great Pacific Garbage Patch (Ongoing)</h2>
        <!-- Great Pacific Garbage Patch: Text on the right, image on the left -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='garbage_patch.jpg') }}" alt="Great Pacific Garbage Patch" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
            <div style="flex: 1;">
                <ul>
                    <li><strong>Location:</strong> Central North Pacific (between Hawaii and California)</li>
                    <li><strong>Magnitude:</strong>
                        <ul>
                            <li>Estimated size: Over 1.6 million square kilometers (three times the size of France)</li>
                            <li>Contains 1.8 trillion pieces of plastic</li>
                            <li>Weighs over 80,000 metric tons</li>
                        </ul>
                    </li>
                    <li><strong>Cause:</strong>
                        <ul>
                            <li>Ocean currents trapping plastic waste</li>
                            <li>Global plastic pollution from land and ships</li>
                        </ul>
                    </li>
                    <li><strong>Impact:</strong>
                        <ul>
                            <li>Microplastic ingestion by marine species</li>
                            <li>Disruption of food chains</li>
                            <li>Entanglement of marine animals (whales, turtles, and seabirds)</li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
        '''
    },
    "Atlantic Ocean": {
        "description": "The Atlantic Ocean is the second-largest ocean, known for the Bermuda Triangle and Gulf Stream currents.",
        "details": '''
        <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px;">
        <h1 style="text-align: center; color: #1a73e8;">Atlantic Ocean</h1>

        <h2 style="color: #1a73e8;">Atlantic Ocean Overview</h2>
        <p>The Atlantic Ocean is the second-largest ocean, covering approximately 41 million square miles (106 million square kilometers). It separates the Americas to the west from Europe and Africa to the east.</p>

        <h3 style="color: #1a73e8;">Key Facts and Figures</h3>
        <ul>
            <li><strong>Size:</strong> ~41 million square miles (~106 million km²)</li>
            <li><strong>Depth:</strong> Average depth ~12,254 ft (3,736 m); Maximum depth at the Puerto Rico Trench (~28,232 ft or ~8,605 m)</li>
            <li><strong>Volume:</strong> ~310 million cubic kilometers</li>
            <li><strong>Temperature:</strong> Ranges from -2°C (28.4°F) near the poles to over 30°C (86°F) in tropical regions</li>
        </ul>

        <h2 style="color: #1a73e8;">Unique Features</h2>
        <ul>
            <li><strong>Bermuda Triangle</strong> – A region known for mysterious disappearances of ships and aircraft</li>
            <li><strong>Gulf Stream</strong> – A powerful, warm Atlantic ocean current</li>
            <li><strong>Mid-Atlantic Ridge</strong> – The longest mountain range in the world, mostly underwater</li>
        </ul>

        <h2 style="color: #1a73e8;">Ocean's Rarest Gems: Mysterious and Rarest Creatures of Marine Life</h2>

        <!-- Bluefin Tuna: Text on the left, image on the right -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #006400;">🐠 Atlantic Bluefin Tuna (Thunnus thynnus)</h3>
                <ul>
                    <li><strong>Size:</strong> One of the largest and fastest fish in the ocean</li>
                    <li><strong>Depth:</strong>Known for its incredible migratory behavior</li>
                    <li><strong>Notable Fact:</strong>Heavily overfished, making it a threatened species</li>
                </ul>
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='Bluefin_Tuna.jpg') }}" alt="Bluefin Tuna" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
        </div>

        <!-- North Atlantic Right Whale: Text on the right, image on the left -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='North_ Atlantic_Right_Whale.jpg') }}" alt="North Atlantic Right Whale" sstyle="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
            <div style="flex: 1;">
                <h3 style="color: #006400;">🐋 North Atlantic Right Whale (Eubalaena glacialis)</h3>
                <ul>
                    <li><strong>Size:</strong>One of the most endangered whale species, with fewer than 350 individuals remaining.</li>
                    <li><strong>Depth:</strong>Known for their slow movements and close proximity to shorelines.</li>
                    <li><strong>Notable Fact:</strong>Threatened by ship strikes and entanglement in fishing gear</li>
                </ul>
            </div>
        </div>

        <h2 style="color: #1a73e8;">Extinct Beneath the Waves: How Pollution Erased Marine Species</h2>

        <!-- Xiphactinus: Text on the left, image on the right -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #006400;">🐠 Xiphactinus (Xiphactinus audax)</h3>
                <ul>
                    <li><strong>Time Period:</strong>A large predatory fish, reaching lengths of up to 6 meters (20 feet)</li>
                    <li><strong>Size:</strong>Had sharp teeth and an aggressive hunting style</li>
                    <li><strong>Diet:</strong>Went extinct around 66 million years ago during the Late Cretaceous</li>
                    <li><strong>Cause of Extinction:</strong>
                        <ul>
                            <li>Asteroid Impact – Chicxulub impact caused climate change and food chain collapse</li>
                            <li>Ocean Acidification – Volcanic activity altered ocean chemistry</li>
                            <li>Loss of Prey – Decline of smaller fish reduced food availability</li>
                        </ul>
                    </li>
                </ul>
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='Xiphactinus.jpg') }}" alt="Xiphactinus " style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
        </div>

        <!-- Ammonites: Text on the right, image on the left -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='Ammonites.jpg') }}" alt="Ammonites " style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
            <div style="flex: 1;">
                <h3 style="color: #006400;">🐚 Ammonites (Ammonoidea)</h3>
                <ul>
                    <li><strong>Time Period:</strong>Marine mollusks with coiled, chambered shells</li>
                    <li><strong>Size:</strong>Lived from the Devonian to Cretaceous (~400 to 66 million years ago)</li>
                    <li><strong>Habitat:</strong>Grew from a few cm to over 2 meters (6.5 feet) in diameter</li>
                    <li><strong>Cause of Extinction:</strong>
                        <ul>
                            <li>Ocean Acidification – Increased CO₂ levels weakened their calcium carbonate shells</li>
                            <li>Temperature Drop – Cooling oceans affected their ability to survive and reproduce</li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>

        <h2 style="color: #1a73e8;">Tides of Destruction: The Worst Ocean Pollution Disasters in History</h2>

        <!-- Deepwater Horizon Oil Spill: Text on the left, image on the right -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #FF0000;">🛢 1. Deepwater Horizon Oil Spill (2010)</h3>
                <ul>
                    <li><strong>Location:</strong>Gulf of Mexico (connected to the Atlantic Ocean)</li>
                    <li><strong>Magnitude:</strong>
                        <ul>
                            <li>Over 1,000 tons of heavy fuel oil spilled</li>
                        </ul>
                    </li>
                    <li><strong>Cause:</strong>
                        <ul>
                            <li>Explosion of the Deepwater Horizon drilling rig</li>
                        </ul>
                    </li>
                    <li><strong>Impact:</strong>
                        <ul>
                            <li>Released over 210 million gallons of crude oil</li>
                            <li>Devastated marine life and coastal ecosystems</li>
                            <li>Long-term damage to fish, marine mammals, and seabirds</li>
                        </ul>
                    </li>
                </ul>
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='Deepwater_Horizon_Oil_Spill.jpg') }}" alt="Deepwater Horizon Oil Spill" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
        </div>

        <h2 style="color: #FF0000;">🌐Plastic Pollution Crisis (Ongoing)</h2>
        <!-- North_Atlantic_Gyre_location: Text on the right, image on the left -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='Atlantic_plastic.jpg') }}" alt="North_Atlantic_Gyre_location" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
            <div style="flex: 1;">
                <ul>
                    <li><strong>Location:</strong>North Atlantic Garbage Patch</li>
                    <li><strong>Magnitude:</strong>
                        <ul>
                            <li>North Atlantic Garbage Patch Size: Estimated to cover hundreds of thousands of square kilometers</li>
                            <li>Plastic Accumulation Rate: Over 200,000 tons of plastic waste accumulate annually in the Atlantic</li>
                            <li>Microplastic Concentration: Around 580,000 pieces/km² in some areas of the North Atlantic</li>
                        </ul>
                    </li>
                    <li><strong>Cause:</strong>
                        <ul>
                            <li>Poor Waste Management – Plastic from urban areas and landfills enters rivers and oceans due to improper disposal and lack of recycling</li>
                            <li>Fishing and Shipping Waste – Lost fishing nets, gear, and plastic waste from ships contribute significantly to ocean pollution</li>
                        </ul>
                    </li>
                    <li><strong>Impact:</strong>
                        <ul>
                            <li>Millions of tons of plastic accumulate in ocean gyres</li>
                            <li>Ingestion and entanglement of marine life</li>
                            <li>Microplastics found in fish, birds, and deep-sea organisms</li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
        '''
    },
    "Indian Ocean": {
        "description": "The Indian Ocean is the warmest ocean, playing a crucial role in monsoon weather patterns.",
        "details": '''
        <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px;">
        <h1 style="text-align: center; color: #1a73e8;">Indian Ocean</h1>

        <h2 style="color: #1a73e8;">Indian Ocean Overview</h2>
        <p>The Indian Ocean is the third-largest ocean, covering approximately 27 million square miles (70 million square kilometers). It is bounded by Asia to the north, Africa to the west, and Australia to the east.</p>

        <h3 style="color: #1a73e8;">Key Facts and Figures</h3>
        <ul>
            <li><strong>Size:</strong> ~27 million square miles (~70 million km²)</li>
            <li><strong>Depth:</strong> Average depth ~12,762 ft (3,890 m); Maximum depth at the Java Trench (~24,460 ft or ~7,455 m)</li>
            <li><strong>Volume:</strong> ~264 million cubic kilometers</li>
            <li><strong>Temperature:</strong> Ranges from 22°C (71.6°F) to 28°C (82.4°F) in most regions</li>
        </ul>

        <h2 style="color: #1a73e8;">Unique Features</h2>
        <ul>
            <li><strong>Monsoon System</strong> – Drives seasonal weather patterns in South Asia</li>
            <li><strong>Coral Atolls</strong> – Found in the Maldives and Seychelles</li>
            <li><strong>Underwater Volcanoes</strong> – Active volcanic activity in certain regions</li>
        </ul>

        <h2 style="color: #1a73e8;">Ocean's Rarest Gems: Mysterious and Rarest Creatures of Marine Life</h2>

        <!-- Dugong: Text on the left, image on the right -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #006400;">Dugong (Dugong dugon)</h3>
                <ul>
                    <li><strong>Size:</strong> Can grow up to 13 feet (4 meters)</li>
                    <li><strong>Depth:</strong> Found in shallow coastal waters up to 10 meters</li>
                    <li><strong>Notable Fact:</strong> Known as "sea cows," they are vulnerable due to habitat loss and are rare in many regions.</li>
                </ul>
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='dugong.jpg') }}" alt="Dugong" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
        </div>

        <!-- Coelacanth: Text on the right, image on the left -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='coelacanth.jpg') }}" alt="Coelacanth" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
            <div style="flex: 1;">
                <h3 style="color: #006400;">Coelacanth (Latimeria chalumnae)</h3>
                <ul>
                    <li><strong>Size:</strong> Up to 6.5 feet (2 meters)</li>
                    <li><strong>Depth:</strong> Found at depths of 150–700 meters</li>
                    <li><strong>Notable Fact:</strong> A "living fossil" thought extinct for 66 million years until rediscovered in 1938 off the Comoros Islands.</li>
                </ul>
            </div>
        </div>

        <h2 style="color: #1a73e8;">Extinct Beneath the Waves: How Pollution Erased Marine Species</h2>

        <!-- Plesiosaur: Text on the left, image on the right -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #006400;">Plesiosaur (e.g., Elasmosaurus)</h3>
                <ul>
                    <li><strong>Time Period:</strong> Lived during the Mesozoic era (~200–66 million years ago)</li>
                    <li><strong>Size:</strong> Up to 46 feet (14 meters) with a long neck</li>
                    <li><strong>Diet:</strong> Fed on fish and other marine animals</li>
                    <li><strong>Cause of Extinction:</strong>
                        <ul>
                            <li>Cretaceous–Paleogene extinction event (~66 million years ago)</li>
                            <li>Massive environmental changes</li>
                        </ul>
                    </li>
                </ul>
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='plesiosaur.jpg') }}" alt="Plesiosaur" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
        </div>

        <!-- Megalochelys atlas: Text on the right, image on the left -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='megalochelys.jpg') }}" alt="Megalochelys atlas" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
            <div style="flex: 1;">
                <h3 style="color: #006400;">Megalochelys atlas – Giant Tortoise</h3>
                <ul>
                    <li><strong>Time Period:</strong> Lived during the Pliocene to Pleistocene (~5–0.1 million years ago)</li>
                    <li><strong>Size:</strong> Shell length up to 8 feet (2.5 meters)</li>
                    <li><strong>Habitat:</strong> Coastal plains and possibly nearshore waters of ancient India</li>
                    <li><strong>Cause of Extinction:</strong>
                        <ul>
                            <li>Climate change during the Pleistocene</li>
                            <li>Human hunting and habitat destruction</li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>

        <h2 style="color: #1a73e8;">Tides of Destruction: The Worst Ocean Pollution Disasters in History</h2>

        <!-- Tasman Spirit Oil Spill: Text on the left, image on the right -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #FF0000;">Tasman Spirit Oil Spill (2003)</h3>
                <ul>
                    <li><strong>Location:</strong> Off the coast of Karachi, Pakistan in the northern Indian Ocean</li>
                    <li><strong>Magnitude:</strong>
                        <ul>
                            <li>Over 30,000 tons of crude oil spilled</li>
                        </ul>
                    </li>
                    <li><strong>Cause:</strong>
                        <ul>
                            <li>Greek oil tanker Tasman Spirit ran aground during a storm</li>
                        </ul>
                    </li>
                    <li><strong>Impact:</strong>
                        <ul>
                            <li>Contamination of beaches and coastal ecosystems</li>
                            <li>Death of marine life, including fish and birds</li>
                            <li>Economic losses for local fishing and tourism industries</li>
                        </ul>
                    </li>
                </ul>
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='tasman_spirit_spill.jpg') }}" alt="Tasman Spirit Oil Spill" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
        </div>

        <!-- Indian Ocean Garbage Gyre: Text on the right, image on the left -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='indian_garbage_gyre.jpg') }}" alt="Indian Ocean Garbage Gyre" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
            <div style="flex: 1;">
                <h3 style="color: #FF0000;">Indian Ocean Garbage Gyre (Ongoing)</h3>
                <ul>
                    <li><strong>Location:</strong> Central Indian Ocean</li>
                    <li><strong>Magnitude:</strong>
                        <ul>
                            <li>Estimated to contain millions of tons of plastic debris</li>
                            <li>Smaller than the Pacific Garbage Patch but growing rapidly</li>
                        </ul>
                    </li>
                    <li><strong>Cause:</strong>
                        <ul>
                            <li>Ocean currents trapping plastic waste from rivers and coastal areas</li>
                            <li>Heavy pollution from South Asia and East Africa</li>
                        </ul>
                    </li>
                    <li><strong>Impact:</strong>
                        <ul>
                            <li>Microplastic contamination affecting marine life</li>
                            <li>Threat to coral reefs and endangered species</li>
                            <li>Disruption of fishing communities</li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
        '''
    },
    "Southern Ocean": {
        "description": "The Southern Ocean surrounds Antarctica and is defined by the Antarctic Circumpolar Current.",
        "details": '''
        <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px;">
        <h1 style="text-align: center; color: #1a73e8;">Southern Ocean</h1>

        <h2 style="color: #1a73e8;">Southern Ocean Overview</h2>
        <p>The Southern Ocean is the fourth-largest ocean, covering approximately 7.8 million square miles (20 million square kilometers). It surrounds Antarctica and is characterized by strong winds and currents.</p>

        <h3 style="color: #1a73e8;">Key Facts and Figures</h3>
        <ul>
            <li><strong>Size:</strong> ~7.8 million square miles (~20 million km²)</li>
            <li><strong>Depth:</strong> Average depth ~13,100 ft (4,000 m); Maximum depth at the South Sandwich Trench (~23,737 ft or ~7,235 m)</li>
            <li><strong>Volume:</strong> ~71 million cubic kilometers</li>
            <li><strong>Temperature:</strong> Ranges from -2°C (28.4°F) to 10°C (50°F)</li>
        </ul>

        <h2 style="color: #1a73e8;">Unique Features</h2>
        <ul>
            <li><strong>Antarctic Circumpolar Current</strong> – The world's most powerful ocean current</li>
            <li><strong>Icebergs</strong> – Large icebergs are common in this region</li>
            <li><strong>Penguin Colonies</strong> – Home to large populations of penguins</li>
        </ul>

        <h2 style="color: #1a73e8;">Ocean's Rarest Gems: Mysterious and Rarest Creatures of Marine Life</h2>

        <!-- Icefish: Text on the left, image on the right -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #006400;">🐟 Icefish (Channichthyidae)</h3>
                <ul>
                    <li><strong>Size:</strong> Typically 6–25 inches (15–63 cm)</li>
                    <li><strong>Depth:</strong> Found at depths of 50–1,500 meters</li>
                    <li><strong>Notable Fact:</strong> The only vertebrate group with antifreeze proteins in their blood, allowing them to survive in sub-zero Antarctic waters. They also lack hemoglobin, making their blood appear colorless instead of red.</li>
                </ul>
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='icefish.jpg') }}" alt="icefish" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
        </div>

        <!-- Weddell Seal: Text on the right, image on the left -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='weddell_seal.jpg') }}" alt="Weddell Seal" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
            <div style="flex: 1;">
                <h3 style="color: #006400;">🐋 Weddell Seal (Leptonychotes weddellii)</h3>
                <ul>
                    <li><strong>Size:</strong> Up to 11 feet (3.5 meters), weighing 880–1,300 lbs (400–600 kg)</li>
                    <li><strong>Depth:</strong> Can dive up to 600 meters (1,970 feet)</li>
                    <li><strong>Notable Fact:</strong> Holds the record for the longest dive among seals, staying underwater for over 80 minutes while hunting under Antarctic ice. Their teeth wear down over time from chewing ice to maintain breathing holes.</li>
                </ul>
            </div>
        </div>

        <h2 style="color: #1a73e8;">Extinct Beneath the Waves: How Pollution Erased Marine Species</h2>

        <!-- Colossus Penguin: Text on the left, image on the right -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #006400;">🐧 Palaeeudyptes klekowskii (Colossus Penguin)</h3>
                <ul>
                    <li><strong>Time Period:</strong> Lived around 37 million years ago (Eocene epoch)</li>
                    <li><strong>Size:</strong> Estimated to grow up to 6.5 feet (2 meters) tall and weigh over 250 lbs (115 kg)</li>
                    <li><strong>Diet:</strong> Likely fed on fish, squid, and other marine life</li>
                    <li><strong>Cause of Extinction:</strong>
                        <ul>
                            <li>Climate change and shifting ocean currents</li>
                            <li>Loss of habitat as Antarctica became increasingly ice-covered</li>
                            <li>Possible competition with emerging smaller penguin species</li>
                        </ul>
                    </li>
                </ul>
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='Colossus_Penguin.jpg') }}" alt="Colossus Penguin" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
        </div>

        <!-- Kekenodon onamata: Text on the right, image on the left -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='Kekenodon_onamata.jpg') }}" alt="Kekenodon onamata" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
            <div style="flex: 1;">
                <h3 style="color: #006400;">🐋 Kekenodon onamata</h3>
                <ul>
                    <li><strong>Time Period:</strong>  Lived during the Cretaceous period (~100–66 million years ago)</li>
                    <li><strong>Size:</strong> Exact size unknown, but related species grew up to 10 feet (3 meters)</li>
                    <li><strong>Diet:</strong> Likely fed on fish, squid, and smaller marine reptiles</li>
                    <li><strong>Cause of Extinction:</strong>
                        <ul>
                            <li>Mass extinction event ~66 million years ago (likely caused by an asteroid impact)</li>
                            <li>Drastic climate and oceanic changes</li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>

        <h2 style="color: #1a73e8;">Tides of Destruction: The Worst Ocean Pollution Disasters in History</h2>

        <!-- Soviet Nuclear Waste Dumping: Text on the left, image on the right -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #FF0000;">☢ Soviet Nuclear Waste Dumping (1950s–1980s)</h3>
                <ul>
                    <li><strong>Location:</strong>  Various sites in the Southern Ocean</li>
                    <li><strong>Magnitude:</strong>
                        <ul>
                            <li>Exact amount unknown, but reports suggest significant quantities of radioactive waste were discarded</li>
                        </ul>
                    </li>
                    <li><strong>Cause:</strong>
                        <ul>
                            <li>The Soviet Union allegedly disposed of nuclear waste in the ocean, before stricter international regulations were established</li>
                        </ul>
                    </li>
                    <li><strong>Impact:</strong>
                        <ul>
                            <li>Potential long-term radiation contamination of marine life and ecosystems</li>
                            <li>Increased concerns over Antarctic fisheries and food chain safety</li>
                            <li>Raised global alarm, leading to stricter environmental protections under the London Convention (1972) and the Antarctic Treaty System</li>
                        </ul>
                    </li>
                </ul>
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='Soviet_Nuclear_Waste_Dumping.jpg') }}" alt="Soviet Nuclear Waste Dumping" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
        </div>

        <h2 style="color: #FF0000;">🗑 Microplastic Pollution (Ongoing, Increasing)</h2>
        <!-- Microplastic Pollution: Text on the right, image on the left -->
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="flex: 1; text-align: center;">
                <img src="{{ url_for('static', filename='Microplastic_Pollution.jpg') }}" alt="Microplastic Pollutio" style="width: 100%; max-width: 300px; border-radius: 10px;">
            </div>
            <div style="flex: 1;">
                <ul>
                    <li><strong>Location:</strong>  Entire Southern Ocean</li>
                    <li><strong>Magnitude:</strong>
                        <ul>
                            <li> Trillions of microplastic particles detected, with concentrations rising due to global ocean currents</li>

                        </ul>
                    </li>
                    <li><strong>Cause:</strong>
                        <ul>
                            <li>Breakdown of larger plastic waste from global pollution</li>
                            <li>Waste from research stations, tourism, and fishing activities</li>
                            <li>Ocean currents carrying plastics from other regions into Antarctic waters</li>
                        </ul>
                    </li>
                    <li><strong>Impact:</strong>
                        <ul>
                            <li>Microplastics found in Antarctic krill, affecting the entire marine food chain</li>
                            <li>Potential health risks for seals, whales, and seabirds that ingest contaminated prey</li>
                            <li>Growing concern over long-term ecosystem damage in one of Earth's most pristine environments</li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
        '''
    },
    "Arctic Ocean": {
        "description": "The Arctic Ocean is the smallest and shallowest, covered in sea ice most of the year.",
        "details": '''
        <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px;">
    <h1 style="text-align: center; color: #1a73e8;">Arctic Ocean</h1>

    <h2 style="color: #1a73e8;">Arctic Ocean Overview</h2>
    <p>The Arctic Ocean is the smallest and shallowest ocean, covering approximately 5.4 million square miles (14 million square kilometers). It is mostly covered by sea ice and is home to unique ecosystems.</p>

    <h3 style="color: #1a73e8;">Key Facts and Figures</h3>
    <ul>
        <li><strong>Size:</strong> ~5.4 million square miles (~14 million km²)</li>
        <li><strong>Depth:</strong> Average depth ~3,953 ft (1,205 m); Maximum depth at the Eurasian Basin (~17,881 ft or ~5,450 m)</li>
        <li><strong>Volume:</strong> ~18 million cubic kilometers</li>
        <li><strong>Temperature:</strong> Ranges from -1.8°C (28.8°F) to 5°C (41°F)</li>
    </ul>

    <h2 style="color: #1a73e8;">Unique Features</h2>
    <ul>
        <li><strong>Polar Ice Cap</strong> – Covers most of the ocean year-round</li>
        <li><strong>Arctic Wildlife</strong> – Home to polar bears, walruses, and narwhals</li>
        <li><strong>Midnight Sun</strong> – Continuous daylight during summer months</li>
    </ul>

    <h2 style="color: #1a73e8;">Ocean's Rarest Gems: Mysterious and Rarest Creatures of Marine Life</h2>

    <!-- Narwhal -->
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="flex: 1;">
            <h3 style="color: #006400;">🐟 Narwhal (Monodon monoceros)</h3>
            <ul>
                <li><strong>Size:</strong> Males typically grow 13-18 feet (4-5.5 meters) long, with tusks reaching up to 10 feet (3 meters).</li>
                <li><strong>Habitat & Distribution:</strong> Prefers deep, icy waters and migrates seasonally.</li>
                <li><strong>Notable Fact:</strong> Dives to depths of 5,000 feet (1,500 meters) to hunt for fish, squid, and shrimp.</li>
            </ul>
        </div>
        <div style="flex: 1; text-align: center;">
            <img src="{{ url_for('static', filename='Narwhal.jpg') }}" alt="Narwhal" style="width: 100%; max-width: 300px; border-radius: 10px;">
        </div>
    </div>

    <!-- Polar Bear -->
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="flex: 1; text-align: center;">
            <img src="{{ url_for('static', filename='Polar_Bear.jpg') }}" alt="Polar Bear" style="width: 100%; max-width: 300px; border-radius: 10px;">
        </div>
        <div style="flex: 1;">
            <h3 style="color: #006400;">🐻 Polar Bear (Ursus maritimus)</h3>
            <ul>
                <li><strong>Size:</strong> Males can grow up to 10 feet (3 meters) long and weigh 900-1,600 pounds (400-720 kg).</li>
                <li><strong>Habitat & Distribution:</strong> Prefers sea ice for hunting but can be seen on shorelines.</li>
                <li><strong>Notable Fact:</strong> Faces severe threats from climate change due to melting ice.</li>
            </ul>
        </div>
    </div>

    <h2 style="color: #1a73e8;">Extinct Beneath the Waves: How Pollution Erased Marine Species</h2>

    <!-- Great Auk -->
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="flex: 1;">
            <h3 style="color: #006400;">🦆 Great Auk (Pinguinus impennis)</h3>
            <ul>
                <li><strong>Time Period:</strong> Declared extinct in the mid-19th century due to overhunting.</li>
                <li><strong>Size:</strong> Grew up to 3 feet (90 cm) tall and weighed around 11 pounds (5 kg).</li>
                <li><strong>Cause of Extinction:</strong> Excessive hunting for feathers and food.</li>
            </ul>
        </div>
        <div style="flex: 1; text-align: center;">
            <img src="{{ url_for('static', filename='Great_Auk.jpg') }}" alt="Great Auk" style="width: 100%; max-width: 300px; border-radius: 10px;">
        </div>
    </div>

    <h2 style="color: #FF0000;">Tides of Destruction: The Worst Ocean Pollution Disasters in History</h2>

    <!-- Arctic Ocean Oil Spills -->
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="flex: 1;">
            <h3 style="color: #FF0000;">Arctic Ocean Oil Spills (Multiple Incidents)</h3>
            <ul>
                <li><strong>Location:</strong> Norilsk Diesel Spill (2020)</li>
                <li><strong>Magnitude:</strong> Over 21,000 tons of diesel leaked into the Arctic Ocean.</li>
                <li><strong>Impact:</strong> Devastation of fragile Arctic ecosystems and marine life.</li>
            </ul>
        </div>
        <div style="flex: 1; text-align: center;">
            <img src="{{ url_for('static', filename='Arctic-oil-spill.jpg') }}" alt="Arctic Ocean Oil Spills" style="width: 100%; max-width: 300px; border-radius: 10px;">
        </div>
    </div>

    <h2 style="color: #FF0000;">Arctic Ocean Plastic Pollution (Ongoing)</h2>
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="flex: 1; text-align: center;">
            <img src="{{ url_for('static', filename='haultail.jpg') }}" alt="Arctic Ocean Plastic Pollution" style="width: 100%; max-width: 300px; border-radius: 10px;">
        </div>
        <div style="flex: 1;">
            <ul>
                <li><strong>Location:</strong> Arctic waters, from Canada to Siberia</li>
                <li><strong>Magnitude:</strong> 12,000 microplastic particles per liter found in Arctic sea ice.</li>
                <li><strong>Impact:</strong> Bioaccumulation of toxic chemicals in fish and polar wildlife.</li>
            </ul>
        </div>
    </div>
</div>
        '''
    }
}

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    story = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Story by {self.name}>'

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Feedback {self.rating} stars>'

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<QuizResult {self.name}: {self.score}/10>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactMessage from {self.name}>'

# Create database tables
with app.app_context():
    db.create_all()

# Helper functions for charts
def create_bar_chart():
    fig = px.bar(
        x=oceans, y=total_pollution,
        labels={'x': "Oceans", 'y': "Total Pollution (Metric Tons)"},
        title="Total Pollution Levels in the World's Oceans",
        text=[f"{p:,}" for p in total_pollution],
        color=total_pollution, color_continuous_scale="reds"
    )
    fig.update_traces(
        textposition="outside",
        marker=dict(line=dict(color='black', width=1)))
    fig.update_layout(clickmode='event+select')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
def create_pie_chart(ocean_index=0):
    labels = ["Plastic", "Chemical", "Metal"]
    values = [
        plastic_pollution[ocean_index],
        chemical_pollution[ocean_index],
        metal_pollution[ocean_index]
    ]
    fig = px.pie(
        names=labels, values=values,
        title=f"Pollution Breakdown in {oceans[ocean_index]}",
        color=labels,
        color_discrete_map={"Plastic": "blue", "Chemical": "red", "Metal": "orange"}
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_world_map():
    fig = go.Figure()
    for ocean, (lon, lat) in ocean_coords.items():
        fig.add_trace(go.Scattergeo(
            lon=[lon], lat=[lat],
            text=f'<a href="/ocean/{ocean}" style="color:black;" target="_blank">{ocean}</a>',
            mode='markers+text',
            marker=dict(size=10, color='red'),
            textposition="top center"
        ))
    fig.update_layout(
        width=1200,
        height=700,
        geo=dict(
            showland=True, landcolor="lightgray",
            showocean=True, oceancolor="lightblue",
            projection_type="natural earth",
            center=dict(lon=0, lat=0),
            projection_scale=1
        )
    )
    return fig.to_html(full_html=False)

# Routes
@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>  
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Register</title>
        <style>
        body, html {
            height: 100%;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #002f4b, #007bb5);
            color: white;
        }
        .form-container {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 350px;
            color: black;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            font-size: 14px;
            margin-bottom: 8px;
            display: block;
        }
        input {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #004c70;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
        }
        .error {
            color: red;
            text-align: center;
            margin-bottom: 15px;
        }
        .success {
            color: green;
            text-align: center;
            margin-bottom: 15px;
        }
        p {
            text-align: center;
            font-size: 14px;
        }
        a {
            color: #004c70;
            text-decoration: none;
        }
    </style>
    </head>
    <body>
        <div class="form-container">
            <h1>Create an Account</h1>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="{{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            <form method="POST">
                <label for="first_name">First Name:</label>
                <input type="text" id="first_name" name="first_name" required>
                
                <label for="last_name">Last Name:</label>
                <input type="text" id="last_name" name="last_name" required>
                <label for="email">Email ID:</label>
                <input type="email" id="email" name="email" required>
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
                <label for="confirm_password">Confirm Password:</label>
                <input type="password" id="confirm_password" name="confirm_password" required>
                <button type="submit">Register</button>
            </form>
            <p>Already have an account? <a href="{{ url_for('login') }}">Login here</a></p>
        </div>
    </body>
    </html>
    """
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash("Passwords do not match. Please try again.", "error")
            return render_template_string(html_code)
        
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash("Email or Username already registered. Please try again.", "error")
            return render_template_string(html_code)
        
        hashed_password = generate_password_hash(password)
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template_string(html_code)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <style>
        body, html {
            height: 100%;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #003366, #006699, #0099cc);
            color: white;
            overflow: hidden;
            position: relative;
        }

        /* Water wave animation */
        @keyframes wave {
            0% { transform: translateX(0); }
            50% { transform: translateX(-10px); }
            100% { transform: translateX(0); }
        }

        .wave {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 150px;
            background: url('https://i.imgur.com/VgB7JON.png'); /* Example wave texture */
            opacity: 0.5;
            animation: wave 3s infinite ease-in-out;
        }

        .form-container {
            position: relative;
            background-color: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 350px;
            color: #003366;
            z-index: 1;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            font-size: 14px;
            margin-bottom: 8px;
            display: block;
        }
        input {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #006699;
            border-radius: 5px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #006699;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #004c66;
        }
        .error {
            color: red;
            text-align: center;
            margin-bottom: 15px;
        }
        p {
            text-align: center;
            font-size: 14px;
        }
        a {
            color: #006699;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
    </head>
    <body>
        <div class="form-container">
            <h1>Login to Your Account</h1>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="{{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            <form method="POST">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
                <button type="submit">Login</button>
            </form>
            <p>Don't have an account? <a href="{{ url_for('register') }}">Register here</a></p>
        </div>
    </body>
    </html>
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            flash("Incorrect username or password. Please try again.", "error")
            return render_template_string(login_html_code)
        
        flash("Login successful!", "success")
        return redirect(url_for('dashboard'))
    
    return render_template_string(login_html_code)

@app.route('/dashboard')
def dashboard():
    dashboard_html_code = """
    <!DOCTYPE html>
    <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        body, html {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            background: linear-gradient(to bottom, #002f4b, #00587a, #008891);
            color: #ffffff;
        }

        .navbar {
            background-color: rgba(0, 47, 75, 0.9);
            width: 100%;
            padding: 10px 0;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 10;
            text-align: center;
        }

        .navbar a {
            display: inline-block;
            color: white;
            padding: 14px 20px;
            text-decoration: none;
            font-weight: bold;
        }

        .navbar a:hover {
            background-color: #00a8cc;
            color: black;
        }

        .container {
            text-align: center;
            margin-top: 100px;
            flex-grow: 1;
        }

        .ocean-awareness {
            font-size: 32px;
            font-weight: bold;
            color: #00e6e6;
            margin-bottom: 10px;
        }

        .bold-text {
            font-size: 24px;
            font-weight: bold;
            color: #00d5ff;
            margin-bottom: 30px;
        }

        .description-text {
            font-size: 18px;
            color: #cce7ff;
            margin-bottom: 30px;
            line-height: 1.6;
        }

        .section-title {
            font-size: 26px;
            font-weight: bold;
            color: #00ffcc;
            margin-top: 40px;
            margin-bottom: 15px;
        }

        .section-content {
            font-size: 18px;
            color: #cce7ff;
            line-height: 1.6;
            margin-bottom: 30px;
        }

        .video-container {
            margin-top: 50px;
            margin-bottom: 50px;
            text-align: center;
        }

        .video-container video {
            width: 100%;  /* Reduce width slightly */
            height: 450px;  /* Increase height for better fit */
            max-width: 800px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
            object-fit: cover; /* Ensures video scales properly */
}


        .find-out-more-btn {
            padding: 12px 25px;
            background-color: #0099cc;
            color: white;
            font-size: 18px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            display: inline-block;
            text-align: center;
            transition: background 0.3s ease;
        }

        .find-out-more-btn:hover {
            background-color: #0077b6;
        }
    </style>
</head>
    <body>
        <div class="navbar">
            <a href="{{ url_for('dashboard') }}">Home</a>
            <a href="{{ url_for('ocean_facts') }}">Ocean Facts</a>
            <a href="{{ url_for('ocean_news') }}">Ocean News</a>
            <a href="{{ url_for('contact_us') }}">Contact Us</a>
            <a href="{{ url_for('about_us') }}">About Us</a>
        </div>
        <div class="container">
         <h1 style="color: white;">Ocean Guard: An approach for awareness to clean Ocean</h1>
            <div class="ocean-awareness">
                We are all ocean citizens - are you ocean aware?
            </div>
            <div class="bold-text">
                Oceans Aware: Inform, Inspire, Involve. <br>
                The more you know about the ocean, the more you can do to protect and restore it.
            </div>
            <div class="video-container">
            <video autoplay loop muted>
                <source src="{{ url_for('static', filename='video.mp4') }}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
            <div class="description-text" style="text-align: justify;">
                Oceans Aware is designed to inform, inspire, and involve. It offers information on ocean-related themes, explaining ocean challenges, showcasing possible solutions, and putting the spotlight on organizations involved in ocean protection.
                <br><br>
                It aims to encourage you to delve deeper into ocean-related topics, to inspire you to follow a lifestyle that supports the ocean, to prompt you to get involved in ocean protection, and to find ways to restore the ocean to a state where it is no longer under threat.
                <br><br>
                Simply put: to be an ocean citizen.
            </div>
            <head>
    <style>
        .description-text {
            text-align: justify;
            padding: 20px;
            margin: 20px auto;
            max-width: 1500px;
        }
    </style>
</head>

            <div class="section-title">The Ocean</div>
            <div class="section-content" style="text-align: justify;">
                The ocean covers approximately 360 million square kilometers, about 71% of the Earth's surface. It contains 97% of the Earth's water, which comes to roughly 1.35 billion cubic kilometers of water. The average depth of the ocean is 3,688 meters, its deepest point is at 10,983 meters.
                <br><br>
                95% of the ocean has yet to be explored, 91% of ocean species are yet to be classified, and 75% of the ocean floor remains to be mapped at high definition. Scientists estimate that the species diversity of the ocean lies between 1 and 2 million species, with millions more bacteria, other microbes, and viruses.
                <br><br>
                Ocean habitats vary dramatically, from tropical coral reefs to the freezing poles, from mangroves to the deep sea; each habitat is shaped by its range of light, temperature, depth, pressure, and salinity.
                <br><br>
                The ocean never rests, its movement stems from the Earth's rotation, tides, wind, temperature, and salinity.
                <br><br>
                Ocean water temperature ranges from 30ºC at the surface to -1ºC at the ocean floor. It can reach up to 400ºC at hydrothermal vents, where the intense pressure at these depths keeps the water from boiling.
            </div>
                        <head>
    <style>
        .section-content {
            text-align: justify;
            padding: 20px;
            margin: 20px auto;
            max-width: 1500px;
        }
    </style>
</head>
            <div class="section-title">Its Importance</div>
            <div class="section-content">
                The ocean produces between 50 and 80% of the planet's oxygen, absorbs over 90% of the excess heat caused by climate change, and takes up about 23% of carbon dioxide emissions.
                <br><br>
                If the ocean were a national economy, it would be the seventh largest in the world. The OECD estimates that the annual market value of all marine and coastal resources and industries will reach US$ 3 trillion by 2030. Already back in 2015, the World Wildlife Fund for Nature's report "Reviving the Ocean Economy: The case for action—2015" estimated ocean resources to be worth US$ 24 trillion.
                <br><br>
                More than 3 billion people rely on the ocean for their livelihoods, and more than 350 million jobs are linked to it. Nearly 2.4 billion people, about 40% of the world's population, live within 100 km of the coast.
                <br><br>
                97% of our communications are carried via more than 400 submarine cables extending over 1.2 million kilometers in length. 90% of goods are transported by a fleet of just under 100,000 ships of 100 gross tons or more, registered in over 150 nations, crewed by over a million seafarers, and carrying cargo all over the world. Ocean-related tourism, from surfing to restaurants, hotels to cruise ships, accounts for more than 80% of tourism and is growing at an estimated € 114 billion a year.
            </div>
            <div class="section-title">Our Impact</div>
            <div class="section-content">
                The ocean is heavily affected by humankind: climate change is heating the ocean, causing sea levels to rise, melting polar ice, killing coral reefs, increasing levels of acidification and storm intensity, and causing more frequent marine heatwaves. Over-exploitation and destructive fishing practices are crippling fish stocks and destroying deep-sea ecosystems, while the shipping and extraction industries both pollute the ocean environment and harm marine life.
                <br><br>
                Each year around 11 million tonnes of pollution enter the ocean from land-based activities or from ships. Whether plastic, runoff, oil, or discarded fishing nets, the ocean is fighting a losing battle against anthropogenic waste. The number of dead zones is on the rise, and marine life is being stifled. Plastic waste kills up to 1 million seabirds, 100,000 sea mammals, and marine turtles, and countless fish each year.
                <br><br>
                We have chosen to ignore our impact on ocean ecosystems and marine life for too long. Now is the time to turn this around and to stand up for the ocean, not just for its protection but also for its restoration.
            </div>
            <a href="{{ url_for('ocean_facts') }}">
                <button class="find-out-more-btn">Find Out More</button>
            </a>
        </div>
    </body>
    </html>
    """
    return render_template_string(dashboard_html_code)

@app.route('/about_us')
def about_us():
    about_html_code = """
    <!DOCTYPE html>
 <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Us</title>
    <style>
        body, html {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.6;
            background: linear-gradient(to bottom, #002f4b, #00587a, #008891); /* Ocean gradient */
            color: #ffffff; /* Light text for contrast */
        }

        .navbar {
            background-color: rgba(0, 47, 75, 0.9); /* Dark ocean blue with slight transparency */
            overflow: hidden;
            padding: 10px 0;
            text-align: center;
        }
        .navbar a {
            display: inline-block;
            color: white;
            padding: 14px 20px;
            text-decoration: none;
            font-weight: bold;
        }
        .navbar a:hover {
            background-color: #00a8cc;
            color: black;
        }

        .container {
            padding: 40px 20px;
            max-width: 900px;
            margin: auto;
            background: rgba(0, 47, 75, 0.8); /* Semi-transparent background for readability */
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        }

        h1, h2 {
            text-align: center;
        }
        h1 {
            color: #00e6e6;
            margin-bottom: 20px;
        }
        h2 {
            color: #00ffcc;
        }

        p, li {
            text-align: justify;
            color: #cce7ff;
        }

        ul {
            margin-left: 20px;
        }

        .call-to-action {
            text-align: center;
            margin-top: 30px;
        }
        .call-to-action p {
            font-size: 20px;
            font-weight: bold;
            color: #ffeb3b;
        }
    </style>
</head>
<body>
        <div class="navbar">
            <a href="{{ url_for('dashboard') }}">Home</a>
            <a href="{{ url_for('ocean_facts') }}">Ocean Facts</a>
            <a href="{{ url_for('ocean_news') }}">Ocean News</a>
            <a href="{{ url_for('contact_us') }}">Contact Us</a>
            <a href="{{ url_for('about_us') }}">About Us</a>
        </div>
        <div class="container">
            <h1>About Us</h1>
            <div class="mission">
                <h2>Our Mission</h2>
                <p>Our mission is to raise awareness about ocean pollution and inspire positive change in how we treat our oceans. We believe that every individual has the power to make a difference. Our goal is to provide you with the knowledge, tools, and resources to understand the urgency of ocean pollution and take action.</p>
                <p>We aim to:</p>
                <ul>
                    <li><strong>Educate:</strong> By providing reliable, science-based information about ocean pollution, its causes, and its effects.</li>
                    <li><strong>Inspire:</strong> By sharing real stories of individuals and organizations working to combat pollution, we hope to inspire others to take action.</li>
                    <li><strong>Empower:</strong> Our website gives you the resources to reduce your own environmental impact, from small changes in daily habits to involvement in larger conservation efforts.</li>
                </ul>
            </div>
            <div class="why-it-matters">
                <h2>Why It Matters</h2>
                <p>The ocean is more than just a body of water; it's the backbone of life on Earth. Covering over 70% of the planet's surface, oceans regulate our climate, generate most of the oxygen we breathe, and provide food and resources for millions of species—humans included. However, with increasing pollution and plastic waste, marine ecosystems are suffering.</p>
                <p>From the toxic chemicals in the water to the plastic choking marine creatures, ocean pollution is a massive problem that we cannot ignore. It's impacting marine biodiversity, fish stocks, and the health of coastal communities. The time to act is now.</p>
            </div>
            <div class="what-we-do">
                <h2>What We Do</h2>
                <p>This website serves as a platform for knowledge and action. We offer:</p>
                <ul>
                    <li><strong>Educational Content:</strong> Learn the facts about ocean pollution, its sources, and the impact it has on both marine life and humans.</li>
                    <li><strong>Sustainable Solutions:</strong> Discover how you can reduce your personal carbon footprint and plastic use.</li>
                    <li><strong>News & Updates:</strong> Stay informed with the latest research, campaigns, and initiatives to tackle ocean pollution.</li>
                    <li><strong>Ways to Get Involved:</strong> Find local events, organizations, and global movements working to protect our oceans and join the fight.</li>
                </ul>
            </div>
            <div class="vision">
                <h2>Our Vision for the Future</h2>
                <p>We envision a future where oceans are free from pollution. A future where every individual understands the importance of ocean health and takes steps to ensure its protection. Together, we can reverse the damage done and restore our oceans to their former beauty.</p>
            </div>
            <div class="call-to-action">
                <h2>Join Us in the Fight for Cleaner Oceans</h2>
                <p>It's time to turn the tide on ocean pollution. Be part of the solution and help protect our oceans for future generations.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(about_html_code)

@app.route('/submit_story', methods=['POST'])
def submit_story():
    name = request.form.get('name')
    story = request.form.get('story')
    
    if name and story:
        new_story = Story(name=name, story=story)
        db.session.add(new_story)
        db.session.commit()
        flash("Thank you for sharing your story!", "success")
    else:
        flash("Please fill in all fields", "error")
    
    return redirect(url_for('ocean_news'))

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    if rating:
        new_feedback = Feedback(rating=int(rating), comment=comment)
        db.session.add(new_feedback)
        db.session.commit()
        flash("Thank you for your feedback!", "success")
    else:
        flash("Please provide a rating", "error")
    
    return redirect(url_for('contact_us'))

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    if name and email and subject and message:
        new_contact = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(new_contact)
        db.session.commit()
        flash("Your message has been sent successfully!", "success")
    else:
        flash("Please fill in all fields", "error")
    
    return redirect(url_for('contact_us'))

@app.route('/ocean_news')
def ocean_news():
    ocean_news_html_code = """
    <!DOCTYPE html>
    <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ocean News & Action</title>
    <style>
        body, html {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(to bottom, #b3e0ff, #66c2ff, #0096c7);
            color: #00334d;
            line-height: 1.6;
            text-align: center;
        }
        .navbar {
            background-color: rgba(0, 60, 120, 0.9);
            overflow: hidden;
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
            padding: 10px 0;
        }
        .navbar a {
            display: inline-block;
            color: white;
            text-align: center;
            padding: 14px 20px;
            text-decoration: none;
            font-weight: bold;
        }
        .navbar a:hover {
            background-color: #0080ff;
            color: white;
            border-radius: 5px;
        }
        .container {
            padding: 100px 20px 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #005b99;
            font-size: 2.5em;
        }
        h2 {
            color: #007acc;
            font-size: 2em;
            margin-top: 40px;
            text-decoration: underline;
        }
        p, ul {
            font-size: 1.2em;
            max-width: 900px;
            margin: 0 auto;
            padding: 10px;
        }
        .news-item {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            color: #00334d;
        }
        .btn {
            display: inline-block;
            padding: 12px 25px;
            background-color: #0099cc;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin-top: 10px;
        }
        .btn:hover {
            background-color: #0077b6;
        }
    </style>
    <script>
        function showSubmissionMessage() {
            alert("Your submission has been recorded!");
            return true;
        }
    </script>
</head>
<body>
        <div class="navbar">
            <a href="{{ url_for('dashboard') }}">Home</a>
            <a href="{{ url_for('ocean_facts') }}">Ocean Facts</a>
            <a href="{{ url_for('ocean_news') }}">Ocean News</a>
            <a href="{{ url_for('contact_us') }}">Contact Us</a>
            <a href="{{ url_for('about_us') }}">About Us</a>
        </div>
        <div class="container">
         <h1>⚓ Ocean News & Action Hub 📰</h1>
            <p>Stay informed, get inspired, and take action to combat ocean pollution—all right here!</p>

            <h2>💡 Solutions You Can Use ♻️</h2>
            <div class="solution-item">
                <h3>Cut Plastic Use</h3>
                <p>Here's how to start a 30-day plastic-free challenge:</p>
                <ul>
                    <li>Day 1-10: Replace plastic bags with reusable cloth bags.</li>
                    <li>Day 11-20: Switch to a metal or glass water bottle instead of plastic ones.</li>
                    <li>Day 21-30: Avoid straws or use bamboo/metal alternatives.</li>
                </ul>
                <p>Track your progress and share your success below! </p>
            </div>
                       <head>
    <style>
 .solution-item {
    text-align: left;  /* Aligns text to the left */
    padding: 20px;
    margin: 20px auto; /* Centers the div */
    max-width: 800px;  /* Adjust as needed */
}


.solution-item h3,.solution-item p
 {
    text-align: lef; /* Center align heading & paragraph */
}

    </style>
</head>
            <div class="solution-item">
                <h3>Advocate for Change</h3>
                <p>Push for better waste management with these steps:</p>
                <ul>
                    <li>Step 1: Identify local waste issues (e.g., overflowing bins, no recycling).</li>
                    <li>Step 2: Write a letter to your local council: "Dear [Council], I urge you to improve waste disposal to protect our oceans by [specific action]."</li>
                    <li>Step 3: Share your letter with friends to build support.</li>
                </ul>
                <p>Your voice can make a difference—start today!</p>
            </div>

            <h2>Get Involved</h2>
            <div class="quiz-container">
                <h3>Test Your Knowledge</h3>
                <p>How much do you know about ocean pollution? Take our 10-question quiz!</p>
                <a href="{{ url_for('quiz') }}" class="btn">Start Quiz</a>
            </div>
            <div class="submission-form">
                <h3>Share Your Story</h3>
                <p>Have you reduced waste or cleaned a beach? Tell us!</p>
                <form action="/submit_story" method="POST" onsubmit="return showSubmissionMessage()">
                    <input type="text" name="name" placeholder="Your Name" required style="width: 100%; padding: 10px; margin-bottom: 10px;">
                    <textarea name="story" placeholder="Your Story" required style="width: 100%; height: 100px; padding: 10px;"></textarea>
                    <button type="submit" class="btn">Submit</button>
                </form>
            </div>

            <h2>Join the Movement</h2>
            <p>Every action counts. Donate to support our efforts or volunteer with us today!</p>
            <a href="{{ url_for('donate') }}" class="btn">Donate</a>
            <a href="{{ url_for('contact_us') }}" class="btn">Volunteer</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(ocean_news_html_code)

@app.route('/donate')
def donate():
    bank_details = {
        "Bank Name": "Ocean Conservation Bank",
        "Account Name": "Save the Oceans Fund",
        "Account Number": "1234-5678-9012",
        "Routing Number": "098765432",
        "SWIFT Code": "OCB12345"
    }

    donate_html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Donate to Save the Oceans</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 0;
                background-color: #e6f0ff;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h1 {
                text-align: center;
                color: #1a73e8;
            }
            .bank-details {
                margin: 20px 0;
            }
            .bank-details p {
                margin: 5px 0;
            }
            .btn {
                display: inline-block;
                padding: 10px 20px;
                background-color: #1a73e8;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 5px;
            }
            .btn:hover {
                background-color: #1557b0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Donate to Save the Oceans</h1>
            <p>Thank you for supporting our mission! Please use the bank details below to make your donation.</p>

            <div class="bank-details">
                <h2>Bank Details</h2>
                <p><strong>Bank Name:</strong> {{ bank_details['Bank Name'] }}</p>
                <p><strong>Account Name:</strong> {{ bank_details['Account Name'] }}</p>
                <p><strong>Account Number:</strong> {{ bank_details['Account Number'] }}</p>
                <p><strong>Routing Number:</strong> {{ bank_details['Routing Number'] }}</p>
                <p><strong>SWIFT Code:</strong> {{ bank_details['SWIFT Code'] }}</p>
            </div>

            <a href="{{ url_for('ocean_news') }}" class="btn">Back to Ocean News</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(donate_html_code, bank_details=bank_details)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        name = request.form.get('name')
        score = int(request.form.get('score'))
        
        if name and score is not None:
            new_result = QuizResult(name=name, score=score)
            db.session.add(new_result)
            db.session.commit()
            flash("Your quiz results have been saved!", "success")
            return redirect(url_for('quiz_results'))
    
    quiz_html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ocean Pollution Quiz</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #e6f0ff;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h1 {
                text-align: center;
                color: #1a73e8;
            }
            #quiz-container {
                display: block;
            }
            #result-container {
                display: none;
                text-align: center;
            }
            .question {
                margin-bottom: 20px;
            }
            .options label {
                display: block;
                margin: 10px 0;
            }
            button {
                padding: 10px 20px;
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #1557b0;
            }
            #back-btn {
                margin-top: 20px;
                background-color: #00695c;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Ocean Pollution Quiz</h1>
            <div id="quiz-container">
                <div id="question"></div>
                <div id="options" class="options"></div>
                <button onclick="nextQuestion()">Next</button>
            </div>
            <div id="result-container">
                <h2>Your Results</h2>
                <p id="score"></p>
                <form id="result-form" method="POST" style="display: none;">
                    <input type="hidden" name="name" id="result-name">
                    <input type="hidden" name="score" id="result-score">
                </form>
                <a href="{{ url_for('ocean_news') }}"><button id="back-btn">Back to Ocean News</button></a>
            </div>
        </div>

        <script>
            const questions = [
                { q: "How many tons of plastic enter the oceans yearly?", o: ["8 million", "2 million", "15 million", "500,000"], a: 0 },
                { q: "What percentage of marine species have microplastics?", o: ["50%", "90%", "30%", "70%"], a: 1 },
                { q: "Which ocean has the most plastic pollution?", o: ["Atlantic", "Pacific", "Indian", "Arctic"], a: 1 },
                { q: "What is a major source of chemical pollution?", o: ["Oil spills", "Rain", "Wind", "Sunlight"], a: 0 },
                { q: "How much of Earth's surface is covered by oceans?", o: ["50%", "71%", "30%", "90%"], a: 1 },
                { q: "What is the largest ocean?", o: ["Atlantic", "Indian", "Pacific", "Southern"], a: 2 },
                { q: "What kills up to 1 million seabirds yearly?", o: ["Oil", "Plastic", "Fishing nets", "Storms"], a: 1 },
                { q: "Which ocean is the smallest?", o: ["Arctic", "Southern", "Indian", "Pacific"], a: 0 },
                { q: "What percentage of oxygen does the ocean produce?", o: ["20-30%", "50-80%", "10-15%", "90%"], a: 1 },
                { q: "What is the Great Pacific Garbage Patch made of?", o: ["Oil", "Plastic", "Metal", "Wood"], a: 1 },
            ];
            let currentQuestion = 0;
            let score = 0;

            function loadQuestion() {
                const q = questions[currentQuestion];
                document.getElementById('question').innerText = `Question ${currentQuestion + 1}/10: ${q.q}`;
                const optionsDiv = document.getElementById('options');
                optionsDiv.innerHTML = '';
                q.o.forEach((option, index) => {
                    const label = document.createElement('label');
                    label.innerHTML = `<input type="radio" name="answer" value="${index}"> ${option}`;
                    optionsDiv.appendChild(label);
                });
            }

            function nextQuestion() {
                const selected = document.querySelector('input[name="answer"]:checked');
                if (selected) {
                    if (parseInt(selected.value) === questions[currentQuestion].a) {
                        score++;
                    }
                    currentQuestion++;
                    if (currentQuestion < questions.length) {
                        loadQuestion();
                    } else {
                        showResults();
                    }
                } else {
                    alert("Please select an answer!");
                }
            }

            function showResults() {
                document.getElementById('quiz-container').style.display = 'none';
                document.getElementById('result-container').style.display = 'block';
                document.getElementById('score').innerText = `You scored ${score} out of 10! ${(score / 10 * 100).toFixed(1)}%`;
                
                // Set up the form for submission
                const name = prompt("Please enter your name to save your results:");
                if (name) {
                    document.getElementById('result-name').value = name;
                    document.getElementById('result-score').value = score;
                    document.getElementById('result-form').submit();
                }
            }

            // Start the quiz
            loadQuestion();
        </script>
    </body>
    </html>
    """
    return render_template_string(quiz_html_code)

@app.route('/quiz_results')
def quiz_results():
    results = QuizResult.query.order_by(QuizResult.score.desc()).all()
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quiz Results</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 0;
                background-color: #e6f0ff;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h1 {
                color: #1a73e8;
                text-align: center;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #1a73e8;
                color: white;
            }
            tr:hover {
                background-color: #f5f5f5;
            }
            .btn {
                display: inline-block;
                padding: 10px 20px;
                background-color: #1a73e8;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }
            .btn:hover {
                background-color: #1557b0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Quiz Results</h1>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Name</th>
                        <th>Score</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for result in results %}
                    <tr>
                        <td>{{ loop.index }}</td>
                        <td>{{ result.name }}</td>
                        <td>{{ result.score }}/10</td>
                        <td>{{ result.created_at.strftime('%Y-%m-%d') }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <a href="{{ url_for('quiz') }}" class="btn">Take Quiz Again</a>
            <a href="{{ url_for('ocean_news') }}" class="btn">Back to Ocean News</a>
        </div>
    </body>
    </html>
    """, results=results)

@app.route('/ocean_facts')
def ocean_facts():
    bar_chart_json = create_bar_chart()
    pie_chart_json = create_pie_chart()
    world_map_html = create_world_map()

    template = ''' 
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ocean Pollution Fact</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    text-align: center; 
                    background-color: #e3f2fd; /* Light blue background */
                    margin: 0;
                }
                /* Navbar styles */
                .navbar {
            background-color: rgba(0, 47, 75, 0.9); /* Dark ocean blue with slight transparency */
            overflow: hidden;
            padding: 10px 0;
            text-align: center;
        }
        .navbar a {
            display: inline-block;
            color: white;
            padding: 14px 20px;
            text-decoration: none;
            font-weight: bold;
        }
        .navbar a:hover {
            background-color: #00a8cc;
            color: black;
        }


                .container { 
                    display: flex; 
                    justify-content: space-around; 
                    flex-wrap: wrap;
                    margin-top: 20px; 
                }
                .chart { 
                    width: 45%; 
                    min-height: 400px; 
                    background: white;
                    padding: 10px;
                    border-radius: 8px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                } 
                .map { 
                    margin-top: 20px; 
                    display: flex; 
                    justify-content: center;
                }
            </style>
        </head>
        <body>

            <!-- Navbar -->
            <div class="navbar">
            <a href="{{ url_for('dashboard') }}">Home</a>
            <a href="{{ url_for('ocean_facts') }}">Ocean Facts</a>
            <a href="{{ url_for('ocean_news') }}">Ocean News</a>
            <a href="{{ url_for('contact_us') }}">Contact Us</a>
            <a href="{{ url_for('about_us') }}">About Us</a>
        </div>

            <div class="container">
                <div class="chart">
                    <div id="bar-chart"></div>
                </div>
                <div class="chart">
                    <div id="pie-chart"></div>
                </div>
            </div>

            <h2>World Map</h2>
            <div class="map">{{ world_map_html | safe }}</div>

            <script>
                console.log('Plotly loaded:', typeof Plotly !== 'undefined'); /* Debug Plotly */
                var barChart = {{ bar_chart_json | safe }};
                console.log('Bar Chart:', barChart); /* Debug bar chart data */
                var pieChart = {{ pie_chart_json | safe }};
                console.log('Pie Chart:', pieChart); /* Debug pie chart data */

                Plotly.newPlot('bar-chart', barChart.data, barChart.layout);
                Plotly.newPlot('pie-chart', pieChart.data, pieChart.layout);

                document.getElementById('bar-chart').on('plotly_click', function(data) {
                    var ocean = data.points[0].x;
                    fetch('/update_pie_chart?ocean=' + encodeURIComponent(ocean))
                        .then(response => response.json())
                        .then(pieChartData => {
                            Plotly.react('pie-chart', pieChartData.data, pieChartData.layout);
                        });
                });
            </script>
        </body>
        </html>
        '''

    return render_template_string(template,
                                  bar_chart_json=bar_chart_json,
                                  pie_chart_json=pie_chart_json,
                                  world_map_html=world_map_html)

@app.route('/update_pie_chart')
def update_pie_chart():
    ocean = request.args.get('ocean')
    if ocean in oceans:
        ocean_index = oceans.index(ocean)
        pie_chart_json = create_pie_chart(ocean_index)
        return pie_chart_json
    return jsonify({"error": "Invalid ocean"}), 400

@app.route('/ocean/<name>')
def ocean_detail(name):
    if name in ocean_details:
        details = ocean_details[name]
        return render_template_string(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f5f9ff;
                }}

                .content {{
                    margin: 20px;
                    text-align: left;
                }}

                h1, h2, h3 {{
                    color: #1a73e8;
                }}

                ul {{
                    list-style-type: disc;
                    margin-left: 20px;
                }}

                li {{
                    margin-bottom: 10px;
                }}

                img {{
                    width: 100%;
                    max-width: 300px;
                    border-radius: 8px;
                }}

                /* 🌟 Improved Button Style */
                button {{
                    margin: 20px;
                    border-radius: 6px;
                    border: none;
                    padding: 10px 18px;
                    background: linear-gradient(135deg, #1a73e8, #0b5ed7);
                    cursor: pointer;
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                }}

                button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 15px rgba(26, 115, 232, 0.4);
                }}

                button a {{
                    color: white;
                    text-decoration: none;
                    font-weight: 600;
                }}
            </style>
        </head>

        <body>
            <div class="content">
                {details["details"] if name in ocean_details else details}
            </div>

            <button>
                <a href="{{{{ url_for('ocean_facts') }}}}">← Back to Ocean Facts</a>
            </button>
        </body>
        </html>
        ''')
    return "Ocean not found", 404


@app.route('/contact_us')
def contact_us():
    contact_us_html_code = """
    <!DOCTYPE html>
   <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us</title>
    <style>
            body, html {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                line-height: 1.6;
                background: linear-gradient(to bottom, #d4f1f9, #75cbe9, #0077b6);
                color: #002244;
                text-align: center;
            }
            .navbar {
                background-color: rgba(0, 50, 100, 0.9);
                overflow: hidden;
                padding: 10px 0;
                position: fixed;
                top: 0;
                width: 100%;
                z-index: 1000;
            }
            .navbar a {
                display: inline-block;
                color: white;
                padding: 14px 20px;
                text-decoration: none;
                font-weight: bold;
            }
            .navbar a:hover {
                background-color: #0096c7;
                border-radius: 5px;
            }
            .container {
                padding: 100px 20px 20px;
                max-width: 800px;
                margin: auto;
                background: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            }
            h1, h3 {
                color: #005a8d;
            }
            .form-group {
                margin-bottom: 15px;
                text-align: left;
            }
            .form-group label {
                display: block;
                color: #003366;
                font-weight: bold;
            }
            .form-group input, .form-group textarea, .form-group select {
                width: 100%;
                padding: 10px;
                border: 1px solid #0077b6;
                border-radius: 5px;
                background: #ffffff;
                color: #000;
            }
            .form-group textarea {
                height: 150px;
            }
            .form-group button {
                background-color: #0077b6;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            }
            .form-group button:hover {
                background-color: #005a8d;
            }
            .social-links a {
                color: #0077b6;
                text-decoration: none;
                font-weight: bold;
            }
            .social-links a:hover {
                text-decoration: underline;
            }
            /* Feedback Modal */
            .modal {
                display: none;
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                align-items: center;
                justify-content: center;
            }
            .modal-content {
                background-color: white;
                padding: 20px;
                width: 40%;
                text-align: center;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                position: relative;
            }
            .close {
                position: absolute;
                top: 10px;
                right: 15px;
                font-size: 22px;
                cursor: pointer;
            }
            /* Star rating */
            .stars {
                display: flex;
                justify-content: center;
                margin: 15px 0;
            }
            .stars span {
                font-size: 30px;
                cursor: pointer;
                color: gray;
            }
            .stars span.active {
                color: gold;
            }
            textarea {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                resize: none;
            }
            .submit-btn {
                margin-top: 10px;
                padding: 10px 15px;
                background-color: #28a745;
                color: white;
                border: none;
                cursor: pointer;
                border-radius: 5px;
            }
        </style>
</head>
<body>
    <body>
        <div class="navbar">
            <a href="{{ url_for('dashboard') }}">Home</a>
            <a href="{{ url_for('ocean_facts') }}">Ocean Facts</a>
            <a href="{{ url_for('ocean_news') }}">Ocean News</a>
            <a href="{{ url_for('contact_us') }}">Contact Us</a>
            <a href="{{ url_for('about_us') }}">About Us</a>
        </div>
        <div class="container">
            <h1>Contact Us</h1>
            <p>If you have any questions or want to get involved, feel free to reach out to us.</p>
            <h3>Contact Information</h3>
            <p><strong>Email:</strong> <a href="mailto:123456@gmail.com">123456@gmail.com</a></p>
            <p><strong>Phone:</strong> <a href="tel:+1234567890">123-456-7890</a></p>
            <p><strong>Follow Us on Instagram:</strong> <a href="https://www.instagram.com/YourOrganization" target="_blank">Instagram</a></p>
            <h3>Get in Touch</h3>
            <form action="/submit_contact" method="POST">
                <div class="form-group">
                    <label for="name">Your Name</label>
                    <input type="text" id="name" name="name" required placeholder="Your Name">
                </div>
                <div class="form-group">
                    <label for="email">Your Email</label>
                    <input type="email" id="email" name="email" required placeholder="Your Email">
                </div>
                <div class="form-group">
                    <label for="subject">Subject</label>
                    <select id="subject" name="subject" required>
                        <option value="General Inquiry">General Inquiry</option>
                        <option value="Volunteer">Volunteer</option>
                        <option value="Partnership">Partnership</option>
                        <option value="Event Inquiry">Event Inquiry</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="message">Message</label>
                    <textarea id="message" name="message" required placeholder="Your Message"></textarea>
                </div>
                <div class="form-group">
                    <button type="submit">Submit</button>
                </div>
            </form>
            <div class="feedback">
                <h3>Feedback</h3>
                <p>We would love to hear your thoughts on our website and campaigns.</p>
                <a href="#" id="openFeedback">Share your feedback</a>
            </div>

            <!-- Modal -->
            <div id="feedbackModal" class="modal">
                <div class="modal-content">
                    <span class="close">&times;</span>
                    <h2>Rate Us</h2>
                    <div class="stars">
                        <span data-value="1">&#9733;</span>
                        <span data-value="2">&#9733;</span>
                        <span data-value="3">&#9733;</span>
                        <span data-value="4">&#9733;</span>
                        <span data-value="5">&#9733;</span>
                    </div>
                    <textarea id="suggestion" rows="4" placeholder="Write your feedback here..."></textarea>
                    <form action="/submit_feedback" method="POST" id="feedbackForm">
                        <input type="hidden" name="rating" id="ratingValue">
                        <input type="hidden" name="comment" id="commentValue">
                    </form>
                    <button class="submit-btn" onclick="submitFeedback()">Submit</button>
                </div>
            </div>
        </div>

        <script>
            document.getElementById("openFeedback").addEventListener("click", function(event) {
                event.preventDefault();
                document.getElementById("feedbackModal").style.display = "flex";
            });

            document.querySelector(".close").addEventListener("click", function() {
                document.getElementById("feedbackModal").style.display = "none";
            });

            window.onclick = function(event) {
                let modal = document.getElementById("feedbackModal");
                if (event.target === modal) {
                    modal.style.display = "none";
                }
            };

            document.querySelectorAll(".stars span").forEach(star => {
                star.addEventListener("click", function() {
                    let value = this.getAttribute("data-value");
                    document.querySelectorAll(".stars span").forEach(s => s.classList.remove("active"));
                    for (let i = 0; i < value; i++) {
                        document.querySelectorAll(".stars span")[i].classList.add("active");
                    }
                    document.getElementById("ratingValue").value = value;
                });
            });

            function submitFeedback() {
                const rating = document.querySelectorAll(".stars span.active").length;
                const comment = document.getElementById("suggestion").value.trim();
                
                if (rating === 0 && comment === "") {
                    alert("Please select a rating or enter feedback before submitting.");
                    return;
                }
                
                document.getElementById("commentValue").value = comment;
                document.getElementById("feedbackForm").submit();
                
                // Show success message
                let successMessage = document.createElement("div");
                successMessage.textContent = "Your feedback has been submitted!";
                successMessage.style.position = "fixed";
                successMessage.style.top = "50%";
                successMessage.style.left = "50%";
                successMessage.style.transform = "translate(-50%, -50%)";
                successMessage.style.backgroundColor = "green";
                successMessage.style.color = "white";
                successMessage.style.padding = "15px 20px";
                successMessage.style.borderRadius = "5px";
                successMessage.style.fontWeight = "bold";
                successMessage.style.zIndex = "1000";

                document.body.appendChild(successMessage);

                // Hide the modal
                document.getElementById("feedbackModal").style.display = "none";

                // Remove the message after 2 seconds
                setTimeout(function() {
                    successMessage.remove();
                }, 2000);

                // Clear the feedback form after submission
                document.getElementById("suggestion").value = "";
                document.querySelectorAll(".stars span").forEach(s => s.classList.remove("active"));
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(contact_us_html_code)

if __name__ == '__main__':
    app.run(debug=True)