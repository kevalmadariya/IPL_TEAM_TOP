class Graph:
    def __init__(self, max_points, t1, teams, matches, points_table):
        self.teams = teams
        self.matches = matches
        self.points_table = points_table
        self.max_points = max_points
        
        print("...................")
        print(teams)
        print("...................")
        print(points_table)
        print("...................")
        print(matches)
        for team,points_table,match in zip(teams,points_table,matches):
            team['name'].replace('\xa0\xa0(E)','')
            match['teamA'].replace('\xa0\xa0(E)','')
            match['teamB'].replace('\xa0\xa0(E)','')
            
        
        self.team_count = len(teams)
        self.match_count = len(matches)
        self.node_count = self.match_count + self.team_count + 2  # Includes source & sink

        self.capacity_matrix = [[0] * self.node_count for _ in range(self.node_count)]
        self.node_indexes = {}

        self.node_indexes["s"] = 0
        self.node_indexes["t"] = self.node_count - 1

        index = 1
        for match in self.matches:
            match_team_a = match['teamA'].replace('\xa0\xa0(E)','')
            match_team_b = match['teamB'].replace('\xa0\xa0(E)','')
            self.node_indexes[f"match-{match_team_a}-{match_team_b}-{match['Id']}"] = index
            index += 1
        for team in self.teams:
            team_name = team['name'].replace('\xa0\xa0(E)','')
            self.node_indexes[f"team-{team_name}"] = index
            index += 1
        
        self.build_graph(t1)

    def build_graph(self, t1):
        for match in self.matches:
            match_node_index = self.node_indexes[f"match-{match['teamA']}-{match['teamB']}-{match['Id']}"]
            self.capacity_matrix[self.node_indexes["s"]][match_node_index] = 1

        for match in self.matches:
            match_node_index = self.node_indexes[f"match-{match['teamA']}-{match['teamB']}-{match['Id']}"]
            teamA_index = self.node_indexes[f"team-{match['teamA']}"]
            teamB_index = self.node_indexes[f"team-{match['teamB']}"]

            self.capacity_matrix[match_node_index][teamA_index] = 1
            self.capacity_matrix[match_node_index][teamB_index] = 1

        for team in self.teams:
                team_index = self.node_indexes[f"team-{team['name']}"]
                points_data = next((p for p in self.points_table if p["teamId"] == team["Id"]), None)

                if points_data:
                    remaining_capacity = self.max_points - points_data["points"] - 1
                    self.capacity_matrix[team_index][self.node_indexes["t"]] = remaining_capacity

class MaxFlowAlgorithm:
    def __init__(self, graph):
        self.graph = graph

    def bfs(self, s, t, parent):
        visited = [False] * len(self.graph)
        queue = [s]
        visited[s] = True

        while queue:
            u = queue.pop(0)
            for v in range(len(self.graph)):
                if self.graph[u][v] > 0 and not visited[v]:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True
        return False

    def max_flow(self, source, sink):
        parent = [-1] * len(self.graph)
        max_flow = 0

        while self.bfs(source, sink, parent):
            path_flow = float("Inf")
            v = sink
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.graph[u][v])
                v = parent[v]

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow

        return max_flow

# def load_data(filename):
#     with open(filename,'r') as f:
#         return json.load(f)

def predict_team_success(team_name,points_data,schedule_data):
    
    points_tabel_json = points_data
    team_name = next(team["Team"] for team in points_tabel_json if team["Id"] == int(team_name))
    print(team_name)
    teams = [ { "Id":i, "name":team["Team"] } for i,team in zip(range(10),points_tabel_json) if team["Team"] != team_name]
    
    schedule_json = schedule_data
    matches = [
        {"Id": match["Match No"], "teamA": match["Team 1"], "teamB": match["Team 2"]}
        for match in schedule_json if match["Team 1"] != team_name and match["Team 2"] != team_name and match["Result"] == ""
    ]
    print(matches)
    per_win_points = 2

    points_table = [
        {"teamId": i, "points": (int(team["Points"])/per_win_points) } for i,team in zip(range(10),points_tabel_json) if team["Team"] != team_name
    ]

    #from current point to max by winning all matches
    selected_team_name_curr_point = next((int(team["Points"])/per_win_points) for team in points_tabel_json if team["Team"] == team_name)
    selected_team_names_all_matches = [{"Result":match["Result"]} for match in schedule_json if match["Team 1"] == team_name or match["Team 2"] == team_name]
    
    selected_team_names_all_rem_matches = 0
    for i in selected_team_names_all_matches:
        if i["Result"] == "":
            selected_team_names_all_rem_matches += 1

    max_points = selected_team_name_curr_point + selected_team_names_all_rem_matches
    t1 = {"name": team_name}
    graph = Graph(max_points, t1, teams, matches, points_table)
    max_flow_algo = MaxFlowAlgorithm(graph.capacity_matrix)
    
    maxFlow = max_flow_algo.max_flow(graph.node_indexes["s"], graph.node_indexes["t"])

    remaining_match_points = len(matches)
    points_per_match = 2
    print(maxFlow)
    if maxFlow == remaining_match_points:
        return f"Congratulations! Team {t1['name']} can reach the top of the points table."
    else:
        return f"Unfortunately, Team {t1['name']} cannot reach the top of the points table."

# predict_team_success("1")