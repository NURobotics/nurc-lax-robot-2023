MECH ENG 314
SEAN MORTON
FINAL PROJECT
12/08/2022

 1. You should include a brief description of what you originally proposed and 
	what changes you needed to make to your original proposal (and why you made them).
	
	Original proposal: clacker balls simulation. 2 balls on 2 strings; 6 configuration 
	variables (x_base, y_base, theta1, theta2, phi1_ball1, phi2_balls). External forcing
	provided by user's click-and-drag. 
	
	Changes made to the original proposal: in original proposal, plots of the energy
	of the system over time were supposed to be generated at the end of a simulation.
	This is not something I approached for this project, because I thought it would
	not be meaningful. Due to constant external forcing, the Hamiltonian changes
	constantly; to get a system where the Hamiltonian is constant would mean having the 
	balls fall straight down in gravity, which would not be interesting.
____

 2. You should include a drawing of the system you are modeling that includes all the 
	frames you are using, with frame labels. In addition to the drawing, you should 
	include all of the rigid body transformations you are using between the frames. 
	These frames and their labels should be clearly identifiable in your code.
	
	See PDFs with frames and transformation matrices
____

 3. Using the drawing and the rigid body transformations, you should say in writing 
	how you calculate the Euler-Lagrange equations, the constraints, the external forces
	 and impact update laws.
	 
	The Euler-Lagrange equations are calculated using the forced Euler-Lagrange equations
	formula, d/dt( dL/dqdot) - dL/dq = F_ext, with no forces of constraint. 
	Forces are defined as F_x, F_y, ... F_phi2 symbolically	during the Sympy solve, then
	"lambdified" into function inputs during the numerical conversion of xdd, ydd, etc.
	This gives more freedom as to how the forces are defined later on during simulation testing.
	
	Constraints: none
	Forces: in the end I decided on forces being calculated using a PD control law:
		a set trajectory was defined for x and y, and forces for both x and y were
		proportional to the distance of the base of the pendula from the desired path 
		(spring-force term) and to the current velocity of the base (damping term).
		F_y also has a constant force of 19.62N that counteracts gravity (2m*g, m = 1kg).
		
	Impact update laws: there are 8 vertices, each with 4 modes of impact. This yields
	8 impact conditions (see below), and 32 phi(q) functions.
	From there, I find the minimum absolute value of phi(q) across all 32 calculated phi(q), 
	and apply the impact update corresponding to that phi(q):
	
	  - impact_condition() returns an array of length 8 of T/F values based on which of 
		8 impact conditions is currently being met: "-bound < vertex_x < bound
		and -bound < vertex_y < bound" meaning that this vertex is inside the other box.

	  - phi_closetozero() returns an array of length 32 of values of phi(q)
		
	  - filter_phiq() takes the results of impact_condition() and matches it to 
		phi_closetozero, and discards any phi(q) near zero that don't correspond to an 
		impact happening
		
	  - "argmin" is the index of a valid phi(q) (0-31)  - valid meaning "corresponds to a 
		real impact" - with the smallest abs. value.
		

____

 4. If your code works, you should describe in words what happens in the simulation and 
	why you think it is correct (e.g., at a high level, describe why you think the 
	behavior is reasonable or not). 
	
	In the simulation, the boxes bounce up and down on the strings, occasionally impacting
	each other. After an impact, velocity thetad usually changes signs, and velocity phid
	usually either changes magnitude or changes direction. Acceleration upward in the y direction
	results in a downward motion of the clacker balls. I think the behavior of the system is
	reasonable because when I tested with no impacts, and just had a force term opposing gravity,
	the balls fell in gravity, towards each other, and some rotational KE in Phi was transferred 
	to translational KE in r*thetad. When I did test with impacts, I have eventually gotten the code
	to a state where the impacts are recognized and the system repels itself after impact.
	
	Known issues/bugs:
	- When there is a 180 degree angle between the two strings, the balls have been known
		to approach a singularity, and the values of velocity approach infinity. This
		may inhibit swinging the balls above the horizontal.
	- There are occasional double-hits of the balls; i.e. an impact followed directly after
		by another impact. I initially tried what Jake suggested, to detect if there's an impact
		two timesteps from now and apply the impact update upon that condition, but this made my
		impacts happen too far out from the actual point of collision.
	- About 1 in 50 collisions (rough guess), one vertex of a box will clip inside another box,
		causing the simulation to grow unstable and diverge to infinity. This is far less frequent
		than it used to be (1 in 5 collisions) but still something to note.
	- Errors caused by no solution being found by nsolve() are not handled, not are errors caused
		by reaching the end of simulation.
	- My inertia calculations may be off, as I have my inertia tensor as m*w^2 * eye(3), but an
		online source from MIT suggests that for a rectangular plate, the inertia tensor is really
		m*w^2/12 * [[1, 0, 0],[0, 1, 0], [0, 0, 2]] (for a system w/ principal axes).
		Source: https://tinyurl.com/ocwdyn
	- Don't let the balls come to rest!
		
___

Some of my code is derived from previous helper functions I had used during Tkinter projects
	in CS110. Functions from that course, both by the professor and by me, are noted in plotting_helpers.py.
