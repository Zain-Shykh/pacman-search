**Artificial Intelligence** 

**Assignment 01** 

**Course Title:** Artificial Intelligence (AI2002) 

**Total Marks:** 150 Marks | **Work Mode:** 2-3 people 

**Programming Language:** Python 3   
**Deadline:** 27th September 2026 

**1\. Instructions** 

**Step 1: Download & Workspace Setup** 

● Download search.zip folder 

● Extract the archive into your working project directory. Ensure the relative folder structure (like layouts/)  remains intact. 

● Verify that Python 3 (Python 3.7+) is configured on your machine by running python \--version or python3 \-- version in your terminal. 

● Test running the base environment without search logic: 

python pacman.py 

**Step 2: Files You Are Permitted to Edit / Create** 

● search.py: **PRIMARY EDITABLE FILE.** All core search algorithms (DFS, BFS, UCS, GBFS, A\*) and  automated CSV logging logic must be written here. 

● searchAgents.py: **SECONDARY EDITABLE FILE.** All state space formulations, custom heuristic  functions, and agent wrappers (e.g., CornersProblem, FoodSearchProblem) must be implemented here. ● layouts/Search.lay: **CUSTOM FILE TO ADD.** Create one original layout file inside the layouts/ folder  named. 

**Step 3: Strictly Forbidden File Modifications** 

To ensure full compatibility with autograders(for testing not for grading) and live evaluation scripts, **DO NOT EDIT** any  of the following core system files: 

● pacman.py: The main game loop runner, game state controller, and CLI argument parser. ● game.py: Underlying physics, grid data structures, directions (North, South, East, West), agent actions,  and state representations. 

● util.py: Data structures including Stack, Queue, and PriorityQueue. Use these provided classes  exclusively. 

● layout.py, graphicsDisplay.py, graphicsUtils.py, textDisplay.py: Maze layout loader and graphic rendering  components.  
Welcome to the Pacman Search Game Project\! 

***All those colored walls,*** 

***mazes give pacman the blues,***   
***![][image1]so teach him to search.***

**2\. Tasks** 

**Task 1: Depth-First Search (DFS)** 

**Goal:** Implement graph-search Depth-First Search in the function depthFirstSearch inside search.py. **Technical Requirements:** 

● Use a LIFO Stack from util.py as your fringe/frontier. 

● Implement strict graph search: maintain an explicit explored set to prevent visiting previously expanded  states and avoiding infinite loops. 

● Return a valid list of actions (e.g., \['North', 'East', 'South'\]) that leads Pacman from start state to goal state. ● Follow the mandatory successor expansion order: **North → East → South → West**. 

python pacman.py \-l tinyMaze \-p SearchAgent \-a fn=dfs 

python pacman.py \-l mediumMaze \-p SearchAgent \-a fn=dfs 

python pacman.py \-l bigMaze \-z .5 \-p SearchAgent \-a fn=dfs 

**Task 2: Breadth-First Search (BFS)** 

**Goal:** Implement graph-search Breadth-First Search in breadthFirstSearch inside search.py. 

**Technical Requirements:** 

● Use a FIFO Queue from util.py as your fringe/frontier.   
● Ensure that for unweighted graphs (where every step cost is equal to 1), BFS guarantees finding the  shallowest/optimal path in terms of total action steps. 

● Avoid re-enqueuing states that are already present in the frontier or explored set. 

python pacman.py \-l mediumMaze \-p SearchAgent \-a fn=bfs 

python pacman.py \-l bigMaze \-z .5 \-p SearchAgent \-a fn=bfs 

**Task 3: Uniform-Cost Search (UCS)** 

**Goal:** Implement Uniform-Cost Search in uniformCostSearch inside search.py. 

**Technical Requirements:** 

● Use a PriorityQueue from util.py ordered by accumulated path cost \$g(n)\$. 

● Test your implementation across varying step costs (e.g., mazes with directional costs like  stayEastSearch). 

● Handle frontier updates: if a newly generated successor offers a cheaper path cost \$g(n)\$ to a state  already on the fringe, update its priority in the queue. 

python pacman.py \-l mediumMaze \-p SearchAgent \-a fn=ucs 

python pacman.py \-l mediumDenselyMaze \-p SearchAgent \-a fn=ucs 

python pacman.py \-l stayEastSearch \-p SearchAgent \-a fn=ucs 

**Task 4: Greedy Best-First Search (GBFS)** 

**Goal:** Implement Greedy Best-First Search in greedyBestFirstSearch (alias gbfs) inside search.py. **Technical Requirements:** 

● Use a PriorityQueue ordered strictly by heuristic value \$h(n)\$. 

● Integrate command-line heuristic parameter passing so that different heuristics (e.g., Manhattan distance,  Euclidean distance) can be passed dynamically. 

python pacman.py \-l bigMaze \-z .5 \-p SearchAgent \-a fn=gbfs,heuristic=manhattanHeuristic 

**Task 5: A\* Search** 

**Goal:** Implement A\* Search in aStarSearch inside search.py. 

**Technical Requirements:** 

● Use a PriorityQueue ordered by evaluation function \$f(n) \= g(n) \+ h(n)\$, where \$g(n)\$ is accumulated  path cost and \$h(n)\$ is estimated heuristic cost to goal. 

● Verify optimality: ensure A\* returns the true shortest cost path when paired with an admissible and  consistent heuristic. 

python pacman.py \-l bigMaze \-z .5 \-p SearchAgent \-a fn=astar,heuristic=nullHeuristic 

python pacman.py \-l bigMaze \-z .5 \-p SearchAgent \-a fn=astar,heuristic=manhattanHeuristic 

**Task 6: Multi-Goal State Space (Corners Problem)** 

**Goal:** Formulate a new state space search problem in searchAgents.py to touch all four corners of a maze in minimal  steps. 

**Technical Requirements:**  
● Define state representation in CornersProblem: a tuple containing (pacman\_position,  tuple\_of\_visited\_corners). 

● Implement cornersHeuristic in searchAgents.py. The heuristic must be mathematically admissible (never  overestimate cost) and consistent. 

python pacman.py \-l tinyCorners \-p SearchAgent \-a fn=bfs,prob=CornersProblem 

python pacman.py \-l mediumCorners \-p AStarCornersAgent \-z .5 

**Task 7: Eating All Food Dots & Nearest Food Search** 

**Goal:** Design specialized search solutions for complex multi-dot food collection in searchAgents.py. **Technical Requirements:** 

● Implement foodHeuristic for FoodSearchProblem using minimum spanning trees (MST) or bottleneck  distance calculations to optimize node expansions on trickySearch. 

● Implement AnyFoodSearchProblem to allow Pacman to quickly locate and navigate to the single closest  food dot using BFS. 

python pacman.py \-l trickySearch \-p AStarFoodSearchAgent 

python pacman.py \-l bigSearch \-p ClosestDotSearchAgent 

**3\. Automated CSV Trace Logging Specification** 

To prove algorithmic correctness and generate automated trace data, every algorithm execution must write execution  logs state-by-state to a CSV file inside the evidence/ folder. 

**Mandatory CSV Columns:** 

iteration, expanded\_state, parent, action, generated\_successors, frontier\_before, frontier\_after, explored, g, h, f 

**4\. Custom Maze Creation & Experiments** 

Create an original layout file layouts/\[YourID\]Search.lay (e.g., 21I1234Search.lay). The maze must contain multiple  decision branches, dead ends, and deceptive traps designed to show differences between Greedy Best-First Search  and A\* Search. Test all 5 algorithms on your layout and include screenshot comparisons in your report. 

**5\. Final Submission Package Requirements** 

Your final submission must be a single ZIP archive containing the full project folder with all original starter code,  modified files, custom layout, written PDF report, and **ALL generated CSV trace logs inside the evidence/  directory**. 

**Example zip format:** 

\[SearchProject.zip 

│ 

├── search.py (Edited: DFS, BFS, UCS, GBFS, A\*, CSV Logger) 

├── searchAgents.py (Edited: CornersProblem, FoodHeuristic, etc.) 

├── pacman.py (Original starter file \- DO NOT MODIFY) 

├── game.py (Original starter file \- DO NOT MODIFY)  
├── util.py (Original starter file \- DO NOT MODIFY) 

├── layout.py (Original starter file \- DO NOT MODIFY) ├── README.txt (Contains Python version, run commands, system specs) ├── report.pdf (Detailed 6-10 page analysis report) 

│ 

├── layouts/ 

│ ├── \*.lay (Standard starter layouts) 

│ └── \[YourID\]Search.lay (Your custom maze layout file) 

│ 

└── evidence/ 

 ├── \*.csv (ALL complete execution CSV logs for all runs)  └── screenshots/ (Visual maze solution graphics)

| Student Name Roll number |  |
| :---- | :---- |
|  |  |
|  |  |
|  |  |

**Evaluation Rubric (Bring its print during viva)**

| Evaluation Category  | Allocated Marks  | Specific Assessment Criteria  | Obtained Marks |
| :---- | :---- | :---- | :---- |
| **Automated Test   Cases Execution** | 20 Marks  | 100% passing rate on standard tests  across all 5 algorithms and search  problems. |  |
| **Live Demonstration /  Viva Defense** | 20 Marks  | Live code walkthrough, answering line-by line questions, and running algorithms on  unseen mazes. |  |
| **A\* Search   Implementation** | 10 Marks  | Flawless f(n)=g(n)+h(n) queue ordering,  priority updates, and optimal path finding. |  |
| **Uniform-Cost Search  (UCS) Implementation** | 10 Marks  | Accurate path-cost accumulated tracking  g(n) and re-prioritizing frontier nodes. |  |
| **Heuristic Design &  Analysis** | 10 Marks  | Admissibility and consistency mathematical  proofs, non-trivial custom heuristics. |  |
| **Depth-First Search  (DFS) Implementation** | 10 Marks  | Correct LIFO graph search, visited state  set management, valid action sequences. |  |
| **Breadth-First Search  (BFS) Implementation** | 10 Marks  | Correct FIFO queue implementation,  optimal path length guarantees on   unweighted mazes. |  |
| **Greedy Best-First   Search (GBFS)   Implementation** | 10 Marks  | Strict h(n) heuristic prioritization and  command-line integration. |  |
| **Multi-Goal Search   Tasks** | 10 Marks  | CornersProblem state tuple design and  FoodSearch heuristics optimization. |  |
| **Automatic CSV Trace  Logging** | 10 Marks  | Full step-by-step CSV log files generated  inside evidence/ directory for all tasks. |  |
| **Custom Maze &   Experiments** | 10 Marks  | Well-designed .lay custom maze, empirical  performance tables, and screenshots. |  |

| Report & Complexity  Analysis | 10 Marks  | Comprehensive PDF report (6-10 pages)  analyzing space/time complexity and state  spaces. |  |
| :---- | :---- | :---- | :---- |
| **Code Quality & Style**  | 10 Marks  | Clean Python code formatting, comments,  and strict adherence to provided interface  rules. |  |
| **TOTAL MARKS**  | **150 Marks** |  |  |

**REMARKS:**

[image1]: <data:image/png;base64,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>