import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.mplot3d import Axes3D

# Node data
node_data = {
    'stool_2446b': ['stool', [1.7988970171940815, 0.6628147375042005, -1.2393224694867078]],
    'stool_7e953': ['stool', [1.8305892683722957, 1.5230015299088804, -1.2473324219606476]],
    'lamp_be40f': ['lamp', [2.2771584496130046, -0.7675085519764773, -0.26804856535538707]],
    'closet door_7d3d9': ['closet door', [-0.17656870998422403, -1.1140875319589072, -0.3999633642694331]],
    'window_d7626': ['window', [-0.8388011869985428, 1.1046669767841135, 0.0064978196526785355]],
    'toaster_30f22': ['toaster', [-0.6573392615827228, 0.767469439806694, -0.7984911774014567]],
    'end table_4bf61': ['end table', [2.4514023795355757, -0.5636138301330379, -0.8241480498269006]],
    'power outlet_52c48': ['power outlet', [1.2434891482993815, -1.1086242428629243, -0.33072167621898657]],
    'light switch_90852': ['light switch', [1.2133378913039532, -1.0957591515210474, 0.013021983907620018]],
    'coffee kettle_ecf03': ['coffee kettle', [-0.5823077430818279, 0.5187755704382429, -0.7129683820456404]],
    'book_9f457': ['book', [-0.6640348390154791, 1.468042864506555, -0.8300680956769392]],
    'cabinet_75ccf': ['cabinet', [-0.5931866184027476, 1.092521860752992, -1.1549963472869336]],
    'lamp_df238': ['lamp', [1.949304199110873, -1.121701109460599, -0.27823576779449655]],
    'pillow_42e7c': ['pillow', [2.768915265993274, -0.37325852365826456, -0.8375685125890958]],
    'poster_7001d': ['poster', [3.7135058258533613, -1.1031901916252667, 0.07785962267388223]],
    'closet door_ca69b': ['closet door', [0.21600050761435435, -1.123977206730785, -0.29243748528723085]],
    'cushion_28a13': ['cushion', [1.7411143540276486, -0.1581372049317568, -1.4946076836037012]],
    'lamp_3134b': ['lamp', [2.174731295246341, -1.123832995172951, -0.2636554041746148]],
    'potted plant_c504e': ['potted plant', [-0.6097432291568309, 1.8425168716431055, -0.6111066121483949]],
    'power outlet_1cf7f': ['power outlet', [-0.4984304923542678, 3.3187061232384303, -1.0504060239927548]],
    'lamp_4a868': ['lamp', [2.0793188753670813, -1.1175265004864798, -1.3523835360062684]],
    'pillow_fa026': ['pillow', [2.8489039132371565, 2.4930974851120906, -0.819454510890856]],
    'couch_a78e1': ['couch', [3.694228331914835, 2.5832933868903427, -0.9800293105946739]],
    'end table_7cb21': ['end table', [2.325120235584508, -0.5942881588533708, -1.4829396985840453]],
    'sofa chair_3552f': ['sofa chair', [1.4484863518218778, 2.7736593516531522, -1.4959179552889308]],
    'lamp_0c8b7': ['lamp', [1.95548847877268, -0.8341979816260381, -0.3501052349596587]],
    'pillow_e603f': ['pillow', [3.2190818572073248, -0.4507833358568451, -0.8335874215139616]],
    'pillow_c55a8': ['pillow', [3.761496128513835, -0.6778734933473642, -0.8177636061731359]],
    'pillow_6fbed': ['pillow', [4.030930918914593, -0.5264944338894206, -0.8388997849291183]],
    'pillow_3f9b7': ['pillow', [4.32234031853095, -0.4309148863140728, -0.8315622071331413]],
    'pillow_ccb99': ['pillow', [4.421150162208448, -0.5663752556958497, -0.6205669674039983]],
    'pillow_e0f60': ['pillow', [3.681514450956099, -0.4235117916065984, -1.0128198753950286]],
    'cup_41fb6': ['cup', [3.5976897514337893, 1.0920673491074329, -0.8841219694024961]],
    'sofa chair_b11c9': ['sofa chair', [5.338944503938246, 0.18415728359295686, -1.1414830302519676]],
    'bottle_0f910': ['bottle', [3.8865980132429057, 0.983075326252793, -0.847643123749636]],
    'armchair_d9749': ['armchair', [5.724529289983195, 0.5036101003381178, -0.8999178715872848]],
    'pillow_db103': ['pillow', [5.836350589203797, 0.2838710460975585, -0.8703351320601913]],
    'blinds_ad991': ['blinds', [6.794206080671845, 0.7369806438591313, 0.32324119631903814]],
    'pillow_22515': ['pillow', [5.822591311670754, 0.4586107626213796, -0.8567497193760768]],
    'potted plant_1104f': ['potted plant', [4.025801622663858, 1.0735774962893083, -0.6984122215825678]],
    'radiator_7db5c': ['radiator', [6.696780466740646, -0.6412594260484688, -0.9750198353623569]],
    'coffee table_cc0ec': ['coffee table', [5.555558641474217, -0.16178294880352456, -1.4786782542523782]],
    'chair_c870e': ['chair', [5.683722536307596, 1.159830821079132, -0.7466787313700952]],
    'pillow_0560d': ['pillow', [5.877986476428022, 1.4802950826984416, -0.8770623761929788]],
    'armchair_e9853': ['armchair', [5.720741729894924, 1.4969428272952046, -0.871604444690494]],
    'lamp_28f24': ['lamp', [5.180241604698308, 2.7549703053815615, -0.2034317792734612]],
    'pillow_39334': ['pillow', [4.643521700258944, 2.5685209454664983, -0.7220294834227431]],
    'pillow_4095e': ['pillow', [4.517000400658934, 2.4237904274594375, -0.782445223128899]],
    'pillow_b6e7e': ['pillow', [4.46709798862448, 2.6297692638779813, -0.7503831671366001]],
    'coffee table_2d6ac': ['coffee table', [3.709322042534102, 1.0260946946720588, -1.1131477990608019]],
    'blinds_01be1': ['blinds', [3.167652475648485, 3.1471809399455966, 0.3107865449150456]],
    'lamp_9d1bb': ['lamp', [6.429014899319393, 3.183389881946939, -0.5983940065528384]],
    'paper bag_f1a6f': ['paper bag', [2.3168960545063713, 2.903497871637273, -1.3626449605326392]],
    'sofa chair_4d503': ['sofa chair', [6.749895627394694, 1.0197865954581673, -1.0027056393182228]],
    'book_ec5b3': ['book', [5.219677192951505, 2.5866476188525307, -0.8501941432544659]],
    'power outlet_c2b55': ['power outlet', [6.2332578504549545, 3.279706470086833, -1.039960046763663]],
    'lamp_0fe0c': ['lamp', [5.6178739995322795, 3.1159394200256902, -0.24482471278878817]],
    'end table_e1bd2': ['end table', [5.784083672672842, 2.8129594247269885, -1.379246996300906]],
    'lamp_e8ab2': ['lamp', [6.536634274473923, 3.1386307141331353, -0.9003948230931645]],
    'lamp_b2450': ['lamp', [2.3605847420746846, -1.1179933903205168, -1.102397957154325]],
    'lamp_7fbca': ['lamp', [6.179270255620318, 3.411013104476472, -0.3054937926951259]]
}

# Edges
edges = [
    ['lamp_be40f', 'end table_4bf61', 'on'],
    ['light switch_90852', 'power outlet_52c48', 'beside'],
    ['book_9f457', 'cabinet_75ccf', 'on'],
    ['toaster_30f22', 'cabinet_75ccf', 'on'],
    ['coffee kettle_ecf03', 'cabinet_75ccf', 'on'],
    ['lamp_0c8b7', 'end table_4bf61', 'on'],
    ['lamp_3134b', 'end table_4bf61', 'on'],
    ['pillow_42e7c', 'end table_7cb21', 'on'],
    ['lamp_4a868', 'end table_7cb21', 'on'],
    ['cup_41fb6', 'coffee table_2d6ac', 'on'],
    ['bottle_0f910', 'coffee table_2d6ac', 'on'],
    ['potted plant_1104f', 'coffee table_2d6ac', 'on'],
    ['paper bag_f1a6f', 'sofa chair_3552f', 'on'],
    ['book_ec5b3', 'end table_e1bd2', 'on'],
    ['lamp_28f24', 'end table_e1bd2', 'on'],
    ['lamp_e8ab2', 'power outlet_c2b55', 'near'],
    ['radiator_7db5c', 'blinds_ad991', 'below'],
    ['closet door_7d3d9', 'closet door_ca69b', 'beside'],
    ['cabinet_75ccf', 'window_d7626', 'below'],
    ['potted plant_c504e', 'cabinet_75ccf', 'beside']
]

# Create graph
G = nx.Graph()

# Add nodes with positions
pos = {node: (coord[0], coord[1], coord[2]) for node, (_, coord) in node_data.items()}
for node, coord in pos.items():
    G.add_node(node, pos=coord)

# Add edges with relationships
for edge in edges:
    source, target, relationship = edge
    G.add_edge(source, target, relationship=relationship)

# Prepare 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot nodes
for node, (x, y, z) in pos.items():
    ax.scatter(x, y, z, s=100, label=node)  # Scatter plot for nodes

# Plot edges
for edge in G.edges():
    source, target = edge
    source_pos = pos[source]
    target_pos = pos[target]
    ax.plot(
        [source_pos[0], target_pos[0]],
        [source_pos[1], target_pos[1]],
        [source_pos[2], target_pos[2]],
        color='black',
        alpha=0.6,
    )

    # Annotate edges with relationships
    relationship = G.edges[source, target].get('relationship', 'undefined')
    mid_point = [
        (source_pos[0] + target_pos[0]) / 2,
        (source_pos[1] + target_pos[1]) / 2,
        (source_pos[2] + target_pos[2]) / 2,
    ]
    ax.text(
        mid_point[0], mid_point[1], mid_point[2],
        relationship,
        color='red',
        fontsize=8,
    )

# Set plot labels
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

# Show plot
plt.title("3D Graph Visualization with Relationships")
plt.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.show()