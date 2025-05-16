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

# node_data_bbx = {'stool_2446b': ['stool', OrientedBoundingBox: center: (1.7989, 0.662815, -1.23932), extent: 0.693243, 0.665566, 0.484514)], 'stool_7e953': ['stool', OrientedBoundingBox: center: (1.83059, 1.523, -1.24733), extent: 0.663333, 0.657216, 0.484983)], 'lamp_be40f': ['lamp', OrientedBoundingBox: center: (2.27716, -0.767509, -0.268049), extent: 0.460661, 0.418258, 0.346508)], 'closet door_7d3d9': ['closet door', OrientedBoundingBox: center: (-0.176569, -1.11409, -0.399963), extent: 2.30801, 1.37996, 0.0680792)], 'window_d7626': ['window', OrientedBoundingBox: center: (-0.838801, 1.10467, 0.00649782), extent: 1.11754, 1.05367, 0.0309147)], 'toaster_30f22': ['toaster', OrientedBoundingBox: center: (-0.657339, 0.767469, -0.798491), extent: 0.420717, 0.319626, 0.120052)], 'end table_4bf61': ['end table', OrientedBoundingBox: center: (2.4514, -0.563614, -0.824148), extent: 0.91904, 0.761346, 0.352581)], 'power outlet_52c48': ['power outlet', OrientedBoundingBox: center: (1.24349, -1.10862, -0.330722), extent: 0.17442, 0.127481, 0.0102435)], 'light switch_90852': ['light switch', OrientedBoundingBox: center: (1.21334, -1.09576, 0.013022), extent: 0.28328, 0.128176, 0.0703107)], 'coffee kettle_ecf03': ['coffee kettle', OrientedBoundingBox: center: (-0.582308, 0.518776, -0.712968), extent: 0.284295, 0.205163, 0.174267)], 'book_9f457': ['book', OrientedBoundingBox: center: (-0.664035, 1.46804, -0.830068), extent: 0.591068, 0.519132, 0.0323206)], 'cabinet_75ccf': ['cabinet', OrientedBoundingBox: center: (-0.593187, 1.09252, -1.155), extent: 2.05936, 0.756558, 0.577907)], 'lamp_df238': ['lamp', OrientedBoundingBox: center: (1.9493, -1.1217, -0.278236), extent: 0.178685, 0.0196346, 0.000199233)], 'pillow_42e7c': ['pillow', OrientedBoundingBox: center: (2.76892, -0.373259, -0.837569), extent: 0.549248, 0.468125, 0.446936)], 'poster_7001d': ['poster', OrientedBoundingBox: center: (3.71351, -1.10319, 0.0778596), extent: 1.9801, 1.33198, 0.0592874)], 'closet door_ca69b': ['closet door', OrientedBoundingBox: center: (0.216001, -1.12398, -0.292437), extent: 2.38644, 1.68156, 0.104982)], 'cushion_28a13': ['cushion', OrientedBoundingBox: center: (1.74111, -0.158137, -1.49461), extent: 0.788509, 0.314979, 0.0197472)], 'lamp_3134b': ['lamp', OrientedBoundingBox: center: (2.17473, -1.12383, -0.263655), extent: 0.750578, 0.257922, 0.00453329)], 'potted plant_c504e': ['potted plant', OrientedBoundingBox: center: (-0.609743, 1.84252, -0.611107), extent: 0.516254, 0.270464, 0.2602)], 'power outlet_1cf7f': ['power outlet', OrientedBoundingBox: center: (-0.49843, 3.31871, -1.05041), extent: 0.154576, 0.144703, 0.007448)], 'lamp_4a868': ['lamp', OrientedBoundingBox: center: (2.07932, -1.11753, -1.35238), extent: 0.0940945, 0.0639494, 0.00136575)], 'pillow_fa026': ['pillow', OrientedBoundingBox: center: (2.8489, 2.4931, -0.819455), extent: 0.740887, 0.642965, 0.303498)], 'couch_a78e1': ['couch', OrientedBoundingBox: center: (3.69423, 2.58329, -0.980029), extent: 2.45134, 1.31876, 1.01715)], 'end table_7cb21': ['end table', OrientedBoundingBox: center: (2.32512, -0.594288, -1.48294), extent: 0.963896, 0.714667, 0.041352)], 'sofa chair_3552f': ['sofa chair', OrientedBoundingBox: center: (1.44849, 2.77366, -1.49592), extent: 0.668321, 0.108235, 0.00246462)], 'lamp_0c8b7': ['lamp', OrientedBoundingBox: center: (1.95549, -0.834198, -0.350105), extent: 0.980344, 0.373524, 0.230412)], 'pillow_e603f': ['pillow', OrientedBoundingBox: center: (3.21908, -0.450783, -0.833587), extent: 0.791186, 0.471468, 0.259392)], 'pillow_c55a8': ['pillow', OrientedBoundingBox: center: (3.7615, -0.677873, -0.817764), extent: 0.478713, 0.143146, 0.113117)], 'pillow_6fbed': ['pillow', OrientedBoundingBox: center: (4.03093, -0.526494, -0.8389), extent: 0.427058, 0.225424, 0.113882)], 'pillow_3f9b7': ['pillow', OrientedBoundingBox: center: (4.32234, -0.430915, -0.831562), extent: 0.849807, 0.581407, 0.347297)], 'pillow_ccb99': ['pillow', OrientedBoundingBox: center: (4.42115, -0.566375, -0.620567), extent: 0.343985, 0.18615, 0.0932913)], 'pillow_e0f60': ['pillow', OrientedBoundingBox: center: (3.68151, -0.423512, -1.01282), extent: 2.32574, 1.24258, 0.79832)], 'cup_41fb6': ['cup', OrientedBoundingBox: center: (3.59769, 1.09207, -0.884122), extent: 0.374605, 0.367261, 0.30326)], 'sofa chair_b11c9': ['sofa chair', OrientedBoundingBox: center: (5.33894, 0.184157, -1.14148), extent: 0.313153, 0.169359, 0.160175)], 'bottle_0f910': ['bottle', OrientedBoundingBox: center: (3.8866, 0.983075, -0.847643), extent: 0.218885, 0.0743843, 0.0310543)], 'armchair_d9749': ['armchair', OrientedBoundingBox: center: (5.72453, 0.50361, -0.899918), extent: 1.28793, 0.965101, 0.591153)], 'pillow_db103': ['pillow', OrientedBoundingBox: center: (5.83635, 0.283871, -0.870335), extent: 0.307155, 0.199554, 0.0787794)], 'blinds_ad991': ['blinds', OrientedBoundingBox: center: (6.79421, 0.736981, 0.323241), extent: 3.9006, 2.15777, 0.163371)], 'pillow_22515': ['pillow', OrientedBoundingBox: center: (5.82259, 0.458611, -0.85675), extent: 0.468548, 0.305386, 0.185987)], 'potted plant_1104f': ['potted plant', OrientedBoundingBox: center: (4.0258, 1.07358, -0.698412), extent: 0.761881, 0.597586, 0.437923)], 'radiator_7db5c': ['radiator', OrientedBoundingBox: center: (6.69678, -0.641259, -0.97502), extent: 1.15754, 1.03487, 0.214662)], 'coffee table_cc0ec': ['coffee table', OrientedBoundingBox: center: (5.55556, -0.161783, -1.47868), extent: 0.862451, 0.636534, 0.019737)], 'chair_c870e': ['chair', OrientedBoundingBox: center: (5.68372, 1.15983, -0.746679), extent: 0.969814, 0.332232, 0.151999)], 'pillow_0560d': ['pillow', OrientedBoundingBox: center: (5.87799, 1.4803, -0.877062), extent: 0.480818, 0.301633, 0.218522)], 'armchair_e9853': ['armchair', OrientedBoundingBox: center: (5.72074, 1.49694, -0.871604), extent: 1.26775, 0.915039, 0.576282)], 'lamp_28f24': ['lamp', OrientedBoundingBox: center: (5.18024, 2.75497, -0.203432), extent: 0.481787, 0.467498, 0.346561)], 'pillow_39334': ['pillow', OrientedBoundingBox: center: (4.64352, 2.56852, -0.722029), extent: 0.792069, 0.563767, 0.341118)], 'pillow_4095e': ['pillow', OrientedBoundingBox: center: (4.517, 2.42379, -0.782445), extent: 0.408706, 0.173036, 0.0428488)], 'pillow_b6e7e': ['pillow', OrientedBoundingBox: center: (4.4671, 2.62977, -0.750383), extent: 0.951701, 0.587509, 0.387328)], 'coffee table_2d6ac': ['coffee table', OrientedBoundingBox: center: (3.70932, 1.02609, -1.11315), extent: 1.42469, 0.837541, 0.653472)], 'blinds_01be1': ['blinds', OrientedBoundingBox: center: (3.16765, 3.14718, 0.310787), extent: 6.17042, 2.16616, 0.728607)], 'lamp_9d1bb': ['lamp', OrientedBoundingBox: center: (6.42901, 3.18339, -0.598394), extent: 0.854441, 0.741761, 0.283376)], 'paper bag_f1a6f': ['paper bag', OrientedBoundingBox: center: (2.3169, 2.9035, -1.36264), extent: 0.845846, 0.537433, 0.48784)], 'sofa chair_4d503': ['sofa chair', OrientedBoundingBox: center: (6.7499, 1.01979, -1.00271), extent: 0.925571, 0.327943, 0.196273)], 'book_ec5b3': ['book', OrientedBoundingBox: center: (5.21968, 2.58665, -0.850194), extent: 0.747306, 0.425439, 0.165954)], 'power outlet_c2b55': ['power outlet', OrientedBoundingBox: center: (6.23326, 3.27971, -1.03996), extent: 0.412163, 0.204042, 0.0297779)], 'lamp_0fe0c': ['lamp', OrientedBoundingBox: center: (5.61787, 3.11594, -0.244825), extent: 1.3938, 0.515743, 0.480937)], 'end table_e1bd2': ['end table', OrientedBoundingBox: center: (5.78408, 2.81296, -1.37925), extent: 1.72275, 0.71068, 0.233002)], 'lamp_e8ab2': ['lamp', OrientedBoundingBox: center: (6.53663, 3.13863, -0.900395), extent: 0.503988, 0.139862, 0.0532418)], 'lamp_b2450': ['lamp', OrientedBoundingBox: center: (2.36058, -1.11799, -1.1024), extent: 1.14514, 0.388891, 0.00440057)], 'lamp_7fbca': ['lamp', OrientedBoundingBox: center: (6.17927, 3.41101, -0.305494), extent: 0.466539, 0.259022, 0.123388)]}

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