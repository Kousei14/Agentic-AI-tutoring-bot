def get_calculus_problem(index: int = None) -> str:
    calculus_problems = [

    # Derivatives
    "Find the derivative of f(x) = 3x^4 - 5x^2 + 2.",
    "Differentiate f(x) = sin(x) * e^x.",
    "Find the second derivative of f(x) = ln(x^2 + 1).",
    "Find dy/dx if y = tan(x^2).",

    # Implicit Differentiation
    "Find dy/dx if x^2 + y^2 = 25.",
    "Differentiate implicitly: x^3 + y^3 = 6xy.",

    # Applications of Derivatives
    "Find the equation of the tangent line to f(x) = x^3 - 2x at x = 1.",
    "Determine the intervals where f(x) = x^3 - 6x^2 + 9x is increasing or decreasing.",
    "Find the local maxima and minima of f(x) = x^4 - 4x^3.",
    "Use the second derivative test to classify critical points of f(x) = x^3 - 3x + 1.",

    # Optimization
    "Find the dimensions of a rectangle with maximum area that can be inscribed under the curve y = 4 - x^2.",
    "A farmer wants to fence a rectangular field with a fixed perimeter of 100 meters. What dimensions maximize the area?",

    # Related Rates (Time Rates)
    "A balloon is rising vertically at 5 m/s. A person is standing 30 meters away. How fast is the distance between the person and the balloon increasing when the balloon is 40 meters high?",
    "Water is being poured into a conical tank at a rate of 3 m³/min. The tank has a height of 6 m and a base radius of 2 m. How fast is the water level rising when the water is 4 m deep?",
    "A ladder 10 ft long is leaning against a wall. The bottom is sliding away at 2 ft/s. How fast is the top sliding down when the bottom is 6 ft from the wall?",

    # Integrals (Bonus)
    "Evaluate the integral ∫(2x^3 - 3x^2 + x - 5) dx.",
    "Find the area under the curve y = x^2 from x = 0 to x = 3.",
    "Use substitution to evaluate ∫x * sqrt(x^2 + 1) dx."
]
    
    return calculus_problems[index] if index is not None else calculus_problems[0]

def get_lin_alg_problem(index: int = None) -> str:
    lin_alg_problems = ["""Given the following matrices: 
    A = [2 4 1 0 − 1 3], B = [1 5 2 0 − 1 4]
    A = [2 0 4 −1 1 3​], B = 1 2 −1 5 0 4
    What is the resulting matrix C
    C when you multiply matrix A
    A by matrix B
    B?
    That is, compute 
    C = A × B
    C = A × B."""]

    return lin_alg_problems[index] if index is not None else lin_alg_problems[0]

def get_physics_problem(index: int = None) -> str:
    physics_problems = [
        "A car accelerates from rest at 3 m/s². How far does it travel in 5 seconds?",
        "What is the net force on a 10 kg object accelerating at 2 m/s²?",
        "How much work is done in lifting a 5 kg object to a height of 10 meters?",
        "Two objects collide elastically. Object A (2 kg) moves at 3 m/s, and object B (1 kg) is at rest. What are their velocities after the collision?",
        "What is the centripetal force on a 1 kg object moving in a circle of radius 2 m at 4 m/s?",
        "What is the current through a 10-ohm resistor connected to a 12 V battery?",
        "A wave has a frequency of 500 Hz and a wavelength of 0.6 m. What is its speed?",
        "How much heat is required to raise the temperature of 200 g of water from 25°C to 75°C? (Specific heat of water = 4.18 J/g°C)"
    ]
    
    return physics_problems[index] if index is not None else physics_problems[0]

def get_chemistry_problem(index: int = None) -> str:
    chemistry_problems = [
        "How many grams of water are produced when 8 grams of hydrogen gas reacts with excess oxygen?",
        "A gas occupies 3.0 L at 1.0 atm and 300 K. What will be its volume at 2.0 atm and 400 K?",
        "If the combustion of methane releases 890 kJ/mol, how much energy is released when 5 moles of methane are burned?",
        "For the reaction N₂ + 3H₂ ⇌ 2NH₃, what happens to the equilibrium position if pressure is increased?",
        "What is the pH of a 0.001 M HCl solution?",
        "Balance the redox reaction: MnO₄⁻ + Fe²⁺ → Mn²⁺ + Fe³⁺ in acidic solution.",
        "How much water must be added to 100 mL of 6 M HCl to make a 1 M solution?"
    ]

    return chemistry_problems[index] if index is not None else chemistry_problems[0]