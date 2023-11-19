from datetime import datetime

# Initialize online_agents dictionary to store agent information
online_agents = {}


def track_agent_activity(agent_id, activity):
    if agent_id not in online_agents:
        online_agents[agent_id] = {'last_activity': None, 'activities': []}

    online_agents[agent_id]['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    online_agents[agent_id]['activities'].append(activity)


def update_online_agents(agent_id):
    if agent_id not in online_agents:
        online_agents[agent_id] = {'last_activity': None, 'activities': []}


def view_online_agents():
    print("Online Agents:")
    for agent_id, agent_info in online_agents.items():
        print(f"Agent ID: {agent_id}, Last Activity: {agent_info['last_activity']}")


def view_agent_activities(agent_id):
    if agent_id in online_agents:
        print(f"Activities for Agent ID {agent_id}:")
        for activity in online_agents[agent_id]['activities']:
            print(activity)
    else:
        print(f"Agent ID {agent_id} not found.")
