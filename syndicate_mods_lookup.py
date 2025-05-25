import re


def get_wiki_content():
    # Default file path to use
    # This is the wiki edit html from https://wiki.warframe.com/w/Template:AugmentNav?action=edit May 24, 2025
    default_text_path = """
    {{UpdateMe|Add better documentation on how to add new mod entries}}
<onlyinclude>{| class="navbox mw-collapsible {{#if:{{{collapsed|}}}|mw-collapsed|}}"
|-
! colspan=2 class="navboxhead" | [[Warframe Augment Mods|Warframe Augments]] {{Edit|Template:AugmentNav}}
|-
|<div class="tabber-borderless"><tabber>PvE=
{{LuaNavbox
| bodyclass = navbox
| bodystyle = font-size:small; text-align:left;
| groupclass = navboxgroup
| groupstyle = white-space: nowrap; text-align:center;
| alternaterows = yes
| rowclass = navboxrow
| altrowclass = navboxrowalt
| handleCustom = true
| ignoreTitle = true
| state = plain
| skipGutter = true
| group1 = WF_Ash_
| list1 = M_Seeking Shuriken_ • M_Smoke Shadow_ • M_Teleport Rush_ • M_Rising Storm_
| group2 = WF_Atlas_
| list2 = M_Rubble Heap_ • M_Path of Statues_ • M_Tectonic Fracture_ • M_Ore Gaze_ • M_Rumbled_ • M_Titanic Rumbler_
| group3 = WF_Banshee_
| list3 = M_Sonic Fracture_ • M_Resonance_ • M_Savage Silence_ • M_Resonating Quake_
| group4 = WF_Baruuk_
| list4 = M_Elusive Retribution_ • M_Endless Lullaby_ • M_Reactive Storm_
| group5 = WF_Chroma_
| list5 = M_Afterburn_ • M_Everlasting Ward_ • M_Guardian Armor_ • M_Vexing Retaliation_ • M_Guided Effigy_
| group6 = WF_Citrine_
| list6 = M_Recrystalize_
| group7 = WF_Dagath_
| list7 = M_Spectral Spirit_
| group8 = WF_Ember_
| list8 = M_Fireball Frenzy_ • M_Immolated Radiance_ • M_Healing Flame_ • M_Purifying Flames_ • M_Exothermic_
| group9 = WF_Equinox_
| list9 = M_Duality_ • M_Calm & Frenzy_ • M_Peaceful Provocation_ • M_Energy Transfer_
| group10 = WF_Excalibur_
| list10 = M_Purging Slash_ • M_Surging Dash_ • M_Radiant Finish_ • M_Furious Javelin_ • M_Chromatic Blade_
| group11 = WF_Excalibur Umbra_
| list11 = M_Warrior's Rest_
| group12 = WF_Frost_
| list12 = M_Biting Frost_ • M_Freeze Force_ • M_Ice Wave Impedance_ • M_Chilling Globe_ • M_Icy Avalanche_
| group13 = WF_Gara_
| list13 = M_Mending Splinters_ • M_Spectrosiphon_ • M_Shattered Storm_
| group14 = WF_Garuda_
| list14 = M_Dread Ward_ • M_Blood Forge_ • M_Blending Talons_
| group15 = WF_Gauss_
| list15 = M_Mach Crash_ • M_Thermal Transfer_
| group16 = WF_Grendel_
| list16 = M_Gourmand_ • M_Hearty Nourishment_ • M_Catapult_ • M_Gastro_
| group17 = WF_Gyre_
| list17 = M_Conductive Sphere_ • M_Coil Recharge_ • M_Cathode Current_
| group18 = WF_Harrow_
| list18 = M_Tribunal_ • M_Warding Thurible_ • M_Lasting Covenant_
| group19 = WF_Hildryn_
| list19 = M_Balefire Surge_ • M_Blazing Pillage_ • M_Aegis Gale_
| group20 = WF_Hydroid_
| list20 = M_Viral Tempest_ • M_Tidal Impunity_ • M_Rousing Plunder_ • M_Pilfering Swarm_
| group21 = WF_Inaros_
| list21 = M_Desiccation's Curse_ • M_Elemental Sandstorm_ • M_Negation Armor_
| group22 = WF_Ivara_
| list22 = M_Empowered Quiver_ • M_Power of Three_ • M_Piercing Navigator_ • M_Infiltrate_ • M_Concentrated Arrow_
| group23 = WF_Khora_
| list23 = M_Accumulating Whipclaw_ • M_Venari Bodyguard_ • M_Pilfering Strangledome_
| group24 = WF_Koumei_
| list24 = M_Omikuji's Fortune_
| group25 = WF_Kullervo_
| list25 = M_Wrath of Ukko_
| group26 = WF_Lavos_
| list26 = M_Valence Formation_ • M_Swift Bite_
| group27 = WF_Limbo_
| list27 = M_Rift Haven_ • M_Rift Torrent_ • M_Cataclysmic Continuum_
| group28 = WF_Loki_
| list28 = M_Damage Decoy_ • M_Deceptive Bond_ • M_Savior Decoy_ • M_Hushed Invisibility_ • M_Safeguard Switch_ • M_Irradiating Disarm_
| group29 = WF_Mag_
| list29 = M_Greedy Pull_ • M_Magnetized Discharge_ • M_Counter Pulse_ • M_Fracturing Crush_
| group30 = WF_Mesa_
| list30 = M_Ballistic Bullseye_ • M_Muzzle Flash_ • M_Staggering Shield_ • M_Mesa's Waltz_
| group31 = WF_Mirage_
| list31 = M_Hall of Malevolence_ • M_Explosive Legerdemain_ • M_Total Eclipse_ • M_Prism Guard_
| group32 = WF_Nekros_
| list32 = M_Soul Survivor_ • M_Creeping Terrify_ • M_Despoil_ • M_Shield of Shadows_
| group33 = WF_Nezha_
| list33 = M_Controlled Slide_ • M_Pyroclastic Flow_ • M_Reaping Chakram_ • M_Safeguard_ • M_Divine Retribution_
| group34 = WF_Nidus_
| list34 = M_Abundant Mutation_ • M_Teeming Virulence_ • M_Larva Burst_  • M_Parasitic Vitality_ • M_Insatiable_
| group35 = WF_Nova_
| list35 = M_Neutron Star_ • M_Antimatter Absorb_ • M_Escape Velocity_ • M_Molecular Fission_
| group36 = WF_Nyx_
| list36 = M_Mind Freak_ • M_Pacifying Bolts_ • M_Chaos Sphere_ • M_Assimilate_ • M_Singularity_
| group37 = WF_Oberon_
| list37 = M_Smite Infusion_ • M_Hallowed Eruption_ • M_Phoenix Renewal_ • M_Hallowed Reckoning_
| group38 = WF_Octavia_
| list38 = M_Partitioned Mallet_ • M_Conductor_
| group39 = WF_Protea_
| list39 = M_Temporal Artillery_ • M_Repair Dispensary_ • M_Temporal Erosion_
| group40 = WF_Qorvex_
| list40 = M_Wrecking Wall_ • M_Fused Crucible_
| group41 = WF_Revenant_
| list41 = M_Thrall Pact_ • M_Blinding Reave_ • M_Mesmer Shield_
| group42 = WF_Rhino_
| list42 = M_Ironclad Charge_ • M_Iron Shrapnel_ • M_Piercing Roar_ • M_Reinforcing Stomp_
| group43 = WF_Saryn_
| list43 = M_Revealing Spores_ • M_Venom Dose_ • M_Regenerative Molt_ • M_Contagion Cloud_
| group44 = WF_Sevagoth_
| list44 = M_Shadow Haze_ • M_Dark Propagation_
| group45 = WF_Styanax_
| list45 = M_Axios Javelineers_ • M_Intrepid Stand_
| group46 = WF_Titania_
| list46 = M_Ironclad Flight_ • M_Spellbound Harvest_ • M_Beguiling Lantern_ • M_Razorwing Blitz_
| group47 = WF_Trinity_
| list47 = M_Pool of Life_ • M_Vampire Leech_ • M_Abating Link_ • M_Champion's Blessing_
| group48 = WF_Valkyr_
| list48 = M_Swing Line_ • M_Eternal War_ • M_Prolonged Paralysis_ • M_Enraged_ • M_Hysterical Assault_
| group49 = WF_Vauban_
| list49 = M_Tesla Bank_ • M_Photon Repeater_ • M_Repelling Bastille_
| group50 = WF_Volt_
| list50 = M_Shock Trooper_ • M_Shocking Speed_ • M_Recharge Barrier_ • M_Transistor Shield_ • M_Capacitance_
| group51 = WF_Voruna_
| list51 = M_Prey of Dynar_ • M_Ulfrun's Endurance_
| group52 = WF_Wisp_
| list52 = M_Fused Reservoir_ • M_Critical Surge_ • M_Cataclysmic Gate_
| group53 = WF_Wukong_
| list53 = M_Celestial Stomp_ • M_Enveloping Cloud_ • M_Primal Rage_
| group54 = WF_Xaku_
| list54 = M_Vampiric Grasp_ • M_The Relentless Lost_
| group55 = WF_Yareli_
| list55 = M_Surging Blades_ • M_Loyal Merulina_ • M_Merulina Guardian_
| group56 = WF_Zephyr_
| list56 = M_Anchored Glide_ • M_Target Fixation_ • M_Airburst Rounds_ • M_Jet Stream_ • M_Funnel Clouds_
}}
|-|PvP=
{{LuaNavbox
| bodyclass = navbox
| bodystyle = font-size:small; text-align:left;
| groupclass = navboxgroup
| groupstyle = white-space: nowrap; text-align:center;
| alternaterows = yes
| rowclass = navboxrow
| altrowclass = navboxrowalt
| handleCustom = true
| ignoreTitle = true
| state = plain
| skipGutter = true
| group1 = WF_Ash_
| list1 = M_Tear Gas_
| group2 = WF_Atlas_
| list2 = M_Rumbled_
| group3 = WF_Chroma_
| list3 = M_Afterburn_
| group4 = WF_Ember_
| list4 = M_Purifying Flames_
| group5 = WF_Equinox_
| list5 = M_Push & Pull_
| group6 = WF_Excalibur_
| list6 = M_Purging Slash_ • M_Signal Flare_
| group7 = WF_Frost_
| list7 = M_Ice Wave Impedance_
| group8 = WF_Ivara_
| list8 = M_Power of Three_
| group9 = WF_Loki_
| list9 = M_Deceptive Bond_
| group10 = WF_Mag_
| list10 = M_Sapping Reach_ • M_Shield Overload_
| group11 = WF_Mesa_
| list11 = M_Mesa's Waltz_
| group12 = WF_Mirage_
| list12 = M_Prism Guard_
| group13 = WF_Nekros_
| list13 = M_Discharge Strike_
| group14 = WF_Nezha_
| list14 = M_Ward Recovery_
| group15 = WF_Nova_
| list15 = M_Antimatter Mine_
| group16 = WF_Nyx_
| list16 = M_Singularity_
| group17 = WF_Oberon_
| list17 = M_Defiled Reckoning_
| group18 = WF_Rhino_
| list18 = M_Iron Shrapnel_
| group19 = WF_Valkyr_
| list19 = M_Hysterical Fixation_
| group20 = WF_Volt_
| list20 = M_Recharge Barrier_ • M_Kinetic Collision_
}}
</tabber></div>
|}</onlyinclude>
[[Category:Navbox]]
<noinclude>
[[es:Plantilla:ModAumentoWarframeNav]]
</noinclude>
    """
    return default_text_path

# Function to extract items from list lines and remove undesirables
def extract_mods(content):
    # Find all list entries that follow the pattern list# = M_XXX_ • M_YYY_ • ...
    list_pattern = r'list\d+ = (.*?)(?=\n|$)'
    lists = re.findall(list_pattern, content)

    syndicate_mods = []

    for item_list in lists:
        # Split by bullet points to get individual mods
        mods = item_list.split('•')
        for mod in mods:
            # Strip whitespace
            mod = mod.strip()
            # Remove M_ prefix and trailing _
            if mod.startswith('M_') and mod.endswith('_'):
                mod_name = mod[2:-1]
                # Replace spaces with underscores
                mod_name = mod_name.replace(' ', '_')
                # remove hyphens
                mod_name = mod_name.replace('\'', '')
                # replace & with 'and'
                mod_name = mod_name.replace('&', 'and')
                # lowercase the mod to match api
                mod_name = mod_name.lower()
                # changed mods not reflected in the api
                mod_name = mod_name.replace('teleport_rush', 'fatal_teleport')
                mod_name = mod_name.replace('negation_armor', 'negation_swarm')
                # convert mod names to lowercase
                syndicate_mods.append(mod_name)

    return syndicate_mods


def extract_mods_from_file(file_path):
    """Extract mod names from a user-provided file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Check if the file appears to be in the wiki template format
        if 'list' in content and '•' in content:
            return extract_mods(content)

        # Otherwise, parse as a simple list (one mod per line)
        mods_list = []
        for line in content.splitlines():
            mod_name = line.strip()
            if mod_name and not mod_name.startswith('#'):  # Skip empty lines and comments
                # Process the mod name to match API format
                mod_name = mod_name.replace(' ', '_')
                mod_name = mod_name.replace('\'', '')
                mod_name = mod_name.replace('&', 'and')
                mod_name = mod_name.lower()

                # Apply the same special case replacements
                mod_name = mod_name.replace('teleport_rush', 'fatal_teleport')
                mod_name = mod_name.replace('negation_armor', 'negation_swarm')

                if len(mod_name) > 3:  # Skip very short entries
                    mods_list.append(mod_name)

        return mods_list
    except Exception as e:
        print(f"Error extracting mods from file: {e}")
        return []


# Get the wiki content from file
wiki_content = get_wiki_content()

# Extract the mods from the content
syndicate_mods = extract_mods(wiki_content)