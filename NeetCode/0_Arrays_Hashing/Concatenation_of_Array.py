class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        ans = []
        # take every number in nums and append it and put it in the array
        for i in range(2):
            for num in nums:
                ans.append(num)
        return ans
