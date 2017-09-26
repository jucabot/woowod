
import random
from copy import deepcopy

"""
	Wod engine
"""
class Wod(object):
	UNBUILT = "unbuilt"
	BUILT = "built"
	state = None
	scheme = None
	box = None
	mobility = None
	skill = None
	metcon = None
	after_party = None

	def __init__(self,box,scheme="default"):
		self.box = box
		self.scheme = scheme
		self.state = self.UNBUILT

	def __str__(self):
		return "%s" % (self.metcon["description"])

	def build(self):

		metcon = deepcopy(random.choice(self.box.protocols[self.scheme]))
		moves = metcon["moves"]
		for move in moves:
			move["move"] = self._choice_one_move(category=move["category"],intensity=move["intensity"])

		self.metcon = {
			"description" : self._build_metcon(metcon),
			"score" : metcon["score"],
			"delay" : metcon["delay"]
			}

		self.state = self.BUILT

	def _choice_one_move(self,category,intensity):
		# randomly select a move from the category with the requested intensity. '' or None means not a such intensity.
		selected_moves = filter(lambda m : m['Mode']==category and m.get(intensity,None) not in ('',None), self.box.get_available_moves())
		move = random.choice(selected_moves)
		move['Intensity'] = move[intensity]
		return move


	def _build_metcon(self,metcon):
		template = metcon["template"]
		moves = metcon["moves"]
		flatten_moves = {}
		
		for move in moves:
			for name, value in move["move"].items():
				flatten_moves[move["category"].lower() + '.' + name.lower()] = value

		return template % (flatten_moves)


	def _build_warmup(self,cardio=None,gym=None,weight=None):

		warmup = []

		if cardio:
			warmup.append(cardio["Warmup"])
		if gym:
			warmup.append(gym["Warmup"])
		if weight:
			warmup.append(weight["Warmup"])

		return "\n".join(warmup)

class Box(object):

	MOVES = "moves"
	
	DEFAULT_CONFIG = {
		MOVES : [],
	}

	config = {}
	protocols = {}

	def __init__(self,box_config,protocols):
		self.config = box_config
		self.protocols = protocols

	def get_available_moves(self):
		return self.config[self.MOVES]

	def get_available_schemes(self):
		return self.protocols.keys()

	def create_workout(self,scheme):
		random.seed()
		wod = Wod(self,scheme)
		wod.build()
		return wod