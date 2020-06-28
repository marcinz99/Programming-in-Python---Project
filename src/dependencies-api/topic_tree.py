import json


class Device:
    """
    Device data structure
    """
    Switchable = 0
    Detector = 1
    device_types = {"switchable": Switchable,
                    "detector": Detector}
    human_readable = {Switchable: "Switchable",
                      Detector: "Detector"}
    
    class States_Switchable:
        OFF = 0
        ON = 1
    
    class States_Detector:
        IDLE = 0
        EXCITED = 1
    
    states_to_enum = {
        "OFF": States_Switchable.OFF,
        "ON": States_Switchable.ON,
        "IDLE": States_Detector.IDLE,
        "EXCITED": States_Detector.EXCITED
    }
    
    def __init__(self, x_pos, y_pos, dev_type, init_state, info):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.dev_type = Device.device_types[dev_type]
        self.state = init_state
        self.info = info
        self.id = -1
    
    def __str__(self):
        return "[{}][X: {}, Y: {}] Type: '{}', State: '{}'\n> Info: '{}'".format(
            self.id,
            self.x_pos,
            self.y_pos,
            Device.human_readable[self.dev_type],
            self.state,
            self.info
        )


class TopicNode:
    """
    Topic node data structure
    """
    Root = 0
    Branch = 1
    Device = 2
    
    def __init__(self, node_type, name, device):
        self.node_type = node_type
        self.name = name
        self.parent = None
        self.children = {}
        self.topic_path = None
        self.device = device
        
    @property
    def topic(self):
        if self.topic_path == None:
            path = []
            node = self
            while node:
                path = [node.name] + path
                node = node.parent
            
            self.topic_path = '/'.join(path[1:])
        
        return self.topic_path
    
    def __getitem__(self, idx):
        return self.children[idx]
    
    def __setitem__(self, idx, node):
        self.children[idx] = node
        node.parent = self
    
    def __str__(self):
        if self.device: return str(self.device)
        else:           return "Not a device"
    
    def treewise_str(self, depth=0):
        this_level = "{}'{}'\n".format(depth * '> ', self.name)
        lower_level = ""
        
        for _, child in sorted(iter(self.children.items())):
            lower_level += child.treewise_str(depth + 1)
        
        return this_level + lower_level

    
class TopicTree:
    """
    Topic tree data structure
    """
    def __init__(self):
        self.root = TopicNode(TopicNode.Root, "root", None)
        self.device_dict = {}
    
    def __getitem__(self, idx):
        return self.device_dict[idx] if idx in self.device_dict else None
    
    def __setitem__(self, idx, node):
        self.device_dict[idx] = node
    
    @property
    def devices(self):
        return self.device_dict.items()
    
    def __str__(self):
        return self.root.treewise_str()

    
def readFile(source, verbose=True):
    """
    Read the json file to get the json dictionary object

    :param source: string path to the json file
    :param verbose: exception handling feedback
    :return: result - json dictionary
    """
    result = None

    with open(source, "r", encoding="UTF-8") as file:
        try:
            result = json.load(file)
        except json.JSONDecodeError as e:
            if verbose:
                print("JSON file seems to be corrupted:")
                print(e)
    
    return result


def parse(json_dict):
    """
    Make the topic tree on the basis of the json file

    :param json_dict: json file with containing the info about the devices to register
    :return: topic tree
    """
    if not json_dict:
        print("Not a proper data in")
        return None
    
    def in_depth_traverse(data, node, tree):
        for key, value in data.items():
            if type(value) == dict:
                node[key] = TopicNode(TopicNode.Branch, key, None)
                in_depth_traverse(value, node[key], tree)
            else:
                dev = Device(*value)
                node[key] = TopicNode(TopicNode.Device, key, dev)
                tree[node[key].topic] = node[key]
        
    tree = TopicTree()
    in_depth_traverse(json_dict["root"], tree.root, tree)
    
    return tree
