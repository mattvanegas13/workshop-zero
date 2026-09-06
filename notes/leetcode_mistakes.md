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

## 3. Search in rotated array

**Pattern** Binary Search

** Initial instinct **
considering we have a time complexity constraint of O(log n) that gives us the idea of that we need to do a binary search. The problem is that the rotated twist violates the monotomically increasing constraint that usually is there for a binary search. So what do we do here..? Well if we rotate the array key theres a porition that has to be sorted still - which actuall is the pivot point. Thus we need to find out which portion is still sorted. So we check the left side of the pivot - we know that the left is sorted if nums[left] <= nums[mid] otherwise the right side is the sorted. if the left half is sorted then we need to do a binary search on the left side. then if the left is sorted we check to see if the target is in that left sub array otherwise look at the left part. THen we address the mirror scenario where the right side is the sorted portion and then we check if the tartget is in that part

if youre confuse walk through this example
[2,4,5,6,7,0,1]
find 1 


** Key Invariant **
one potion of the array has to be sorted

** Complexity **
Time: O(log n)
Complexity O(log n) 

why not O(1)? because our recursive structure causes us to maintain a stack of recursive funcition calls
had we had a while loop then it would go to O(1)
