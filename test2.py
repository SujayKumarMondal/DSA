from pathlib import Path


# ============================================================
# DSA 351 PROBLEM FILE GENERATOR
# Run this script from the directory where you want the
# complete DSA folder structure to be created.
# ============================================================

BASE_DIR = Path.cwd()


sections = {
    "01_Arrays_Hashing": [
        "Two Sum",
        "Best Time to Buy and Sell Stock",
        "Single Number",
        "Majority Element",
        "Contains Duplicate",
        "Missing Number",
        "Move Zeroes",
        "Find All Numbers Disappeared in an Array",
        "Maximum Subarray",
        "Product of Array Except Self",
        "Longest Consecutive Sequence",
        "Find All Duplicates in an Array",
        "Maximum Product Subarray",
        "Rotate Array",
        "First Missing Positive",
        "Kth Largest Element in an Array",
        "Top K Frequent Elements",
        "Subarray Sum Equals K",
        "Maximum Size Subarray Sum Equals k",
        "Continuous Subarray Sum",
        "Majority Element II",
        "Find the Difference of Two Arrays",
        "Intersection of Two Arrays",
        "Intersection of Two Arrays II",
        "Longest Harmonious Subsequence",
        "Sort an Array",
    ],

    "02_Strings": [
        "Valid Anagram",
        "Valid Palindrome",
        "Longest Substring Without Repeating Characters",
        "Longest Palindromic Substring",
        "Is Subsequence",
        "Backspace String Compare",
        "Decode Ways",
        "Palindrome Partitioning",
        "Group Anagrams",
        "Longest Common Subsequence",
        "Minimum Window Substring",
        "Permutation in String",
        "Longest Repeating Character Replacement",
        "Palindromic Substrings",
        "Longest Common Prefix",
        "Reverse Words in a String",
        "String Compression",
        "Find the Index of the First Occurrence in a String",
        "Isomorphic Strings",
        "Word Pattern",
        "Valid Palindrome II",
        "Partition Labels",
        "Longest Palindrome",
        "String to Integer (atoi)",
    ],

    "03_Two_Pointers": [
        "Container With Most Water",
        "3Sum",
        "3Sum Closest",
        "Squares of a Sorted Array",
        "Valid Palindrome",
        "Trapping Rain Water",
        "Find K Closest Elements",
        "Interval List Intersections",
        "Two Sum II - Input Array Is Sorted",
        "3Sum Smaller",
        "Remove Duplicates from Sorted Array",
        "Remove Element",
        "Move Zeroes",
        "Sort Colors",
        "Boats to Save People",
    ],

    "04_Sliding_Window": [
        "Maximum Average Subarray I",
        "Longest Substring Without Repeating Characters",
        "Minimum Size Subarray Sum",
        "Longest Repeating Character Replacement",
        "Permutation in String",
        "Subarray Product Less Than K",
        "Fruit Into Baskets",
        "Substring with Concatenation of All Words",
        "Minimum Window Substring",
        "Sliding Window Maximum",
        "Sliding Window Median",
        "Maximum Consecutive Ones III",
        "Longest Subarray of 1's After Deleting One Element",
        "Minimum Window Subsequence",
        "Longest Substring with At Most K Distinct Characters",
        "Subarrays with K Different Integers",
        "Permutation in String",
    ],

    "05_Stack": [
        "Valid Parentheses",
        "Backspace String Compare",
        "Maximum Frequency Stack",
        "Trapping Rain Water",
        "Min Stack",
        "Evaluate Reverse Polish Notation",
        "Daily Temperatures",
        "Next Greater Element I",
        "Next Greater Element II",
        "Largest Rectangle in Histogram",
        "Asteroid Collision",
        "Online Stock Span",
        "Remove K Digits",
        "Decode String",
        "Basic Calculator II",
    ],

    "06_Linked_List": [
        "Merge Two Sorted Lists",
        "Remove Duplicates from Sorted List",
        "Linked List Cycle",
        "Remove Linked List Elements",
        "Reverse Linked List",
        "Palindrome Linked List",
        "Middle of the Linked List",
        "Add Two Numbers",
        "Remove Nth Node From End of List",
        "Swap Nodes in Pairs",
        "Rotate List",
        "Reverse Linked List II",
        "Linked List Cycle II",
        "Reorder List",
        "Sort List",
        "Odd Even Linked List",
        "Merge k Sorted Lists",
        "Reverse Nodes in k-Group",
        "Intersection of Two Linked Lists",
        "Remove Duplicates from Sorted List II",
        "Copy List with Random Pointer",
        "LRU Cache",
    ],

    "07_Binary_Search": [
        "Binary Search",
        "Search in Rotated Sorted Array",
        "Search in Rotated Sorted Array II",
        "Find Minimum in Rotated Sorted Array",
        "Find Peak Element",
        "Minimum Size Subarray Sum",
        "Search a 2D Matrix",
        "Search a 2D Matrix II",
        "Kth Smallest Element in a Sorted Matrix",
        "Find K Closest Elements",
        "Peak Index in a Mountain Array",
        "Median of Two Sorted Arrays",
        "First Bad Version",
        "Search Insert Position",
        "Find First and Last Position of Element in Sorted Array",
        "Sqrt(x)",
        "Koko Eating Bananas",
        "Capacity To Ship Packages Within D Days",
        "Find Minimum in Rotated Sorted Array II",
        "Time Based Key-Value Store",
        "Split Array Largest Sum",
    ],

    "08_Trees_Binary_Trees": [
        "Same Tree",
        "Maximum Depth of Binary Tree",
        "Minimum Depth of Binary Tree",
        "Path Sum",
        "Invert Binary Tree",
        "Binary Tree Paths",
        "Subtree of Another Tree",
        "Merge Two Binary Trees",
        "Average of Levels in Binary Tree",
        "Validate Binary Search Tree",
        "Binary Tree Level Order Traversal",
        "Binary Tree Zigzag Level Order Traversal",
        "Construct Binary Tree from Preorder and Inorder Traversal",
        "Path Sum II",
        "Binary Tree Right Side View",
        "Kth Smallest Element in a BST",
        "Lowest Common Ancestor of a BST",
        "Lowest Common Ancestor of a Binary Tree",
        "Path Sum III",
        "Maximum Binary Tree",
        "Maximum Width of Binary Tree",
        "All Nodes Distance K in Binary Tree",
        "Binary Tree Maximum Path Sum",
        "Serialize and Deserialize Binary Tree",
        "Binary Tree Inorder Traversal",
        "Binary Tree Preorder Traversal",
        "Binary Tree Postorder Traversal",
        "Diameter of Binary Tree",
        "Balanced Binary Tree",
        "Symmetric Tree",
        "Populating Next Right Pointers in Each Node",
        "Convert Sorted Array to Binary Search Tree",
        "Delete Node in a BST",
        "Validate Binary Search Tree",
        "Flatten Binary Tree to Linked List",
    ],

    "09_Graph": [
        "Number of Islands",
        "Course Schedule",
        "Course Schedule II",
        "Graph Valid Tree",
        "Minimum Height Trees",
        "Number of Connected Components in an Undirected Graph",
        "Clone Graph",
        "Pacific Atlantic Water Flow",
        "Alien Dictionary",
        "Flood Fill",
        "Rotting Oranges",
        "Surrounded Regions",
        "Number of Provinces",
        "Max Area of Island",
        "Word Ladder",
        "Open the Lock",
        "Redundant Connection",
        "Accounts Merge",
        "Number of Operations to Make Network Connected",
        "Most Stones Removed with Same Row or Column",
        "Network Delay Time",
        "Cheapest Flights Within K Stops",
        "Path With Minimum Effort",
        "Swim in Rising Water",
        "Min Cost to Connect All Points",
    ],

    "10_Heap_Priority_Queue": [
        "Kth Largest Element in an Array",
        "Top K Frequent Elements",
        "Find K Pairs with Smallest Sums",
        "Kth Smallest Element in a Sorted Matrix",
        "K Closest Points to Origin",
        "Merge k Sorted Lists",
        "Find Median from Data Stream",
        "Rearrange String k Distance Apart",
        "Sliding Window Median",
        "Smallest Range Covering Elements from K Lists",
        "Employee Free Time",
        "Last Stone Weight",
        "Kth Largest Element in a Stream",
        "Task Scheduler",
        "IPO",
        "Find K Closest Elements",
    ],

    "11_Backtracking": [
        "Letter Combinations of a Phone Number",
        "Generate Parentheses",
        "Combination Sum",
        "Combination Sum II",
        "Permutations",
        "Permutations II",
        "Combinations",
        "Subsets",
        "Word Search",
        "Subsets II",
        "Combination Sum III",
        "Factor Combinations",
        "Target Sum",
        "Partition to K Equal Sum Subsets",
        "Letter Case Permutation",
        "Sudoku Solver",
        "N-Queens",
        "Word Search II",
        "Word Squares",
        "Palindrome Partitioning II",
        "Restore IP Addresses",
        "Matchsticks to Square",
        "Beautiful Arrangement",
        "Combination Sum IV",
    ],

    "12_Dynamic_Programming": [
        "Climbing Stairs",
        "Counting Bits",
        "Maximum Subarray",
        "Unique Paths",
        "Decode Ways",
        "Word Break",
        "House Robber",
        "House Robber II",
        "Coin Change",
        "Combination Sum IV",
        "Partition Equal Subset Sum",
        "Target Sum",
        "Longest Increasing Subsequence",
        "Longest Common Subsequence",
        "Maximum Product Subarray",
        "Best Time to Buy and Sell Stock with Cooldown",
        "Number of Longest Increasing Subsequences",
        "Count Unique Characters of All Substrings of a Given String",
        "Min Cost Climbing Stairs",
        "House Robber",
        "Decode Ways II",
        "Perfect Squares",
        "Integer Break",
        "0/1 Knapsack",
        "Partition Equal Subset Sum",
        "Last Stone Weight II",
        "Coin Change II",
        "Minimum Path Sum",
        "Unique Paths II",
        "Triangle",
        "Edit Distance",
        "Distinct Subsequences",
        "Word Break II",
    ],

    "13_Greedy": [
        "Jump Game",
        "Gas Station",
        "Non-overlapping Intervals",
        "Minimum Number of Arrows to Burst Balloons",
        "Task Scheduler",
        "Reorganize String",
        "Rearrange String k Distance Apart",
        "Employee Free Time",
        "Jump Game II",
        "Partition Labels",
        "Assign Cookies",
        "Merge Triplets to Form Target Triplet",
        "Hand of Straights",
        "Maximum Units on a Truck",
        "Candy",
        "Non-decreasing Array",
    ],

    "14_Trie": [
        "Implement Trie",
        "Design Add and Search Words Data Structure",
        "Word Search II",
        "Word Squares",
        "Concatenated Words",
        "Design Search Autocomplete System",
        "Prefix and Suffix Search",
        "Implement Trie II",
        "Replace Words",
        "Maximum XOR of Two Numbers in an Array",
    ],

    "15_Bit_Manipulation": [
        "Single Number",
        "Counting Bits",
        "Number of 1 Bits",
        "Reverse Bits",
        "Sum of Two Integers",
        "Single Number II",
        "Missing Number",
        "Power of Two",
        "Counting Bits",
        "Reverse Integer",
        "Bitwise AND of Numbers Range",
        "Subsets",
    ],

    "16_Intervals": [
        "Meeting Rooms",
        "Merge Intervals",
        "Insert Interval",
        "Meeting Rooms II",
        "Non-overlapping Intervals",
        "Minimum Number of Arrows to Burst Balloons",
        "Interval List Intersections",
        "Employee Free Time",
        "Minimum Number of Platforms",
        "Remove Covered Intervals",
        "Data Stream as Disjoint Intervals",
    ],

    "17_Prefix_Sum": [
        "Range Sum Query - Immutable",
        "Product of Array Except Self",
        "Subarray Sum Equals K",
        "Maximum Size Subarray Sum Equals k",
        "Continuous Subarray Sum",
        "Range Sum Query 2D - Immutable",
        "Subarray Sums Divisible by K",
        "Corporate Flight Bookings",
        "Car Pooling",
    ],

    "18_Fast_Slow_Pointer": [
        "Linked List Cycle",
        "Linked List Cycle II",
        "Middle of the Linked List",
        "Palindrome Linked List",
        "Reorder List",
        "Happy Number",
        "Find the Duplicate Number",
    ],

    "19_Cyclic_Sort": [
        "Missing Number",
        "Find All Numbers Disappeared in an Array",
        "Find All Duplicates in an Array",
        "Set Mismatch",
        "First Missing Positive",
        "Find the Duplicate Number",
    ],

    "20_Union_Find_DSU": [
        "Number of Connected Components in an Undirected Graph",
        "Graph Valid Tree",
        "Redundant Connection",
        "Accounts Merge",
        "Number of Operations to Make Network Connected",
        "Most Stones Removed with Same Row or Column",
        "Min Cost to Connect All Points",
    ],
}


def clean_filename(name):
    """Convert problem name into a safe Python filename."""
    replacements = {
        "'": "",
        '"': "",
        "(": "",
        ")": "",
        "/": "_",
        "-": "_",
        "–": "_",
        "—": "_",
        ",": "",
        ".": "",
        ":": "",
    }

    for old, new in replacements.items():
        name = name.replace(old, new)

    # Replace spaces with underscores
    name = name.replace(" ", "_")

    # Remove duplicate underscores
    while "__" in name:
        name = name.replace("__", "_")

    return name


def create_file(file_path, number, problem, section):
    content = f'''"""
Problem {number}: {problem}

Category: {section}

LeetCode / Interview Problem
"""


# ============================================================
# Problem
# ============================================================

# {problem}


# ============================================================
# Approach
# ============================================================

# TODO:
# Explain your approach here.


# ============================================================
# Solution
# ============================================================

def solution():
    pass


# ============================================================
# Complexity
# ============================================================

# Time Complexity:
# Space Complexity:


# ============================================================
# Test Cases
# ============================================================

if __name__ == "__main__":
    # Add your test cases here
    pass
'''

    file_path.write_text(content, encoding="utf-8")


def main():
    problem_number = 1
    total_files = 0

    print("=" * 70)
    print("Creating DSA 351 Problem Structure")
    print("=" * 70)
    print(f"Base directory: {BASE_DIR}")
    print()

    for section, problems in sections.items():

        section_dir = BASE_DIR / section
        section_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[{section}]")

        for problem in problems:

            filename = (
                f"{problem_number:03d}_"
                f"{clean_filename(problem)}.py"
            )

            file_path = section_dir / filename

            create_file(
                file_path,
                problem_number,
                problem,
                section,
            )

            print(f"  Created: {filename}")

            problem_number += 1
            total_files += 1

    print()
    print("=" * 70)
    print("DONE")
    print("=" * 70)
    print(f"Total files created: {total_files}")
    print(f"Expected files:      351")
    print(f"Location:            {BASE_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    main()