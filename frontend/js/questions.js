window.INITIAL_QUESTIONS = [
    {
        id: "q-101",
        title: "Pair Target Finder",
        slug: "pair-target-finder",
        difficulty: "Easy",
        category: "Algorithms",
        company_tags: ["TechCorp", "CloudScale", "DevPrep"],
        description: "Locate two indices in an array of numbers whose sum matches the specified target value. Assume exactly one valid pair exists.",
        starter_code: {
            javascript: "function findPair(nums, target) {\n    const map = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const diff = target - nums[i];\n        if (map.has(diff)) return [map.get(diff), i];\n        map.set(nums[i], i);\n    }\n    return [];\n}",
            python: "def find_pair(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i\n    return []"
        },
        function_name: "findPair",
        test_cases: [
            { id: "tc-1", input: [[2, 7, 11, 15], 9], expected_output: [0, 1] },
            { id: "tc-2", input: [[3, 2, 4], 6], expected_output: [1, 2] }
        ],
        hints: ["A hash map provides O(1) lookup times."]
    },
    {
        id: "q-102",
        title: "Alphanumeric Symmetry Check",
        slug: "alphanumeric-symmetry-check",
        difficulty: "Easy",
        category: "Algorithms",
        company_tags: ["SysFlow", "CloudScale"],
        description: "Determine if a string reads identically forward and backward after filtering out non-alphanumeric characters and normalizing case.",
        starter_code: {
            javascript: "function isSymmetric(s) {\n    const filtered = s.toLowerCase().replace(/[^a-z0-9]/g, '');\n    return filtered === filtered.split('').reverse().join('');\n}",
            python: "def is_symmetric(s: str) -> bool:\n    c = [ch.lower() for ch in s if ch.isalnum()]\n    return c == c[::-1]"
        },
        function_name: "isSymmetric",
        test_cases: [
            { id: "tc-1", input: ["Level, level!"], expected_output: true },
            { id: "tc-2", input: ["hello world"], expected_output: false }
        ],
        hints: ["Use two pointers moving inward to minimize memory usage."]
    },
    {
        id: "q-103",
        title: "Continuous Range Consolidator",
        slug: "continuous-range-consolidator",
        difficulty: "Medium",
        category: "Algorithms",
        company_tags: ["DataMesh", "DevPrep"],
        description: "Merge contiguous and overlapping numerical spans within an unordered list of intervals.",
        starter_code: {
            javascript: "function consolidateRanges(ranges) {\n    if (!ranges.length) return [];\n    ranges.sort((a, b) => a[0] - b[0]);\n    const out = [ranges[0]];\n    for (let i = 1; i < ranges.length; i++) {\n        const curr = ranges[i];\n        const prev = out[out.length - 1];\n        if (curr[0] <= prev[1]) prev[1] = Math.max(prev[1], curr[1]);\n        else out.push(curr);\n    }\n    return out;\n}"
        },
        function_name: "consolidateRanges",
        test_cases: [
            { id: "tc-1", input: [[ [1, 3], [2, 6], [8, 10] ]], expected_output: [[1, 6], [8, 10]] }
        ],
        hints: ["Sorting beforehand ensures sequential examination."]
    },
    {
        id: "q-104",
        title: "Second Maximum Compensation Query",
        slug: "second-max-compensation",
        difficulty: "Medium",
        category: "SQL",
        company_tags: ["DataMesh", "EnterpriseCorp"],
        description: "Construct a SQL query to identify the second highest compensation value present in the staff registry.",
        starter_code: {
            sql: "SELECT MAX(compensation) AS SecondHighestCompensation\nFROM Staff\nWHERE compensation < (SELECT MAX(compensation) FROM Staff);"
        },
        function_name: "executeSQL",
        test_cases: [
            { id: "tc-1", input: "SELECT MAX(compensation) AS SecondHighestCompensation FROM Staff WHERE compensation < (SELECT MAX(compensation) FROM Staff);", expected_output: 200 }
        ],
        hints: ["Subquery comparison or descending ranking handles duplicates gracefully."]
    }
];
