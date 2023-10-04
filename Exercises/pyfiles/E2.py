import numpy as np, pandas as pd
from scipy import optimize, stats as scipy

class MAC:


	def __init__(self):
		""" Initialize with default values in key-value database. """
		self.db = {'α': .5, 'γ': 1, 'pe': 1, 'ϕ': .25, 'γd': 100}

	def Egrid(self, start_v = 0, end_v = 1, n = 1000):
		""" Generate a grid of E values """
		return np.linspace(start_v, end_v, n)
	

	
	def grids(self):
		"""Place to store the grids of E, and solutions C, Ctilde, M and MAC"""
		pd.Index(self.Egrid(), name = 'E') # grid of E values
		self.df = pd.DataFrame(index = self.Egrid(), columns = ['C', 'Ctilde', 'M', 'MAC'])

	def C(self, E, return_grid = False,  **kwargs):
		""" Cost function: Baseline without damage """
		Cgrid = self.db['γ'] * np.power(E, self.db['α'])-self.db['pe']*E
		
		#Save in df 
		self.df['C'] = Cgrid
		if return_grid == True:
			return Cgrid

	
	def M(self, E, return_grid = False, **kwargs):
		"""Emission function """

		Mgrid = self.db['ϕ']*E
		self.df['M'] = Mgrid

		if return_grid == True:
			return Mgrid

	
	def Ctilde(self, E, return_grid= False,**kwargs):
		""" Cost function with damage """
		Ctildegrid = self.C(E, return_grid=True)-self.db['γd']*np.power(self.M(E, return_grid=True),2)*0.5

		self.df['Ctilde'] = Ctildegrid

		if return_grid == True:
			return Ctildegrid
		

	def MAC(self, E, return_grid = False):
		""" Marginal abatement cost function """

		MACgrid = (self.db['α']*self.db['γ']*np.power(E, self.db['α']-1)-self.db['pe'])/self.db['ϕ']
		self.df['MAC'] = MACgrid

		if return_grid == True:
			return MACgrid
		
	def fill_grids(self):
		self.grids()
		Egrid = self.df.index.values
		self.C(Egrid)
		self.M(Egrid)
		self.Ctilde(Egrid)
		self.MAC(Egrid)

	def baseline_solution(self, print_sol = False):
		E_0 = optimize.fsolve(lambda E: self.db['α']*self.db['γ']*E**(self.db['α']-1)-self.db['pe'], 0.5)
		C_0 = self.C(E_0) # consumption level for E_0
		M_0 = self.M(E_0) # emmission level for E_0
		if print_sol == True:
			print('Baseline values: E_0 = ', E_0, 'C_0 = ', C_0, 'M_0 = ', M_0)

	
class MACTech(MAC):
	def __init__(self, α = .5, γ = 1, pe = 1, ϕ = .25, γd = 100, θ = None, c = None, σ = None):
		super().__init__(α = α, γ = γ, pe = pe, ϕ = ϕ, γd = γd) # use __init__ method from parent class
		self.initTechs(θ = θ, c = c, σ = σ)
		
	def initTechs(self, θ = None, c = None, σ = None):
		""" Initialize technologies from default values """
		if θ is None:
			self.db['Tech'] = pd.Index(['T1'], name = 'i')
			self.db['θ'] = pd.Series(0, index = self.db['Tech'], name = 'θ')
			self.db['c'] = pd.Series(1, index = self.db['Tech'], name = 'c')
			self.db['σ'] = pd.Series(1, index = self.db['Tech'], name = 'σ')
		elif isinstance(θ, pd.Series):
			self.db['θ'] = θ
			self.db['c'] = c
			self.db['σ'] = σ
			self.db['Tech'] = self.db['θ'].index
		else:
			self.db['Tech'] = 'T'+pd.Index(range(1, len(θ)+1), name = 'i').astype(str)
			self.db['θ'] = pd.Series(θ, index = self.db['Tech'], name = 'θ')
			self.db['c'] = pd.Series(c, index = self.db['Tech'], name = 'c')
			self.db['σ'] = pd.Series(σ, index = self.db['Tech'], name = 'σ')
