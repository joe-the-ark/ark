from arkserver.models import *
from arkserver.management.commands.utils import *
from itertools import combinations
import math

def calc_circles(game):
    votes, n = get_u5(game)

    safezone = {}
    players = list(votes.keys())

    for player in votes:
        pvotes = votes[player]
        for power in pvotes:
            if power not in safezone:
                safezone[power] = 0
            cell = pvotes[power]
            for p in cell:
                score = cell[p]
                safezone[power] += score / (n * n)

    result = {}
    for bar in range(1, 100):
        data = calc_single(players, votes, n, safezone, bar)
        if not data['circles'] and not data['dyads']:
            continue

        result[bar] = data

        if len(data['circle_count']) == n and len(data['circles']) == 1:
            mono_circle = all(data['circle_count'][k] == 1 for k in data['circle_count'])
            if mono_circle:
                break

    return {'players': players, 'circles': result}

def calc_single(players, votes, n, safezone, safebar):
    result = {
        player: {target: {} for target in votes} for player in votes
    }

    for player in votes:
        pvotes = votes[player]
        for power in pvotes:
            cell = pvotes[power]
            for target in cell:
                result[player][target][power] = cell[target]

    for p1 in result:
        for p2 in result[p1]:
            s = 0
            for p in result[p1][p2]:
                score = result[p1][p2][p]
                baseline = safezone[p]
                delta = abs(score - baseline) / safebar
                s += delta / n
            result[p1][p2] = s

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = players[i], players[j]
            s1 = result[p1][p2]
            s2 = result[p2][p1]
            if s1 <= 1 and s2 <= 1:
                cell_ij = votes[p1].get(p2, {})
                cell_ji = votes[p2].get(p1, {})
                raw1 = sum(cell_ij.values()) / len(cell_ij) if cell_ij else 0
                raw2 = sum(cell_ji.values()) / len(cell_ji) if cell_ji else 0
                edges.append({
                    'i': i,
                    'j': j,
                    'normDist': max(s1, s2),
                    'raw1': raw1,
                    'raw2': raw2,
                    'baseline1': safezone.get(p2, 0),
                    'baseline2': safezone.get(p1, 0),
                })

    circles = {}
    seen = set()
    for size in range(n, 1, -1):
        for com in combinations(range(n), size):
            if any(set(com).issubset(set(existing)) for existing in circles):
                continue
            good = True
            s = 0
            for x in com:
                for y in com:
                    if x == y:
                        continue
                    s1 = result[players[x]][players[y]]
                    if s1 > 1:
                        good = False
                        break
                    s += s1
                if not good:
                    break
            if good:
                circles[tuple(com)] = s / (len(com) * (len(com) - 1))

    dyads = []
    used_in_circle = set()
    for c in circles:
        used_in_circle.update(c)

    for edge in edges:
        i, j = edge['i'], edge['j']
        if i in used_in_circle and j in used_in_circle:
            continue
        if all(i not in circle or j not in circle for circle in circles):
            dyads.append([i, j])

    circle_count = {}
    for circle in list(circles.keys()) + dyads:
        for idx in circle:
            circle_count[idx] = circle_count.get(idx, 0) + 1

    return {
        "circles": [[idx for idx in c] for c in circles],
        "dyads": dyads,
        "circle_count": circle_count,
        "edges": edges,
    }

def calc_in_groups(game, min_tolerance=4, max_tolerance=20):
    """
    Detect in-groups: player pairs that vote similarly for each other,
    with high mutual votes (above team average), but are NOT in safecircles
    because their votes are outside the current tolerance window.
    
    Tests for tolerance window range [min_tolerance, max_tolerance].
    """
    from .management.commands.utils import get_u5
    import statistics
    
    votes, n = get_u5(game)
    players = list(votes.keys())
    
    # Calculate safezone (same as in calc_circles)
    safezone = {}
    for player in votes:
        pvotes = votes[player]
        for power in pvotes:
            if power not in safezone:
                safezone[power] = 0
            cell = pvotes[power]
            for p in cell:
                score = cell[p]
                safezone[power] += score / (n * n)
    
    # Calculate team average for all votes
    all_votes = []
    for player in votes:
        for power_pair in votes[player]:
            for target in votes[player][power_pair]:
                all_votes.append(votes[player][power_pair][target])
    team_avg = statistics.mean(all_votes) if all_votes else 0
    
    # Get all safecircles for the tolerance range to exclude pairs already in circles
    # Only exclude if they are in safecircles at MULTIPLE tolerance values (stable safecircle)
    # This allows pairs that are only in safecircles at high tolerance to still be in-groups
    pair_circle_count = {}  # Track how many tolerance values each pair appears in circles
    for tolerance in range(min_tolerance, max_tolerance + 1):
        circles_data = calc_single(players, votes, n, safezone, tolerance)
        # Collect all pairs that are in circles at this tolerance
        pairs_at_tolerance = set()
        for circle in circles_data['circles']:
            for idx1 in circle:
                for idx2 in circle:
                    if idx1 < idx2:
                        pairs_at_tolerance.add((idx1, idx2))
        # Also check dyads
        for dyad in circles_data['dyads']:
            if len(dyad) == 2:
                i, j = sorted(dyad)
                pairs_at_tolerance.add((i, j))
        
        # Count occurrences
        for pair in pairs_at_tolerance:
            pair_circle_count[pair] = pair_circle_count.get(pair, 0) + 1
    
    # Exclude pairs that are in safecircles at more than half the tolerance range
    # (i.e., stable safecircles, not just appearing at high tolerance)
    threshold_count = (max_tolerance - min_tolerance + 1) // 2
    stable_circle_pairs = {pair for pair, count in pair_circle_count.items() 
                          if count > threshold_count}
    
    # Store safecircles per tolerance for filtering
    safecircles_per_tolerance = {}
    for tolerance in range(min_tolerance, max_tolerance + 1):
        circles_data = calc_single(players, votes, n, safezone, tolerance)
        pairs_at_tolerance = set()
        for circle in circles_data['circles']:
            for idx1 in circle:
                for idx2 in circle:
                    if idx1 < idx2:
                        pairs_at_tolerance.add((idx1, idx2))
        for dyad in circles_data['dyads']:
            if len(dyad) == 2:
                i, j = sorted(dyad)
                pairs_at_tolerance.add((i, j))
        safecircles_per_tolerance[tolerance] = pairs_at_tolerance
    
    in_groups = []
    
    # Check each player pair for each tolerance value
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = players[i], players[j]
            
            # Skip if in stable safecircle (appears in more than half the tolerance range)
            if (i, j) in stable_circle_pairs:
                continue
            
            # Get all votes from p1 to p2 and p2 to p1
            votes_p1_to_p2 = []
            votes_p2_to_p1 = []
            
            for power_pair in votes[p1]:
                if power_pair in votes[p1] and p2 in votes[p1][power_pair]:
                    votes_p1_to_p2.append(votes[p1][power_pair][p2])
            for power_pair in votes[p2]:
                if power_pair in votes[p2] and p1 in votes[p2][power_pair]:
                    votes_p2_to_p1.append(votes[p2][power_pair][p1])
            
            if not votes_p1_to_p2 or not votes_p2_to_p1:
                continue
            
            # Calculate average votes
            avg_p1_to_p2 = statistics.mean(votes_p1_to_p2)
            avg_p2_to_p1 = statistics.mean(votes_p2_to_p1)
            
            # Check similarity (how close are the votes?)
            similarity_diff = abs(avg_p1_to_p2 - avg_p2_to_p1)
            
            # Average of both votes must be above team average
            avg_of_both = (avg_p1_to_p2 + avg_p2_to_p1) / 2
            avg_above_team = avg_of_both > team_avg
            
            # Check for each tolerance value if this pair qualifies as in-group
            # The similarity_threshold equals the tolerance value
            # Find the lowest tolerance where it qualifies, and the highest tolerance where it still qualifies
            # An in-group stops existing when it enters a safecircle
            min_qualifying_tolerance = None
            max_qualifying_tolerance = None
            
            for tolerance in range(min_tolerance, max_tolerance + 1):
                similarity_threshold = tolerance  # Threshold equals tolerance value
                
                # Check if pair is in safecircle at this tolerance
                is_in_safecircle = (i, j) in safecircles_per_tolerance[tolerance]
                
                # If in safecircle, this is where the in-group stops (if it existed before)
                if is_in_safecircle:
                    if min_qualifying_tolerance is not None:
                        # We found the end of the in-group range
                        max_qualifying_tolerance = tolerance - 1
                        break
                    # If not in qualifying range yet, continue
                    continue
                
                is_similar = similarity_diff <= similarity_threshold
                
                # In-group criteria:
                # 1. Similar voting (difference <= tolerance value)
                # 2. Average of both votes above team average
                # 3. NOT in safecircle at this tolerance (already checked above)
                if is_similar and avg_above_team:
                    if min_qualifying_tolerance is None:
                        min_qualifying_tolerance = tolerance
                    # Continue to find the highest tolerance where it still qualifies
                    # (until it enters a safecircle, which we check above)
                    max_qualifying_tolerance = tolerance
            
            # If we found a qualifying range, add the in-group
            if min_qualifying_tolerance is not None:
                # If max is None, it means it qualifies up to max_tolerance (never entered a safecircle)
                if max_qualifying_tolerance is None:
                    max_qualifying_tolerance = max_tolerance
                
                in_groups.append({
                    'i': i,
                    'j': j,
                    'avg_p1_to_p2': round(avg_p1_to_p2, 1),
                    'avg_p2_to_p1': round(avg_p2_to_p1, 1),
                    'similarity': round(similarity_diff, 1),
                    'team_avg': round(team_avg, 1),
                    'similarity_threshold': min_qualifying_tolerance,  # Use the lowest threshold where it qualifies
                    'tolerance': min_qualifying_tolerance,  # Store the lowest tolerance where it was detected
                    'max_tolerance': max_qualifying_tolerance  # Store the highest tolerance where it still qualifies (before entering safecircle)
                })
    
    return in_groups
