# 4DOF Ballistic Calculator

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📝 Description

A sophisticated ballistic calculator that implements both a 4 Degrees of Freedom (4DOF) model and a Point Mass model for projectile trajectory simulation. This tool provides high-precision ballistic calculations considering various aerodynamic effects and environmental factors.

## 🚀 Features

- **Dual Model Implementation:**
- 4DOF (4 Degrees of Freedom) Model
  - Drag force calculation
  - Lift force consideration
  - Pitching moment effects
  - Variable angle of attack
  - Coriolis effect integration
- Point Mass Model
  - Simplified trajectory calculations
  - Gravity and drag force consideration
  - Computationally efficient

- **User Interface:**
- Intuitive GUI built with Tkinter
- Real-time trajectory visualization
- Parameter input validation
- Results export to CSV

## 🛠️ Installation

1. Clone the repository:
bash
python main.py

3. Input the required parameters in the GUI:
   - Initial velocity
   - Launch angle
   - Projectile characteristics
   - Environmental conditions

4. Select the desired model (4DOF or Point Mass)

5. Run the simulation and analyze results

## 📁 Project Structure

4Dof_Project/
├── main.py           # Application entry point
├── gui.py           # GUI implementation
├── funciones.py     # Utility functions
├── modelos/         # Mathematical models
│   ├── 4dof.py     # 4DOF model implementation
│   └── puntual.py  # Point mass model
└── calculadora/     # Core calculation logic


## 🔧 Technical Details

### 4DOF Model
- Implements complete aerodynamic force calculations
- Considers variable angle of attack
- Includes Coriolis effect
- Assumes no spin (Magnus effect = 0)

### Point Mass Model
- Simplified trajectory calculations
- Considers basic forces (gravity and drag)
- Ideal for quick estimations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

Luchinol - luisantoniooc@gmail.com

Project Link: [https://github.com/Luchinol/4Dof_Project](https://github.com/Luchinol/4Dof_Project)

## 🙏 Acknowledgments

- Reference to any research papers or resources used
- Credits to contributors or inspiration sources