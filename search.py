# search.py
# ---------


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import csv
import os
import sys
import util


def format_state(state):
    """Safely format search states (tuples, coordinates, strings, grid states)."""
    if state is None:
        return 'None'
    try:
        # Handle FoodSearchProblem state: (position, foodGrid)
        if isinstance(state, tuple) and len(state) == 2:
            if hasattr(state[1], 'asList'):
                return f"({state[0]}, food_remaining={len(state[1].asList())})"
        return str(state)
    except Exception:
        return str(state)


class CSVTraceLogger:
    """
    Automated CSV trace logger for search algorithms.
    Writes state-by-state execution traces to evidence/<filename>.csv
    with schema:
    iteration, expanded_state, parent, action, generated_successors,
    frontier_before, frontier_after, explored, g, h, f
    """
    HEADERS = [
        'iteration',
        'expanded_state',
        'parent',
        'action',
        'generated_successors',
        'frontier_before',
        'frontier_after',
        'explored',
        'g',
        'h',
        'f'
    ]

    def __init__(self, algorithm_name, problem=None, filename=None, evidence_dir='evidence', max_repr_items=40):
        self.evidence_dir = evidence_dir
        os.makedirs(self.evidence_dir, exist_ok=True)
        self.iteration = 0
        self.parent_map = {}  # state -> (parent_state, action)
        self.max_repr_items = max_repr_items

        if filename:
            name = filename if filename.endswith('.csv') else f"{filename}.csv"
        else:
            layout_name = self._resolve_layout_name(problem)
            name = f"{algorithm_name}_{layout_name}.csv"

        self.filepath = os.path.join(self.evidence_dir, name)
        self.file = open(self.filepath, mode='w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(self.HEADERS)
        self.file.flush()

    def _resolve_layout_name(self, problem=None):
        """Extract layout name from CLI args (-l/--layout) or problem type."""
        for i, arg in enumerate(sys.argv):
            if arg == '-l' and i + 1 < len(sys.argv):
                return sys.argv[i + 1]
            if arg.startswith('--layout='):
                return arg.split('=', 1)[1]
        if problem is not None:
            if hasattr(problem, 'layout_name'):
                return getattr(problem, 'layout_name')
            return problem.__class__.__name__
        return "trace"

    def record_parent(self, child_state, parent_state, action):
        """Record the predecessor state and action that reached child_state."""
        self.parent_map[child_state] = (parent_state, action)

    def _format_collection(self, items):
        """Format a list or set of states, truncating if excessively large."""
        formatted = [format_state(item) for item in items]
        if len(formatted) <= self.max_repr_items:
            return str(formatted)
        return f"[{', '.join(formatted[:self.max_repr_items])}, ... (+{len(formatted) - self.max_repr_items} more)]"

    def snapshot_frontier(self, frontier):
        """Extract a string representation of states currently inside the frontier."""
        try:
            if hasattr(frontier, 'heap'):
                # PriorityQueue: items are (priority, count, item)
                raw_items = [entry[2] for entry in frontier.heap]
                states = [item[0] if isinstance(item, (tuple, list)) else item for item in raw_items]
                return self._format_collection(states)
            elif hasattr(frontier, 'list'):
                # Stack or Queue: items are (state, actions, ...) or state
                states = [item[0] if isinstance(item, (tuple, list)) else item for item in frontier.list]
                return self._format_collection(states)
        except Exception:
            pass
        return "[]"

    def log_expansion(self, expanded_state, successors, frontier_before, frontier_after, explored_states, g=0, h=0, f=0):
        """Record a single state expansion step into the CSV file."""
        self.iteration += 1
        parent_info = self.parent_map.get(expanded_state, ('START', 'START'))
        parent_state = parent_info[0]
        action = parent_info[1]

        succ_states = [succ[0] for succ in successors]
        succ_repr = self._format_collection(succ_states)
        explored_repr = self._format_collection(explored_states)

        row = [
            self.iteration,
            format_state(expanded_state),
            format_state(parent_state) if parent_state != 'START' else 'START',
            action,
            succ_repr,
            frontier_before,
            frontier_after,
            explored_repr,
            round(g, 4) if isinstance(g, float) else g,
            round(h, 4) if isinstance(h, float) else h,
            round(f, 4) if isinstance(f, float) else f
        ]
        self.writer.writerow(row)
        self.file.flush()

    def close(self):
        """Flush and close the open CSV file."""
        if self.file and not self.file.closed:
            self.file.flush()
            self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    """
    from util import Stack

    logger = CSVTraceLogger('dfs', problem)
    st = Stack()
    st.push((problem.getStartState(), []))
    visited = set()

    try:
        while not st.isEmpty():
            frontier_before = logger.snapshot_frontier(st)
            current_node = st.pop()
            current_state = current_node[0]
            current_actions = current_node[1]

            if current_state not in visited:
                visited.add(current_state)
                g_val = len(current_actions)

                if problem.isGoalState(current_state):
                    frontier_after = logger.snapshot_frontier(st)
                    logger.log_expansion(
                        expanded_state=current_state,
                        successors=[],
                        frontier_before=frontier_before,
                        frontier_after=frontier_after,
                        explored_states=visited,
                        g=g_val,
                        h=0,
                        f=g_val
                    )
                    return current_actions

                nodes = problem.getSuccessors(current_state)
                for node in nodes:
                    new_actions = list(current_actions)
                    new_actions.append(node[1])
                    st.push((node[0], new_actions))
                    logger.record_parent(node[0], current_state, node[1])

                frontier_after = logger.snapshot_frontier(st)
                logger.log_expansion(
                    expanded_state=current_state,
                    successors=nodes,
                    frontier_before=frontier_before,
                    frontier_after=frontier_after,
                    explored_states=visited,
                    g=g_val,
                    h=0,
                    f=g_val
                )

        return []
    finally:
        logger.close()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    from util import Queue

    logger = CSVTraceLogger('bfs', problem)
    q = Queue()
    q.push((problem.getStartState(), []))
    visited = set()

    try:
        while not q.isEmpty():
            frontier_before = logger.snapshot_frontier(q)
            current_node = q.pop()
            current_state = current_node[0]
            current_actions = current_node[1]
            g_val = len(current_actions)

            if problem.isGoalState(current_state):
                frontier_after = logger.snapshot_frontier(q)
                logger.log_expansion(
                    expanded_state=current_state,
                    successors=[],
                    frontier_before=frontier_before,
                    frontier_after=frontier_after,
                    explored_states=visited,
                    g=g_val,
                    h=0,
                    f=g_val
                )
                return current_actions

            if current_state not in visited:
                visited.add(current_state)
                nodes = problem.getSuccessors(current_state)
                for node in nodes:
                    new_actions = list(current_actions)
                    new_actions.append(node[1])
                    q.push((node[0], new_actions))
                    logger.record_parent(node[0], current_state, node[1])

                frontier_after = logger.snapshot_frontier(q)
                logger.log_expansion(
                    expanded_state=current_state,
                    successors=nodes,
                    frontier_before=frontier_before,
                    frontier_after=frontier_after,
                    explored_states=visited,
                    g=g_val,
                    h=0,
                    f=g_val
                )

        return []
    finally:
        logger.close()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    logger = CSVTraceLogger('ucs', problem)
    start_state = problem.getStartState()
    frontier = util.PriorityQueue()
    # Queue item: (state, actions, current_g)
    frontier.push((start_state, [], 0), 0)
    best_g = {start_state: 0}
    explored = set()

    try:
        while not frontier.isEmpty():
            frontier_before = logger.snapshot_frontier(frontier)
            state, actions, current_g = frontier.pop()

            # Guard against stale entries in the priority queue
            if current_g > best_g.get(state, float('inf')):
                continue

            explored.add(state)

            # Evaluate goal strictly upon popping for optimality
            if problem.isGoalState(state):
                frontier_after = logger.snapshot_frontier(frontier)
                logger.log_expansion(
                    expanded_state=state,
                    successors=[],
                    frontier_before=frontier_before,
                    frontier_after=frontier_after,
                    explored_states=explored,
                    g=current_g,
                    h=0,
                    f=current_g
                )
                return actions

            successors = problem.getSuccessors(state)
            for next_state, action, step_cost in successors:
                new_g = current_g + step_cost
                # If a lower accumulated cost to next_state is found, re-enqueue
                if next_state not in best_g or new_g < best_g[next_state]:
                    best_g[next_state] = new_g
                    frontier.push((next_state, actions + [action], new_g), new_g)
                    logger.record_parent(next_state, state, action)

            frontier_after = logger.snapshot_frontier(frontier)
            logger.log_expansion(
                expanded_state=state,
                successors=successors,
                frontier_before=frontier_before,
                frontier_after=frontier_after,
                explored_states=explored,
                g=current_g,
                h=0,
                f=current_g
            )

        return []
    finally:
        logger.close()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def greedyBestFirstSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest heuristic estimate first."""
    logger = CSVTraceLogger('gbfs', problem)
    start_state = problem.getStartState()
    frontier = util.PriorityQueue()
    start_h = heuristic(start_state, problem)
    # Queue item: (state, actions, current_g)
    frontier.push((start_state, [], 0), start_h)
    visited = set()

    try:
        while not frontier.isEmpty():
            frontier_before = logger.snapshot_frontier(frontier)
            state, actions, current_g = frontier.pop()

            # Guard against expanding already visited states to prevent cycles
            if state in visited:
                continue
            visited.add(state)

            current_h = heuristic(state, problem)

            # Evaluate goal strictly upon popping
            if problem.isGoalState(state):
                frontier_after = logger.snapshot_frontier(frontier)
                logger.log_expansion(
                    expanded_state=state,
                    successors=[],
                    frontier_before=frontier_before,
                    frontier_after=frontier_after,
                    explored_states=visited,
                    g=current_g,
                    h=current_h,
                    f=current_h
                )
                return actions

            successors = problem.getSuccessors(state)
            for next_state, action, step_cost in successors:
                if next_state not in visited:
                    h_val = heuristic(next_state, problem)
                    frontier.push((next_state, actions + [action], current_g + step_cost), h_val)
                    logger.record_parent(next_state, state, action)

            frontier_after = logger.snapshot_frontier(frontier)
            logger.log_expansion(
                expanded_state=state,
                successors=successors,
                frontier_before=frontier_before,
                frontier_after=frontier_after,
                explored_states=visited,
                g=current_g,
                h=current_h,
                f=current_h
            )

        return []
    finally:
        logger.close()

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    logger = CSVTraceLogger('astar', problem)
    start_state = problem.getStartState()
    frontier = util.PriorityQueue()
    start_h = heuristic(start_state, problem)
    # Queue item: (state, actions, current_g)
    frontier.push((start_state, [], 0), start_h)
    best_g = {start_state: 0}
    explored = set()

    try:
        while not frontier.isEmpty():
            # 1. Snapshot frontier state before popping
            frontier_before = logger.snapshot_frontier(frontier)
            state, actions, current_g = frontier.pop()

            # Guard against stale entries in the priority queue
            if current_g > best_g.get(state, float('inf')):
                continue

            explored.add(state)
            current_h = heuristic(state, problem)
            current_f = current_g + current_h

            # Evaluate goal strictly upon popping for optimality
            if problem.isGoalState(state):
                frontier_after = logger.snapshot_frontier(frontier)
                logger.log_expansion(
                    expanded_state=state,
                    successors=[],
                    frontier_before=frontier_before,
                    frontier_after=frontier_after,
                    explored_states=explored,
                    g=current_g,
                    h=current_h,
                    f=current_f
                )
                return actions

            successors = problem.getSuccessors(state)
            for next_state, action, step_cost in successors:
                new_g = current_g + step_cost
                # If a lower accumulated cost to next_state is found, re-enqueue
                if next_state not in best_g or new_g < best_g[next_state]:
                    best_g[next_state] = new_g
                    priority = new_g + heuristic(next_state, problem)
                    frontier.push((next_state, actions + [action], new_g), priority)
                    logger.record_parent(next_state, state, action)

            # 2. Snapshot frontier state after successors pushed, then log expansion
            frontier_after = logger.snapshot_frontier(frontier)
            logger.log_expansion(
                expanded_state=state,
                successors=successors,
                frontier_before=frontier_before,
                frontier_after=frontier_after,
                explored_states=explored,
                g=current_g,
                h=current_h,
                f=current_f
            )

        return []
    finally:
        logger.close()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch
