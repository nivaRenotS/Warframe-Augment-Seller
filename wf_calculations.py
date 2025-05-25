
import pywmapi as wm
import matplotlib.pyplot as plt
from typing import List, Dict, Any
import time
import json

import syndicate_mods_lookup


"""Fetch statistics for a given mod from the Warframe Market API"""
def get_mod_statistics(mod_name):

    try:
        statistics = wm.statistics.get_statistic(mod_name)
        return statistics
    except Exception as e:
        print(f"Error fetching statistics for {mod_name}: {e}")
        return None


"""Calculate average price and volume from a list of statistics"""
def calculate_averages(stats):
    if not stats or len(stats) == 0:
        return 0, 0, 0  # Return zeros if no data

    total_volume = sum(stat.volume for stat in stats)
    avg_price = sum(stat.avg_price * stat.volume for stat in stats) / total_volume if total_volume > 0 else 0

    # Calculate moving average if available
    moving_avgs = [stat.moving_avg for stat in stats if stat.moving_avg is not None]
    avg_moving_avg = sum(moving_avgs) / len(moving_avgs) if moving_avgs else None

    return avg_price, total_volume, avg_moving_avg


"""Find Pareto optimal mods for both 48h and 90d timeframes"""
def find_pareto_optimal_mods(mod_stats: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:

    pareto_optimal = {
        '48h': [],
        '90d': []
    }

    for timeframe in ['48h', '90d']:
        # Extract data for the current timeframe
        mods_data = []
        for mod_name, stats in mod_stats.items():
            if stats[f'avg_price_{timeframe}'] > 0 and stats[f'volume_{timeframe}'] > 0:
                mods_data.append({
                    'name': mod_name,
                    'price': stats[f'avg_price_{timeframe}'],
                    'volume': stats[f'volume_{timeframe}']
                })

        # Find Pareto optimal mods in terms of price and volume
        pareto_mods = []
        for mod1 in mods_data:
            is_pareto = True
            for mod2 in mods_data:
                if (mod2['price'] >= mod1['price'] and mod2['volume'] > mod1['volume']) or \
                        (mod2['price'] > mod1['price'] and mod2['volume'] >= mod1['volume']):
                    is_pareto = False
                    break
            if is_pareto:
                pareto_mods.append(mod1['name'])

        pareto_optimal[timeframe] = pareto_mods

    return pareto_optimal


"""Analyze syndicate mods to find the best trading opportunities"""
def analyze_syndicate_mods(syndicate_mods):
    mod_stats = {}

    print("Collecting statistics for syndicate mods...")

    # iterate through the syndicate mods
    for i, mod_name in enumerate(syndicate_mods):
        if i % 10 == 0:
            print(f"Processing mod {i + 1}/{len(syndicate_mods)}: {mod_name}")

        # statistics for the mods
        stats = get_mod_statistics(mod_name)
        if not stats:
            continue

        # Calculate averages for 48h and 90d
        avg_price_48h, volume_48h, moving_avg_48h = calculate_averages(stats.closed_48h)
        avg_price_90d, volume_90d, moving_avg_90d = calculate_averages(stats.closed_90d)

        mod_stats[mod_name] = {
            'avg_price_48h': avg_price_48h,
            'volume_48h': volume_48h,
            'moving_avg_48h': moving_avg_48h,
            'avg_price_90d': avg_price_90d,
            'volume_90d': volume_90d,
            'moving_avg_90d': moving_avg_90d
        }

        # delay to avoid rate limiting
        time.sleep(0.1)

    # Find Pareto optimal mods
    pareto_optimal = find_pareto_optimal_mods(mod_stats)

    # Display results
    print("\n=== PARETO OPTIMAL SYNDICATE MODS ===")

    print("\n== 48 HOUR OPTIMAL MODS ==")
    print(f"Found {len(pareto_optimal['48h'])} Pareto optimal mods for 48h timeframe:")
    for mod_name in pareto_optimal['48h']:
        stats = mod_stats[mod_name]
        print(f"Mod: {mod_name.replace('_', ' ')}")
        print(f"  Average Price: {stats['avg_price_48h']:.2f} platinum")
        print(f"  Total Volume: {stats['volume_48h']} trades")
        print(
            f"  Moving Average: {stats['moving_avg_48h']:.2f}" if stats['moving_avg_48h'] else "  Moving Average: N/A")
        print()

    print("\n== 90 DAY OPTIMAL MODS ==")
    print(f"Found {len(pareto_optimal['90d'])} Pareto optimal mods for 90d timeframe:")
    for mod_name in pareto_optimal['90d']:
        stats = mod_stats[mod_name]
        print(f"Mod: {mod_name.replace('_', ' ')}")
        print(f"  Average Price: {stats['avg_price_90d']:.2f} platinum")
        print(f"  Total Volume: {stats['volume_90d']} trades")
        print(
            f"  Moving Average: {stats['moving_avg_90d']:.2f}" if stats['moving_avg_90d'] else "  Moving Average: N/A")
        print()

    # Plot the Pareto fronts
    plot_pareto_fronts(mod_stats, pareto_optimal)

    return mod_stats, pareto_optimal


# Function to plot Pareto fronts
def plot_pareto_fronts(mod_stats, pareto_optimal):
    """Create a visualization of the Pareto fronts for both timeframes"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))

    for i, timeframe in enumerate(['48h', '90d']):
        ax = axes[i]

        # Plot all mods
        x, y, names = [], [], []
        for mod_name, stats in mod_stats.items():
            if stats[f'avg_price_{timeframe}'] > 0 and stats[f'volume_{timeframe}'] > 0:
                x.append(stats[f'volume_{timeframe}'])
                y.append(stats[f'avg_price_{timeframe}'])
                names.append(mod_name)

        ax.scatter(x, y, alpha=0.5, label='All Mods')

        # Highlight Pareto optimal mods
        pareto_x, pareto_y, pareto_names = [], [], []
        for mod_name in pareto_optimal[timeframe]:
            stats = mod_stats[mod_name]
            pareto_x.append(stats[f'volume_{timeframe}'])
            pareto_y.append(stats[f'avg_price_{timeframe}'])
            pareto_names.append(mod_name)

        ax.scatter(pareto_x, pareto_y, color='red', label='Pareto Optimal')

        # Label the Pareto optimal points
        for i, name in enumerate(pareto_names):
            ax.annotate(name.replace('_', ' '), (pareto_x[i], pareto_y[i]),
                        textcoords="offset points", xytext=(0, 10), ha='center')

        # Add a line connecting the Pareto optimal points
        if pareto_x and len(pareto_x) > 1:
            # Sort points by x-coordinate
            pareto_points = sorted(zip(pareto_x, pareto_y), key=lambda p: p[0])
            pareto_x_sorted, pareto_y_sorted = zip(*pareto_points)
            ax.plot(pareto_x_sorted, pareto_y_sorted, 'r--', label='Pareto Front')

        ax.set_title(f'Pareto Optimal Syndicate Mods ({timeframe})')
        ax.set_xlabel('Trading Volume')
        ax.set_ylabel('Average Price (platinum)')
        ax.grid(True, alpha=0.3)
        ax.legend()

    plt.tight_layout()
    plt.savefig('syndicate_mods_pareto.png')
    plt.show()


# main
if __name__ == "__main__":
    test_mods = syndicate_mods_lookup.syndicate_mods #[:10] #testing

    # analysis
    mod_stats, pareto_optimal = analyze_syndicate_mods(test_mods)

    # Convert any non-serializable values (like datetimes) to strings
    serializable_stats = {}
    for mod, stats in mod_stats.items():
        serializable_stats[mod] = {
            key: float(value) if isinstance(value, (int, float)) else str(value)
            for key, value in stats.items()
        }
    # save to a json
    with open('syndicate_mod_stats.json', 'w') as f:
        json.dump({
            'mod_stats': serializable_stats,
            'pareto_optimal_48h': pareto_optimal['48h'],
            'pareto_optimal_90d': pareto_optimal['90d']
        }, f, indent=2)
