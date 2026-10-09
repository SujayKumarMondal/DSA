import sys
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define Palette
PRIMARY = colors.HexColor("#1A365D")    # Deep Navy
SECONDARY = colors.HexColor("#2B6CB0")  # Slate Blue
ACCENT = colors.HexColor("#D69E2E")     # Warm Amber
DARK_TEXT = colors.HexColor("#2D3748")  # Charcoal
LIGHT_BG = colors.HexColor("#F7FAFC")   # Soft Off-White
BORDER_COLOR = colors.HexColor("#E2E8F0")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress header and footer on cover page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(DARK_TEXT)

        # Header
        self.drawString(54, 11 * 72 - 36, "90-DAY DSA MASTER ROADMAP (PYTHON) | MNC INTERVIEW PREPARATION")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL - PERSONAL PREPARATION CURRICULUM")
        self.line(54, 48, 8.5 * 72 - 54, 48)

        self.restoreState()

def build_pdf(filename="90_Day_DSA_Master_Roadmap_Python.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=PRIMARY,
        alignment=0,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=DARK_TEXT,
        alignment=0,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=PRIMARY,
        backColor=LIGHT_BG,
        borderColor=BORDER_COLOR,
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=8,
        spaceBefore=4
    )

    table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=DARK_TEXT
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("90-DAY DSA MASTER ROADMAP", title_style))
    story.append(Paragraph("A Rigorous, Python-First Curriculum Engineered for MNC & Product-Based Backend Software Engineering Interviews", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=3, color=ACCENT, spaceAfter=20))
    
    meta_data = [
        [Paragraph("<b>Target Role:</b> Python Backend / Software Engineer", body_style), Paragraph("<b>Total Duration:</b> 90 Days (12.8 Weeks)", body_style)],
        [Paragraph("<b>Start Date:</b> September 9, 2026", body_style), Paragraph("<b>End Date:</b> December 7, 2026", body_style)],
        [Paragraph("<b>Weekday Time Commitment:</b> 2.5 - 3.0 Hours/Day", body_style), Paragraph("<b>Weekend Time Commitment:</b> 5.0 Hours/Day", body_style)],
        [Paragraph("<b>Target Problem Count:</b> ~230 Selected Problems", body_style), Paragraph("<b>Primary Language:</b> Python 3.11+", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 40))

    story.append(Paragraph("Curriculum Architecture Highlights", h2_style))
    bullets = [
        "<b>Zero Hand-Waving:</b> Complete coverage of all 90 days with daily scheduled focus areas and problem targets.",
        "<b>Python-First Mastery:</b> Built entirely around idiomatic Python (built-ins, standard library modules like <code>collections</code>, <code>heapq</code>, <code>bisect</code>, and recursion memory profiling).",
        "<b>Interview-Centric Strategy:</b> Focused exclusively on pattern recognition, time-bounded problem-solving, and clean verbal articulation.",
        "<b>Spaced Repetition & Re-Solving:</b> Strict revision loops (3-day, 7-day, 21-day) to build intuition rather than rote memory.",
        "<b>Realistic Time Budgeting:</b> Precision workloads structured explicitly for working professionals (2.5-3 hrs M-F, 5 hrs Sat-Sun)."
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", body_style))
    
    story.append(PageBreak())

    # =========================================================================
    # 2. HOW TO USE & GOALS
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & How to Use This Roadmap", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=10))
    story.append(Paragraph(
        "This curriculum is engineered for backend developers aiming to clear coding interviews at Tier-1 MNCs, high-growth product companies, and top-tier startups. "
        "It treats Data Structures and Algorithms not as abstract competitive programming puzzles, but as practical engineering patterns.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Daily Execution Loop:</b> On weekdays, allocate 20 minutes to theory/pattern recognition, 60-90 minutes to active coding, 20 minutes to debugging/dry-running, and 15 minutes to documenting trade-offs in your mistake log. "
        "On weekends, use the 5-hour allocation for deep-dive topics, timed weekly assessments, and spaced-repetition re-solving.",
        body_style
    ))

    story.append(Paragraph("2. 90-Day Architecture & Phase Breakdown", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=10))

    phase_data = [
        [Paragraph("Phase", table_header), Paragraph("Dates / Days", table_header), Paragraph("Focus & Objectives", table_header), Paragraph("Target Problems", table_header)],
        [Paragraph("Phase 1: Foundations", table_text), Paragraph("Sept 09 - Sept 22<br/>(Days 1-14)", table_text), Paragraph("Python DSA primitives, complexity, Arrays, Strings, Two Pointers, Sliding Window, Prefix Sum.", table_text), Paragraph("35 Easy/Medium", table_text)],
        [Paragraph("Phase 2: Core Linear & Non-Linear", table_text), Paragraph("Sept 23 - Oct 13<br/>(Days 15-35)", table_text), Paragraph("Linked Lists, Stacks, Queues, Monotonic Structures, Binary Search, Trees, BSTs, Heaps/Top-K.", table_text), Paragraph("55 Medium/Hard", table_text)],
        [Paragraph("Phase 3: Graphs & Recursion", table_text), Paragraph("Oct 14 - Nov 03<br/>(Days 36-56)", table_text), Paragraph("Backtracking, Graph Traversals (BFS/DFS), Topological Sort, Union-Find, Shortest Paths (Dijkstra), Tries.", table_text), Paragraph("50 Medium/Hard", table_text)],
        [Paragraph("Phase 4: Dynamic Programming & Greedy", table_text), Paragraph("Nov 04 - Nov 24<br/>(Days 57-77)", table_text), Paragraph("Greedy Intervals, 1D DP, 2D Grid DP, Knapsack, Subsequences, State Machine DP.", table_text), Paragraph("50 Medium/Hard", table_text)],
        [Paragraph("Phase 5: Interview Bootcamp & Final Prep", table_text), Paragraph("Nov 25 - Dec 07<br/>(Days 78-90)", table_text), Paragraph("Mixed problem sets, timed mock interviews, weak spot repair, speed optimization, final assessment.", table_text), Paragraph("40 Mixed Medium/Hard", table_text)],
    ]
    t_phase = Table(phase_data, colWidths=[90, 80, 240, 94])
    t_phase.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG])
    ]))
    story.append(t_phase)
    story.append(Spacer(1, 15))

    # =========================================================================
    # 3. PYTHON FOR DSA CHEAT SHEET
    # =========================================================================
    story.append(Paragraph("3. Python-Specific DSA Essentials", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=10))

    py_data = [
        [Paragraph("Module / Feature", table_header), Paragraph("Key Use Cases in DSA", table_header), Paragraph("Time Complexity Highlights", table_header)],
        [Paragraph("<code>collections.deque</code>", table_text), Paragraph("Double-ended queue. Essential for BFS and Sliding Window Monotonic Queues.", table_text), Paragraph("Append/Pop left/right: O(1)<br/>Index lookup: O(N)", table_text)],
        [Paragraph("<code>heapq</code>", table_text), Paragraph("Min-Heap by default. Invert values for Max-Heap. Essential for Top-K and Dijkstra.", table_text), Paragraph("heappush / heappop: O(log N)<br/>heapify: O(N)", table_text)],
        [Paragraph("<code>bisect</code>", table_text), Paragraph("Binary search on sorted lists. <code>bisect_left</code>, <code>bisect_right</code>.", table_text), Paragraph("Search: O(log N)<br/>Insertion: O(N) due to shift", table_text)],
        [Paragraph("<code>functools.lru_cache</code>", table_text), Paragraph("Automatic memoization for Top-Down Dynamic Programming.", table_text), Paragraph("O(1) overhead per lookup", table_text)],
        [Paragraph("<code>collections.defaultdict</code>", table_text), Paragraph("Graph adjacency lists, grouping anagrams, hash maps with default collections.", table_text), Paragraph("Key lookup/insert: O(1) avg", table_text)]
    ]
    t_py = Table(py_data, colWidths=[120, 230, 154])
    t_py.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG])
    ]))
    story.append(t_py)
    story.append(Spacer(1, 15))

    # Python Code Example Template
    story.append(Paragraph("Idiomatic Python Template: Binary Search on Answer", h2_style))
    bs_code = """def binary_search_on_answer(arr, target_condition):
    low, high = min_possible_val, max_possible_val
    ans = low
    
    while low <= high:
        mid = (low + high) // 2
        if is_feasible(mid, arr, target_condition):
            ans = mid         # Feasible! Save answer and try to optimize further
            high = mid - 1    # E.g., searching for minimum possible max
        else:
            low = mid + 1     # Infeasible, increase bound
            
    return ans"""
    story.append(Paragraph(f"<pre>{bs_code}</pre>", code_style))

    story.append(PageBreak())

    # =========================================================================
    # 4. DAILY ROADMAP (ALL 90 DAYS GENERATED PROGRAMMATICALLY)
    # =========================================================================
    story.append(Paragraph("4. Complete 90-Day Daily Roadmap", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=10))

    start_date = datetime(2026, 9, 9)

    # Detailed Schedule Mapping for 90 Days
    # Structure: (Topic, Theory/Pattern Focus, Recommended Problems, Target Hours)
    curriculum_data = [
        # Phase 1: Foundations (Days 1-14)
        ("Big-O Analysis & Python Internals", "Time/Space Complexity, Recursion Limit, List vs Deque Memory", "Two Sum (LeetCode #1), Valid Anagram (#242)", "2.5 hrs"),
        ("Arrays & Two Pointers - Opposite Direction", "Left/Right pointer convergence on sorted arrays", "Two Sum II (#167), 3Sum (#15), Container With Most Water (#11)", "2.5 hrs"),
        ("Two Pointers - Fast & Slow Pointer", "Cycle detection, In-place array modification", "Remove Duplicates (#26), Move Zeroes (#283), Happy Number (#202)", "2.5 hrs"),
        ("Sliding Window - Fixed Size", "Maintain window state across contiguous subarrays", "Maximum Average Subarray I (#643), Permutation in String (#567)", "2.5 hrs"),
        ("Sliding Window - Variable Size (Max/Min)", "Expand right to satisfy condition, shrink left to optimize", "Minimum Size Subarray Sum (#209), Longest Substring Without Repeating Characters (#3)", "2.5 hrs"),
        ("Weekend Mastery: Two Pointers & Sliding Window", "Deep dive on edge cases, shrink conditions, multi-character sets", "Longest Repeating Character Replacement (#424), Subarrays with K Different Integers (#992)", "5.0 hrs"),
        ("Weekend Revision & Timed Test 1", "Weekly Review 1 + 60-min Timed Assessment on Two Pointers & Windows", "Re-solve missed problems; Test Set: 1 Easy, 2 Mediums", "5.0 hrs"),
        ("Prefix Sum Fundamentals", "Range sum queries in O(1) after O(N) precomputation", "Range Sum Query - Immutable (#303), Subarray Sum Equals K (#560)", "2.5 hrs"),
        ("Prefix Sum + Hash Map Combinations", "Handling negative numbers and modulo prefix sums", "Continuous Subarray Sum (#523), Subarray Sums Divisible by K (#974)", "2.5 hrs"),
        ("Strings & Hashing Techniques", "Custom hash keys, frequency maps, character array manipulation", "Group Anagrams (#49), Minimum Window Substring (#76)", "2.5 hrs"),
        ("Difference Array Pattern", "Range updates in O(1) time across array ranges", "Corporate Flight Bookings (#1109), Car Pooling (#1094)", "2.5 hrs"),
        ("Matrix Manipulation & Traversals", "2D grid indexing, in-place rotations, spiral orders", "Spiral Matrix (#54), Rotate Image (#48), Set Matrix Zeroes (#73)", "2.5 hrs"),
        ("Weekend Focus: Advanced Strings & Matrix", "String matching algorithms (KMP/Rabin-Karp concepts) & Grid transformations", "Find All Anagrams in a String (#438), Word Search Grid Prep (#79)", "5.0 hrs"),
        ("Weekend Revision & Timed Test 2", "Weekly Review 2 + 60-min Timed Assessment on Prefix Sums & Matrices", "Re-solve missed problems; Test Set: 3 Mediums", "5.0 hrs"),

        # Phase 2: Core Linear & Non-Linear (Days 15-35)
        ("Linked List Core & Two Pointers", "Singly/Doubly linked lists, dummy nodes, pointer mutation", "Reverse Linked List (#206), Merge Two Sorted Lists (#21)", "2.5 hrs"),
        ("Linked List Cycle & Fast/Slow Pointers", "Floyd's Cycle Detection algorithm and intersection discovery", "Linked List Cycle II (#142), Reorder List (#143)", "2.5 hrs"),
        ("Advanced Linked List Operations", "In-place group reversals, node swapping without extra memory", "Reverse Nodes in k-Group (#25), Copy List with Random Pointer (#138)", "2.5 hrs"),
        ("Stack Fundamentals & Matching", "LIFO execution, balanced parenthesis state matching", "Valid Parentheses (#20), Min Stack (#155), Evaluate Reverse Polish Notation (#150)", "2.5 hrs"),
        ("Monotonic Stack - Next Greater Element", "Maintaining monotonic decreasing/increasing order in stack", "Next Greater Element I (#496), Daily Temperatures (#739)", "2.5 hrs"),
        ("Weekend Focus: Monotonic Stack Applications", "Histogram area calculations, trapped water mechanics", "Largest Rectangle in Histogram (#84), Trapping Rain Water (#42)", "5.0 hrs"),
        ("Weekend Revision & Timed Test 3", "Weekly Review 3 + Timed Assessment on Linked Lists & Monotonic Stacks", "Test Set: 2 Mediums, 1 Hard", "5.0 hrs"),
        ("Binary Search - Standard Templates", "Lower bound, upper bound, avoiding integer overflow", "Binary Search (#704), Search in Rotated Sorted Array (#33)", "2.5 hrs"),
        ("Binary Search on Answer Space", "Monotonic predicate functions, searching boundary values", "Koko Eating Bananas (#875), Capacity To Ship Packages Within D Days (#1011)", "2.5 hrs"),
        ("Advanced Binary Search Patterns", "Median of two sorted arrays, split array largest sum", "Find Minimum in Rotated Sorted Array (#153), Split Array Largest Sum (#410)", "2.5 hrs"),
        ("Tree Fundamentals & Traversals", "Recursive DFS (Pre-order, In-order, Post-order), Iterative stack variants", "Binary Tree Inorder Traversal (#94), Maximum Depth of Binary Tree (#104)", "2.5 hrs"),
        ("Tree BFS & Level Order Traversal", "Queue-based level-by-level evaluation, zigzag patterns", "Binary Tree Level Order Traversal (#102), Binary Tree Right Side View (#199)", "2.5 hrs"),
        ("Weekend Deep-Dive: Tree Properties", "Lowest Common Ancestor, Tree construction from traversals", "Lowest Common Ancestor of a Binary Tree (#236), Construct Binary Tree from Preorder & Inorder (#105)", "5.0 hrs"),
        ("Weekend Revision & Timed Test 4", "Weekly Review 4 + Diagnostic Mock Assessment 1", "Diagnostic Mock Interview Set: 2 Mediums, Verbal Explanation Practice", "5.0 hrs"),
        ("Binary Search Trees (BST)", "BST properties, insertion, deletion, validation", "Validate Binary Search Tree (#98), Kth Smallest Element in a BST (#230)", "2.5 hrs"),
        ("Tree Path & Diameter Problems", "Bottom-up recursion, subtree sum tracking", "Diameter of Binary Tree (#543), Binary Tree Maximum Path Sum (#124)", "2.5 hrs"),
        ("Heaps / Priority Queues Fundamentals", "Binary heap representation, <code>heapq</code> in Python", "Kth Largest Element in an Array (#215), Top K Frequent Elements (#347)", "2.5 hrs"),
        ("Two Heaps Pattern", "Maintaining streaming median using min-heap and max-heap", "Find Median from Data Stream (#295), Sliding Window Median (#480)", "2.5 hrs"),
        ("K-Way Merge & Monotonic Queue", "Merging sorted streams, sliding window maximums", "Merge k Sorted Lists (#23), Sliding Window Maximum (#239)", "2.5 hrs"),
        ("Weekend Mastery: Heaps & Complex Trees", "Serialize and deserialize trees, hard heap problems", "Serialize and Deserialize Binary Tree (#297), Smallest Range Covering Elements from K Lists (#632)", "5.0 hrs"),
        ("Weekend Revision & Timed Test 5", "Weekly Review 5 + Timed Assessment on Trees & Heaps", "Test Set: 3 Mediums", "5.0 hrs"),

        # Phase 3: Graphs & Recursion (Days 36-56)
        ("Recursion & Backtracking Foundations", "Decision trees, base cases, state backtracking", "Subsets (#78), Subsets II (#90)", "2.5 hrs"),
        ("Backtracking - Combinations & Permutations", "Pruning search space, handling duplicate elements", "Permutations (#46), Combination Sum (#39)", "2.5 hrs"),
        ("Backtracking - Grid & Puzzle Search", "2D matrix paths, constraint satisfaction", "Word Search (#79), N-Queens (#51)", "2.5 hrs"),
        ("Graph Representation & BFS", "Adjacency lists, level-by-level shortest path in unweighted graphs", "Clone Graph (#133), Number of Islands (#200)", "2.5 hrs"),
        ("Graph DFS & Connected Components", "Visited tracking, cycle detection in undirected graphs", "Max Area of Island (#695), Surrounding Regions (#130)", "2.5 hrs"),
        ("Weekend Deep-Dive: Advanced Graph Traversals", "Bipartite graph checking, 0-1 BFS with Deque", "Is Graph Bipartite? (#785), Shortest Path in Binary Matrix (#1091)", "5.0 hrs"),
        ("Weekend Revision & Timed Test 6", "Weekly Review 6 + Timed Assessment on Backtracking & Basic Graphs", "Test Set: 2 Mediums, 1 Hard", "5.0 hrs"),
        ("Cycle Detection & Topological Sort (Kahn's)", "In-degree tracking, DAG ordering", "Course Schedule (#207), Course Schedule II (#210)", "2.5 hrs"),
        ("Topological Sort via DFS", "Post-order DFS state coloring (Unvisited, Visiting, Visited)", "Alien Dictionary (#269), Find Eventual Safe States (#802)", "2.5 hrs"),
        ("Disjoint Set Union (DSU / Union-Find)", "Path compression, union by rank", "Number of Connected Components in Undirected Graph (#323), Redundant Connection (#684)", "2.5 hrs"),
        ("DSU Advanced Applications", "Dynamic connectivity, grid components", "Accounts Merge (#721), Number of Islands II (#305)", "2.5 hrs"),
        ("Shortest Path - Dijkstra's Algorithm", "Weighted graphs with non-negative edge weights using <code>heapq</code>", "Network Delay Time (#743), Path with Minimum Effort (#1631)", "2.5 hrs"),
        ("Weekend Deep-Dive: Shortest Path Variations", "Cheapest Flights Within K Stops, Bellman-Ford/Floyd-Warshall theory", "Cheapest Flights Within K Stops (#787), Swim in Rising Water (#778)", "5.0 hrs"),
        ("Weekend Revision & Timed Test 7", "Weekly Review 7 + Mid-Program Diagnostic Mock Interview", "Mid-Program Mock: 2 Mediums, 1 System Design / DSA crossover", "5.0 hrs"),
        ("Minimum Spanning Tree (MST)", "Prim's & Kruskal's Algorithms", "Min Cost to Connect All Points (#1584), Critical Connections in a Network (#1192)", "2.5 hrs"),
        ("Trie (Prefix Tree) Foundations", "TrieNode structure, insert, search, startsWith", "Implement Trie (Prefix Tree) (#208), Design Add and Search Words Data Structure (#211)", "2.5 hrs"),
        ("Trie Applications & Hard Problems", "Bitwise XOR tries, dynamic word searching", "Word Search II (#212), Maximum XOR of Two Numbers in an Array (#421)", "2.5 hrs"),
        ("Bit Manipulation - Basics & Bitmasking", "XOR properties, bit shifts, clearing/setting bits", "Single Number (#136), Number of 1 Bits (#191), Counting Bits (#338)", "2.5 hrs"),
        ("Bitmasking Applications", "Representing sets as integers in DP/Backtracking", "Subsets using Bitmasking, Minimum XOR Sum of Two Arrays (#1879)", "2.5 hrs"),
        ("Weekend Mastery: Advanced Graph & Bit Manipulation", "Complex graph patterns, bitmask DP prep", "Reconstruct Itinerary (#332), Shortest Path Visiting All Nodes (#847)", "5.0 hrs"),
        ("Weekend Revision & Timed Test 8", "Weekly Review 8 + Timed Assessment on Graphs, Tries & Bitmasking", "Test Set: 3 Mediums", "5.0 hrs"),

        # Phase 4: Dynamic Programming & Greedy (Days 57-77)
        ("Greedy Strategy Fundamentals", "Local optimal choices leading to global optimum, proof techniques", "Assign Cookies (#455), Gas Station (#134)", "2.5 hrs"),
        ("Greedy Intervals - Overlap & Merging", "Sorting by start/end times, interval consolidation", "Merge Intervals (#56), Non-overlapping Intervals (#435)", "2.5 hrs"),
        ("Greedy Intervals - Scheduling & Meeting Rooms", "Min platforms/rooms allocation", "Meeting Rooms II (#253), Minimum Number of Arrows to Burst Balloons (#452)", "2.5 hrs"),
        ("Dynamic Programming - 1D Core", "Memoization vs Tabulation, identifying subproblems", "Climbing Stairs (#70), House Robber (#198), House Robber II (#213)", "2.5 hrs"),
        ("1D DP - Subsequences & Partitioning", "Unbounded vs bounded choices", "Coin Change (#322), Word Break (#139), Decode Ways (#91)", "2.5 hrs"),
        ("Weekend Focus: Longest Increasing Subsequence (LIS)", "O(N^2) DP to O(N log N) binary search solution", "Longest Increasing Subsequence (#300), Russian Doll Envelopes (#354)", "5.0 hrs"),
        ("Weekend Revision & Timed Test 9", "Weekly Review 9 + Timed Assessment on Greedy & 1D DP", "Test Set: 3 Mediums", "5.0 hrs"),
        ("2D Grid DP - Paths & Minimum Cost", "Grid traversals with directional moves", "Unique Paths (#62), Minimum Path Sum (#64)", "2.5 hrs"),
        ("2D Grid DP - Advanced Constraints", "Dungeon Game, grid paths with obstacles", "Unique Paths II (#63), Dungeon Game (#174)", "2.5 hrs"),
        ("Knapsack DP - 0/1 Knapsack Pattern", "Subset sum, equal partition matching", "Partition Equal Subset Sum (#416), Target Sum (#494)", "2.5 hrs"),
        ("Knapsack DP - Unbounded Knapsack", "Infinite supply items, rod cutting", "Coin Change II (#518), Combination Sum IV (#377)", "2.5 hrs"),
        ("String DP - Longest Common Subsequence (LCS)", "Two-pointer string DP matrix alignment", "Longest Common Subsequence (#1143), Edit Distance (#72)", "2.5 hrs"),
        ("Weekend Mastery: String DP & Palindromes", "Palindromic subproblems, interval DP", "Longest Palindromic Substring (#5), Palindromic Substrings (#647), Distinct Subsequences (#115)", "5.0 hrs"),
        ("Weekend Revision & Timed Test 10", "Weekly Review 10 + Advanced Diagnostic Mock Interview", "Advanced Mock: 1 Medium, 1 Hard with full interview communication", "5.0 hrs"),
        ("DP with Stock Trading State Machines", "State transitions (Hold, Unhold, Cooldown, Fee)", "Best Time to Buy and Sell Stock with Cooldown (#309), Best Time to Buy and Sell Stock IV (#188)", "2.5 hrs"),
        ("Interval DP Pattern", "Solving subproblems on sub-ranges [i...j]", "Burst Balloons (#312), Matrix Chain Multiplication", "2.5 hrs"),
        ("Tree DP Fundamentals", "Subtree state computation, bottom-up DP on trees", "House Robber III (#337), Tree Diameter via DP", "2.5 hrs"),
        ("Bitmask DP", "Traveling Salesperson Problem (TSP) style states", "Can I Win (#464), Matchsticks to Square (#473)", "2.5 hrs"),
        ("DP Optimization Techniques", "Space optimization from O(N^2) to O(N) using rolling arrays", "Space-optimized LCS & Knapsack re-implementations", "2.5 hrs"),
        ("Weekend Focus: Complex DP Consolidation", "Systematic approach to identifying DP transitions under pressure", "Regular Expression Matching (#10), Wildcard Matching (#44)", "5.0 hrs"),
        ("Weekend Revision & Timed Test 11", "Weekly Review 11 + Timed Assessment on Advanced DP", "Test Set: 2 Mediums, 1 Hard", "5.0 hrs"),

        # Phase 5: Interview Bootcamp & Final Prep (Days 78-90)
        ("Bootcamp: Mixed Array & Two Pointer Speed Run", "Speed solving, verbalizing optimal trade-offs within 15 mins", "3 Unseen Medium Problems under 20-min timers", "2.5 hrs"),
        ("Bootcamp: Mixed Graph & Tree Blitz", "Identifying BFS vs DFS vs DSU instantly", "3 Unseen Medium/Hard Graph Problems", "2.5 hrs"),
        ("Bootcamp: Mixed DP & Greedy Blitz", "Distinguishing Greedy vs DP choices", "3 Unseen Medium DP Problems", "2.5 hrs"),
        ("Bootcamp: Hard Problem Strategies", "Partial credit strategies, simplifying constraints", "Sliding Window Maximum (#239), Alien Dictionary (#269)", "2.5 hrs"),
        ("Bootcamp: Full Interview Simulation 1", "Real-time interview simulation (45 mins per problem)", "Simulated Round 1: 2 Medium Problems + Verbal Communication", "2.5 hrs"),
        ("Weekend Bootcamp: Full Mock Coding Marathon", "4-hour continuous coding round simulation covering 4 mixed topics", "Full Mock Set: Array, Graph, DP, System-style DSA", "5.0 hrs"),
        ("Weekend Bootcamp: Weak Spot Surgical Repair", "Targeted repair based on mistake log history", "Re-solving 5 lowest-confidence problems from log", "5.0 hrs"),
        ("Bootcamp: Full Interview Simulation 2", "Real-time interview simulation (MNC Tier-1 standard)", "Simulated Round 2: 1 Medium, 1 Hard Problem", "2.5 hrs"),
        ("Bootcamp: Edge Case & Bug Hunting Drills", "Identifying off-by-one errors, null pointers, integer overflows", "10 buggy code snippets to audit and fix in Python", "2.5 hrs"),
        ("Bootcamp: Python DSA Speed Optimization", "In-place ops, list comprehensions vs generators, fast I/O", "Refactoring past code for maximum speed and clean syntax", "2.5 hrs"),
        ("Bootcamp: Ultimate Pattern Cheat Sheet Memorization", "Trigger word recognition (e.g. 'Shortest Path Unweighted' -> BFS)", "Pattern drill quiz across all 50 major patterns", "2.5 hrs"),
        ("Bootcamp: Final Full-Length Mock Interview", "External or simulated peer interview with full evaluation rubric", "2 Mixed Medium/Hard Problems with edge-case testing", "5.0 hrs"),
        ("DAY 90: GRADUATION & MNC READINESS ASSESSMENT", "Final Assessment, Complete Progress Audit, Next 30-Day Maintenance Plan", "Final Mixed Assessment Test + Review of Readiness Checklist", "5.0 hrs")
    ]

    for day_idx in range(90):
        day_num = day_idx + 1
        current_date = start_date + timedelta(days=day_idx)
        date_str = current_date.strftime("%b %d, %Y (%a)")
        
        # Determine Phase
        if day_num <= 14:
            phase_str = "Phase 1: Foundations"
        elif day_num <= 35:
            phase_str = "Phase 2: Core Linear & Non-Linear"
        elif day_num <= 56:
            phase_str = "Phase 3: Graphs & Recursion"
        elif day_num <= 77:
            phase_str = "Phase 4: DP & Greedy"
        else:
            phase_str = "Phase 5: Final Bootcamp"

        topic_info = curriculum_data[day_idx]
        
        # Format table for each day
        day_table_data = [
            [Paragraph(f"<b>DAY {day_num}: {date_str}</b>", table_header), Paragraph(f"<b>{phase_str}</b>", table_header)],
            [Paragraph("<b>Topic Focus:</b>", table_text), Paragraph(f"{topic_info[0]}", table_text)],
            [Paragraph("<b>Theory / Pattern:</b>", table_text), Paragraph(f"{topic_info[1]}", table_text)],
            [Paragraph("<b>Target Problems:</b>", table_text), Paragraph(f"{topic_info[2]}", table_text)],
            [Paragraph("<b>Allocated Time:</b>", table_text), Paragraph(f"{topic_info[3]}", table_text)]
        ]
        
        t_day = Table(day_table_data, colWidths=[110, 394])
        t_day.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), SECONDARY if current_date.weekday() < 5 else PRIMARY),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('PADDING', (0,0), (-1,-1), 4),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG])
        ]))
        
        story.append(KeepTogether([t_day, Spacer(1, 8)]))

    story.append(PageBreak())

    # =========================================================================
    # 5. PATTERN RECOGNITION CHEAT SHEET & TEMPLATES
    # =========================================================================
    story.append(Paragraph("5. Pattern Recognition Cheat Sheet", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=10))

    cheat_data = [
        [Paragraph("Problem Clue / Trigger", table_header), Paragraph("Primary Pattern", table_header), Paragraph("Data Structure / Method", table_header)],
        [Paragraph("Contiguous array + Target sum / Max length", table_text), Paragraph("Sliding Window / Prefix Sum", table_text), Paragraph("Two Pointers / Hash Map", table_text)],
        [Paragraph("Sorted array + Pair target / Duplicate removal", table_text), Paragraph("Two Pointers", table_text), Paragraph("Opposite / Fast-Slow Pointers", table_text)],
        [Paragraph("Top K elements / Streaming values", table_text), Paragraph("Heap / Priority Queue", table_text), Paragraph("Min-Heap / Max-Heap (<code>heapq</code>)", table_text)],
        [Paragraph("Next greater/smaller element / Histogram area", table_text), Paragraph("Monotonic Stack", table_text), Paragraph("Stack storing indices", table_text)],
        [Paragraph("Shortest path on unweighted graph/grid", table_text), Paragraph("Breadth-First Search (BFS)", table_text), Paragraph("<code>collections.deque</code>", table_text)],
        [Paragraph("Shortest path on weighted graph (non-negative)", table_text), Paragraph("Dijkstra's Algorithm", table_text), Paragraph("Min-Heap + Distance Array", table_text)],
        [Paragraph("Dependencies / Task scheduling / DAG order", table_text), Paragraph("Topological Sort", table_text), Paragraph("Kahn's (In-degree) / DFS State", table_text)],
        [Paragraph("Dynamic connectivity / Disjoint groups", table_text), Paragraph("Union-Find (DSU)", table_text), Paragraph("Parent array + Rank/Size", table_text)],
        [Paragraph("Prefix matching / Autocomplete / XOR max", table_text), Paragraph("Trie", table_text), Paragraph("TrieNode with Dict children", table_text)],
        [Paragraph("Count ways / Min cost to reach state / Subarrays", table_text), Paragraph("Dynamic Programming", table_text), Paragraph("1D/2D DP array or Memoization", table_text)]
    ]
    t_cheat = Table(cheat_data, colWidths=[180, 160, 164])
    t_cheat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG])
    ]))
    story.append(t_cheat)
    story.append(Spacer(1, 15))

    # Dynamic Programming Template
    story.append(Paragraph("Idiomatic Python Template: Top-Down DP with LRU Cache", h2_style))
    dp_code = """from functools import lru_cache

def solve_dp_problem(arr):
    @lru_cache(maxsize=None)
    def dp(idx, state_param):
        # Base Cases
        if idx >= len(arr):
            return 0
            
        # Transition Choices
        option1 = dp(idx + 1, state_param)
        option2 = arr[idx] + dp(idx + 1, new_state)
        
        return max(option1, option2)
        
    return dp(0, initial_state)"""
    story.append(Paragraph(f"<pre>{dp_code}</pre>", code_style))

    story.append(Spacer(1, 15))

    # =========================================================================
    # 6. MISTAKE TRACKER & READINESS CHECKLIST
    # =========================================================================
    story.append(Paragraph("6. Mistake Log & Spaced Repetition System", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=10))
    story.append(Paragraph(
        "Never resolve a problem without logging your failure mode. Categorize every error using these 5 categories:",
        body_style
    ))
    
    mistakes = [
        "<b>1. Concept Gap:</b> Didn't know the underlying algorithm or data structure property.",
        "<b>2. Pattern Recognition Failure:</b> Knew the concept but failed to map problem clues to the pattern.",
        "<b>3. Logic Error:</b> Correct pattern, but incorrectly implemented condition/transition (e.g., off-by-one).",
        "<b>4. Edge Case Failure:</b> Solution failed on empty input, single element, negative numbers, or integer bounds.",
        "<b>5. Time/Space Management Failure:</b> Solved correctly but exceeded time limit (TLE) or memory limit (MLE)."
    ]
    for m in mistakes:
        story.append(Paragraph(f"• {m}", body_style))

    story.append(Spacer(1, 15))
    story.append(Paragraph("7. MNC Interview Readiness Final Checklist", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=10))

    readiness_items = [
        [Paragraph("[  ]", table_header), Paragraph("Readiness Criterion", table_header), Paragraph("Target Standard", table_header)],
        [Paragraph("[  ]", table_text), Paragraph("Problem Solving Velocity", table_text), Paragraph("Easy: &lt;10 mins | Medium: 20-25 mins | Hard: 40 mins", table_text)],
        [Paragraph("[  ]", table_text), Paragraph("Complexity Articulation", table_text), Paragraph("Instantly state Big-O Time & Space before typing code", table_text)],
        [Paragraph("[  ]", table_text), Paragraph("Python Built-in Fluency", table_text), Paragraph("Zero hesitation using <code>heapq</code>, <code>collections</code>, <code>bisect</code>", table_text)],
        [Paragraph("[  ]", table_text), Paragraph("Verbal Communication", table_text), Paragraph("Thinking out loud continuously; leading interviewer through solution tree", table_text)],
        [Paragraph("[  ]", table_text), Paragraph("Dry-Running Discipline", table_text), Paragraph("Testing code against edge cases manually before pressing Run/Submit", table_text)],
        [Paragraph("[  ]", table_text), Paragraph("Pattern Library Mastery", table_text), Paragraph("Can identify core pattern for 90%+ of unseen Medium problems in &lt;3 mins", table_text)]
    ]
    t_ready = Table(readiness_items, colWidths=[30, 210, 254])
    t_ready.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG])
    ]))
    story.append(t_ready)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_pdf()
    
    
#------------------------------------------------------------------#
    
    
    
    
    

import os

# Base directory path
base_dir = r"D:\SUJAY\DSA_New"

# Files required inside Day_01
day_01_files = [
    "theory.md",
    "patterns.md",
    "solutions.py",
    "dry_run.md",
    "mistake_log.md",
    "interview_notes.md",
]

# Create Day_01 folder and its files
day_01_path = os.path.join(base_dir, "Day_01")
os.makedirs(day_01_path, exist_ok=True)

for file_name in day_01_files:
    file_path = os.path.join(day_01_path, file_name)
    with open(file_path, "w") as f:
        pass  # Creates an empty file

# Create folders from Day_02 to Day_90
for i in range(2, 91):
    day_folder = os.path.join(base_dir, f"Day_{i:02d}")
    os.makedirs(day_folder, exist_ok=True)

print("Folders and files created successfully.")

