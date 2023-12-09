from numpy import array, shape, linspace, size, interp, digitize, stack, transpose, radians, sin
from shapely import Polygon

from zupplemental.helpers import load_shaperecords

nan = 0.99999999
colormap = array([
	[nan, nan, nan],
	[0.9945973, 0.99613082, 0.98856642],
	[0.98991378, 0.9916072, 0.98068901],
	[0.98517785, 0.98715549, 0.97254927],
	[0.98047281, 0.98274878, 0.96408531],
	[0.97586481, 0.97836064, 0.95529566],
	[0.97138939, 0.97397255, 0.94621879],
	[0.96705583, 0.96957507, 0.93690541],
	[0.96285835, 0.96516531, 0.92740045],
	[0.95878484, 0.96074379, 0.91774001],
	[0.95482252, 0.95631264, 0.90794718],
	[0.9509589, 0.95187411, 0.89804315],
	[0.94718313, 0.94743035, 0.88804395],
	[0.9434858, 0.9429832, 0.87796328],
	[0.93986079, 0.93853444, 0.86780247],
	[0.93630182, 0.93408526, 0.85756966],
	[0.93281723, 0.92963072, 0.84727738],
	[0.92957358, 0.92510484, 0.83692259],
	[0.92662401, 0.92048693, 0.82649236],
	[0.92397255, 0.91577219, 0.81600845],
	[0.92161918, 0.91095718, 0.80549345],
	[0.91955955, 0.90603996, 0.79497101],
	[0.91778534, 0.9010201, 0.78446439],
	[0.91628436, 0.89589867, 0.77399642],
	[0.91504156, 0.89067807, 0.76358779],
	[0.91403979, 0.88536175, 0.75325656],
	[0.91326001, 0.87995415, 0.74301882],
	[0.9126825, 0.87446035, 0.73288749],
	[0.91228718, 0.8688859, 0.72287286],
	[0.91205412, 0.86323663, 0.71298279],
	[0.91196446, 0.85751834, 0.70322207],
	[0.91200438, 0.85173494, 0.69359431],
	[0.91216167, 0.84588965, 0.68410389],
	[0.91241344, 0.83999117, 0.67474727],
	[0.91274234, 0.83404556, 0.66552582],
	[0.91315532, 0.82804852, 0.65643923],
	[0.91362336, 0.82201201, 0.64748265],
	[0.91414301, 0.81593662, 0.63865457],
	[0.91470891, 0.80982388, 0.62995254],
	[0.91530533, 0.80368036, 0.62137183],
	[0.91593498, 0.79750402, 0.61291036],
	[0.91658457, 0.79130058, 0.60456292],
	[0.91724987, 0.78507148, 0.59632617],
	[0.91793173, 0.77881561, 0.58819848],
	[0.91861499, 0.77254016, 0.58017186],
	[0.91930729, 0.76624062, 0.57224738],
	[0.920002, 0.75992003, 0.56441807],
	[0.92068803, 0.75358344, 0.55668177],
	[0.92137053, 0.74722799, 0.54903431],
	[0.92205269, 0.74085148, 0.54147387],
	[0.92272294, 0.73445959, 0.53399526],
	[0.92337861, 0.7280533, 0.52659675],
	[0.92402063, 0.72163188, 0.51927412],
	[0.92465338, 0.71519246, 0.512026],
	[0.92527303, 0.70873666, 0.50484937],
	[0.92587567, 0.70226628, 0.49774057],
	[0.92644765, 0.69578493, 0.49074586],
	[0.92699345, 0.68928545, 0.48392211],
	[0.92751341, 0.68276687, 0.47727477],
	[0.92800409, 0.67623017, 0.47081193],
	[0.92845249, 0.66968013, 0.46456788],
	[0.92886072, 0.66311618, 0.45853196],
	[0.92922549, 0.65653987, 0.45270812],
	[0.92954226, 0.64995329, 0.44710421],
	[0.92980604, 0.64335895, 0.44172793],
	[0.93000003, 0.63676406, 0.43662572],
	[0.93013072, 0.63016722, 0.4317666],
	[0.93019313, 0.62357154, 0.42715609],
	[0.93018229, 0.61698027, 0.42279916],
	[0.93007993, 0.61040243, 0.41874407],
	[0.92989467, 0.6038362, 0.41494989],
	[0.92962232, 0.59728502, 0.41141807],
	[0.92925429, 0.59075449, 0.40816373],
	[0.92878175, 0.58425059, 0.4052023],
	[0.92821145, 0.57777231, 0.40250019],
	[0.92754051, 0.57132305, 0.40005382],
	[0.92675799, 0.56491, 0.39788722],
	[0.92586688, 0.55853391, 0.39598044],
	[0.9248709, 0.55219507, 0.39431115],
	[0.92376932, 0.54589589, 0.39287161],
	[0.92255425, 0.53964215, 0.3916808],
	[0.92123167, 0.53343279, 0.39071248],
	[0.91980629, 0.52726718, 0.38994582],
	[0.91827938, 0.52114636, 0.38937104],
	[0.91665301, 0.51507073, 0.38897854],
	[0.91492074, 0.50904516, 0.38878606],
	[0.91309456, 0.5030645, 0.38875481],
	[0.91117737, 0.49712835, 0.38887445],
	[0.9091721, 0.49123612, 0.38913554],
	[0.90708209, 0.48538677, 0.38952923],
	[0.90491038, 0.47957945, 0.39004638],
	[0.90266025, 0.47381299, 0.39067835],
	[0.90033392, 0.4680866, 0.39142149],
	[0.89793444, 0.46239889, 0.39226974],
	[0.89546782, 0.45674665, 0.39320796],
	[0.89293751, 0.45112798, 0.39422939],
	[0.89034611, 0.44554185, 0.39532571],
	[0.88769792, 0.43998512, 0.39649307],
	[0.88499575, 0.43445621, 0.39772467],
	[0.88224257, 0.42895324, 0.39901445],
	[0.87944229, 0.42347298, 0.4003596],
	[0.87659663, 0.41801483, 0.40175155],
	[0.87371001, 0.41257452, 0.40319038],
	[0.87078389, 0.40715155, 0.40466751],
	[0.86782021, 0.40174318, 0.406189],
	[0.8648213, 0.39634757, 0.4077488],
	[0.86179112, 0.39096131, 0.40933953],
	[0.85873256, 0.38558123, 0.41095952],
	[0.85564742, 0.38020559, 0.41260368],
	[0.85253835, 0.37483125, 0.41427043],
	[0.84940775, 0.36945514, 0.41595813],
	[0.84625772, 0.36407454, 0.41766433],
	[0.84308909, 0.35868776, 0.41938804],
	[0.83990172, 0.35329031, 0.42115542],
	[0.83667903, 0.34790409, 0.42293799],
	[0.83342336, 0.34252304, 0.42475646],
	[0.83013273, 0.33714873, 0.42661175],
	[0.82680567, 0.33178177, 0.42850772],
	[0.82343946, 0.32642519, 0.43044225],
	[0.82003186, 0.32108127, 0.43241546],
	[0.81657104, 0.31576401, 0.43442957],
	[0.81306525, 0.31046315, 0.43648471],
	[0.80951226, 0.30518153, 0.43857928],
	[0.80591025, 0.29992079, 0.44071666],
	[0.80225634, 0.29468526, 0.44289314],
	[0.79854847, 0.28947736, 0.44511082],
	[0.79478401, 0.28430133, 0.44736695],
	[0.79096075, 0.2791604, 0.44966233],
	[0.78707616, 0.27405916, 0.45199387],
	[0.78312802, 0.26900135, 0.45436174],
	[0.77911389, 0.2639922, 0.45676152],
	[0.77503167, 0.25903586, 0.4591929],
	[0.77087917, 0.25413762, 0.46165187],
	[0.76665439, 0.24930273, 0.4641348],
	[0.76235547, 0.24453621, 0.46663927],
	[0.75798069, 0.23984372, 0.46916023],
	[0.75352856, 0.23523084, 0.47169288],
	[0.74899777, 0.23070299, 0.47423289],
	[0.74438725, 0.22626571, 0.47677507],
	[0.73969621, 0.22192451, 0.4793134],
	[0.73492415, 0.21768468, 0.48184197],
	[0.73007082, 0.21355128, 0.48435476],
	[0.72513628, 0.20952909, 0.48684565],
	[0.72011408, 0.20563483, 0.48930657],
	[0.71501117, 0.20186167, 0.49173228],
	[0.70982924, 0.19821188, 0.49411661],
	[0.70456966, 0.19468824, 0.49645339],
	[0.69923425, 0.19129289, 0.49873602],
	[0.69382485, 0.18802738, 0.50095914],
	[0.68834369, 0.18489259, 0.50311724],
	[0.68279313, 0.18188874, 0.50520528],
	[0.67717603, 0.17901521, 0.50721768],
	[0.671495, 0.17627093, 0.50915076],
	[0.66575291, 0.17365415, 0.51100088],
	[0.65995296, 0.17116229, 0.51276407],
	[0.65409842, 0.1687922, 0.51443707],
	[0.64819205, 0.16654064, 0.51601864],
	[0.64223741, 0.16440324, 0.51750585],
	[0.63623787, 0.16237535, 0.5188969],
	[0.63019618, 0.16045249, 0.52019188],
	[0.6241164, 0.15862855, 0.52138814],
	[0.61800056, 0.15689918, 0.52248802],
	[0.61185326, 0.15525704, 0.5234884],
	[0.60567598, 0.15369791, 0.52439297],
	[0.5994735, 0.15221377, 0.52519899],
	[0.59324739, 0.15079999, 0.52591008],
	[0.58700095, 0.14944992, 0.52652663],
	[0.5807375, 0.14815674, 0.52704922],
	[0.57445878, 0.14691545, 0.52748112],
	[0.5681627, 0.14573028, 0.52782043],
	[0.56184986, 0.1445994, 0.52806756],
	[0.55552862, 0.14350405, 0.52822893],
	[0.54920143, 0.14243834, 0.52830663],
	[0.54287108, 0.14139605, 0.52830238],
	[0.53653999, 0.14037146, 0.5282184],
	[0.53020967, 0.13935998, 0.52805809],
	[0.5238674, 0.13838637, 0.52781581],
	[0.51752564, 0.13742426, 0.52749969],
	[0.5111899, 0.13646152, 0.52711441],
	[0.50486205, 0.13549347, 0.52666277],
	[0.49852829, 0.13453311, 0.5261673],
	[0.49222235, 0.1335206, 0.52563184],
	[0.4859399, 0.13245665, 0.52507149],
	[0.47967972, 0.13134181, 0.52448981],
	[0.47344176, 0.13017623, 0.52388672],
	[0.46722578, 0.12896029, 0.52326228],
	[0.46103267, 0.12769646, 0.52260808],
	[0.45486156, 0.12638486, 0.52192676],
	[0.44871105, 0.12502444, 0.5212249],
	[0.44257992, 0.12361647, 0.52050331],
	[0.43646809, 0.12216092, 0.51976146],
	[0.4303754, 0.12065785, 0.51899882],
	[0.42430127, 0.11910775, 0.51821523],
	[0.41824407, 0.11751359, 0.51740869],
	[0.41220495, 0.11587538, 0.5165743],
	[0.40618198, 0.11419195, 0.51571889],
	[0.40017337, 0.11246497, 0.51484297],
	[0.39418014, 0.11069312, 0.51394411],
	[0.38819947, 0.10887917, 0.51302348],
	[0.3822322, 0.10702198, 0.5120785],
	[0.37627591, 0.1051239, 0.51110953],
	[0.37033128, 0.10318407, 0.51011386],
	[0.36439493, 0.10120585, 0.50909221],
	[0.35846789, 0.0991881, 0.50804115],
	[0.35254804, 0.09713299, 0.50695979],
	[0.34663388, 0.09504216, 0.50584642],
	[0.34072474, 0.09291644, 0.50469837],
	[0.3348192, 0.09075758, 0.50351331],
	[0.32891531, 0.08856803, 0.50228903],
	[0.32301171, 0.08634979, 0.5010225],
	[0.31710678, 0.08410529, 0.49971055],
	[0.31119952, 0.0818431, 0.49833919],
	[0.30528779, 0.07956447, 0.49690882],
	[0.29936952, 0.0772709, 0.49541916],
	[0.29344297, 0.07496633, 0.49386548],
	[0.28750574, 0.07265583, 0.49224297],
	[0.28155598, 0.07034517, 0.49054488],
	[0.27559136, 0.06805937, 0.48873943],
	[0.26960979, 0.06578794, 0.48684435],
	[0.26360887, 0.06353832, 0.48485287],
	[0.25758533, 0.06132985, 0.48274495],
	[0.25153785, 0.05918188, 0.48049794],
	[0.24546285, 0.05708736, 0.47812794],
	[0.23935856, 0.05507246, 0.47560546],
	[0.23322115, 0.05315867, 0.47291209],
	[0.22704941, 0.05133423, 0.47006463],
	[0.2208408, 0.04965834, 0.46699741],
	[0.21459229, 0.04810128, 0.46375105],
	[0.20830249, 0.04671594, 0.46026515],
	[0.20197019, 0.04547941, 0.45656622],
	[0.19559423, 0.04443972, 0.45259717],
	[0.18917438, 0.04356121, 0.44839348],
	[0.18271085, 0.04289756, 0.44388513],
	[0.17620461, 0.04240256, 0.43911292],
	[0.16965782, 0.0420926, 0.43404151],
	[0.16307374, 0.04195538, 0.42866475],
	[0.15644831, 0.04195979, 0.42300797],
	[0.14980491, 0.0418395, 0.41734748],
	[0.14314498, 0.04152601, 0.41176633],
	[0.13646096, 0.04102857, 0.40626486],
	[0.12974849, 0.04034679, 0.40084617],
	[0.12300148, 0.0394773, 0.3955129],
	[0.11621389, 0.03843774, 0.39026846],
	[0.10937323, 0.0372402, 0.38511363],
	[0.10247278, 0.03588654, 0.38005353],
	[0.09549628, 0.03438787, 0.37508968],
	[0.08842349, 0.03275523, 0.3702238],
	[0.08124001, 0.03098875, 0.36546251],
	[0.07392146, 0.02909417, 0.36081046],
	[0.06644184, 0.02707246, 0.35627482],
	[0.05875324, 0.02493463, 0.351859],
	[0.05080482, 0.02268113, 0.34757159],
	[0.04251822, 0.02031596, 0.34342051],
	[0.03400054, 0.01783756, 0.33941712],
	[0.02600119, 0.01526206, 0.33556622],
	[0.01841184, 0.01268338, 0.3318399],
])*256

COUNTRIES_BY_AREA = {
	"VAT": 0.49,
	"PGA": 2.0,
	"CSI": 2.0,
	"BRI": 2.5,
	"MCO": 2.08,
	"GIB": 6.8,
	"CLP": 8.9,
	"TKL": 10,
	"IOA": 135 + 14,
	"UMI": 49.26,
	"NRU": 21,
	"BLM": 25,
	"TUV": 26,
	"MAC": 115.3,
	"SXM": 34,
	"NFK": 34.6,
	"PCN": 47,
	"MAF": 34,
	"BMU": 53.2,
	"IOT": 60,
	"SMR": 61.2,
	"GGY": 62,
	"USG": 117,
	"AIA": 91,
	"MSR": 102,
	"ATC": 112,
	"JEY": 119.6,
	"WLF": 142.42,
	"SCR": 150,
	"VGB": 153,
	"LIE": 160,
	"ABW": 179.64,
	"MHL": 181.43,
	"ASM": 200,
	"BJN": 234,
	"COK": 236.7,
	"SPM": 242,
	"WSB": 127,
	"ESB": 127,
	"NIU": 261.46,
	"KNA": 261,
	"CYM": 259,
	"MDV": 298,
	"SER": 1200,
}

density_bins = array([.02, 10, 20, 50, 100, 200, 500, 1000, 2000])

swatches = stack(
	[
		interp(
			linspace(0, 1, size(density_bins) + 2),
			linspace(0, 1, shape(colormap)[0], endpoint=False),
			colormap[:, i]
		) for i in range(shape(colormap)[1])
	],
	axis=1)

binned_keys = [[] for i in range(len(density_bins) + 1)]
max_density = 0
total_area = 0
for shape, record in load_shaperecords("ne_10m_admin_0_countries"):
	population = record["pop_est"]
	if record["adm0_a3"] in COUNTRIES_BY_AREA:
		area = COUNTRIES_BY_AREA[record["adm0_a3"]]
	else:
		area = 0
		for i in range(len(shape.parts)):
			start_index = shape.parts[i]
			end_index = shape.parts[i + 1] if i + 1 < len(shape.parts) else None
			λ, ф = transpose(shape.points[start_index:end_index])
			x, y = 6371*radians(λ), 6371*sin(radians(ф))
			area += Polygon(stack([x, y], axis=1)).area
		if area < 300:
			raise ValueError(f"this area ({area:.0f}km² for {record['name']} is likely inaccurate.  please specify it manually.")
	density = population/area
	binned_keys[digitize(density, density_bins, right=True)].append(record["adm0_a3"])

	if density > max_density:
		max_density = density
	total_area += area

bin_ranges = [
	(
		density_bins[i - 1] if i > 0 else 0,
		density_bins[i] if i < len(density_bins) else max_density
	) for i in range(size(density_bins) + 1)
]

for (min_density, max_density), (r, g, b), keys in zip(bin_ranges, swatches, binned_keys):
	print(f"\t\t.{', .'.join(keys)} {{\n"
	      f"\t\t\tfill: #{int(r):02x}{int(g):02x}{int(b):02x}; /* {min_density}--{max_density:.0f} person/km^2 */\n"
	      f"\t\t}}")
