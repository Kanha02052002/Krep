from pyvis.network import Network
import json
import os

GRAPH_DIR = 'graph_format'

def load_course_data(json_path):
    """Load course data from JSON file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

def create_interactive_graph(data):
    # Create a new network
    net = Network(height="750px", width="100%", bgcolor="#000000", font_color="#ffffff")
    
    # Configure physics
    net.force_atlas_2based()
    net.toggle_physics(True)
    
    # Add center node (course title)
    net.add_node(data["course_title"], 
                 label=data["course_title"],
                 color="#ff9999",
                 size=50,
                 font={'size': 30, 'face': 'Arial'},
                 title=f"Course Code: {data['course_code']}")
    
    # Add module nodes and their topics
    for module in data["modules"]:
        module_id = module["module_number"]
        module_label = f"{module['module_number']}\n{module['module_name']}"
        
        # Add module node
        net.add_node(module_id,
                     label=module_label,
                     color="#99ff99",
                     size=40,
                     font={'size': 20, 'face': 'Arial'},
                     title=module['module_name'])
        
        # Connect module to center
        net.add_edge(data["course_title"], module_id, 
                     length=200,
                     color={'color': 'gray'})


        # Add topic nodes
        for i, topic in enumerate(module["topics"]):
            topic_id = f"{module_id}_topic_{i}"
            
            # Format topic text for better display
            topic_words = topic.split()
            formatted_topic = '\n'.join([' '.join(topic_words[i:i+5]) 
                                       for i in range(0, len(topic_words), 5)])


            # Add topic node
            net.add_node(topic_id,
                         label=formatted_topic,
                         color="#9999ff",
                         size=30,
                         font={'size': 15, 'face': 'Arial'},
                         title=topic)
            
            # Connect topic to its module
            net.add_edge(module_id, topic_id,
                         length=150,
                         color={'color': 'gray'})
    
    # Add some network options for better visualization
    net.set_options("""
        var options = {
            "nodes": {
                "shape": "dot",
                "shadow": true
            },
            "edges": {
                "smooth": {
                    "type": "continuous",
                    "forceDirection": "none"
                },
                "shadow": true
            },
            "physics": {
                "forceAtlas2Based": {
                    "springLength": 200,
                    "springConstant": 0.05,
                    "damping": 0.4,
                    "avoidOverlap": 1
                },
                "minVelocity": 0.75,
                "solver": "forceAtlas2Based"
            }
        }
    """)
    
    return net

def save_visualization(json_path, filename="course_structure.html"):
    # Load course data from JSON
    course_data = load_course_data(json_path)
    if not course_data:
        return False
    
    # Create and save the network
    net = create_interactive_graph(course_data)
    
    # Ensure the GRAPH_DIR exists
    if not os.path.exists(GRAPH_DIR):
        os.makedirs(GRAPH_DIR)

    # Join the directory and filename to form the full path
    # file_path = os.path.join(GRAPH_DIR, filename)
    file_path1 = os.path.join('templates', filename)
    
    # Save the graph to the specified path
    net.save_graph(file_path1)
    print(f"Visualization has been saved to {file_path1}")
    return True

# Execute the visualization
if __name__ == "__main__":
    json_path = "json_format/syllabus.json"  # Specify your JSON file path
    save_visualization(json_path)
