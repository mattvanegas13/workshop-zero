# LeetCode Mistake Log

## 1. Longest Substring Without Repeating Characters

**Pattern:** Sliding window + set

**Initial issue:**  
I knew sliding window was appropriate but lost track of the invariant while implementing it.

**Key invariant:**  
The active window contains no duplicate characters.

**Key insight:**  
Expand `right` automatically. If the invariant breaks, move `left` until uniqueness is restored.

**Complexity:**  
Time: O(n)  
Space: O(min(n, charset size))

**Retention:**  
Re-solved independently the next day in 8 minutes.

---

## 2. Subarray Sum Equals K

**Pattern:** Prefix sum + hashmap

**Initial instinct:**  
Tried to think of the problem as a sliding/fixed-size window.

**Why that was insufficient:**  
Subarrays can have different lengths, and negative numbers mean the window cannot be adjusted monotonically.

**Core relationship:**

`Sj - Si = k`

therefore:

`Si = Sj - k`

**Key invariant:**  
Before processing/storing the current prefix sum, the hashmap contains the frequencies of prefix sums seen previously.

**Key insight:**  
Search for `Sj - k`. Store `Sj`.

A contiguous range is the difference between two cumulative prefixes, similar to cancellation.

**Complexity:**  
Time: O(n)  
Space: O(n)

**Revisit:**  
[leave blank]
